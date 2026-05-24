# CC Project Template 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现一个模块化的 Claude Code 项目模板仓库，包含 10 个模块、4 个预设和 Python 初始化脚本

**Architecture:** 模块化模板仓库，每个模块通过 module.yml 声明元数据、snippet、变量和文件贡献。init.py 负责模块加载、依赖解析、变量收集、文件合并和写入

**Tech Stack:** Python 3.10+、PyYAML、pytest

---

## 文件结构

```
cc-project-template/
├── modules/
│   ├── core/
│   │   ├── module.yml
│   │   ├── snippets/
│   │   │   ├── project-info.md
│   │   │   ├── behavior-guidelines.md
│   │   │   ├── coding-standards.md
│   │   │   └── testing.md
│   │   ├── config/
│   │   │   └── settings.json.snippet
│   │   └── templates/
│   │       ├── gitignore
│   │       └── README.md
│   ├── git-convention/
│   │   ├── module.yml
│   │   ├── snippets/
│   │   │   └── git-convention.md
│   │   ├── config/
│   │   │   └── commands/
│   │   │       └── commit.md
│   │   └── templates/
│   │       └── pre-commit-config.yaml
│   ├── testing/
│   │   ├── module.yml
│   │   ├── snippets/
│   │   │   └── testing.md
│   │   └── config/
│   │       └── commands/
│   │           └── test-run.md
│   ├── code-review/
│   │   ├── module.yml
│   │   ├── snippets/
│   │   │   └── code-review.md
│   │   ├── hooks/
│   │   │   └── pre-push-reminder.yaml
│   │   └── config/
│   │       └── commands/
│   │           └── review.md
│   ├── api-design/
│   │   ├── module.yml
│   │   ├── snippets/
│   │   │   ├── api-design-rest.md
│   │   │   ├── api-design-graphql.md
│   │   │   └── api-design-grpc.md
│   │   └── templates/
│   │       ├── openapi.yaml
│   │       ├── schema.graphql
│   │       └── service.proto
│   ├── automation/
│   │   ├── module.yml
│   │   ├── snippets/
│   │   │   ├── ci-github-actions.md
│   │   │   └── ci-gitlab-ci.md
│   │   ├── config/
│   │   │   └── settings.json.snippet
│   │   └── templates/
│   │       ├── ci.yml
│   │       └── gitlab-ci.yml
│   ├── security/
│   │   ├── module.yml
│   │   ├── snippets/
│   │   │   └── security.md
│   │   ├── hooks/
│   │   │   └── gitleaks.yaml
│   │   └── templates/
│   │       └── env.example
│   ├── lang-python/
│   │   ├── module.yml
│   │   ├── snippets/
│   │   │   ├── coding-standards.md
│   │   │   ├── testing.md
│   │   │   ├── testing.pytest.md
│   │   │   └── testing.unittest.md
│   │   ├── config/
│   │   │   ├── settings.json.snippet
│   │   │   └── commands/
│   │   │       └── pytest.md
│   │   ├── hooks/
│   │   │   ├── ruff.yaml
│   │   │   └── black.yaml
│   │   └── templates/
│   │       └── pyproject.toml
│   ├── lang-cpp/
│   │   ├── module.yml
│   │   ├── snippets/
│   │   │   ├── coding-standards.md
│   │   │   └── testing.md
│   │   ├── config/
│   │   │   ├── settings.json.snippet
│   │   │   └── commands/
│   │   │       └── ctest.md
│   │   ├── hooks/
│   │   │   └── clang-format.yaml
│   │   └── templates/
│   │       ├── CMakeLists.txt
│   │       ├── clang-format
│   │       └── clang-tidy
│   └── lang-shell/
│       ├── module.yml
│       ├── snippets/
│       │   ├── coding-standards.md
│       │   └── testing.md
│       ├── config/
│       │   ├── settings.json.snippet
│       │   └── commands/
│       │       └── bats.md
│       ├── hooks/
│       │   └── shellcheck.yaml
│       └── templates/
│           └── script-template.sh
├── presets/
│   ├── preset-minimal.yml
│   ├── preset-python.yml
│   ├── preset-cpp.yml
│   └── preset-shell.yml
├── scripts/
│   └── init.py
├── tests/
│   ├── conftest.py
│   ├── test_module_loader.py
│   ├── test_dependency_resolver.py
│   ├── test_merger.py
│   ├── test_variable_collector.py
│   ├── test_generator.py
│   └── test_init.py
├── pyproject.toml
└── README.md
```

---

### Task 1: 项目骨架与依赖

**Files:**
- Create: `pyproject.toml`
- Create: `tests/conftest.py`

- [ ] **Step 1: 创建 pyproject.toml**

```toml
[project]
name = "cc-project-template"
version = "0.1.0"
description = "Claude Code 项目开发工程模板"
requires-python = ">=3.10"
dependencies = [
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
]

[project.scripts]
cc-init = "scripts.init:main"
```

- [ ] **Step 2: 创建 tests/conftest.py**

```python
"""共享测试 fixtures"""
import sys
from pathlib import Path

# 将项目根目录加入 sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

MODULES_DIR = PROJECT_ROOT / "modules"
PRESETS_DIR = PROJECT_ROOT / "presets"
```

- [ ] **Step 3: 安装依赖**

Run: `pip install -e ".[dev]"`
Expected: 成功安装

- [ ] **Step 4: 验证 pytest 可用**

Run: `python -m pytest --co -q`
Expected: 无报错（可能显示 collected 0 items）

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml tests/conftest.py
git commit -m "feat: project skeleton with pyproject.toml and test conftest"
```

---

### Task 2: 模块加载器

**Files:**
- Create: `scripts/__init__.py`
- Create: `scripts/module_loader.py`
- Create: `tests/test_module_loader.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_module_loader.py
"""模块加载器测试"""
import pytest
from pathlib import Path
from module_loader import Module, ModuleLoader


class TestModuleLoader:
    def test_load_single_module(self, tmp_path):
        """能正确加载单个模块的 module.yml"""
        # 创建测试模块
        mod_dir = tmp_path / "core"
        mod_dir.mkdir()
        (mod_dir / "module.yml").write_text(
            "name: core\nversion: 1.0.0\ndescription: Core module\ntype: core\n"
            "depends: []\n"
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
            "depends: []\n"
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
            "depends: [core]\n"
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

    def test_load_modules_from_real_dir(self):
        """能从真实 modules 目录加载"""
        from conftest import MODULES_DIR
        if not MODULES_DIR.exists():
            pytest.skip("modules directory not yet created")
        loader = ModuleLoader(MODULES_DIR)
        modules = loader.load_all()
        assert "core" in modules
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m pytest tests/test_module_loader.py -v`
Expected: FAIL（module_loader 模块不存在）

- [ ] **Step 3: 实现 module_loader.py**

```python
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
            sections=data.get("sections", []),
            variables=data.get("variables", []),
            templates=data.get("templates", []),
            pre_commit_hooks=data.get("pre_commit_hooks", []),
            gitignore_entries=data.get("gitignore_entries", []),
            commands=data.get("commands", []),
            path=mod_dir,
        )
```

- [ ] **Step 4: 创建 scripts/__init__.py**

```python
# scripts/__init__.py
```

- [ ] **Step 5: 运行测试确认通过**

Run: `python -m pytest tests/test_module_loader.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add scripts/__init__.py scripts/module_loader.py tests/test_module_loader.py
git commit -m "feat: module loader with YAML parsing"
```

---

### Task 3: 依赖解析器

**Files:**
- Create: `scripts/dependency_resolver.py`
- Create: `tests/test_dependency_resolver.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_dependency_resolver.py
"""依赖解析器测试"""
import pytest
from module_loader import Module
from dependency_resolver import DependencyResolver


