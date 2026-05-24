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
                 path: Path | None = None) -> Module:
    return Module(
        name=name, version="1.0.0", description="", type=type,
        sections=sections or [], gitignore_entries=gitignore_entries or [],
        pre_commit_hooks=pre_commit_hooks or [], variables=variables or [],
        templates=templates or [], commands=commands or [],
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
        """snippet 前后插入更新标记"""
        core = _make_module("core", "core", sections=[
            {"slot": "coding-standards", "file": "snippets/coding.md", "order": 0},
        ], path=tmp_path / "core")
        (tmp_path / "core" / "snippets").mkdir(parents=True)
        (tmp_path / "core" / "snippets" / "coding.md").write_text("## 编码规范\n\n内容", encoding="utf-8")

        merger = Merger({"core": core}, ["core"], {})
        result = merger.merge_claude_md()
        assert "<!-- module:core:1.0.0:coding-standards -->" in result
        assert "<!-- /module:core:1.0.0:coding-standards -->" in result


class TestSettingsMerger:
    def test_deep_merge(self, tmp_path):
        """settings.json 深度合并"""
        core = _make_module("core", "core", path=tmp_path / "core")
        (tmp_path / "core" / "config").mkdir(parents=True)
        (tmp_path / "core" / "config" / "settings.json.snippet").write_text(json.dumps({
            "permissions": {"allow": ["Read", "Glob"]},
        }), encoding="utf-8")

        lang = _make_module("lang-python", "language", path=tmp_path / "lang-python")
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
        core = _make_module("core", "core", path=tmp_path / "core")
        (tmp_path / "core" / "config").mkdir(parents=True)
        (tmp_path / "core" / "config" / "settings.json.snippet").write_text(json.dumps({
            "permissions": {"allow": ["Read", "Glob"]},
        }), encoding="utf-8")

        lang = _make_module("lang-python", "language", path=tmp_path / "lang-python")
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
