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
        "depends: []\nconflicts: []\n"
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
        """已有文件不覆盖（追加策略）"""
        core = _make_core_module(tmp_path)
        target = tmp_path / "output"
        target.mkdir()
        (target / "CLAUDE.md").write_text("existing content")

        gen = Generator(
            modules={"core": core},
            load_order=["core"],
            variables={"PROJECT_NAME": "test-api"},
        )
        gen.generate(target, strategy="append")

        content = (target / "CLAUDE.md").read_text(encoding="utf-8")
        assert "existing content" in content
        assert "test-api" in content

    def test_overwrite_creates_backup(self, tmp_path):
        """覆盖策略创建备份"""
        core = _make_core_module(tmp_path)
        target = tmp_path / "output"
        target.mkdir()
        (target / "CLAUDE.md").write_text("original")

        gen = Generator(
            modules={"core": core},
            load_order=["core"],
            variables={"PROJECT_NAME": "test-api"},
        )
        gen.generate(target, strategy="overwrite")

        assert (target / "CLAUDE.md.bak").exists()
        assert (target / "CLAUDE.md.bak").read_text() == "original"
        assert "test-api" in (target / "CLAUDE.md").read_text(encoding="utf-8")

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
