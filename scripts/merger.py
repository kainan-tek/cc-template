# scripts/merger.py
"""合并器：将多模块内容合并为最终产出"""
from __future__ import annotations

import copy
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

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

    # ── 变量替换 ──────────────────────────────────────────────

    def _replace_variables(self, content: str) -> str:
        """将 {{VAR}} 替换为变量值，未定义变量保留原样并输出警告"""
        def _replacer(match: re.Match) -> str:
            var_name = match.group(1)
            if var_name in self.variables:
                return self.variables[var_name]
            print(f"  Warning: undefined variable {{{{{var_name}}}}}")
            return match.group(0)

        return re.sub(r"\{\{(\w+)\}\}", _replacer, content)

    # ── 条件解析 ──────────────────────────────────────────────

    def _resolve_condition(self, definition: dict[str, Any], key: str) -> str:
        """解析条件定义，返回匹配条件的值或默认值"""
        conditions = definition.get("conditions", [])
        for cond in conditions:
            when_expr = cond.get("when", "")
            if self._evaluate_when(when_expr):
                return cond[key]
        return definition[key]

    def _evaluate_when(self, when_expr: str) -> bool:
        """求值 when 表达式（仅支持 变量名 == 值）"""
        match = re.match(r"(\w+)\s*==\s*(.+)", when_expr.strip())
        if not match:
            return False
        var_name, expected = match.group(1), match.group(2).strip()
        # 去除值两端的引号，兼容 "graphql" 和 'graphql' 写法
        if (expected.startswith('"') and expected.endswith('"')) or \
           (expected.startswith("'") and expected.endswith("'")):
            expected = expected[1:-1]
        if var_name not in self.variables:
            print(f"  Warning: condition references undefined variable '{var_name}'")
            return False
        return self.variables[var_name] == expected

    # ── CLAUDE.md 合并 ───────────────────────────────────────

    def merge_claude_md(self) -> str:
        """合并所有模块的 snippet，按章节组织，返回完整 CLAUDE.md 内容"""
        # 收集所有章节内容
        sections: dict[str, list[tuple[int, str, str, str]]] = defaultdict(list)
        # (order, module_name, module_version, snippet_content)

        for mod_name in self.load_order:
            mod = self.modules[mod_name]
            for sec_def in mod.sections:
                slot = sec_def["slot"]
                order = sec_def.get("order", 50)

                # 解析条件 snippet
                file_rel = self._resolve_condition(sec_def, "file")
                snippet_path = mod.path / file_rel

                if not snippet_path.exists():
                    continue

                content = snippet_path.read_text(encoding="utf-8")
                content = self._replace_variables(content)

                # 添加更新标记（仅开始标记，下一个标记或 EOF 为天然边界）
                marked = (
                    f"<!-- module:{mod.name}:{mod.version}:{slot} -->\n"
                    f"{content}"
                )
                sections[slot].append((order, mod.name, mod.version, marked))

        # 按预定义顺序 + 自定义章节排序
        ordered_slots: list[str] = []
        for slot in SECTION_ORDER:
            if slot in sections:
                ordered_slots.append(slot)
        # 自定义章节追加到末尾
        for slot in sorted(sections.keys()):
            if slot not in SECTION_ORDER:
                ordered_slots.append(slot)

        # 组装最终内容
        parts: list[str] = []
        for slot in ordered_slots:
            entries = sorted(sections[slot], key=lambda x: (x[0], x[1]))
            for _order, _mod_name, _mod_ver, marked in entries:
                parts.append(marked)

        return "\n\n".join(parts)

    # ── settings.json 合并 ───────────────────────────────────

    def merge_settings(self) -> dict[str, Any]:
        """深度合并所有模块的 settings.json.snippet"""
        result: dict[str, Any] = {}

        for mod_name in self.load_order:
            mod = self.modules[mod_name]
            snippet_path = mod.settings_snippet_path
            if snippet_path is None:
                continue

            content = snippet_path.read_text(encoding="utf-8")
            content = self._replace_variables(content)

            try:
                snippet = json.loads(content)
            except json.JSONDecodeError:
                print(f"  Warning: invalid JSON in {snippet_path}")
                continue

            result = self._deep_merge(result, snippet)

        return result

    @staticmethod
    def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
        """深度合并两个字典"""
        result = copy.deepcopy(base)
        for key, value in override.items():
            if key in result:
                if isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = Merger._deep_merge(result[key], value)
                elif isinstance(result[key], list) and isinstance(value, list):
                    # 数组拼接后按 JSON 序列化值去重
                    merged_list = result[key] + value
                    seen: list[str] = []
                    deduped: list[Any] = []
                    for item in merged_list:
                        serialized = json.dumps(item, sort_keys=True, ensure_ascii=False)
                        if serialized not in seen:
                            seen.append(serialized)
                            deduped.append(item)
                    result[key] = deduped
                else:
                    # 标量：后加载模块覆盖先加载
                    result[key] = value
            else:
                result[key] = copy.deepcopy(value)
        return result

    # ── .pre-commit-config.yaml 合并 ─────────────────────────

    def merge_pre_commit(self, existing_content: str | None = None) -> str | None:
        """合并 pre-commit 配置"""
        import yaml

        # 收集所有模块的 pre_commit_hooks
        hook_snippets: list[str] = []
        for mod_name in self.load_order:
            mod = self.modules[mod_name]
            for hook_def in mod.pre_commit_hooks:
                file_rel = self._resolve_condition(hook_def, "file")
                hook_path = mod.path / file_rel
                if not hook_path.exists():
                    continue
                content = hook_path.read_text(encoding="utf-8")
                content = self._replace_variables(content)
                hook_snippets.append(content)

        if not hook_snippets and not existing_content:
            return None

        # 解析已有内容
        existing_repos: list[Any] = []
        if existing_content:
            try:
                existing_data = yaml.safe_load(existing_content)
                if existing_data and "repos" in existing_data:
                    existing_repos = existing_data["repos"]
            except yaml.YAMLError:
                pass

        # 解析新 hook 片段
        new_repos: list[Any] = []
        for snippet in hook_snippets:
            try:
                data = yaml.safe_load(snippet)
                if data and "repos" in data:
                    new_repos.extend(data["repos"])
                elif data:
                    new_repos.append(data)
            except yaml.YAMLError:
                continue

        # 按 repo URL 去重
        existing_urls = set()
        for repo in existing_repos:
            url = repo.get("repo", "")
            if url:
                existing_urls.add(url)

        for repo in new_repos:
            url = repo.get("repo", "")
            if url and url not in existing_urls:
                existing_repos.append(repo)
                existing_urls.add(url)

        result_data = {"repos": existing_repos}
        return yaml.dump(result_data, default_flow_style=False, allow_unicode=True)

    # ── .gitignore 合并 ──────────────────────────────────────

    def merge_gitignore(self, existing_content: str | None = None) -> str:
        """合并 .gitignore 条目，行级去重"""
        # 收集已有行
        existing_lines: list[str] = []
        if existing_content:
            existing_lines = existing_content.splitlines()

        # 收集所有模块的 gitignore 条目
        new_entries: list[str] = []
        for mod_name in self.load_order:
            mod = self.modules[mod_name]
            new_entries.extend(mod.gitignore_entries)

        # 去重：保留已有行，追加不重复的新条目
        seen: set[str] = set()
        result_lines: list[str] = []

        for line in existing_lines:
            stripped = line.strip()
            if stripped:
                seen.add(stripped)
            result_lines.append(line)

        for entry in new_entries:
            stripped = entry.strip()
            if not stripped:
                # 空行：直接追加（用于分组间隔）
                result_lines.append("")
                continue
            if stripped not in seen:
                seen.add(stripped)
                result_lines.append(entry)

        return "\n".join(result_lines) + "\n" if result_lines else ""
