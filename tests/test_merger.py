"""文件合并器测试"""
import json
import pytest
from pathlib import Path
from module_loader import Module
from merger import Merger


def _make_module(name: str, type: str = "general",
                 sections: list[dict] | None = None,
                 gitignore_entries: list[str] | None = None,
                 pre_commit_hooks: list[dict] | None = None,
                 variables: list[dict] | None = None,
                 templates: list[dict] | None = None,
                 commands: list[dict] | None = None,
                 settings: dict | None = None,
                 path: Path | None = None) -> Module:
    return Module(
        name=name, version="1.0.0", description="", type=type,
        sections=sections or [], gitignore_entries=gitignore_entries or [],
        pre_commit_hooks=pre_commit_hooks or [], variables=variables or [],
        templates=templates or [], commands=commands or [],
        settings=settings or {},
        path=path or Path("."),
    )


class TestClaudeMdMerger:
    def test_merge_sections_by_slot(self, tmp_path):
        """按章节聚合，章节内按 order 排序"""
        core = _make_module("core", "core", sections=[
            {"slot": "coding-standards", "file": "snippets/core-coding.md", "order": 0},
        ], path=tmp_path / "core")
        lang = _make_module("lang-python", "language", sections=[
            {"slot": "coding-standards", "file": "snippets/python-coding.md", "order": 100},
        ], path=tmp_path / "lang-python")

        (tmp_path / "core" / "snippets").mkdir(parents=True)
        (tmp_path / "core" / "snippets" / "core-coding.md").write_text("## 编码规范\n\n通用规范", encoding="utf-8")
        (tmp_path / "lang-python" / "snippets").mkdir(parents=True)
        (tmp_path / "lang-python" / "snippets" / "python-coding.md").write_text("### Python 编码规范\n\nPython 规范", encoding="utf-8")

        merger = Merger({"core": core, "lang-python": lang}, ["core", "lang-python"], {})
        result = merger.merge_claude_md()
        assert "通用规范" in result
        assert "Python 规范" in result
        assert result.index("通用规范") < result.index("Python 规范")

    def test_empty_slot_not_appeared(self, tmp_path):
        """没有模块贡献的章节不出现"""
        core = _make_module("core", "core", sections=[], path=tmp_path / "core")
        merger = Merger({"core": core}, ["core"], {})
        result = merger.merge_claude_md()
        assert result.strip() == ""

    def test_update_markers_inserted(self, tmp_path):
        """snippet 前插入更新标记（仅开始标记，下一个标记或 EOF 为边界）"""
        core = _make_module("core", "core", sections=[
            {"slot": "coding-standards", "file": "snippets/coding.md", "order": 0},
        ], path=tmp_path / "core")
        (tmp_path / "core" / "snippets").mkdir(parents=True)
        (tmp_path / "core" / "snippets" / "coding.md").write_text("## 编码规范\n\n内容", encoding="utf-8")

        merger = Merger({"core": core}, ["core"], {})
        result = merger.merge_claude_md()
        assert "<!-- module:core:1.0.0:coding-standards -->" in result
        assert "<!-- /module:" not in result


