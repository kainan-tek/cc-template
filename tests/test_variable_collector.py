"""变量收集器测试"""
import pytest
from module_loader import Module
from variable_collector import VariableCollector


def _make_module(name: str, variables: list[dict] | None = None) -> Module:
    return Module(name=name, version="1.0.0", description="", type="general", variables=variables or [])


class TestVariableCollector:
    def test_collect_from_single_module(self):
        """从单个模块收集变量"""
        modules = {
            "core": _make_module("core", [
                {"name": "PROJECT_NAME", "prompt": "Project name", "default": ""},
            ]),
        }
        collector = VariableCollector(modules, ["core"])
        vars_def = collector.collect_definitions()
        assert "PROJECT_NAME" in vars_def
        assert vars_def["PROJECT_NAME"]["prompt"] == "Project name"

    def test_same_name_variable_merge(self):
        """同名变量合并：language 覆盖 general"""
        modules = {
            "testing": _make_module("testing", [
                {"name": "test_framework", "prompt": "Test framework", "default": "generic", "choices": ["generic"]},
            ]),
            "lang-python": Module(
                name="lang-python", version="1.0.0", description="", type="language",
                variables=[{"name": "test_framework", "prompt": "Test framework", "default": "pytest", "choices": ["pytest", "unittest"]}],
            ),
        }
        collector = VariableCollector(modules, ["testing", "lang-python"])
        vars_def = collector.collect_definitions()
        # language 模块后加载，默认值覆盖
        assert vars_def["test_framework"]["default"] == "pytest"
        # choices 取并集
        assert "generic" in vars_def["test_framework"]["choices"]
        assert "pytest" in vars_def["test_framework"]["choices"]

    def test_non_interactive_uses_defaults(self):
        """非交互模式使用默认值"""
        modules = {
            "core": _make_module("core", [
                {"name": "PROJECT_NAME", "prompt": "Name", "default": "my-project"},
            ]),
        }
        collector = VariableCollector(modules, ["core"])
        values = collector.collect_values(non_interactive=True)
        assert values["PROJECT_NAME"] == "my-project"

    def test_cli_var_overrides_default(self):
        """--var 参数覆盖默认值"""
        modules = {
            "core": _make_module("core", [
                {"name": "PROJECT_NAME", "prompt": "Name", "default": "my-project"},
            ]),
        }
        collector = VariableCollector(modules, ["core"])
        values = collector.collect_values(
            non_interactive=True,
            cli_vars={"PROJECT_NAME": "custom-name"},
        )
        assert values["PROJECT_NAME"] == "custom-name"

    def test_missing_required_var_in_non_interactive(self):
        """非交互模式缺少必填变量时报错"""
        modules = {
            "core": _make_module("core", [
                {"name": "PROJECT_NAME", "prompt": "Name", "default": ""},
            ]),
        }
        collector = VariableCollector(modules, ["core"])
        with pytest.raises(ValueError, match="PROJECT_NAME"):
            collector.collect_values(non_interactive=True)
