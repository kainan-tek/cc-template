### Python 测试规范

- 测试文件命名：`test_<module>.py`
- 测试类命名：`Test<Feature>`
- 测试函数命名：`test_<function>_<scenario>_<expected>`

#### pytest 配置

- 使用 `conftest.py` 管理 fixture
- fixture 命名：`<resource>_<scope>`（如 `db_session`）
- 使用 `@pytest.fixture(scope="module")` 控制生命周期
- Mock 使用 `pytest-mock` 的 `mocker` fixture

#### 常用命令

- 运行所有测试：`pytest`
- 运行单个文件：`pytest tests/test_foo.py`
- 运行匹配测试：`pytest -k "test_login"`
- 查看覆盖率：`pytest --cov=src`
