# Claude Code 项目工程模板生成工具

## 背景

使用 Claude Code 进行项目开发时，存在两大痛点：

1. **重复配置繁琐**：每次新项目都要重新编写 CLAUDE.md、hooks、settings 等配置
2. **输出质量不稳定**：缺少规范约束，Claude Code 生成的代码质量参差不齐

本模板旨在系统性解决这两个问题。

## 设计原则

- **够用就好**：只解决 80% 的高频场景，不为 20% 的边缘情况增加复杂度
- **显式优于隐式**：模块间关系通过声明式配置明确表达，不依赖隐式推断
- **可扩展但不过早抽象**：结构上预留扩展点，但不为尚未出现的需求实现通用机制

## 与原方案的差异

| 机制 | 原方案 | 当前方案 | 理由 |
|------|--------|------------|------|
| init 脚本 | Shell | Python | YAML/JSON 处理、交互输入、依赖排序是 Python 强项 |
| 增量更新 | 锁文件 + 更新标记 + --update | 不支持 | 使用频率低，实现复杂度高，推迟到后续版本 |
| 已有项目接入 | 追加/合并/覆盖三种 | 追加/覆盖两种 | 标题匹配合并逻辑复杂且脆弱 |
| contributions | 通用插入点标记机制 | 按文件类型专用字段 | 各合并逻辑差异大（聚合、深度合并、YAML追加、行级去重），通用机制反增复杂度，按文件类型专用字段更清晰 |
| 条件 snippet | when 语法 | 保留 when 语法 | 可读性好，实现简单 |
| 变量跨模块合并 | 同名变量去重 + 优先级覆盖 | 语言模块可共存，需合并 | 多语言项目常见（如 C++ + Python 绑定） |
| 模块类型判断 | 隐式（lang- 前缀推断） | 显式 type 字段 | 消除歧义 |
| 预设格式 | 目录（未定义格式） | YAML 文件 | 明确规范 |

## 架构：模块化模板仓库

### 目录结构

```
cc-template/
├── modules/
│   ├── core/
│   ├── git-convention/
│   ├── testing/
│   ├── code-review/
│   ├── api-design/
│   ├── automation/
│   ├── security/
│   ├── lang-python/
│   ├── lang-cpp/
│   └── lang-shell/
├── presets/
│   ├── preset-minimal.yml
│   ├── preset-python.yml
│   ├── preset-cpp.yml
│   └── preset-shell.yml
├── scripts/
│   └── init.py              # Python 初始化脚本
├── tests/                   # 模板自身的测试（pytest）
├── docs/
│   ├── getting-started.md
│   └── module-guide.md
└── README.md
```

### 模块内部结构

每个模块遵循统一结构：

```
modules/<module-name>/
├── module.yml                    # 模块元数据
├── snippets/                     # CLAUDE.md 片段，按章节组织
│   ├── coding-standards.md
│   └── testing.md
├── config/
│   ├── settings.json.snippet     # settings.json 合并片段
│   └── commands/                 # 自定义 slash commands
├── hooks/                        # pre-commit hook 配置片段
│   └── ruff.yaml
├── templates/                    # 项目级文件模板
```

### module.yml Schema

```yaml
name: lang-python                  # 模块标识（唯一）
version: 1.0.0                     # 语义版本（当前仅用于展示和模块信息记录，不参与依赖约束或兼容性检查）
description: Python 开发规范模块     # 一行描述
type: language                     # 模块类型：core | general | language
depends: [core]                    # 依赖模块

sections:                          # CLAUDE.md 章节贡献
  - slot: coding-standards         # 目标章节
    file: snippets/coding-standards.md
    order: 100                     # 章节内排序，越小越靠前（core 默认 0，general 默认 50，language 默认 100）
  - slot: testing
    file: snippets/testing.md
    order: 100
    conditions:                    # 条件 snippet：匹配时替换默认 file
      - when: test_framework == pytest
        file: snippets/testing.pytest.md
      - when: test_framework == unittest
        file: snippets/testing.unittest.md

variables:                         # 需用户输入的变量
  - name: formatter
    prompt: "Python 格式化工具"
    default: "ruff"
    choices: ["ruff", "black"]
  - name: test_framework
    prompt: "测试框架"
    default: "pytest"
    choices: ["pytest", "unittest"]

templates:                         # 项目级文件映射（source 相对于模块根目录）
  - source: templates/pyproject.toml
    target: pyproject.toml

pre_commit_hooks:                  # pre-commit 配置片段
  - file: hooks/ruff.yaml
    conditions:
      - when: formatter == black
        file: hooks/black.yaml

gitignore_entries:                 # .gitignore 追加条目
  - "__pycache__/"
  - "*.pyc"
  - ".pytest_cache/"

commands:                          # slash commands
  - name: pytest
    file: config/commands/pytest.md
```

