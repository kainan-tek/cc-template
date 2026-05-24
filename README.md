# CC Template

Claude Code 项目工程模板生成工具，通过模块化配置解决重复配置和质量不稳定两大痛点。

## 它做什么？

当你使用 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 开发项目时，通常需要编写 `CLAUDE.md` 来指导 AI 的行为、配置 `.claude/settings.json` 来控制权限、设置 `.pre-commit-config.yaml` 来保证代码质量。每次新项目都要重复这些工作，而且配置质量参差不齐。

本模板通过**模块化**解决这个问题：

1. **选择模块** → 自动生成 `CLAUDE.md`、`settings.json`、`.pre-commit-config.yaml`、`.gitignore` 等配置文件
2. **变量替换** → 项目名称、技术栈等信息自动填入模板
3. **依赖自动补全** → 选了 `lang-python` 会自动带上 `core`

## 快速开始

```bash
# Python 项目（推荐新手使用预设）
python scripts/init.py /path/to/new-project --preset preset-python

# C++ 项目
python scripts/init.py /path/to/new-project --preset preset-cpp

# Shell 项目
python scripts/init.py /path/to/new-project --preset preset-shell

# 最小配置（仅 core 模块）
python scripts/init.py /path/to/new-project --preset preset-minimal
```

运行后会交互式地询问项目名称、描述、技术栈等信息，然后在目标目录生成配置文件。

## 模块

模块分为三种类型：**core**（必选基础）、**general**（通用规范）、**language**（语言规范）。

| 模块 | 类型 | 说明 |
|------|------|------|
| core | core（必选） | 行为准则（Karpathy 四原则）、通用编码规范、项目信息模板 |
| git-convention | general | Conventional Commits 规范、branch 命名、commit-msg hook |
| testing | general | 测试策略、命名规范 `test_<功能>_<场景>_<预期>`、覆盖率要求 |
| code-review | general | 审查标准、PR 描述模板、pre-push 提醒 |
| api-design | general | 按 `api_style` 变量选择 REST/GraphQL/gRPC 规范 |
| automation | general | 按 `ci_platform` 变量选择 GitHub Actions/GitLab CI、MCP 服务器配置 |
| security | general | 安全编码准则、gitleaks 密钥检测、`.env.example` 模板 |
| lang-python | language | Python 编码规范、pytest/unittest、ruff/black 格式化 |
| lang-cpp | language | C++ 编码规范、clang-format |
| lang-shell | language | Shell 编码规范、ShellCheck、bats 测试 |

## 使用方式

```bash
# 交互式（逐步询问项目信息和模块变量）
python scripts/init.py /path/to/project

# 使用预设（一键配置，最常用）
python scripts/init.py /path/to/project --preset preset-python

# 指定模块（依赖自动补全，如 lang-python 会自动带上 core）
python scripts/init.py /path/to/project --module core,testing,lang-python

# 追加模块到已有项目（自动检测已安装模块，跳过重复内容）
python scripts/init.py --module security /path/to/existing-project

# 预览模式（只看会生成什么文件，不实际写入）
python scripts/init.py --diff --preset preset-python /path/to/project

# 非交互模式（CI/脚本调用，所有变量使用默认值，全局变量通过 --var 传入）
python scripts/init.py --preset preset-python --non-interactive \
  --var PROJECT_NAME=my-api --var PROJECT_DESCRIPTION="My API" \
  /path/to/project
```

### 生成的文件

| 文件 | 说明 |
|------|------|
| `CLAUDE.md` | Claude Code 行为指导文件，按章节聚合各模块的规范片段 |
| `.claude/settings.json` | Claude Code 权限配置（如允许 `Bash(pytest)`） |
| `.claude/commands/*.md` | 自定义 slash commands（如 `/commit`、`/pytest`） |
| `.pre-commit-config.yaml` | Git pre-commit hooks 配置 |
| `.gitignore` | Git 忽略规则 |
| 其他模板文件 | 如 `pyproject.toml`、`CMakeLists.txt`、`.env.example` 等 |

### 已有项目接入

自动判断写入目标：**共享文件不存在时写共享文件，存在时自动回退到 local 文件**。无需手动指定，直接运行即可。

| 文件 | 共享文件不存在 | 共享文件已存在 |
|------|-------------|-------------|
| 行为指导 | 写 `CLAUDE.md` | 写 `CLAUDE.local.md`（已有时询问追加/覆盖） |
| 权限配置 | 写 `.claude/settings.json` | 深度合并到 `.claude/settings.json`（只加不删） |
| `.pre-commit-config.yaml` | 创建 | repo URL 去重后追加 |
| `.gitignore` | 创建 | 行级去重后追加 |
| 其他模板文件 | 创建 | 跳过 |

> `CLAUDE.md`/`settings.json` 提交 git（团队共享）；`CLAUDE.local.md` gitignored（个人本地）。

## 预设

| 预设 | 包含模块 |
|------|---------|
| preset-minimal | core |
| preset-python | core + git-convention + testing + code-review + security + lang-python |
| preset-cpp | core + git-convention + testing + code-review + security + lang-cpp |
| preset-shell | core + git-convention + testing + code-review + security + lang-shell |

## 开发

```bash
pip install -e ".[dev]"
pytest
```
