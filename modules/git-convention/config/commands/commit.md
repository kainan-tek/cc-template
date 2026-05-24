分析当前 `git diff --cached` 的内容，生成符合 Conventional Commits 规范的 commit message。

规则：
- 格式：`<type>(<scope>): <description>`
- type 从 feat/fix/docs/refactor/test/chore 中选择
- description 简洁明确，不超过 72 字符
- 语言：{{commit_lang}}
