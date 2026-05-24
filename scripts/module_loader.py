# scripts/module_loader.py
"""模块加载器：读取 modules/ 目录下的 module.yml"""
from __future__ import annotations

import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Module:
    """模块定义"""
    name: str
    version: str
    description: str
    type: str  # core | general | language
    depends: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    sections: list[dict[str, Any]] = field(default_factory=list)
    variables: list[dict[str, Any]] = field(default_factory=list)
    templates: list[dict[str, Any]] = field(default_factory=list)
    pre_commit_hooks: list[dict[str, Any]] = field(default_factory=list)
    gitignore_entries: list[str] = field(default_factory=list)
    commands: list[dict[str, Any]] = field(default_factory=list)
    path: Path = field(default_factory=Path)

    @property
    def settings_snippet_path(self) -> Path | None:
        p = self.path / "config" / "settings.json.snippet"
        return p if p.exists() else None


class ModuleLoader:
    """从目录加载所有模块"""

    def __init__(self, modules_dir: Path):
        self.modules_dir = modules_dir

    def load_all(self) -> dict[str, Module]:
        modules: dict[str, Module] = {}
        if not self.modules_dir.exists():
            return modules
        for item in sorted(self.modules_dir.iterdir()):
            if not item.is_dir():
                continue
            yml_path = item / "module.yml"
            if not yml_path.exists():
                raise FileNotFoundError(
                    f"module.yml not found in {item}"
                )
            mod = self._load_module(item, yml_path)
            modules[mod.name] = mod
        return modules

    def _load_module(self, mod_dir: Path, yml_path: Path) -> Module:
        with open(yml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return Module(
            name=data["name"],
            version=data.get("version", "0.0.0"),
            description=data.get("description", ""),
            type=data.get("type", "general"),
            depends=data.get("depends", []),
            conflicts=data.get("conflicts", []),
            sections=data.get("sections", []),
            variables=data.get("variables", []),
            templates=data.get("templates", []),
            pre_commit_hooks=data.get("pre_commit_hooks", []),
            gitignore_entries=data.get("gitignore_entries", []),
            commands=data.get("commands", []),
            path=mod_dir,
        )