### 预设定义格式

每个预设是一个 YAML 文件：

```yaml
# presets/preset-python.yml
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

## CLAUDE.md 合并机制

### 章节定义

预定义 9 个核心章节，按以下顺序组织：

| 顺序 | 章节 | 贡献模块 |
|------|------|---------|
| 1 | 项目信息 | core |
| 2 | 行为准则 | core（Karpathy 四原则） |
| 3 | 编码规范 | core + 语言模块 |
| 4 | 测试规范 | core + testing + 语言模块 |
| 5 | Git 规范 | git-convention |
| 6 | 代码审查 | code-review |
| 7 | API 设计 | api-design |
| 8 | 安全规范 | security |
| 9 | 自动化 | automation |

- 没有模块贡献的章节不出现
- 多模块贡献同一章节时，按 `order` 排序；同 order 按模块名字母序
- 语言模块的片段标题自带语言标识（如 `### Python 代码规范`），自然分区
- **章节扩展**：若 module.yml 的 sections 中使用了非预定义 slot 名，该 snippet 作为新章节追加到 9 个核心章节之后，按 order 排序。多个模块使用相同自定义 slot 名时，合并为同一章节（按 order 排序），与预定义章节的合并规则一致。自定义章节的标题由 snippet 文件内容的首行 `## ` 标题决定

### 条件机制

sections、templates 和 pre_commit_hooks 均支持 `conditions` 按变量值选择不同内容：

- 从 conditions 列表中找第一个满足 `when` 条件的条目，**替换**默认的 file（sections/pre_commit_hooks）或 source（templates）；templates 的 conditions 还可替换 target
- 无匹配时使用默认 file 或 source
- 条件语法：`变量名 == 值`（仅支持等值比较）

### 合并规则