def _make_module(name: str, type: str = "general",
                 depends: list[str] | None = None) -> Module:
    return Module(
        name=name, version="1.0.0", description="", type=type,
        depends=depends or [],
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

    def test_multi_language_coexist(self):
        """多语言模块可同时选中"""
        modules = {
            "core": _make_module("core", "core"),
            "lang-python": _make_module("lang-python", "language", depends=["core"]),
            "lang-cpp": _make_module("lang-cpp", "language", depends=["core"]),
        }
        resolver = DependencyResolver(modules)
        result = resolver.resolve(["lang-python", "lang-cpp"])
        assert "lang-python" in result
        assert "lang-cpp" in result

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
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m pytest tests/test_dependency_resolver.py -v`
Expected: FAIL

- [ ] **Step 3: 实现 dependency_resolver.py**

```python
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
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest tests/test_dependency_resolver.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/dependency_resolver.py tests/test_dependency_resolver.py
git commit -m "feat: dependency resolver with topological sort"
```

---

### Task 4: 变量收集器

**Files:**
- Create: `scripts/variable_collector.py`
- Create: `tests/test_variable_collector.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_variable_collector.py
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
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m pytest tests/test_variable_collector.py -v`
Expected: FAIL

- [ ] **Step 3: 实现 variable_collector.py**

```python
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
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest tests/test_variable_collector.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/variable_collector.py tests/test_variable_collector.py
git commit -m "feat: variable collector with merge and interactive input"
```

---

### Task 5: 文件合并器

**Files:**
- Create: `scripts/merger.py`
- Create: `tests/test_merger.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_merger.py
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

        # 创建 snippet 文件
        (tmp_path / "core" / "snippets").mkdir(parents=True)
        (tmp_path / "core" / "snippets" / "core-coding.md").write_text("## 编码规范\n\n通用规范")
        (tmp_path / "lang-python" / "snippets").mkdir(parents=True)
        (tmp_path / "lang-python" / "snippets" / "python-coding.md").write_text("### Python 编码规范\n\nPython 规范")

        merger = Merger({"core": core, "lang-python": lang}, ["core", "lang-python"], {})
        result = merger.merge_claude_md()
        assert "通用规范" in result
        assert "Python 规范" in result
        # core order=0 在前
        assert result.index("通用规范") < result.index("Python 规范")

    def test_empty_slot_not_appeared(self, tmp_path):
        """没有模块贡献的章节不出现"""
        core = _make_module("core", "core", sections=[], path=tmp_path / "core")
        merger = Merger({"core": core}, ["core"], {})
        result = merger.merge_claude_md()
        assert result.strip() == ""

    def test_update_markers_inserted(self, tmp_path):
        """snippet 前插入更新标记（仅开始标记）"""
        core = _make_module("core", "core", sections=[
            {"slot": "coding-standards", "file": "snippets/coding.md", "order": 0},
        ], path=tmp_path / "core")
        (tmp_path / "core" / "snippets").mkdir(parents=True)
        (tmp_path / "core" / "snippets" / "coding.md").write_text("## 编码规范\n\n内容")

        merger = Merger({"core": core}, ["core"], {})
        result = merger.merge_claude_md()
        assert "<!-- module:core:1.0.0:coding-standards -->" in result
        assert "<!-- /module:" not in result


class TestSettingsMerger:
    def test_deep_merge(self, tmp_path):
        """settings.json 深度合并"""
        core = _make_module("core", "core", path=tmp_path / "core")
        (tmp_path / "core" / "config").mkdir(parents=True)
        (tmp_path / "core" / "config" / "settings.json.snippet").write_text(json.dumps({
            "permissions": {"allow": ["Read", "Glob"]},
        }))

        lang = _make_module("lang-python", "language", path=tmp_path / "lang-python")
        (tmp_path / "lang-python" / "config").mkdir(parents=True)
        (tmp_path / "lang-python" / "config" / "settings.json.snippet").write_text(json.dumps({
            "permissions": {"allow": ["Bash(pytest)"]},
        }))

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
        }))

        lang = _make_module("lang-python", "language", path=tmp_path / "lang-python")
        (tmp_path / "lang-python" / "config").mkdir(parents=True)
        (tmp_path / "lang-python" / "config" / "settings.json.snippet").write_text(json.dumps({
            "permissions": {"allow": ["Read", "Bash(pytest)"]},
        }))

        merger = Merger({"core": core, "lang-python": lang}, ["core", "lang-python"], {})
        result = merger.merge_settings()
        # Read 不重复
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
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m pytest tests/test_merger.py -v`
Expected: FAIL

- [ ] **Step 3: 实现 merger.py**

```python
# scripts/merger.py
"""文件合并器：合并 snippets、settings、pre-commit、gitignore"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from module_loader import Module

# 预定义章节顺序
SECTION_ORDER = [
    "project-info",
    "behavior-guidelines",
    "coding-standards",
    "testing",
    "git-convention",
    "code-review",
    "api-design",
    "security",
    "automation",
]


class Merger:
    def __init__(
        self,
        modules: dict[str, Module],
        load_order: list[str],
        variables: dict[str, str],
    ):
        self.modules = modules
        self.load_order = load_order
        self.variables = variables

    def merge_claude_md(self) -> str:
        """合并所有模块的 snippet 为 CLAUDE.md"""
        # 按章节聚合
        sections: dict[str, list[tuple[int, str, Module]]] = {}
        custom_sections: dict[str, list[tuple[int, str, Module]]] = {}

        for name in self.load_order:
            mod = self.modules[name]
            for sec in mod.sections:
                slot = sec["slot"]
                order = sec.get("order", 50)
                # 条件选择
                file_path = self._resolve_condition(sec, "file")
                full_path = mod.path / file_path
                if not full_path.exists():
                    continue
                content = full_path.read_text(encoding="utf-8")
                content = self._replace_variables(content)

                entry = (order, content, mod)
                if slot in SECTION_ORDER:
                    sections.setdefault(slot, []).append(entry)
                else:
                    custom_sections.setdefault(slot, []).append(entry)

        # 按预定义顺序输出
        parts: list[str] = []
        for slot in SECTION_ORDER:
            if slot in sections:
                parts.append(self._render_section(slot, sections[slot]))

        # 自定义章节追加
        for slot in sorted(custom_sections.keys()):
            parts.append(self._render_section(slot, custom_sections[slot]))

        return "\n\n".join(parts)

    def _render_section(self, slot: str, entries: list[tuple[int, str, Module]]) -> str:
        entries.sort(key=lambda e: (e[0], e[2].name))
        parts: list[str] = []
        for order, content, mod in entries:
            marker_open = f"<!-- module:{mod.name}:{mod.version}:{slot} -->"
            parts.append(f"{marker_open}\n{content}")
        return "\n".join(parts)

    def merge_settings(self) -> dict:
        """深度合并 settings.json.snippet"""
        result: dict = {}
        for name in self.load_order:
            mod = self.modules[name]
            snippet_path = mod.settings_snippet_path
            if not snippet_path:
                continue
            content = snippet_path.read_text(encoding="utf-8")
            content = self._replace_variables(content)
            snippet = json.loads(content)
            result = self._deep_merge(result, snippet)
        return result

    def merge_pre_commit(self, existing_content: str | None = None) -> str:
        """合并 .pre-commit-config.yaml"""
        repos: list[dict] = []

        if existing_content:
            existing = yaml.safe_load(existing_content)
            if existing and "repos" in existing:
                repos.extend(existing["repos"])

        existing_urls = {r.get("repo", "") for r in repos}

        for name in self.load_order:
            mod = self.modules[name]
            for hook_def in mod.pre_commit_hooks:
                file_path = self._resolve_condition(hook_def, "file")
                full_path = mod.path / file_path
                if not full_path.exists():
                    continue
                content = full_path.read_text(encoding="utf-8")
                content = self._replace_variables(content)
                hook_data = yaml.safe_load(content)
                if isinstance(hook_data, dict):
                    repo_url = hook_data.get("repo", "")
                    if repo_url not in existing_urls:
                        repos.append(hook_data)
                        existing_urls.add(repo_url)

        if not repos:
            return ""

        result = {"repos": repos}
        return yaml.dump(result, default_flow_style=False, allow_unicode=True, sort_keys=False)

    def merge_gitignore(self, existing_content: str | None = None) -> str:
        """合并 .gitignore 条目"""
        existing_lines: set[str] = set()
        result_lines: list[str] = []

        if existing_content:
            for line in existing_content.strip().split("\n"):
                stripped = line.strip()
                if stripped:
                    existing_lines.add(stripped)
                    result_lines.append(stripped)

        for name in self.load_order:
            mod = self.modules[name]
            for entry in mod.gitignore_entries:
                if entry not in existing_lines:
                    existing_lines.add(entry)
                    result_lines.append(entry)

        return "\n".join(result_lines) + "\n"

    def _resolve_condition(self, definition: dict, key: str) -> str:
        """解析条件，返回匹配的 file 或 source"""
        conditions = definition.get("conditions", [])
        for cond in conditions:
            when = cond.get("when", "")
            if self._evaluate_condition(when):
                return cond.get(key, definition.get(key, ""))
        return definition.get(key, "")

    def _evaluate_condition(self, when: str) -> bool:
        """评估 when 条件：变量名 == 值"""
        match = re.match(r"(\w+)\s*==\s*(.+)", when.strip())
        if not match:
            return False
        var_name, expected = match.group(1), match.group(2).strip()
        actual = self.variables.get(var_name)
        if actual is None:
            print(f"  Warning: variable '{var_name}' referenced in condition is not defined")
            return False
        return actual == expected

    def _replace_variables(self, text: str) -> str:
        """替换 {{VAR}} 为变量值"""
        def replacer(match: re.Match) -> str:
            var_name = match.group(1)
            if var_name in self.variables:
                return self.variables[var_name]
            return match.group(0)  # 保留原样
        return re.sub(r"\{\{(\w+)\}\}", replacer, text)

    @staticmethod
    def _deep_merge(base: dict, override: dict) -> dict:
        """深度合并两个字典"""
        result = dict(base)
        for key, value in override.items():
            if key in result:
                if isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = Merger._deep_merge(result[key], value)
                elif isinstance(result[key], list) and isinstance(value, list):
                    # 数组拼接 + 去重
                    merged = result[key] + value
                    seen: set[str] = set()
                    deduped: list = []
                    for item in merged:
                        key_str = json.dumps(item, sort_keys=True, ensure_ascii=False)
                        if key_str not in seen:
                            seen.add(key_str)
                            deduped.append(item)
                    result[key] = deduped
                else:
                    result[key] = value  # 标量：后覆盖先
            else:
                result[key] = value
        return result
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest tests/test_merger.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/merger.py tests/test_merger.py
git commit -m "feat: file merger for CLAUDE.md, settings, pre-commit, gitignore"
```

---

### Task 6: 生成器

**Files:**
- Create: `scripts/generator.py`
- Create: `tests/test_generator.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_generator.py
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
    (mod_dir / "snippets" / "info.md").write_text("## 项目信息\n\n{{PROJECT_NAME}}")
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
        assert "test-api" in (target / "CLAUDE.md").read_text()
        assert (target / ".claude" / "settings.json").exists()

    def test_generate_does_not_overwrite_existing(self, tmp_path):
        """已有文件不覆盖"""
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

        content = (target / "CLAUDE.md").read_text()
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
        assert "test-api" in (target / "CLAUDE.md").read_text()

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
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m pytest tests/test_generator.py -v`
Expected: FAIL

- [ ] **Step 3: 实现 generator.py**

```python
# scripts/generator.py
"""生成器：将合并结果写入目标目录"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from merger import Merger
from module_loader import Module


