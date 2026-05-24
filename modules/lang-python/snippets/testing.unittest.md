### Python 测试规范

- 测试文件命名：`test_<module>.py`
- 测试类继承 `unittest.TestCase`
- 测试方法命名：`test_<function>_<scenario>_<expected>`
- `setUp` / `tearDown` 管理测试数据
- 使用 `unittest.mock` 进行 mock
- 运行：`python -m pytest` 或 `python -m unittest discover`
