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

    if args.module:
        args.modules = [m.strip() for m in args.module.split(",")]
    else:
        args.modules = None

    args.cli_vars = {}
    if args.var:
        for v in args.var:
            key, _, value = v.partition("=")
            args.cli_vars[key.strip()] = value.strip()

    return args


def main() -> None:
    args = parse_args()

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