class Generator:
    def __init__(
        self,
        modules: dict[str, Module],
        load_order: list[str],
        variables: dict[str, str],
    ):
        self.modules = modules
        self.load_order = load_order
        self.variables = variables
        self.merger = Merger(modules, load_order, variables)
        self.written_files: list[Path] = []

    def generate(
        self,
        target_dir: Path,
        strategy: str = "append",
        dry_run: bool = False,
    ) -> list[Path]:
        """生成所有文件到目标目录，返回写入的文件列表"""
        target_dir.mkdir(parents=True, exist_ok=True)
        self.written_files = []

        # 1. CLAUDE.md
        self._write_claude_md(target_dir, strategy, dry_run)

        # 2. settings.json
        self._write_settings(target_dir, dry_run)

        # 3. .pre-commit-config.yaml
        self._write_pre_commit(target_dir, dry_run)

        # 4. .gitignore
        self._write_gitignore(target_dir, dry_run)

        # 5. commands
        self._write_commands(target_dir, dry_run)

        # 6. templates
        self._write_templates(target_dir, dry_run)

        return self.written_files

    def _write_claude_md(self, target_dir: Path, strategy: str, dry_run: bool) -> None:
        target = target_dir / "CLAUDE.md"
        new_content = self.merger.merge_claude_md()

        if target.exists():
            if strategy == "overwrite":
                if not dry_run:
                    shutil.copy2(target, target_dir / "CLAUDE.md.bak")
                    target.write_text(new_content, encoding="utf-8")
                self.written_files.append(target)
            else:  # append
                existing = target.read_text(encoding="utf-8")
                # 检测重复章节标题
                self._warn_duplicate_headings(existing, new_content)
                if not dry_run:
                    target.write_text(existing + "\n\n" + new_content, encoding="utf-8")
                self.written_files.append(target)
        else:
            if not dry_run:
                target.write_text(new_content, encoding="utf-8")
            self.written_files.append(target)

    def _write_settings(self, target_dir: Path, dry_run: bool) -> None:
        settings_dir = target_dir / ".claude"
        target = settings_dir / "settings.json"

        if target.exists():
            # 不覆盖，输出提示
            print(f"  Skip: {target} already exists")
            return

        merged = self.merger.merge_settings()
        if not merged:
            return

        if not dry_run:
            settings_dir.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        self.written_files.append(target)

    def _write_pre_commit(self, target_dir: Path, dry_run: bool) -> None:
        target = target_dir / ".pre-commit-config.yaml"

        existing_content = None
        if target.exists():
            existing_content = target.read_text(encoding="utf-8")

        result = self.merger.merge_pre_commit(existing_content)
        if not result:
            return

        if target.exists() and not existing_content:
            return

        if not dry_run:
            target.write_text(result, encoding="utf-8")
        self.written_files.append(target)

    def _write_gitignore(self, target_dir: Path, dry_run: bool) -> None:
        target = target_dir / ".gitignore"

        existing_content = None
        if target.exists():
            existing_content = target.read_text(encoding="utf-8")

        result = self.merger.merge_gitignore(existing_content)
        if not dry_run:
            target.write_text(result, encoding="utf-8")
        self.written_files.append(target)

    def _write_commands(self, target_dir: Path, dry_run: bool) -> None:
        commands_dir = target_dir / ".claude" / "commands"
        existing_names: set[str] = set()

        if commands_dir.exists():
            existing_names = {f.name for f in commands_dir.iterdir() if f.is_file()}

        for name in self.load_order:
            mod = self.modules[name]
            for cmd_def in mod.commands:
                cmd_name = cmd_def["name"]
                file_path = mod.path / cmd_def["file"]
                if not file_path.exists():
                    continue

                target_name = f"{cmd_name}.md"
                if target_name in existing_names:
                    print(f"  Error: command file '{target_name}' already exists")
                    continue

                content = file_path.read_text(encoding="utf-8")
                content = self.merger._replace_variables(content)

                if not dry_run:
                    commands_dir.mkdir(parents=True, exist_ok=True)
                    (commands_dir / target_name).write_text(content, encoding="utf-8")
                self.written_files.append(commands_dir / target_name)

    def _write_templates(self, target_dir: Path, dry_run: bool) -> None:
        for name in self.load_order:
            mod = self.modules[name]
            for tpl_def in mod.templates:
                source_path = self.merger._resolve_condition(tpl_def, "source")
                full_source = mod.path / source_path
                if not full_source.exists():
                    continue

                target_path = target_dir / tpl_def["target"]
                if target_path.exists():
                    # 内容相同则跳过，不同则报错
                    existing = target_path.read_bytes()
                    new = full_source.read_bytes()
                    if existing == new:
                        continue
                    print(f"  Skip: {target_path} already exists with different content")
                    continue

                content = full_source.read_text(encoding="utf-8")
                content = self.merger._replace_variables(content)

                if not dry_run:
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    target_path.write_text(content, encoding="utf-8")
                self.written_files.append(target_path)

    @staticmethod
    def _warn_duplicate_headings(existing: str, new_content: str) -> None:
        """检测已有 CLAUDE.md 中与生成内容相同的 ## 级别标题"""
        import re
        existing_headings = set(re.findall(r"^## .+$", existing, re.MULTILINE))
        new_headings = re.findall(r"^## .+$", new_content, re.MULTILINE)
        for h in new_headings:
            if h in existing_headings:
                print(f"  Warning: duplicate heading in CLAUDE.md: {h}")
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m pytest tests/test_generator.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/generator.py tests/test_generator.py
git commit -m "feat: generator with append/overwrite strategies and safe file handling"
```

---

### Task 7: init.py 主脚本

**Files:**
- Create: `scripts/init.py`
- Create: `tests/test_init.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_init.py
"""init.py 集成测试"""
import json
import pytest
from pathlib import Path
from init import run_init


