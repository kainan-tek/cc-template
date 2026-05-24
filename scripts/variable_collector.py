# scripts/variable_collector.py
"""变量收集器：合并模块变量定义，收集用户输入"""
from __future__ import annotations

from module_loader import Module


class VariableCollector:
    def __init__(self, modules: dict[str, Module], load_order: list[str]):
        self.modules = modules
        self.load_order = load_order

    def collect_definitions(self) -> dict[str, dict]:
        """按加载顺序合并所有模块的变量定义，同名变量后覆盖先"""
        merged: dict[str, dict] = {}
        for name in self.load_order:
            mod = self.modules[name]
            for var in mod.variables:
                var_name = var["name"]
                if var_name in merged:
                    # 合并：default 后覆盖先，choices 取并集
                    existing = merged[var_name]
                    new_choices = var.get("choices", [])
                    old_choices = existing.get("choices", [])
                    if new_choices or old_choices:
                        # 并集去重，保持顺序
                        seen = set()
                        merged_choices = []
                        for c in old_choices + new_choices:
                            if c not in seen:
                                seen.add(c)
                                merged_choices.append(c)
                        existing["choices"] = merged_choices
                    existing["default"] = var.get("default", existing.get("default", ""))
                    existing["prompt"] = var.get("prompt", existing.get("prompt", ""))
                else:
                    merged[var_name] = dict(var)
        return merged

    def collect_values(
        self,
        non_interactive: bool = False,
        cli_vars: dict[str, str] | None = None,
    ) -> dict[str, str]:
        """收集变量值。非交互模式使用默认值 + cli_vars"""
        definitions = self.collect_definitions()
        values: dict[str, str] = {}
        cli_vars = cli_vars or {}

        for var_name, var_def in definitions.items():
            if var_name in cli_vars:
                values[var_name] = cli_vars[var_name]
            elif non_interactive:
                default = var_def.get("default", "")
                if not default:
                    raise ValueError(
                        f"Required variable '{var_name}' has no default value. "
                        f"Provide it via --var {var_name}=<value>"
                    )
                values[var_name] = default
            else:
                values[var_name] = self._prompt(var_name, var_def)

        return values

    def _prompt(self, var_name: str, var_def: dict) -> str:
        """交互式收集单个变量"""
        prompt = var_def.get("prompt", var_name)
        default = var_def.get("default", "")
        choices = var_def.get("choices", [])

        if choices:
            choice_str = "/".join(choices)
            display = f"{prompt} [{choice_str}]"
            if default:
                display += f" (default: {default})"
            display += ": "
        else:
            display = f"{prompt}"
            if default:
                display += f" (default: {default})"
            display += ": "

        while True:
            value = input(display).strip()
            if not value and default:
                return default
            if not value:
                print(f"  Error: {var_name} is required")
                continue
            if choices and value not in choices:
                print(f"  Error: must be one of {choices}")
                continue
            return value
