"""生成器测试"""
import json
import pytest
from pathlib import Path
from module_loader import Module
from generator import Generator


def _make_core_module(tmp_path: Path) -> Module:
    mod_dir = tmp_path / "core"
    mod_dir.mkdir()
    (mod_dir / "module.yml").write_text(
        "name: core\nversion: 1.0.0\ndescription: Core\ntype: core\n"
        "depends: []\n"
        "sections:\n  - {slot: project-info, file: snippets/info.md, order: 0}\n"
        "gitignore_entries: ['.env', 'dist/']\n"
    )
    (mod_dir / "snippets").mkdir()
    (mod_dir / "snippets" / "info.md").write_text("## 项目信息\n\n{{PROJECT_NAME}}", encoding="utf-8")
    (mod_dir / "config").mkdir()
    (mod_dir / "config" / "settings.json.snippet").write_text(json.dumps({
        "permissions": {"allow": ["Read", "Glob"]},
    }))
    (mod_dir / "templates").mkdir()
    (mod_dir / "templates" / "gitignore").write_text("# Core ignores\n")
    return Module(
        name="core", version="1.0.0", description="Core", type="core",
        sections=[{"slot": "project-info", "file": "snippets/info.md", "order": 0}],
        gitignore_entries=[".env", "dist/"],
        settings={"file": "config/settings.json.snippet"},
        path=mod_dir,
    )


class TestGenerator:
    def test_generate_new_project(self, tmp_path):
        """生成新项目：所有文件正确写入"""
        core = _make_core_module(tmp_path)
        target = tmp_path / "output"
        gen = Generator(
            modules={"core": core},
            load_order=["core"],
            variables={"PROJECT_NAME": "test-api"},
        )
        gen.generate(target)

        assert (target / "CLAUDE.md").exists()
        assert "test-api" in (target / "CLAUDE.md").read_text(encoding="utf-8")
        assert (target / ".claude" / "settings.json").exists()

    def test_generate_does_not_overwrite_existing(self, tmp_path):
        """CLAUDE.md 已存在时写 CLAUDE.local.md（追加策略）"""
        core = _make_core_module(tmp_path)
        target = tmp_path / "output"
        target.mkdir()
        (target / "CLAUDE.md").write_text("existing content", encoding="utf-8")

        gen = Generator(
            modules={"core": core},
            load_order=["core"],
            variables={"PROJECT_NAME": "test-api"},
        )
        gen.generate(target, strategy="append")

        # 原有 CLAUDE.md 不变
        assert (target / "CLAUDE.md").read_text(encoding="utf-8") == "existing content"
        # 新内容写入 CLAUDE.local.md
        content = (target / "CLAUDE.local.md").read_text(encoding="utf-8")
        assert "test-api" in content

    def test_overwrite_creates_backup(self, tmp_path):
        """CLAUDE.local.md 已存在时覆盖策略创建备份"""
        core = _make_core_module(tmp_path)
        target = tmp_path / "output"
        target.mkdir()
        (target / "CLAUDE.md").write_text("team config", encoding="utf-8")
        (target / "CLAUDE.local.md").write_text("original local", encoding="utf-8")

        gen = Generator(
            modules={"core": core},
            load_order=["core"],
            variables={"PROJECT_NAME": "test-api"},
        )
        gen.generate(target, strategy="overwrite")

        assert (target / "CLAUDE.local.md.bak").exists()
        assert (target / "CLAUDE.local.md.bak").read_text(encoding="utf-8") == "original local"
        assert "test-api" in (target / "CLAUDE.local.md").read_text(encoding="utf-8")

    def test_gitignore_safe_append(self, tmp_path):
        """已有 .gitignore 安全追加"""
        core = _make_core_module(tmp_path)
        target = tmp_path / "output"
        target.mkdir()
        (target / ".gitignore").write_text("node_modules/\n.env\n")

        gen = Generator(
            modules={"core": core},
            load_order=["core"],
            variables={"PROJECT_NAME": "test-api"},
        )
        gen.generate(target, strategy="append")

        content = (target / ".gitignore").read_text()
        assert "node_modules/" in content
        assert content.count(".env") == 1  # 去重
        assert "dist/" in content  # 新增

    def test_auto_writes_shared_when_no_shared_exists(self, tmp_path):
        """共享文件不存在时写共享文件"""
        core = _make_core_module(tmp_path)
        target = tmp_path / "output"

        gen = Generator(
            modules={"core": core},
            load_order=["core"],
            variables={"PROJECT_NAME": "test-api"},
        )
        gen.generate(target)

        # 共享文件不存在，写 CLAUDE.md
        assert (target / "CLAUDE.md").exists()
        assert not (target / "CLAUDE.local.md").exists()
        assert "test-api" in (target / "CLAUDE.md").read_text(encoding="utf-8")

        # settings 同理
        assert (target / ".claude" / "settings.json").exists()
        assert not (target / ".claude" / "settings.local.json").exists()

    def test_auto_writes_local_when_shared_exists(self, tmp_path):
        """共享文件已存在时自动写 local 文件"""
        core = _make_core_module(tmp_path)
        target = tmp_path / "output"
        target.mkdir()
        (target / "CLAUDE.md").write_text("existing team config", encoding="utf-8")
        (target / ".claude").mkdir()
        (target / ".claude" / "settings.json").write_text("{}", encoding="utf-8")

        gen = Generator(
            modules={"core": core},
            load_order=["core"],
            variables={"PROJECT_NAME": "test-api"},
        )
        gen.generate(target)

        # 原有共享文件不变
        assert (target / "CLAUDE.md").read_text(encoding="utf-8") == "existing team config"
        assert (target / ".claude" / "settings.json").read_text(encoding="utf-8") == "{}"

        # 新内容写入 local 文件
        assert (target / "CLAUDE.local.md").exists()
        assert "test-api" in (target / "CLAUDE.local.md").read_text(encoding="utf-8")
        assert (target / ".claude" / "settings.local.json").exists()

    def test_local_file_exists_append(self, tmp_path):
        """CLAUDE.local.md 已存在时按策略追加"""
        core = _make_core_module(tmp_path)
        target = tmp_path / "output"
        target.mkdir()
        (target / "CLAUDE.md").write_text("team config", encoding="utf-8")
        (target / "CLAUDE.local.md").write_text("old local", encoding="utf-8")

        gen = Generator(
            modules={"core": core},
            load_order=["core"],
            variables={"PROJECT_NAME": "test-api"},
        )
        gen.generate(target, strategy="append")
        content = (target / "CLAUDE.local.md").read_text(encoding="utf-8")
        assert "old local" in content
        assert "test-api" in content
