#!/usr/bin/env python3
# scripts/init.py
"""CC Project Template 初始化脚本"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

from dependency_resolver import DependencyResolver
from generator import Generator
from module_loader import ModuleLoader
from variable_collector import VariableCollector


def _detect_installed_modules(target_dir: Path) -> set[str]:
    """从已有 CLAUDE.md / CLAUDE.local.md 中解析 <!-- module:<name>:<version>:<slot> --> 标记，返回已安装模块名集合"""
    installed: set[str] = set()
    pattern = r"<!-- module:(\w[\w-]*):\d+\.\d+\.\d+:\S+ -->"
    for filename in ("CLAUDE.md", "CLAUDE.local.md"):
        claude_md = target_dir / filename
        if claude_md.exists():
            content = claude_md.read_text(encoding="utf-8")
            installed.update(re.findall(pattern, content))
    return installed


def _validate(
    all_modules: dict,
    load_order: list[str],
    variables: dict[str, str],
    gen: Generator,
) -> None:
    """验证生成结果：CLAUDE.md 无空章节、settings.json 合法、依赖满足"""
    import json

    # 1. 检查 CLAUDE.md 无空章节
    claude_md_content = gen.merger.merge_claude_md()
    module_pattern = r"<!-- module:(\w[\w-]*):(\d+\.\d+\.\d+):(\S+) -->"
    # 找到所有标记，检查标记后是否有内容（到下一个标记行或 EOF）
    open_marks = list(re.finditer(module_pattern, claude_md_content))
    for i, match in enumerate(open_marks):
        mod_name, mod_ver, slot = match.group(1), match.group(2), match.group(3)
        open_end = match.end()
        # 取当前标记到下一个标记行之间的内容
        if i + 1 < len(open_marks):
            next_mark_start = open_marks[i + 1].start()
        else:
            next_mark_start = len(claude_md_content)
        between = claude_md_content[open_end:next_mark_start]
        # 去掉其他标记行（相邻不同 slot 的标记）后检查是否有实质内容
        between_clean = re.sub(r'<!-- module:\S+ -->', '', between).strip()
        if not between_clean:
            raise ValueError(
                f"Empty section in CLAUDE.md: module '{mod_name}' slot '{slot}' has no content"
            )

    # 2. 检查 settings.json 合法
    settings = gen.merger.merge_settings()
    if settings:
        try:
            json.dumps(settings)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Generated settings.json is invalid: {e}")

    # 3. 检查依赖满足
    for name in load_order:
        mod = all_modules[name]
        for dep in mod.depends:
            if dep not in load_order:
                raise ValueError(f"Dependency not satisfied: module '{name}' requires '{dep}'")

    # 4. 检查变量未替换（残留 {{VAR}}）
    remaining_vars: set[str] = set()
    # 4.1 检查 CLAUDE.md
    remaining_vars.update(re.findall(r"\{\{(\w+)\}\}", claude_md_content))
    # 4.2 检查 settings.json
    if settings:
        settings_str = json.dumps(settings, ensure_ascii=False)
        remaining_vars.update(re.findall(r"\{\{(\w+)\}\}", settings_str))
    # 4.3 检查 templates
    for name in load_order:
        mod = all_modules[name]
        for tpl_def in mod.templates:
            source_path = gen.merger._resolve_condition(tpl_def, "source")
            full_source = mod.path / source_path
            if full_source.exists():
                tpl_content = full_source.read_text(encoding="utf-8")
                tpl_content = gen.merger._replace_variables(tpl_content)
                remaining_vars.update(re.findall(r"\{\{(\w+)\}\}", tpl_content))
    if remaining_vars:
        print(f"  Warning: unreplaced variables: {', '.join(sorted(remaining_vars))}")


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

    # 3. 依赖解析 + 冲突检测
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

    # 5. 检测已安装模块，过滤掉已安装的贡献
    installed_modules = _detect_installed_modules(target_dir)
    original_load_order = list(load_order)
    if installed_modules:
        new_modules = [n for n in load_order if n not in installed_modules]
        if new_modules != load_order:
            skipped = [n for n in load_order if n in installed_modules]
            print(f"  Skipping already installed modules: {', '.join(skipped)}")
            load_order = new_modules

    if not load_order:
        print("All modules already installed. Nothing to do.")
        return []

    # 6. 在内存中生成文件
    gen = Generator(all_modules, load_order, variables)

    if diff_only:
        files = gen.generate(target_dir, strategy=strategy, dry_run=True)
        print("\nFiles to be generated:")
        for f in files:
            print(f"  {f}")
        return files

    # 7. 验证（使用原始 load_order 检查依赖，因为已安装模块的贡献已存在）
    _validate(all_modules, original_load_order, variables, gen)

    # 8. 检查写入目标是否已存在，确定接入策略
    # 自动判断：共享文件不存在时写共享文件，存在时写 local 文件
    if not non_interactive:
        claude_md = target_dir / "CLAUDE.md"
        if claude_md.exists():
            # 共享文件存在，写入目标是 CLAUDE.local.md
            target_file = target_dir / "CLAUDE.local.md"
            if target_file.exists():
                answer = input(f"\n{target_file} already exists. Strategy (append/overwrite)? [append] ").strip()
                if answer == "overwrite":
                    strategy = "overwrite"

    # 9. 用户确认（交互模式下）
    if not non_interactive:
        answer = input("\nProceed? [Y/n] ").strip().lower()
        if answer and answer not in ("y", "yes"):
            print("Aborted.")
            return []

    # 10. 写入磁盘
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
