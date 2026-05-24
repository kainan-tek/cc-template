"""模块加载器测试"""
import pytest
from pathlib import Path
from module_loader import Module, ModuleLoader


class TestModuleLoader:
    def test_load_single_module(self, tmp_path):
        """能正确加载单个模块的 module.yml"""
        mod_dir = tmp_path / "core"
        mod_dir.mkdir()
        (mod_dir / "module.yml").write_text(
            "name: core\nversion: 1.0.0\ndescription: Core module\ntype: core\n"
            "depends: []\nconflicts: []\n"
        )
        loader = ModuleLoader(tmp_path)
        modules = loader.load_all()
        assert "core" in modules
        assert modules["core"].name == "core"
        assert modules["core"].type == "core"

    def test_load_module_with_sections(self, tmp_path):
        """能加载包含 sections 的模块"""
        mod_dir = tmp_path / "core"
        mod_dir.mkdir()
        (mod_dir / "module.yml").write_text(
            "name: core\nversion: 1.0.0\ndescription: Core\ntype: core\n"
            "depends: []\nconflicts: []\n"
            "sections:\n"
            "  - slot: coding-standards\n"
            "    file: snippets/coding-standards.md\n"
            "    order: 0\n"
        )
        loader = ModuleLoader(tmp_path)
        modules = loader.load_all()
        assert len(modules["core"].sections) == 1
        assert modules["core"].sections[0]["slot"] == "coding-standards"

    def test_load_module_with_variables(self, tmp_path):
        """能加载包含 variables 的模块"""
        mod_dir = tmp_path / "lang-python"
        mod_dir.mkdir()
        (mod_dir / "module.yml").write_text(
            "name: lang-python\nversion: 1.0.0\ndescription: Python\ntype: language\n"
            "depends: [core]\nconflicts: [lang-cpp]\n"
            "variables:\n"
            "  - name: formatter\n"
            "    prompt: 'Formatter'\n"
            "    default: ruff\n"
            "    choices: [ruff, black]\n"
        )
        loader = ModuleLoader(tmp_path)
        modules = loader.load_all()
        assert len(modules["lang-python"].variables) == 1
        assert modules["lang-python"].variables[0]["name"] == "formatter"

    def test_missing_module_yml_raises(self, tmp_path):
        """模块目录缺少 module.yml 时报错"""
        mod_dir = tmp_path / "broken"
        mod_dir.mkdir()
        loader = ModuleLoader(tmp_path)
        with pytest.raises(FileNotFoundError, match="module.yml"):
            loader.load_all()
