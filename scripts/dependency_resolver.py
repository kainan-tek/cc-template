# scripts/dependency_resolver.py
"""依赖解析器：拓扑排序 + 冲突检测"""
from __future__ import annotations

from module_loader import Module

TYPE_ORDER = {"core": 0, "general": 1, "language": 2}


class DependencyResolver:
    def __init__(self, modules: dict[str, Module]):
        self.modules = modules

    def resolve(
        self,
        selected: list[str],
        preset_modules: list[str] | None = None,
        explicit_modules: list[str] | None = None,
    ) -> list[str]:
        # --preset 和 --module 互斥
        if preset_modules and explicit_modules:
            raise ValueError("--preset and --module cannot be used together")

        # 合并选中模块
        needed = set(selected)

        # 自动补全依赖
        needed = self._resolve_deps(needed)

        # core 始终包含
        if "core" in self.modules:
            needed.add("core")
            needed = self._resolve_deps(needed)

        # 冲突检测
        self._check_conflicts(needed)

        # 拓扑排序
        return self._topological_sort(needed)

    def _resolve_deps(self, needed: set[str]) -> set[str]:
        changed = True
        while changed:
            changed = False
            for name in list(needed):
                if name not in self.modules:
                    raise ValueError(
                        f"Dependency not found: module '{name}' does not exist"
                    )
                mod = self.modules[name]
                for dep in mod.depends:
                    if dep not in needed:
                        if dep not in self.modules:
                            raise ValueError(
                                f"Dependency not found: module '{name}' depends on '{dep}' which does not exist"
                            )
                        needed.add(dep)
                        changed = True
        return needed

    def _check_conflicts(self, needed: set[str]) -> None:
        for name in needed:
            mod = self.modules[name]
            for conflict in mod.conflicts:
                if conflict in needed:
                    raise ValueError(
                        f"Conflict: module '{name}' conflicts with '{conflict}'"
                    )

    def _topological_sort(self, needed: set[str]) -> list[str]:
        # Kahn's algorithm
        in_degree: dict[str, int] = {n: 0 for n in needed}
        adj: dict[str, list[str]] = {n: [] for n in needed}

        for name in needed:
            mod = self.modules[name]
            for dep in mod.depends:
                if dep in needed:
                    adj[dep].append(name)
                    in_degree[name] += 1

        # 初始零入度节点按 type + name 排序
        queue = sorted(
            [n for n in needed if in_degree[n] == 0],
            key=lambda n: (TYPE_ORDER.get(self.modules[n].type, 99), n),
        )

        result: list[str] = []
        while queue:
            node = queue.pop(0)
            result.append(node)
            for neighbor in sorted(
                adj[node],
                key=lambda n: (TYPE_ORDER.get(self.modules[n].type, 99), n),
            ):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    queue.sort(key=lambda n: (TYPE_ORDER.get(self.modules[n].type, 99), n))

        if len(result) != len(needed):
            raise ValueError("Circular dependency detected")

        return result