class TestInitIntegration:
    def test_new_project_with_preset(self, tmp_path):
        """使用预设创建新项目"""
        # 需要真实的 modules 和 presets 目录
        from conftest import MODULES_DIR, PRESETS_DIR
        if not MODULES_DIR.exists():
            pytest.skip("modules directory not yet created")

        target = tmp_path / "my-project"
        run_init(
            target_dir=target,
            modules_dir=MODULES_DIR,
            presets_dir=PRESETS_DIR,
            preset="preset-minimal",
            non_interactive=True,
            cli_vars={"PROJECT_NAME": "test-proj", "PROJECT_DESCRIPTION": "Test", "TECH_STACK": "Python"},
        )

        assert (target / "CLAUDE.md").exists()
        assert "test-proj" in (target / "CLAUDE.md").read_text()

    def test_preset_and_module_exclusive(self, tmp_path):
        """--preset 和 --module 不可同时使用"""
        from conftest import MODULES_DIR, PRESETS_DIR
        if not MODULES_DIR.exists():
            pytest.skip("modules directory not yet created")

        target = tmp_path / "my-project"
        with pytest.raises(ValueError, match="[Pp]reset.*[Mm]odule"):
            run_init(
                target_dir=target,
                modules_dir=MODULES_DIR,
                presets_dir=PRESETS_DIR,
                preset="preset-minimal",
                modules=["core"],
                non_interactive=True,
            )

    def test_non_interactive_missing_required_var(self, tmp_path):
        """非交互模式缺少必填变量时报错"""
        from conftest import MODULES_DIR, PRESETS_DIR
        if not MODULES_DIR.exists():
            pytest.skip("modules directory not yet created")

        target = tmp_path / "my-project"
        with pytest.raises(ValueError):
            run_init(
                target_dir=target,
                modules_dir=MODULES_DIR,
                presets_dir=PRESETS_DIR,
                preset="preset-minimal",
                non_interactive=True,
                # 不传 PROJECT_NAME
            )

    def test_diff_mode_no_files_written(self, tmp_path):
        """--diff 模式不写入文件"""
        from conftest import MODULES_DIR, PRESETS_DIR
        if not MODULES_DIR.exists():
            pytest.skip("modules directory not yet created")

        target = tmp_path / "my-project"
        run_init(
            target_dir=target,
            modules_dir=MODULES_DIR,
            presets_dir=PRESETS_DIR,
            preset="preset-minimal",
            non_interactive=True,
            cli_vars={"PROJECT_NAME": "test-proj", "PROJECT_DESCRIPTION": "Test", "TECH_STACK": "Python"},
            diff_only=True,
        )

        assert not (target / "CLAUDE.md").exists()
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m pytest tests/test_init.py -v`
Expected: FAIL

- [ ] **Step 3: 实现 init.py**

```python
#!/usr/bin/env python3
# scripts/init.py
"""CC Project Template 初始化脚本"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from dependency_resolver import DependencyResolver
from generator import Generator
from module_loader import ModuleLoader
from variable_collector import VariableCollector


def run_init(
    target_dir: Path,
    modules_dir: Path,
    presets_dir: Path,
    preset: str | None = None,
    modules: list[str] | None = None,
    non_interactive: bool = False,
    cli_vars: dict[str, str] | None = None,
    diff_only: bool = False,
    strategy: str = "append",
) -> list[Path]:
    """主初始化逻辑"""

    # 1. 加载模块
    loader = ModuleLoader(modules_dir)
    all_modules = loader.load_all()

    # 2. 确定选中模块
    preset_modules = None
    explicit_modules = None

    if preset:
        preset_path = presets_dir / f"{preset}.yml"
        if not preset_path.exists():
            raise ValueError(f"Preset not found: {preset}")
        with open(preset_path, "r", encoding="utf-8") as f:
            preset_data = yaml.safe_load(f)
        preset_modules = preset_data.get("modules", [])

    if modules:
        explicit_modules = modules

    # 3. 依赖解析
    selected = preset_modules or explicit_modules or []
    resolver = DependencyResolver(all_modules)
    load_order = resolver.resolve(
        selected,
        preset_modules=preset_modules,
        explicit_modules=explicit_modules,
    )

    # 4. 收集变量
    collector = VariableCollector(all_modules, load_order)
    variables = collector.collect_values(
        non_interactive=non_interactive,
        cli_vars=cli_vars,
    )

    # 5. 生成
    gen = Generator(all_modules, load_order, variables)

    if diff_only:
        # 干运行：仅预览不写入
        files = gen.generate(target_dir, strategy=strategy, dry_run=True)
        print("\nFiles to be generated:")
        for f in files:
            print(f"  {f}")
        return files

    # 6. 检查已有 CLAUDE.md
    claude_md = target_dir / "CLAUDE.md"
    if claude_md.exists() and not non_interactive:
        answer = input(f"\n{claude_md} already exists. Strategy (append/overwrite)? [append] ").strip()
        if answer == "overwrite":
            strategy = "overwrite"

    # 7. 写入
    files = gen.generate(target_dir, strategy=strategy)
    print(f"\nGenerated {len(files)} files:")
    for f in files:
        print(f"  {f}")

    return files


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CC Project Template Initializer")
    parser.add_argument("target", type=Path, help="Target project directory")
    parser.add_argument("--preset", help="Preset name (e.g., preset-python)")
    parser.add_argument("--module", help="Comma-separated module names")
    parser.add_argument("--non-interactive", action="store_true", help="Use defaults for all variables")
    parser.add_argument("--var", action="append", help="Variable override (KEY=VALUE)")
    parser.add_argument("--diff", action="store_true", help="Dry-run: preview only, no files written")

    args = parser.parse_args(argv)

    # 解析 --module
    if args.module:
        args.modules = [m.strip() for m in args.module.split(",")]
    else:
        args.modules = None

    # 解析 --var
    args.cli_vars = {}
    if args.var:
        for v in args.var:
            key, _, value = v.partition("=")
            args.cli_vars[key.strip()] = value.strip()

    return args


def main() -> None:
    args = parse_args()

    # 确定项目根目录（scripts/init.py 的上上级）
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    modules_dir = project_root / "modules"
    presets_dir = project_root / "presets"

    try:
        run_init(
            target_dir=args.target,
            modules_dir=modules_dir,
            presets_dir=presets_dir,
            preset=args.preset,
            modules=args.modules,
            non_interactive=args.non_interactive,
            cli_vars=args.cli_vars,
            diff_only=args.diff,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 运行测试确认通过（跳过需要真实模块的测试）**

Run: `python -m pytest tests/test_init.py -v -k "not Integration"`
Expected: PASS（集成测试会 skip）

- [ ] **Step 5: Commit**

```bash
git add scripts/init.py tests/test_init.py
git commit -m "feat: init.py main script with CLI argument parsing"
```

---

### Task 8: Core 模块内容

**Files:**
- Create: `modules/core/module.yml`
- Create: `modules/core/snippets/project-info.md`
- Create: `modules/core/snippets/behavior-guidelines.md`
- Create: `modules/core/snippets/coding-standards.md`
- Create: `modules/core/snippets/testing.md`
- Create: `modules/core/config/settings.json.snippet`
- Create: `modules/core/templates/gitignore`
- Create: `modules/core/templates/README.md`

- [ ] **Step 1: 创建 module.yml**

```yaml
# modules/core/module.yml
name: core
version: 1.0.0
description: 核心模块（必选）
type: core
depends: []

sections:
  - slot: project-info
    file: snippets/project-info.md
    order: 0
  - slot: behavior-guidelines
    file: snippets/behavior-guidelines.md
    order: 0
  - slot: coding-standards
    file: snippets/coding-standards.md
    order: 0
  - slot: testing
    file: snippets/testing.md
    order: 0

variables:
  - name: PROJECT_NAME
    prompt: "项目名称"
    default: ""
  - name: PROJECT_DESCRIPTION
    prompt: "项目描述"
    default: ""
  - name: TECH_STACK
    prompt: "技术栈"
    default: ""

templates:
  - source: templates/gitignore
    target: .gitignore
  - source: templates/README.md
    target: README.md

gitignore_entries:
  - ".env"
  - "dist/"
  - "build/"
  - "*.egg-info/"
```

- [ ] **Step 2: 创建 snippets/project-info.md**

```markdown
## 项目信息

- **项目名称**：{{PROJECT_NAME}}
- **项目描述**：{{PROJECT_DESCRIPTION}}
- **技术栈**：{{TECH_STACK}}
```

- [ ] **Step 3: 创建 snippets/behavior-guidelines.md**

```markdown
## 行为准则

基于 Andrej Karpathy 的 LLM 编码观察，遵循以下四原则：

### 1. 先思考再编码

- 不确定时先问，不静默选择解读
- 多种理解全部呈现，由用户决定
- 有更简方案直说，不为了"完整性"添加复杂度
- 不清楚就停，宁可多问一次也不猜错

### 2. 简单至上

- 不添加未请求的功能
- 单次使用不做抽象，三行重复代码优于过早抽象
- 200 行能变 50 行就重写
- 不为假设的未来需求预留扩展点

### 3. 精准修改

- 不顺手改周边代码
- 匹配现有风格，不引入风格不一致的改动
- 无关死代码提及但不删
- 自己造成的废弃代码必须清理

### 4. 目标驱动执行

- 用测试定义成功标准
- 多步骤任务先列计划（步骤 → 验证检查）
- 每步验证后再进入下一步
```

- [ ] **Step 4: 创建 snippets/coding-standards.md**

```markdown
## 编码规范

### 通用规范

- 代码可读性优先于性能优化
- 函数/方法单一职责
- 避免嵌套超过 3 层
- 使用有意义的命名，禁止单字母变量（循环变量除外）

### 文档规范

- 公共 API 必须有文档
- 变更日志通过 commit message 记录
- 复杂逻辑必须加注释说明意图
```

- [ ] **Step 5: 创建 snippets/testing.md**

```markdown
## 测试规范

### 通用测试原则

- 测试是代码质量的保障，不是负担
- 每个功能必须有对应的测试
- 测试应该快速、独立、可重复
- 测试命名应清晰表达测试意图
```

- [ ] **Step 6: 创建 config/settings.json.snippet**

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep"
    ]
  }
}
```

- [ ] **Step 7: 创建 templates/gitignore**

```
# Environment
.env

# Build artifacts
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
```

- [ ] **Step 8: 创建 templates/README.md**

```markdown
# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

## 技术栈

{{TECH_STACK}}

## 使用 Claude Code 开发

本项目使用 Claude Code 辅助开发，请阅读 `CLAUDE.md` 了解项目规范。
```

- [ ] **Step 9: 运行已有测试确认不破坏**

Run: `python -m pytest tests/ -v`
Expected: PASS

- [ ] **Step 10: Commit**

```bash
git add modules/core/
git commit -m "feat: core module with snippets, settings, and templates"
```

---

### Task 9: Git Convention 模块

**Files:**
- Create: `modules/git-convention/module.yml`
- Create: `modules/git-convention/snippets/git-convention.md`
- Create: `modules/git-convention/config/commands/commit.md`
- Create: `modules/git-convention/templates/pre-commit-config.yaml`

- [ ] **Step 1: 创建 module.yml**

```yaml
name: git-convention
version: 1.0.0
description: Git 规范模块
type: general
depends: [core]

sections:
  - slot: git-convention
    file: snippets/git-convention.md
    order: 0

variables:
  - name: commit_lang
    prompt: "Commit message 语言"
    default: "en"
    choices: ["en", "zh"]

templates:
  - source: templates/pre-commit-config.yaml
    target: .pre-commit-config.yaml

commands:
  - name: commit
    file: config/commands/commit.md
```

- [ ] **Step 2: 创建 snippets/git-convention.md**

```markdown
## Git 规范

### Conventional Commits

提交信息格式：`<type>(<scope>): <description>`

**类型**：
- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档变更
- `refactor`: 重构（不改变行为）
- `test`: 测试相关
- `chore`: 构建/工具变更

**分支命名**：`<type>/<description>`（如 `feat/user-auth`）

**PR 标题**：与 commit message 格式一致
```

- [ ] **Step 3: 创建 config/commands/commit.md**

```markdown
分析当前 `git diff --cached` 的内容，生成符合 Conventional Commits 规范的 commit message。

规则：
- 格式：`<type>(<scope>): <description>`
- type 从 feat/fix/docs/refactor/test/chore 中选择
- description 简洁明确，不超过 72 字符
- 语言：{{commit_lang}}
```

- [ ] **Step 4: 创建 templates/pre-commit-config.yaml**

```yaml
repos:
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.6.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
```

- [ ] **Step 5: Commit**

```bash
git add modules/git-convention/
git commit -m "feat: git-convention module with commit-msg hook"
```

---

### Task 10: Testing 模块

**Files:**
- Create: `modules/testing/module.yml`
- Create: `modules/testing/snippets/testing.md`
- Create: `modules/testing/config/commands/test-run.md`

- [ ] **Step 1: 创建 module.yml**

```yaml
name: testing
version: 1.0.0
description: 测试规范模块
type: general
depends: [core]

sections:
  - slot: testing
    file: snippets/testing.md
    order: 50

commands:
  - name: test-run
    file: config/commands/test-run.md
```

- [ ] **Step 2: 创建 snippets/testing.md**

```markdown
### 测试策略

- **单元测试**：覆盖核心逻辑，目标覆盖率 ≥ 80%
- **集成测试**：验证模块间交互
- **E2E 测试**：验证关键用户路径
- 比例建议：单元 70% / 集成 20% / E2E 10%

### 命名规范

测试函数命名：`test_<功能>_<场景>_<预期>`

示例：`test_login_invalid_password_returns_401`

### 核心规则

- Bug 修复必须加回归测试
- 测试应该快速、独立、可重复
- 不为测试而测试，每个测试应验证明确的行为
```

- [ ] **Step 3: 创建 config/commands/test-run.md**

```markdown
运行项目测试并分析失败原因。

步骤：
1. 识别项目使用的测试框架
2. 运行测试
3. 如果有失败，分析失败原因并给出修复建议
```

- [ ] **Step 4: Commit**

```bash
git add modules/testing/
git commit -m "feat: testing module with test strategy and naming conventions"
```

---

### Task 11: Code Review 模块

**Files:**
- Create: `modules/code-review/module.yml`
- Create: `modules/code-review/snippets/code-review.md`
- Create: `modules/code-review/hooks/pre-push-reminder.yaml`
- Create: `modules/code-review/config/commands/review.md`

- [ ] **Step 1: 创建 module.yml**

```yaml
name: code-review
version: 1.0.0
description: 代码审查模块
type: general
depends: [core, git-convention]

sections:
  - slot: code-review
    file: snippets/code-review.md
    order: 0

pre_commit_hooks:
  - file: hooks/pre-push-reminder.yaml

commands:
  - name: review
    file: config/commands/review.md
```

- [ ] **Step 2: 创建 snippets/code-review.md**

```markdown
## 代码审查

### Review Checklist

- [ ] **逻辑正确性**：边界条件、空值处理、错误路径
- [ ] **安全性**：输入校验、权限检查、敏感数据处理
- [ ] **性能**：N+1 查询、不必要的循环、内存泄漏
- [ ] **可读性**：命名清晰、逻辑直观、注释恰当

### PR 描述模板

```
## 变更说明
[简要描述本次变更的目的和内容]

## 变更影响范围
[列出受影响的模块/功能]

## 测试
[描述如何验证本次变更]
```
```

- [ ] **Step 3: 创建 hooks/pre-push-reminder.yaml**

```yaml
repo: local
hooks:
  - id: review-reminder
    name: Review reminder
    entry: echo "Reminder: Please review your changes before pushing"
    language: system
    stages: [pre-push]
```

- [ ] **Step 4: 创建 config/commands/review.md**

```markdown
对当前 `git diff` 的内容做代码审查。

审查维度：
1. 逻辑正确性：边界条件、空值处理
2. 安全性：输入校验、权限检查
3. 性能：N+1 查询、不必要的循环
4. 可读性：命名、逻辑清晰度

输出格式：
- 按严重程度分类（Critical / Major / Minor）
- 每个问题给出具体位置和修复建议
```

- [ ] **Step 5: Commit**

```bash
git add modules/code-review/
git commit -m "feat: code-review module with checklist and pre-push hook"
```

---

### Task 12: API Design 模块

**Files:**
- Create: `modules/api-design/module.yml`
- Create: `modules/api-design/snippets/api-design-rest.md`
- Create: `modules/api-design/snippets/api-design-graphql.md`
- Create: `modules/api-design/snippets/api-design-grpc.md`
- Create: `modules/api-design/templates/openapi.yaml`
- Create: `modules/api-design/templates/schema.graphql`
- Create: `modules/api-design/templates/service.proto`

- [ ] **Step 1: 创建 module.yml**

```yaml
name: api-design
version: 1.0.0
description: API 设计规范模块
type: general
depends: [core]

sections:
  - slot: api-design
    file: snippets/api-design-rest.md
    order: 0
    conditions:
      - when: api_style == graphql
        file: snippets/api-design-graphql.md
      - when: api_style == grpc
        file: snippets/api-design-grpc.md

variables:
  - name: api_style
    prompt: "API 风格"
    default: "rest"
    choices: ["rest", "graphql", "grpc"]

templates:
  - source: templates/openapi.yaml
    target: openapi.yaml
    conditions:
      - when: api_style == graphql
        source: templates/schema.graphql
      - when: api_style == grpc
        source: templates/service.proto
```

- [ ] **Step 2: 创建 snippets/api-design-rest.md**

```markdown
## API 设计

### RESTful 规范

- URL 使用名词复数：`/users`、`/orders`
- HTTP 方法语义：GET（查询）、POST（创建）、PUT（全量更新）、PATCH（部分更新）、DELETE（删除）
- 使用 HTTP 状态码：200（成功）、201（创建）、400（请求错误）、404（未找到）、500（服务器错误）
- 分页：`?page=1&page_size=20`
- 版本控制：URL 路径 `/api/v1/` 或 Header `Accept: application/vnd.api.v1+json`

### OpenAPI 规范

- 所有 API 必须有 OpenAPI 文档
- 请求/响应必须定义 Schema
- 示例值必须提供
```

- [ ] **Step 3: 创建 snippets/api-design-graphql.md**

```markdown
## API 设计

### GraphQL 规范

- Query 只做查询，Mutation 只做变更
- 使用 Input Type 区分创建和更新
- 分页使用 Relay Connection 规范
- 错误处理使用标准 error 格式
- Schema 按领域分模块

### Schema 设计原则

- 类型命名 PascalCase
- 字段命名 camelCase
- 枚举值命名 SCREAMING_SNAKE_CASE
```

- [ ] **Step 4: 创建 snippets/api-design-grpc.md**

```markdown
## API 设计

### gRPC 规范

- 使用 Protocol Buffers v3
- Service 命名 PascalCase
- RPC 方法命名 PascalCase
- Message 命名 PascalCase
- 字段命名 snake_case

### Proto 文件组织

- 每个 Service 一个 proto 文件
- 公共 Message 放在 common.proto
- 使用 package 避免命名冲突
```

- [ ] **Step 5: 创建模板文件**

`templates/openapi.yaml`:
```yaml
openapi: "3.0.3"
info:
  title: "{{PROJECT_NAME}} API"
  version: "1.0.0"
  description: "{{PROJECT_DESCRIPTION}}"
paths: {}
```

`templates/schema.graphql`:
```graphql
# {{PROJECT_NAME}} GraphQL Schema

type Query {
  _empty: String
}
```

`templates/service.proto`:
```protobuf
syntax = "proto3";

package {{PROJECT_NAME}};

service {{PROJECT_NAME}}Service {
}
```

- [ ] **Step 6: Commit**

```bash
git add modules/api-design/
git commit -m "feat: api-design module with REST/GraphQL/gRPC support"
```

---

### Task 13: Automation 模块

**Files:**
- Create: `modules/automation/module.yml`
- Create: `modules/automation/snippets/ci-github-actions.md`
- Create: `modules/automation/snippets/ci-gitlab-ci.md`
- Create: `modules/automation/config/settings.json.snippet`
- Create: `modules/automation/templates/ci.yml`
- Create: `modules/automation/templates/gitlab-ci.yml`

- [ ] **Step 1: 创建 module.yml**

```yaml
name: automation
version: 1.0.0
description: 自动化模块
type: general
depends: [core]

sections:
  - slot: automation
    file: snippets/ci-github-actions.md
    order: 0
    conditions:
      - when: ci_platform == gitlab-ci
        file: snippets/ci-gitlab-ci.md

variables:
  - name: ci_platform
    prompt: "CI 平台"
    default: "github-actions"
    choices: ["github-actions", "gitlab-ci"]

templates:
  - source: templates/ci.yml
    target: .github/workflows/ci.yml
    conditions:
      - when: ci_platform == gitlab-ci
        source: templates/gitlab-ci.yml
        target: .gitlab-ci.yml
```

- [ ] **Step 2: 创建 snippets 和模板**

`snippets/ci-github-actions.md`:
```markdown
## 自动化

### GitHub Actions 规范

- Workflow 文件放在 `.github/workflows/`
- 命名：`ci.yml`、`release.yml`
- 触发条件明确：push 分支、PR、tag
- Job 间依赖通过 `needs` 声明
- 使用缓存加速构建
```

`snippets/ci-gitlab-ci.md`:
```markdown
## 自动化

### GitLab CI 规范

- Pipeline 文件：`.gitlab-ci.yml`
- Stage 定义：build → test → deploy
- 使用 artifacts 传递构建产物
- 使用 cache 加速依赖安装
```

`config/settings.json.snippet`:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

`templates/ci.yml`:
```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install dependencies
        run: pip install -e ".[dev]"
      - name: Run tests
        run: pytest
```

`templates/gitlab-ci.yml`:
```yaml
stages:
  - test

test:
  stage: test
  image: python:3.12
  script:
    - pip install -e ".[dev]"
    - pytest
```

- [ ] **Step 3: Commit**

```bash
git add modules/automation/
git commit -m "feat: automation module with GitHub Actions and GitLab CI"
```

---

### Task 14: Security 模块

**Files:**
- Create: `modules/security/module.yml`
- Create: `modules/security/snippets/security.md`
- Create: `modules/security/hooks/gitleaks.yaml`
- Create: `modules/security/templates/env.example`

- [ ] **Step 1: 创建 module.yml**

```yaml
name: security
version: 1.0.0
description: 安全规范模块
type: general
depends: [core]

sections:
  - slot: security
    file: snippets/security.md
    order: 0

pre_commit_hooks:
  - file: hooks/gitleaks.yaml

gitignore_entries:
  - "*.key"
  - "*.pem"
  - ".env"

templates:
  - source: templates/env.example
    target: .env.example
```

- [ ] **Step 2: 创建 snippets/security.md**

```markdown
## 安全规范

### 编码准则

- 不硬编码密钥、密码、Token
- 输入校验：所有外部输入必须验证
- SQL 参数化：禁止字符串拼接 SQL
- 权限最小化：仅授予必要权限

### 依赖审计

- 定期运行依赖安全扫描
- 及时更新有漏洞的依赖
- 锁定依赖版本

### 敏感文件处理

- `.env` 文件不提交到版本控制
- 密钥文件（`.key`、`.pem`）不提交
- 使用 `.env.example` 记录所需环境变量
```

- [ ] **Step 3: 创建 hooks/gitleaks.yaml**

```yaml
repo: https://github.com/gitleaks/gitleaks
rev: v8.18.4
hooks:
  - id: gitleaks
```

- [ ] **Step 4: 创建 templates/env.example**

```
# 环境变量配置
# 复制此文件为 .env 并填入实际值

# DATABASE_URL=
# SECRET_KEY=
```

- [ ] **Step 5: Commit**

```bash
git add modules/security/
git commit -m "feat: security module with gitleaks hook and env template"
```

---

### Task 15: Lang-Python 模块

**Files:**
- Create: `modules/lang-python/module.yml`
- Create: `modules/lang-python/snippets/coding-standards.md`
- Create: `modules/lang-python/snippets/testing.md`
- Create: `modules/lang-python/snippets/testing.pytest.md`
- Create: `modules/lang-python/snippets/testing.unittest.md`
- Create: `modules/lang-python/config/settings.json.snippet`
- Create: `modules/lang-python/config/commands/pytest.md`
- Create: `modules/lang-python/hooks/ruff.yaml`
- Create: `modules/lang-python/hooks/black.yaml`
- Create: `modules/lang-python/templates/pyproject.toml`

- [ ] **Step 1: 创建 module.yml**

```yaml
name: lang-python
version: 1.0.0
description: Python 开发规范模块
type: language
depends: [core]

sections:
  - slot: coding-standards
    file: snippets/coding-standards.md
    order: 100
  - slot: testing
    file: snippets/testing.md
    order: 100
    conditions:
      - when: test_framework == pytest
        file: snippets/testing.pytest.md
      - when: test_framework == unittest
        file: snippets/testing.unittest.md

variables:
  - name: formatter
    prompt: "Python 格式化工具"
    default: "ruff"
    choices: ["ruff", "black"]
  - name: test_framework
    prompt: "测试框架"
    default: "pytest"
    choices: ["pytest", "unittest"]

templates:
  - source: templates/pyproject.toml
    target: pyproject.toml

pre_commit_hooks:
  - file: hooks/ruff.yaml
    conditions:
      - when: formatter == black
        file: hooks/black.yaml

gitignore_entries:
  - "__pycache__/"
  - "*.pyc"
  - ".pytest_cache/"
  - ".ruff_cache/"

commands:
  - name: pytest
    file: config/commands/pytest.md
```

- [ ] **Step 2: 创建 snippets/coding-standards.md**

```markdown
### Python 编码规范

#### 项目结构

使用 `src` layout：
```
src/
  my_package/
    __init__.py
    module.py
tests/
  test_module.py
```

#### 格式化

- 使用 {{formatter}} 进行代码格式化
- 行宽 88 字符（black 默认）/ 120 字符（ruff 默认）
- import 排序：标准库 → 第三方 → 本地

#### 类型注解

- 所有公共函数必须添加类型注解
- 使用 `from __future__ import annotations` 延迟求值

#### 命名规范

- 模块/包：snake_case
- 类：PascalCase
- 函数/方法/变量：snake_case
- 常量：UPPER_SNAKE_CASE

#### Docstring

- 公共 API 使用 Google 风格 docstring
- 单行 docstring 用于简单函数
```

- [ ] **Step 3: 创建 snippets/testing.md**

```markdown
### Python 测试规范

- 测试文件命名：`test_<module>.py`
- 测试类命名：`Test<Feature>`
- 测试函数命名：`test_<function>_<scenario>_<expected>`
```

- [ ] **Step 4: 创建 snippets/testing.pytest.md**

```markdown
### Python 测试规范

- 测试文件命名：`test_<module>.py`
- 测试类命名：`Test<Feature>`
- 测试函数命名：`test_<function>_<scenario>_<expected>`

#### pytest 配置

- 使用 `conftest.py` 管理 fixture
- fixture 命名：`<resource>_<scope>`（如 `db_session`）
- 使用 `@pytest.fixture(scope="module")` 控制生命周期
- Mock 使用 `pytest-mock` 的 `mocker` fixture

#### 常用命令

- 运行所有测试：`pytest`
- 运行单个文件：`pytest tests/test_foo.py`
- 运行匹配测试：`pytest -k "test_login"`
- 查看覆盖率：`pytest --cov=src`
```

- [ ] **Step 5: 创建 snippets/testing.unittest.md**

```markdown
### Python 测试规范

- 测试文件命名：`test_<module>.py`
- 测试类命名：`Test<Feature>`（继承 `unittest.TestCase`）
- 测试方法命名：`test_<function>_<scenario>_<expected>`

#### unittest 配置

- 使用 `unittest.TestCase` 作为基类
- `setUp` / `tearDown` 管理测试数据
- 使用 `unittest.mock` 进行 mock
- 运行命令：`python -m pytest` 或 `python -m unittest discover`
```

- [ ] **Step 6: 创建 config/settings.json.snippet**

```json
{
  "permissions": {
    "allow": [
      "Bash(pytest)",
      "Bash(ruff)",
      "Bash(python)"
    ]
  }
}
```

- [ ] **Step 7: 创建 config/commands/pytest.md**

```markdown
运行 pytest 测试。

步骤：
1. 运行 `pytest` 并捕获输出
2. 如果有失败，分析失败原因
3. 给出修复建议
```

- [ ] **Step 8: 创建 hooks/ruff.yaml**

```yaml
repo: https://github.com/astral-sh/ruff-pre-commit
rev: v0.4.8
hooks:
  - id: ruff
    args: [--fix]
  - id: ruff-format
```

- [ ] **Step 9: 创建 hooks/black.yaml**

```yaml
repo: https://github.com/psf/black-pre-commit-mirror
rev: 24.4.2
hooks:
  - id: black
```

- [ ] **Step 10: 创建 templates/pyproject.toml**

```toml
[project]
name = "{{PROJECT_NAME}}"
version = "0.1.0"
description = "{{PROJECT_DESCRIPTION}}"
requires-python = ">=3.10"

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "ruff>=0.4.0",
]

[tool.ruff]
line-length = 120
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 11: Commit**

```bash
git add modules/lang-python/
git commit -m "feat: lang-python module with pytest/ruff support"
```

---

### Task 16: Lang-CPP 模块

**Files:**
- Create: `modules/lang-cpp/module.yml` + snippets + config + hooks + templates

- [ ] **Step 1: 创建 module.yml**

```yaml
name: lang-cpp
version: 1.0.0
description: C++ 开发规范模块
type: language
depends: [core]

sections:
  - slot: coding-standards
    file: snippets/coding-standards.md
    order: 100
  - slot: testing
    file: snippets/testing.md
    order: 100

variables:
  - name: test_framework
    prompt: "测试框架"
    default: "gtest"
    choices: ["gtest", "catch2"]

templates:
  - source: templates/CMakeLists.txt
    target: CMakeLists.txt
  - source: templates/clang-format
    target: .clang-format
  - source: templates/clang-tidy
    target: .clang-tidy

pre_commit_hooks:
  - file: hooks/clang-format.yaml

gitignore_entries:
  - "build/"
  - "cmake-build-*/"
  - "*.o"
  - "*.a"

commands:
  - name: ctest
    file: config/commands/ctest.md
```

- [ ] **Step 2: 创建 snippets/coding-standards.md**

```markdown
### C++ 编码规范

#### CMake 约定

- 使用 `CMakePresets.json` 管理构建配置
- 目标命名：`<project>_<library>`
- 使用 `FetchContent` 管理第三方依赖

#### 命名规范

- 类/结构体：PascalCase
- 函数/方法：snake_case
- 变量：snake_case
- 常量：kUpperCamelCase
- 宏：UPPER_SNAKE_CASE

#### 头文件

- 使用 `#pragma once` 作为 include guard
- 头文件自包含
- 前向声明优先于 `#include`

#### RAII 原则

- 资源获取即初始化
- 智能指针优先：`unique_ptr` > `shared_ptr`
- 禁止裸 `new`/`delete`

#### const 正确性

- 能用 `const` 就用 `const`
- 参数传递：基本类型按值，其他按 const 引用
- 成员函数：不修改状态则标记 `const`
```

- [ ] **Step 3: 创建 snippets/testing.md**

```markdown
### C++ 测试规范

- 测试目录：`tests/`
- 测试文件命名：`test_<module>.cpp`
- 测试函数命名：`Test<Feature>_<Scenario>_<Expected>`

#### Google Test / Catch2

- 使用 TEST 宏定义测试用例
- 使用 EXPECT 断言（非致命）优先于 ASSERT（致命）
- 使用 fixture 共享测试数据
```

- [ ] **Step 4: 创建 config/settings.json.snippet**

```json
{
  "permissions": {
    "allow": [
      "Bash(cmake)",
      "Bash(ctest)",
      "Bash(make)"
    ]
  }
}
```

- [ ] **Step 5: 创建 config/commands/ctest.md**

```markdown
运行 ctest 测试。

步骤：
1. 确认构建目录存在
2. 运行 `ctest --output-on-failure`
3. 如果有失败，分析失败原因
```

- [ ] **Step 6: 创建 hooks/clang-format.yaml**

```yaml
repo: https://github.com/pre-commit/mirrors-clang-format
rev: v18.1.8
hooks:
  - id: clang-format
```

- [ ] **Step 7: 创建模板文件**

`templates/CMakeLists.txt`:
```cmake
cmake_minimum_required(VERSION 3.20)
project({{PROJECT_NAME}} VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_subdirectory(src)

enable_testing()
add_subdirectory(tests)
```

`templates/clang-format`:
```yaml
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 120
```

`templates/clang-tidy`:
```yaml
Checks: >
  -*,
  bugprone-*,
  modernize-*,
  performance-*,
  readability-*
```

- [ ] **Step 8: Commit**

```bash
git add modules/lang-cpp/
git commit -m "feat: lang-cpp module with CMake and clang-format support"
```

---

### Task 17: Lang-Shell 模块

**Files:**
- Create: `modules/lang-shell/module.yml` + snippets + config + hooks + templates

- [ ] **Step 1: 创建 module.yml**

```yaml
name: lang-shell
version: 1.0.0
description: Shell 开发规范模块
type: language
depends: [core]

sections:
  - slot: coding-standards
    file: snippets/coding-standards.md
    order: 100
  - slot: testing
    file: snippets/testing.md
    order: 100

pre_commit_hooks:
  - file: hooks/shellcheck.yaml

commands:
  - name: bats
    file: config/commands/bats.md

templates:
  - source: templates/script-template.sh
    target: scripts/main.sh
```

- [ ] **Step 2: 创建 snippets/coding-standards.md**

```markdown
### Shell 编码规范

#### POSIX 兼容性

- Shebang：`#!/usr/bin/env bash`
- 错误处理：`set -euo pipefail`
- 变量引用：始终使用双引号 `"$var"`

#### 最佳实践

- 使用 `printf` 代替 `echo`
- 函数命名：snake_case
- 使用 `local` 声明局部变量
- 使用 `[[ ]]` 代替 `[ ]`
- 使用 `$()` 代替反引号
```

- [ ] **Step 3: 创建 snippets/testing.md**

```markdown
### Shell 测试规范

- 使用 ShellCheck 进行静态分析
- 使用 bats-core 编写测试
- 测试文件命名：`*.bats`
```

- [ ] **Step 4: 创建 config/settings.json.snippet**

```json
{
  "permissions": {
    "allow": [
      "Bash(shellcheck)",
      "Bash(bats)"
    ]
  }
}
```

- [ ] **Step 5: 创建 config/commands/bats.md**

```markdown
运行 bats 测试。

步骤：
1. 查找所有 .bats 测试文件
2. 运行 `bats tests/`
3. 如果有失败，分析失败原因
```

- [ ] **Step 6: 创建 hooks/shellcheck.yaml**

```yaml
repo: https://github.com/shellcheck-py/shellcheck-py
rev: v0.10.0.1
hooks:
  - id: shellcheck
```

- [ ] **Step 7: 创建 templates/script-template.sh**

```bash
#!/usr/bin/env bash
set -euo pipefail

# {{PROJECT_NAME}} - {{PROJECT_DESCRIPTION}}

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log() {
    local level="$1"; shift
    printf "[%s] %s\n" "$level" "$*" >&2
}

main() {
    log "INFO" "Starting {{PROJECT_NAME}}"
    # TODO: implement
}

main "$@"
```

- [ ] **Step 8: Commit**

```bash
git add modules/lang-shell/
git commit -m "feat: lang-shell module with shellcheck and bats support"
```

---

### Task 18: 预设文件

**Files:**
- Create: `presets/preset-minimal.yml`
- Create: `presets/preset-python.yml`
- Create: `presets/preset-cpp.yml`
- Create: `presets/preset-shell.yml`

- [ ] **Step 1: 创建所有预设文件**

`presets/preset-minimal.yml`:
```yaml
name: preset-minimal
description: 最小配置（仅 core）
modules:
  - core
```

`presets/preset-python.yml`:
```yaml
name: preset-python
description: Python 项目完整配置
modules:
  - core
  - git-convention
  - testing
  - code-review
  - security
  - lang-python
```

`presets/preset-cpp.yml`:
```yaml
name: preset-cpp
description: C++ 项目完整配置
modules:
  - core
  - git-convention
  - testing
  - code-review
  - security
  - lang-cpp
```

`presets/preset-shell.yml`:
```yaml
name: preset-shell
description: Shell 项目完整配置
modules:
  - core
  - git-convention
  - testing
  - code-review
  - security
  - lang-shell
```

- [ ] **Step 2: 运行集成测试**

Run: `python -m pytest tests/test_init.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add presets/
git commit -m "feat: preset files for minimal, python, cpp, shell"
```

---

### Task 19: 端到端测试

**Files:**
- Modify: `tests/test_init.py`

- [ ] **Step 1: 补充端到端测试**

在 `tests/test_init.py` 中追加：

```python
class TestEndToEnd:
    def test_preset_python_generates_all_files(self, tmp_path):
        """preset-python 生成所有预期文件"""
        from conftest import MODULES_DIR, PRESETS_DIR
        if not MODULES_DIR.exists():
            pytest.skip("modules directory not yet created")

        target = tmp_path / "my-api"
        run_init(
            target_dir=target,
            modules_dir=MODULES_DIR,
            presets_dir=PRESETS_DIR,
            preset="preset-python",
            non_interactive=True,
            cli_vars={
                "PROJECT_NAME": "my-api",
                "PROJECT_DESCRIPTION": "My API project",
                "TECH_STACK": "Python",
            },
        )

        # CLAUDE.md
        assert (target / "CLAUDE.md").exists()
        content = (target / "CLAUDE.md").read_text()
        assert "my-api" in content
        assert "Python 编码规范" in content
        assert "Git 规范" in content

        # settings.json
        assert (target / ".claude" / "settings.json").exists()
        settings = json.loads((target / ".claude" / "settings.json").read_text())
        assert "Bash(pytest)" in settings["permissions"]["allow"]

        # .pre-commit-config.yaml
        assert (target / ".pre-commit-config.yaml").exists()

        # .gitignore
        assert (target / ".gitignore").exists()
        gitignore = (target / ".gitignore").read_text()
        assert "__pycache__/" in gitignore

        # commands
        assert (target / ".claude" / "commands" / "commit.md").exists()
        assert (target / ".claude" / "commands" / "pytest.md").exists()

        # templates
        assert (target / "pyproject.toml").exists()

    def test_multi_language_coexist_e2e(self, tmp_path):
        """多语言模块可同时选中"""
        from conftest import MODULES_DIR, PRESETS_DIR
        if not MODULES_DIR.exists():
            pytest.skip("modules directory not yet created")

        target = tmp_path / "my-project"
        run_init(
            target_dir=target,
            modules_dir=MODULES_DIR,
            presets_dir=PRESETS_DIR,
            modules=["lang-python", "lang-cpp"],
            non_interactive=True,
            cli_vars={"PROJECT_NAME": "test", "PROJECT_DESCRIPTION": "test", "TECH_STACK": "test"},
        )
        # 应成功生成，两个语言的文件都存在
        assert (target / "pyproject.toml").exists()
        assert (target / "CMakeLists.txt").exists()
```

- [ ] **Step 2: 运行全部测试**

Run: `python -m pytest tests/ -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/test_init.py
git commit -m "test: end-to-end tests for preset-python and multi-language coexist"
```

---

### Task 20: README

**Files:**
- Create: `README.md`

- [ ] **Step 1: 创建 README.md**

```markdown
# CC Project Template

Claude Code 项目开发工程模板，通过模块化配置解决重复配置和质量不稳定两大痛点。

## 快速开始

```bash
# Python 项目
python scripts/init.py /path/to/new-project --preset preset-python

# C++ 项目
python scripts/init.py /path/to/new-project --preset preset-cpp

# Shell 项目
python scripts/init.py /path/to/new-project --preset preset-shell

# 最小配置
python scripts/init.py /path/to/new-project --preset preset-minimal
```

## 模块

| 模块 | 类型 | 说明 |
|------|------|------|
| core | core（必选） | 行为准则、通用编码规范 |
| git-convention | general | Conventional Commits、pre-commit |
| testing | general | 测试策略和命名规范 |
| code-review | general | Review checklist、PR 模板 |
| api-design | general | REST/GraphQL/gRPC 规范 |
| automation | general | CI/CD 配置、MCP 服务器 |
| security | general | 安全编码准则、密钥检测 |
| lang-python | language | Python 编码规范、pytest |
| lang-cpp | language | C++ 编码规范、CMake |
| lang-shell | language | Shell 编码规范、ShellCheck |

## 使用方式

```bash
# 交互式
python scripts/init.py /path/to/project

# 使用预设
python scripts/init.py /path/to/project --preset preset-python

# 指定模块
python scripts/init.py /path/to/project --module core,testing,lang-python

# 追加模块到已有项目
python scripts/init.py --module security /path/to/existing-project

# 预览（不写入）
python scripts/init.py --diff --preset preset-python /path/to/project

# 非交互（CI）
python scripts/init.py --preset preset-python --non-interactive \
  --var PROJECT_NAME=my-api --var PROJECT_DESCRIPTION="My API" \
  /path/to/project
```

## 开发

```bash
pip install -e ".[dev]"
pytest
```
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README with quick start and usage"
```

---

## 自审检查

- [x] **Spec coverage**: 设计文档中的 10 个模块、4 个预设、init.py 所有功能均有对应 Task
- [x] **Placeholder scan**: 无 TBD/TODO/placeholder
- [x] **Type consistency**: Module/ModuleLoader/DependencyResolver/VariableCollector/Merger/Generator 接口一致
