"""依赖解析器测试"""
import pytest
from module_loader import Module
from dependency_resolver import DependencyResolver


def _make_module(name: str, type: str = "general",
                 depends: list[str] | None = None,
                 conflicts: list[str] | None = None) -> Module:
    return Module(
        name=name, version="1.0.0", description="", type=type,
        depends=depends or [], conflicts=conflicts or [],
    )


class TestDependencyResolver:
    def test_auto_include_core(self):
        """core 始终被包含"""
        modules = {
            "core": _make_module("core", "core"),
            "testing": _make_module("testing", depends=["core"]),
        }
        resolver = DependencyResolver(modules)
        result = resolver.resolve(["testing"])
        assert "core" in result

    def test_topological_sort(self):
        """依赖拓扑排序：被依赖的先加载"""
        modules = {
            "core": _make_module("core", "core"),
            "git-convention": _make_module("git-convention", "general", depends=["core"]),
            "code-review": _make_module("code-review", "general", depends=["core", "git-convention"]),
        }
        resolver = DependencyResolver(modules)
        result = resolver.resolve(["code-review"])
        assert result.index("core") < result.index("git-convention")
        assert result.index("git-convention") < result.index("code-review")

    def test_type_ordering(self):
        """同层级 general 在 language 之前"""
        modules = {
            "core": _make_module("core", "core"),
            "testing": _make_module("testing", "general", depends=["core"]),
            "lang-python": _make_module("lang-python", "language", depends=["core"]),
        }
        resolver = DependencyResolver(modules)
        result = resolver.resolve(["testing", "lang-python"])
        assert result.index("testing") < result.index("lang-python")

    def test_conflict_detection(self):
        """冲突模块不可同时选中"""
        modules = {
            "core": _make_module("core", "core"),
            "lang-python": _make_module("lang-python", "language", depends=["core"], conflicts=["lang-cpp"]),
            "lang-cpp": _make_module("lang-cpp", "language", depends=["core"], conflicts=["lang-python"]),
        }
        resolver = DependencyResolver(modules)
        with pytest.raises(ValueError, match="[Cc]onflict"):
            resolver.resolve(["lang-python", "lang-cpp"])

    def test_circular_dependency_detection(self):
        """循环依赖报错"""
        modules = {
            "a": _make_module("a", depends=["b"]),
            "b": _make_module("b", depends=["a"]),
        }
        resolver = DependencyResolver(modules)
        with pytest.raises(ValueError, match="[Cc]ircular"):
            resolver.resolve(["a"])

    def test_missing_dependency(self):
        """依赖不存在时报错"""
        modules = {
            "a": _make_module("a", depends=["nonexistent"]),
        }
        resolver = DependencyResolver(modules)
        with pytest.raises(ValueError, match="[Dd]epend"):
            resolver.resolve(["a"])

    def test_preset_and_module_exclusive(self):
        """--preset 和 --module 不可同时使用"""
        modules = {"core": _make_module("core", "core")}
        resolver = DependencyResolver(modules)
        with pytest.raises(ValueError, match="[Pp]reset.*[Mm]odule"):
            resolver.resolve([], preset_modules=["core"], explicit_modules=["core"])
