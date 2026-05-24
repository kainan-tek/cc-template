### Python 测试规范

- 测试文件命名：`test_<module>.py`
- 测试类命名：`Test<Feature>`
- 测试函数命名：`test_<function>_<scenario>_<expected>`
- 使用 `conftest.py` 管理 fixture，命名 `<resource>_<scope>`（如 `db_session`）
- `@pytest.fixture(scope=...)` 控制生命周期
- Mock 使用 `pytest-mock` 的 `mocker` fixture
- 常用：`pytest` | `pytest tests/test_foo.py` | `pytest -k "test_login"` | `pytest --cov=src`