class TestSettingsMerger:
    def test_deep_merge(self, tmp_path):
        """settings.json 深度合并"""
        core = _make_module("core", "core", path=tmp_path / "core",
                            settings={"file": "config/settings.json.snippet"})
        (tmp_path / "core" / "config").mkdir(parents=True)
        (tmp_path / "core" / "config" / "settings.json.snippet").write_text(json.dumps({
            "permissions": {"allow": ["Read", "Glob"]},
        }), encoding="utf-8")

        lang = _make_module("lang-python", "language", path=tmp_path / "lang-python",
                            settings={"file": "config/settings.json.snippet"})
        (tmp_path / "lang-python" / "config").mkdir(parents=True)
        (tmp_path / "lang-python" / "config" / "settings.json.snippet").write_text(json.dumps({
            "permissions": {"allow": ["Bash(pytest)"]},
        }), encoding="utf-8")

        merger = Merger({"core": core, "lang-python": lang}, ["core", "lang-python"], {})
        result = merger.merge_settings()
        assert "Read" in result["permissions"]["allow"]
        assert "Bash(pytest)" in result["permissions"]["allow"]

    def test_array_dedup(self, tmp_path):
        """数组去重"""
        core = _make_module("core", "core", path=tmp_path / "core",
                            settings={"file": "config/settings.json.snippet"})
        (tmp_path / "core" / "config").mkdir(parents=True)
        (tmp_path / "core" / "config" / "settings.json.snippet").write_text(json.dumps({
            "permissions": {"allow": ["Read", "Glob"]},
        }), encoding="utf-8")

        lang = _make_module("lang-python", "language", path=tmp_path / "lang-python",
                            settings={"file": "config/settings.json.snippet"})
        (tmp_path / "lang-python" / "config").mkdir(parents=True)
        (tmp_path / "lang-python" / "config" / "settings.json.snippet").write_text(json.dumps({
            "permissions": {"allow": ["Read", "Bash(pytest)"]},
        }), encoding="utf-8")

        merger = Merger({"core": core, "lang-python": lang}, ["core", "lang-python"], {})
        result = merger.merge_settings()
        assert result["permissions"]["allow"].count("Read") == 1


class TestGitignoreMerger:
    def test_append_with_dedup(self):
        """追加去重"""
        core = _make_module("core", "core", gitignore_entries=[".env", "dist/"])
        lang = _make_module("lang-python", "language", gitignore_entries=["__pycache__/", ".env"])
        merger = Merger({"core": core, "lang-python": lang}, ["core", "lang-python"], {})
        result = merger.merge_gitignore()
        lines = result.strip().split("\n")
        assert ".env" in lines
        assert lines.count(".env") == 1
        assert "__pycache__/" in lines


class TestVariableReplacement:
    def test_replace_in_text(self):
        """变量替换"""
        core = _make_module("core", "core", sections=[
            {"slot": "project-info", "file": "snippets/info.md", "order": 0},
        ], path=Path("."))
        merger = Merger({"core": core}, ["core"], {"PROJECT_NAME": "my-api"})
        text = "# {{PROJECT_NAME}}\n\nDescription: {{PROJECT_DESCRIPTION}}"
        result = merger._replace_variables(text)
        assert "my-api" in result
        assert "{{PROJECT_DESCRIPTION}}" in result  # 未定义变量保留原样


