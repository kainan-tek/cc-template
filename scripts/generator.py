# scripts/generator.py
"""生成器：将合并结果写入目标目录"""
from __future__ import annotations

import json
import re
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
        self._newly_created_files: list[Path] = []  # 追踪本次新建的文件，用于回滚
        self._overwritten_file: Path | None = None  # 追踪被覆盖的文件

        try:
            self._write_claude_md(target_dir, strategy, dry_run)
            self._write_settings(target_dir, dry_run)
            self._write_pre_commit(target_dir, dry_run)
            self._write_gitignore(target_dir, dry_run)
            self._write_commands(target_dir, dry_run)
            self._write_templates(target_dir, dry_run)
        except Exception:
            if not dry_run:
                self._rollback(target_dir)
            raise

        return self.written_files

    def _rollback(self, target_dir: Path) -> None:
        """回滚：删除本次新建的文件，恢复被覆盖的文件"""
        for f in self._newly_created_files:
            if f.exists():
                f.unlink()
        # 恢复被覆盖的 CLAUDE.md
        bak = target_dir / "CLAUDE.md.bak"
        if bak.exists() and self._overwritten_file:
            shutil.move(str(bak), str(self._overwritten_file))

    def _write_claude_md(self, target_dir: Path, strategy: str, dry_run: bool) -> None:
        new_content = self.merger.merge_claude_md()
        shared = target_dir / "CLAUDE.md"

        # 自动判断写入目标：共享文件不存在时写共享文件，存在时写 local 文件
        if not shared.exists():
            target = shared
        else:
            target = target_dir / "CLAUDE.local.md"

        if target.exists():
            if strategy == "overwrite":
                if not dry_run:
                    shutil.copy2(target, target_dir / f"{target.name}.bak")
                    target.write_text(new_content, encoding="utf-8")
                    self._overwritten_file = target
                self.written_files.append(target)
            else:  # append
                existing = target.read_text(encoding="utf-8")
                self._warn_duplicate_headings(existing, new_content)
                if not dry_run:
                    target.write_text(existing + "\n\n" + new_content, encoding="utf-8")
                self.written_files.append(target)
        else:
            if not dry_run:
                target.write_text(new_content, encoding="utf-8")
                self._newly_created_files.append(target)
            self.written_files.append(target)

    def _write_settings(self, target_dir: Path, dry_run: bool) -> None:
        settings_dir = target_dir / ".claude"
        shared = settings_dir / "settings.json"

        # 自动判断写入目标：共享文件不存在时写共享文件，存在时写 local 文件
        if not shared.exists():
            target = shared
        else:
            target = settings_dir / "settings.local.json"

        if target.exists():
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
        # 非 git 仓库时发出警告但仍生成 .pre-commit-config.yaml
        import subprocess
        try:
            subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=str(target_dir),
                capture_output=True,
                check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("  Warning: target is not in a git repository, pre-commit hooks require git")

        target = target_dir / ".pre-commit-config.yaml"

        existing_content = None
        if target.exists():
            existing_content = target.read_text(encoding="utf-8")

        result = self.merger.merge_pre_commit(existing_content)
        if not result:
            return

        if not dry_run:
            target.write_text(result, encoding="utf-8")
            self._ensure_pre_commit_installed(target_dir)
        self.written_files.append(target)

    @staticmethod
    def _ensure_pre_commit_installed(target_dir: Path) -> None:
        """检查并安装 pre-commit hooks"""
        import shutil
        import subprocess

        if not shutil.which("pre-commit"):
            print("  Warning: pre-commit is not installed")
            print("  Install it with:  pip install pre-commit")
            print("  Then run:         cd <project> && pre-commit install")
            return

        try:
            subprocess.run(
                ["pre-commit", "install"],
                cwd=str(target_dir),
                capture_output=True,
                check=True,
            )
            print("  pre-commit hooks installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"  Warning: pre-commit install failed: {e.stderr.decode(errors='replace').strip()}")
        except FileNotFoundError:
            print("  Warning: pre-commit command not found")

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

                # target 也需要通过条件解析
                target_rel = self.merger._resolve_condition(tpl_def, "target")
                target_path = target_dir / target_rel
                if target_path.exists():
                    existing = target_path.read_bytes()
                    new = full_source.read_bytes()
                    if existing == new:
                        print(f"  Skip: {target_path} already exists with identical content (deduped)")
                    else:
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
        existing_headings = set(re.findall(r"^## .+$", existing, re.MULTILINE))
        new_headings = re.findall(r"^## .+$", new_content, re.MULTILINE)
        for h in new_headings:
            if h in existing_headings:
                print(f"  Warning: duplicate heading in CLAUDE.md: {h}")
