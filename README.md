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