class TestConditionMechanism:
    def test_evaluate_when_match(self):
        """when 表达式匹配"""
        merger = Merger({}, [], {"formatter": "black"})
        assert merger._evaluate_when("formatter == black") is True

    def test_evaluate_when_match_with_double_quotes(self):
        """when 表达式匹配（双引号值）"""
        merger = Merger({}, [], {"formatter": "black"})
        assert merger._evaluate_when('formatter == "black"') is True

    def test_evaluate_when_match_with_single_quotes(self):
        """when 表达式匹配（单引号值）"""
        merger = Merger({}, [], {"formatter": "black"})
        assert merger._evaluate_when("formatter == 'black'") is True

    def test_evaluate_when_no_match(self):
        """when 表达式不匹配"""
        merger = Merger({}, [], {"formatter": "ruff"})
        assert merger._evaluate_when("formatter == black") is False

    def test_evaluate_when_undefined_variable(self):
        """when 引用未定义变量时不匹配"""
        merger = Merger({}, [], {})
        assert merger._evaluate_when("formatter == black") is False

    def test_resolve_condition_default(self):
        """无匹配条件时使用默认值"""
        merger = Merger({}, [], {"formatter": "ruff"})
        definition = {
            "file": "snippets/default.md",
            "conditions": [
                {"when": "formatter == black", "file": "snippets/black.md"},
            ],
        }
        result = merger._resolve_condition(definition, "file")
        assert result == "snippets/default.md"

    def test_resolve_condition_matched(self):
        """匹配条件时替换默认值"""
        merger = Merger({}, [], {"formatter": "black"})
        definition = {
            "file": "snippets/default.md",
            "conditions": [
                {"when": "formatter == black", "file": "snippets/black.md"},
            ],
        }
        result = merger._resolve_condition(definition, "file")
        assert result == "snippets/black.md"

    def test_resolve_condition_first_match_wins(self):
        """多个条件时第一个匹配生效"""
        merger = Merger({}, [], {"test_framework": "pytest"})
        definition = {
            "file": "snippets/default.md",
            "conditions": [
                {"when": "test_framework == pytest", "file": "snippets/pytest.md"},
                {"when": "test_framework == unittest", "file": "snippets/unittest.md"},
            ],
        }
        result = merger._resolve_condition(definition, "file")
        assert result == "snippets/pytest.md"

    def test_resolve_condition_with_target(self):
        """条件中替换 target"""
        merger = Merger({}, [], {"api_style": "graphql"})
        definition = {
            "source": "templates/openapi.yaml",
            "target": "openapi.yaml",
            "conditions": [
                {"when": "api_style == graphql", "source": "templates/schema.graphql", "target": "schema.graphql"},
            ],
        }
        assert merger._resolve_condition(definition, "source") == "templates/schema.graphql"
        assert merger._resolve_condition(definition, "target") == "schema.graphql"

    def test_conditional_snippet_in_merge(self, tmp_path):
        """条件 snippet 在合并中生效"""
        mod = _make_module("lang-python", "language", sections=[
            {
                "slot": "testing",
                "file": "snippets/testing.md",
                "order": 100,
                "conditions": [
                    {"when": "test_framework == pytest", "file": "snippets/testing.pytest.md"},
                ],
            },
        ], path=tmp_path / "lang-python")

        (tmp_path / "lang-python" / "snippets").mkdir(parents=True)
        (tmp_path / "lang-python" / "snippets" / "testing.md").write_text("## 默认测试", encoding="utf-8")
        (tmp_path / "lang-python" / "snippets" / "testing.pytest.md").write_text("## Pytest 测试", encoding="utf-8")

        # formatter=ruff, test_framework=pytest → 应选择 pytest snippet
        merger = Merger({"lang-python": mod}, ["lang-python"], {"test_framework": "pytest"})
        result = merger.merge_claude_md()
        assert "Pytest 测试" in result
        assert "默认测试" not in result


