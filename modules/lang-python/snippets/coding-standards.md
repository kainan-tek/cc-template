### Python 编码规范

- 使用 src layout：源码 `src/<pkg>/__init__.py`，测试 `tests/test_<module>.py`
- 使用 {{formatter}} 进行代码格式化
- 使用 `from __future__ import annotations` 延迟求值
- 命名：模块/包 snake_case、类 PascalCase、函数/方法/变量 snake_case、常量 UPPER_SNAKE_CASE
- 公共 API 使用 Google 风格 docstring