| 产出 | 合并方式 |
|------|---------|
| snippets/*.md | 按章节聚合，章节内按 order 排序，变量替换后写入 CLAUDE.md。每个 snippet 内容前插入更新标记：`<!-- module:<name>:<version>:<slot> -->`，下一个标记或 EOF 为天然边界，用于追加模块时识别已安装模块 |
| settings.json.snippet | 深度合并：(1) 对象递归合并；(2) 数组拼接后按 JSON 序列化值去重；(3) 标量（字符串、数字、布尔）后加载模块覆盖先加载 |
| .pre-commit-config.yaml | 专用合并：git-convention 提供骨架（含 repos 数组），各模块的 pre_commit_hooks 按加载顺序追加到 repos 数组末尾。每个 hook 片段为完整的 repo 对象（含 repo、rev、hooks 字段），直接追加到 repos 数组。若 git-convention 未被选中，但有其他模块贡献 pre_commit_hooks，则自动生成骨架（仅含 repos 数组，无 commit-msg hook） |
| .gitignore | 各模块的 gitignore_entries 按加载顺序追加到文件末尾，行级去重 |
| commands/ | 直接复制到 .claude/commands/，文件名冲突报错 |
| templates/ | 按 source→target 映射复制；目标路径冲突时内容相同则去重，不同则报错 |

### 模块加载顺序

1. **依赖拓扑排序**：被依赖的模块先加载（core 最先）
2. **同层级排序**：同层无依赖关系的模块按以下顺序排列：(a) type=general 在前，type=language 在后；(b) 同类内按字母序
3. **循环依赖检测**：拓扑排序无法完成时，报错退出并列出循环依赖链

示例：选择 core + testing + lang-python 时，加载顺序为 core → testing（general）→ lang-python（language），优先级 lang-python > testing > core。

### 变量处理

- **全局变量**（PROJECT_NAME 等）：由 core 模块在 variables 中声明，始终替换，缺失或为空字符串时验证阶段报错
- **模块变量**（test_framework 等）：仅当定义该变量的模块被选中时才提示；引用了不存在的模块变量时，保留 `{{VAR}}` 原样并输出警告
- **同名变量**：多语言模块可共存，language 模块的默认值覆盖 general 模块的（language 模块后加载，优先级更高）；若两个 general 模块定义同名变量，按加载顺序后覆盖先。同名变量的 choices 取并集（去重），确保所有选项可用
- 替换：snippet、template、settings.json.snippet、pre_commit_hooks 片段、commands 文件中的 `{{VAR}}` 均替换为用户输入值
- **条件求值**：conditions 中的 `when` 表达式引用未定义变量时，该条件视为不匹配，并输出警告

### 已有项目接入策略

自动判断写入目标：共享文件（`CLAUDE.md`/`settings.json`）不存在时写共享文件，存在时自动回退到 local 文件（`CLAUDE.local.md`/`settings.local.json`）。

| 策略 | 行为 |
|------|------|
| 追加（默认） | 新内容追加到目标文件末尾，保留原有内容；若目标文件中存在与生成内容相同的 `## ` 级别标题，发出警告提示可能产生重复章节 |
| 覆盖 | 生成全新文件（需二次确认，覆盖前备份原文件为 `.bak`） |

其他文件的处理策略：

| 文件类型 | 已有文件处理 |
|---------|------------|
| settings.json / settings.local.json | 不覆盖，输出提示 |
| .pre-commit-config.yaml | 安全追加：检测已有 repos，按 repo URL 去重后追加新条目 |
| .gitignore | 安全追加：行级去重后追加新条目 |
| 其他模板文件 | 不覆盖，仅在文件不存在时生成，输出提示 |

---

## 模块详细设计

### core（必选）

CLAUDE.md 行为准则基于 Andrej Karpathy 的 LLM 编码观察，四个原则：

1. **先思考再编码**：不确定时先问，不静默选择解读；多种理解全部呈现；有更简方案直说；不清楚就停
2. **简单至上**：不添加未请求功能；单次使用不做抽象；200 行能变 50 行就重写
3. **精准修改**：不顺手改周边代码；匹配现有风格；无关死代码提及但不删；自己造成的废弃代码必须清理
4. **目标驱动执行**：用测试定义成功标准；多步骤任务先列计划（步骤→验证检查）

| 项目 | 内容 |
|------|------|
| type | core |
| snippets | 项目信息模板（名称/描述/技术栈）、行为准则（Karpathy 四原则）、编码规范（仅保留 AI 易忽略项：避免嵌套超过 3 层、公共 API 必须有文档、复杂逻辑加注释）、通用测试规范 |
| config/settings.json.snippet | 通用权限（allow Read/Glob/Grep）；语言/工具特定权限由各语言模块贡献 |
| templates | `README.md` 骨架（含 Claude Code 使用说明） |
| variables | `PROJECT_NAME`、`PROJECT_DESCRIPTION`、`TECH_STACK` |

### git-convention

| 项目 | 内容 |
|------|------|
| type | general |
| snippets | Conventional Commits 规范（feat/fix/docs/refactor/chore）、branch 命名（`type/description`）、PR 标题格式 |
| config/commands | `/commit`：自动分析 diff 生成规范 commit message（与 commit-msg hook 互补：/commit 主动生成规范格式，hook 被动校验兜底） |
| pre_commit_hooks | conventional-pre-commit hook（commit-msg 校验），作为 `.pre-commit-config.yaml` 的首个 repo 条目 |
| variables | `commit_lang`（默认 en，可选 zh） |
| depends | core |

### testing

| 项目 | 内容 |
|------|------|
| type | general |
| snippets | 测试策略（覆盖率 ≥ 80%、单元/集成/E2E 比例建议）、命名规范 `test_<功能>_<场景>_<预期>`、Bug 修复加回归测试、不为测试而测试 |
| config/commands | `/test-run`：运行测试并分析失败原因 |
| depends | core |

### code-review

| 项目 | 内容 |
|------|------|
| type | general |
| snippets | 审查标准（正确性 > 安全性 > 可维护性 > 其他）、PR 描述模板（变更说明、影响范围、测试验证） |
| pre_commit_hooks | pre-push 提醒检查 |
| config/commands | `/review`：对当前 diff 做 review |
| depends | core, git-convention |

### api-design

| 项目 | 内容 |
|------|------|
| type | general |
| snippets | 按 api_style 变量条件选择：rest → RESTful 规范 + OpenAPI；graphql → GraphQL 规范 + Schema 模板；grpc → gRPC 规范 + proto 模板 |
| templates | OpenAPI 规范骨架（rest 时）；GraphQL Schema 骨架（graphql 时）；proto 文件骨架（grpc 时） |
| variables | `api_style`（默认 rest，可选 graphql、grpc） |
| depends | core |

### automation

| 项目 | 内容 |
|------|------|
| type | general |
| snippets | 按 ci_platform 变量条件选择：github-actions → GitHub Actions 规范；gitlab-ci → GitLab CI 规范 |
| config/settings.json.snippet | MCP 服务器配置：filesystem（项目目录读写）、fetch（HTTP 请求） |
| templates | GitHub Actions workflow 模板（github-actions 时）；GitLab CI pipeline 模板（gitlab-ci 时） |
| variables | `ci_platform`（默认 github-actions，可选 gitlab-ci） |
| depends | core |

### security

| 项目 | 内容 |
|------|------|
| type | general |
| snippets | 安全规范（不硬编码密钥、依赖安全扫描、漏洞更新、锁定版本、.env.example） |
| pre_commit_hooks | gitleaks 密钥检测 |
| gitignore_entries | `*.key`、`*.pem`、`.env` |
| templates | `.env.example` 模板 |
| depends | core |

### lang-python

| 项目 | 内容 |
|------|------|
| type | language |
| snippets (coding-standards, order=100) | 项目结构（src layout）、格式化（{{formatter}}）、`from __future__ import annotations`、命名规范（snake_case）、Google 风格 docstring |
| snippets (testing, order=100) | pytest 配置、fixture 约定、mock 使用规范 |
| config/settings.json.snippet | 允许 `Bash(pytest)`、`Bash(ruff)` 等 |
| pre_commit_hooks | 格式化检查（根据 formatter 变量条件选择 ruff 或 black 配置） |
| gitignore_entries | `__pycache__/`、`*.pyc`、`.pytest_cache/`、`.ruff_cache/` |
| config/commands | `/pytest`：运行 pytest |
| templates | `pyproject.toml` 骨架 |
| variables | `formatter`（默认 ruff，可选 black）、`test_framework`（默认 pytest，可选 unittest） |
| depends | core |

### lang-cpp

| 项目 | 内容 |
|------|------|
| type | language |
| snippets (coding-standards, order=100) | 构建目标命名加项目前缀、依赖管理使用构建系统标准方式、命名遵循 Google C++ Style Guide、前向声明优先 |
| snippets (testing, order=100) | Google Test / Catch2 规范、测试目录结构 |
| config/settings.json.snippet | 允许 `Bash(cmake)`、`Bash(ctest)` 等 |
| gitignore_entries | `build/`、`cmake-build-*/`、`*.o`、`*.a` |
| config/commands | `/ctest`：运行 ctest |
| templates | CMakeLists.txt 骨架、`.clang-format`、`.clang-tidy` |
| variables | `test_framework`（默认 gtest，可选 catch2） |
| depends | core |

### lang-shell

| 项目 | 内容 |
|------|------|
| type | language |
| snippets (coding-standards, order=100) | POSIX 兼容性（#!/usr/bin/env bash）、错误处理（set -euo pipefail）、变量引用双引号、printf 代替 echo、函数命名 snake_case |
| snippets (testing, order=100) | ShellCheck 集成、bats-core 测试规范 |
| config/settings.json.snippet | 允许 `Bash(shellcheck)`、`Bash(bats)` |
| pre_commit_hooks | shellcheck 检查 |
| gitignore_entries | `*.log`、`*.tmp` |
| config/commands | `/bats`：运行 bats 测试 |
| templates | 脚本模板（含参数解析、日志、错误处理骨架） |
| depends | core |

---

## Slash Commands 命名规范

| 模块 | 命令 | 说明 |
|------|------|------|
| git-convention | `/commit` | 分析 diff 生成 commit message |
| testing | `/test-run` | 运行测试并分析失败 |
| code-review | `/review` | review 当前 diff |
| lang-python | `/pytest` | 运行 pytest |
| lang-cpp | `/ctest` | 运行 ctest |
| lang-shell | `/bats` | 运行 bats 测试 |

冲突通过生成时文件名检测解决（仅限 slash commands 文件名冲突）。

---

## init.py 初始化脚本

### 使用方式

```bash
# 新项目（交互式）
python scripts/init.py /path/to/new-project

