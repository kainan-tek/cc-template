### Python 测试规范

- 测试文件命名：`test_<module>.py`
- 测试类命名：`Test<Feature>`（继承 `unittest.TestCase`）
- 测试方法命名：`test_<function>_<scenario>_<expected>`

#### unittest 配置

- 使用 `unittest.TestCase` 作为基类
- `setUp` / `tearDown` 管理测试数据
- 使用 `unittest.mock` 进行 mock
- 运行命令：`python -m pytest` 或 `python -m unittest discover`
