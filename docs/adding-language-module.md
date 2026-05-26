# 添加新语言模块指南

本文档说明如何为 CC Template 添加新的语言模块。

## 1. 目录结构

```
modules/lang-<lang>/
├── module.yml                    # 模块配置
├── snippets/
│   ├── coding-standards.md       # 编码规范（三级标题）
│   ├── testing.md                # 测试规范（默认/fallback）
│   └── testing.<framework>.md    # 测试规范（可选多个框架）
├── config/
│   ├── settings.json.snippet     # Claude Code 权限（JSON 格式）
│   └── commands/
│       └── <cmd>.md              # slash command 文件
├── hooks/                        # pre-commit hooks（可选）
│   └── <linter>.yaml
└── templates/                    # 项目模板文件
    └── <config-file>
```

## 2. module.yml 模板

```yaml
name: lang-<lang>
version: 1.0.0
description: <Language> 开发规范模块
type: language
depends: [core]

sections:
  - slot: coding-standards
    file: snippets/coding-standards.md
    order: 100
  - slot: testing
    file: snippets/testing.md        # 默认文件（conditions 无匹配时使用）
    order: 100
    conditions:                      # 可选：多测试框架
      - when: test_framework == <fw1>
        file: snippets/testing.<fw1>.md
      - when: test_framework == <fw2>
        file: snippets/testing.<fw2>.md

variables:                           # 可选：用户选择
  - name: test_framework
    prompt: "测试框架"
    default: "<fw1>"
    choices: ["<fw1>", "<fw2>"]

templates:
  - source: templates/<config>
    target: <config>

settings:
  file: config/settings.json.snippet

pre_commit_hooks:                    # 可选：pre-commit 配置
  - file: hooks/<linter>.yaml

gitignore_entries:
  - "<lang-specific-patterns>"

commands:
  - name: <cmd>                      # slash command 名称
    file: config/commands/<cmd>.md
```

## 3. Snippet 写法规范

### 编码规范

三级标题，附加到通用编码规范后：

```markdown
### <Language> 编码规范

- 项目结构：<约定>
- 命名规范：<约定>
- 格式化工具：<工具>
- <其他关键约定>
```

### 测试规范

三级标题，附加到通用测试规范后：

```markdown
### <Language> 测试规范

- 测试目录：`<约定>`
- 测试文件命名：`<约定>`
- 测试函数命名：`<约定>`
- <框架特定约定>
```

## 4. settings.json.snippet 格式

```json
{
  "permissions": {
    "allow": [
      "Bash(<test-cmd>)",
      "Bash(<linter>)",
      "Bash(<build-cmd>)"
    ]
  }
}
```

## 5. commands 文件格式

```markdown
<description>

步骤：
1. <step 1>
2. <step 2>
```

## 6. 预设文件格式

```yaml
# presets/preset-<lang>.yml
name: preset-<lang>
description: <Language> 项目完整配置
modules:
  - core
  - git-convention
  - testing
  - code-review
  - security
  - lang-<lang>
```

## 7. 添加步骤

1. **创建目录**：`modules/lang-<lang>/`
2. **编写 module.yml**：参考上面模板
3. **编写 snippets**：编码规范 + 测试规范（默认 + 条件版本）
4. **添加 settings.json.snippet**：允许的 Bash 命令
5. **添加 commands**：slash command 文件（可选）
6. **添加 hooks**：pre-commit 配置（可选）
7. **添加模板文件**：如 `Cargo.toml`、`go.mod` 等
8. **添加预设**（可选）：`presets/preset-<lang>.yml`
9. **编写测试**：验证生成结果

## 8. 注意事项

| 事项 | 说明 |
|------|------|
| **order 固定为 100** | 确保语言规范在通用规范之后 |
| **三级标题** | 语言规范使用 `###`，附加到主章节 |
| **默认 testing.md 必须存在** | 即使使用 conditions，也需要默认文件 |
| **避免重复** | 不要重复通用规范已有的内容 |
| **精简** | 只写 AI 易忽略或语言特定的约定 |

## 9. 常见语言模块示例

| 语言 | 关键文件 | 变量建议 |
|------|----------|----------|
| **Rust** | `Cargo.toml`, `.rustfmt.toml` | `edition: 2021/2024` |
| **Go** | `go.mod`, `.golangci.yml` | `go_version: 1.21/1.22` |
| **Java** | `pom.xml/build.gradle` | `build_tool: maven/gradle` |
| **Kotlin** | `build.gradle.kts` | `jdk_version: 17/21` |
| **TypeScript** | `tsconfig.json` | `runtime: node/bun` |
