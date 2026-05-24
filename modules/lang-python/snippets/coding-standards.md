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