class TestPreCommitMerger:
    def test_merge_hooks(self, tmp_path):
        """合并多个模块的 pre-commit hooks"""
        import yaml

        git_conv = _make_module("git-convention", "general", pre_commit_hooks=[
            {"file": "hooks/conventional.yaml"},
        ], path=tmp_path / "git-convention")
        (tmp_path / "git-convention" / "hooks").mkdir(parents=True)
        (tmp_path / "git-convention" / "hooks" / "conventional.yaml").write_text(
            "repo: https://github.com/compilerla/conventional-pre-commit\n"
            "rev: v3.6.0\n"
            "hooks:\n"
            "  - id: conventional-pre-commit\n"
            "    stages: [commit-msg]\n",
            encoding="utf-8",
        )

        security = _make_module("security", "general", pre_commit_hooks=[
            {"file": "hooks/gitleaks.yaml"},
        ], path=tmp_path / "security")
        (tmp_path / "security" / "hooks").mkdir(parents=True)
        (tmp_path / "security" / "hooks" / "gitleaks.yaml").write_text(
            "repo: https://github.com/gitleaks/gitleaks\n"
            "rev: v8.18.4\n"
            "hooks:\n"
            "  - id: gitleaks\n",
            encoding="utf-8",
        )

        merger = Merger(
            {"git-convention": git_conv, "security": security},
            ["git-convention", "security"],
            {},
        )
        result = merger.merge_pre_commit()
        assert result is not None
        data = yaml.safe_load(result)
        assert "repos" in data
        repo_urls = [r["repo"] for r in data["repos"]]
        assert "https://github.com/compilerla/conventional-pre-commit" in repo_urls
        assert "https://github.com/gitleaks/gitleaks" in repo_urls

    def test_merge_with_existing_content(self, tmp_path):
        """与已有 .pre-commit-config.yaml 合并，按 repo URL 去重"""
        import yaml

        mod = _make_module("security", "general", pre_commit_hooks=[
            {"file": "hooks/gitleaks.yaml"},
        ], path=tmp_path / "security")
        (tmp_path / "security" / "hooks").mkdir(parents=True)
        (tmp_path / "security" / "hooks" / "gitleaks.yaml").write_text(
            "repo: https://github.com/gitleaks/gitleaks\n"
            "rev: v8.18.4\n"
            "hooks:\n"
            "  - id: gitleaks\n",
            encoding="utf-8",
        )

        existing = "repos:\n  - repo: https://github.com/compilerla/conventional-pre-commit\n    rev: v3.6.0\n    hooks:\n      - id: conventional-pre-commit\n"

        merger = Merger({"security": mod}, ["security"], {})
        result = merger.merge_pre_commit(existing_content=existing)
        data = yaml.safe_load(result)
        repo_urls = [r["repo"] for r in data["repos"]]
        assert len(repo_urls) == 2
        assert "https://github.com/compilerla/conventional-pre-commit" in repo_urls
        assert "https://github.com/gitleaks/gitleaks" in repo_urls

    def test_dedup_by_repo_url(self, tmp_path):
        """相同 repo URL 去重"""
        import yaml

        mod = _make_module("security", "general", pre_commit_hooks=[
            {"file": "hooks/gitleaks.yaml"},
        ], path=tmp_path / "security")
        (tmp_path / "security" / "hooks").mkdir(parents=True)
        (tmp_path / "security" / "hooks" / "gitleaks.yaml").write_text(
            "repo: https://github.com/gitleaks/gitleaks\n"
            "rev: v8.18.4\n"
            "hooks:\n"
            "  - id: gitleaks\n",
            encoding="utf-8",
        )

        # 已有内容中已有 gitleaks
        existing = "repos:\n  - repo: https://github.com/gitleaks/gitleaks\n    rev: v8.18.0\n    hooks:\n      - id: gitleaks\n"

        merger = Merger({"security": mod}, ["security"], {})
        result = merger.merge_pre_commit(existing_content=existing)
        data = yaml.safe_load(result)
        repo_urls = [r["repo"] for r in data["repos"]]
        assert repo_urls.count("https://github.com/gitleaks/gitleaks") == 1

    def test_conditional_hook(self, tmp_path):
        """条件选择 pre-commit hook"""
        import yaml

        mod = _make_module("lang-python", "language", pre_commit_hooks=[
            {
                "file": "hooks/ruff.yaml",
                "conditions": [
                    {"when": "formatter == black", "file": "hooks/black.yaml"},
                ],
            },
        ], path=tmp_path / "lang-python")
        (tmp_path / "lang-python" / "hooks").mkdir(parents=True)
        (tmp_path / "lang-python" / "hooks" / "ruff.yaml").write_text(
            "repo: https://github.com/astral-sh/ruff-pre-commit\nrev: v0.4.8\nhooks:\n  - id: ruff\n",
            encoding="utf-8",
        )
        (tmp_path / "lang-python" / "hooks" / "black.yaml").write_text(
            "repo: https://github.com/psf/black-pre-commit\nrev: 24.4.2\nhooks:\n  - id: black\n",
            encoding="utf-8",
        )

        # formatter=black → 选择 black hook
        merger = Merger({"lang-python": mod}, ["lang-python"], {"formatter": "black"})
        result = merger.merge_pre_commit()
        data = yaml.safe_load(result)
        repo_urls = [r["repo"] for r in data["repos"]]
        assert "https://github.com/psf/black-pre-commit" in repo_urls
        assert "https://github.com/astral-sh/ruff-pre-commit" not in repo_urls