# 已有项目追加模块
python scripts/init.py --module testing /path/to/existing-project

# 已有项目追加多个模块
python scripts/init.py --module testing,security /path/to/existing-project

# 使用预设
python scripts/init.py --preset preset-python /path/to/new-project

# diff 预览（干运行模式：仅预览不写入磁盘）
python scripts/init.py --diff --module security /path/to/existing-project

# 非交互模式（CI/脚本调用，所有变量使用默认值；全局变量通过 --var 传入）
python scripts/init.py --preset preset-python --non-interactive --var PROJECT_NAME=my-api --var PROJECT_DESCRIPTION="My API" /path/to/new-project
```

`--module` 指定模块时，依赖自动补全（如 `--module lang-python` 会自动加入 core）。`--preset` 和 `--module` 不可同时使用，同时指定时报错退出。

### 已安装模块识别

向已有项目追加模块时，通过检测 CLAUDE.md 中的 `<!-- module:<name>:<version>:<slot> -->` 更新标记来识别已安装的模块。若 CLAUDE.md 中无更新标记（如手动编写的 CLAUDE.md），则无法识别已安装模块，此时：

- 追加策略：生成所有选中模块的完整内容，可能产生重复章节（会发出警告）
- 覆盖策略：生成全新 CLAUDE.md

已识别的已安装模块的所有贡献（snippet、settings.json.snippet、pre_commit_hooks、gitignore_entries、commands、templates）均跳过，仅处理新增模块的贡献。文件级合并/去重规则仅作用于新增模块的产出。

### 交互流程

1. 收集项目信息（名称、描述、技术栈——对应 core 模块的 PROJECT_NAME、PROJECT_DESCRIPTION、TECH_STACK 变量）
2. 选择预设或自定义模块
3. 解析依赖，自动补全（core 始终被包含）
4. 收集模块变量（同名变量按优先级合并后只问一次）
5. 在内存中生成文件（合并 snippets、settings、pre-commit hooks、gitignore、commands、templates）
6. 变量替换
7. 验证（CLAUDE.md 无空章节、settings.json 合法、依赖满足）
8. diff 预览（展示将要写入/新建的文件列表，对已有文件展示内容差异；`--diff` 模式仅执行到本步骤后退出，不写入磁盘）
9. 用户确认
10. 写入磁盘

### 验证失败处理

| 验证项 | 失败处理 |
|--------|---------|
| CLAUDE.md 有空章节 | 报错退出，提示哪个章节为空及对应模块 |
| settings.json 不合法 | 报错退出，提示合并后的 JSON 语法错误位置 |
| 依赖不满足 | 报错退出，提示缺失的依赖模块 |
| 变量未替换（残留 {{VAR}}） | 警告，列出未替换的变量名，继续执行 |

### 循环依赖检测

依赖补全完成后，对最终模块集合（含用户显式选择和自动补全的依赖）进行拓扑排序。

- 若检测到循环依赖，报错退出

### init.py 失败处理

| 场景 | 处理方式 |
|------|---------|
| 目标目录不存在 | 自动创建 |
| 目标已有 CLAUDE.md | 询问接入策略（追加/覆盖） |
| 目标已有其他配置文件 | 按已有项目接入策略中的文件类型规则处理 |
| 预设引用的模块不存在 | 报错退出，提示缺失的模块名 |
| 模块依赖无法解析 | 报错退出，提示缺失模块 |
| 写入失败 | 删除本次已写入的新建文件（不删除已有文件）；若覆盖了 CLAUDE.md，从 .bak 备份恢复 |
| 目标不在 git 仓库内 | 警告提示（pre-commit 需要 git），仍生成 .pre-commit-config.yaml |

### Windows 兼容性

- Python 脚本天然跨平台
- 生成的文件路径使用正斜杠
- pre-commit 配置中的 entry 使用 `python` 而非硬编码路径

### 本地化说明

当前唯一支持本地化的变量是 git-convention 模块的 `commit_lang`（en/zh）。如需更多本地化维度，可通过条件 snippet 机制扩展。

---

## 模板自身测试

使用 pytest 编写测试，覆盖：

- 各预设生成的文件是否完整
- 变量替换是否正确
- 依赖解析是否自动补全
- diff 模式输出是否符合预期
- 多模块共存时章节是否正确分区
- settings.json 深度合并是否正确
- .pre-commit-config.yaml 合并是否合法
- .gitignore 条目去重是否正确
- 条件 snippet 选择是否正确
- 已有文件不覆盖策略是否生效

---

## 预设

| 预设 | 包含模块 |
|------|---------|
| preset-minimal | core |
| preset-python | core + git-convention + testing + code-review + security + lang-python |
| preset-cpp | core + git-convention + testing + code-review + security + lang-cpp |
| preset-shell | core + git-convention + testing + code-review + security + lang-shell |

---

## 后续版本规划（暂不实现）

以下特性推迟到后续版本：

- **增量更新**：锁文件 + 更新标记 + `--update` 模式
- **已有项目合并策略**：按标题匹配合并
- **模块卸载**：移除已安装模块及其生成内容
- **自定义章节位置控制**：允许模块指定新章节在文档中的精确位置（当前仅支持追加到核心章节之后）
- **更多语言模块**：lang-rust、lang-go、lang-java 等
- **CLI 脚手架**：npm/pip 发布的 CLI 工具
