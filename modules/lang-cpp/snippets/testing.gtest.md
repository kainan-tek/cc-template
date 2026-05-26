### C++ 测试规范（Google Test）

- 测试目录：`tests/`
- 测试文件命名：`test_<module>.cpp`
- 测试函数命名：`TEST(<Feature>, <Scenario>_<Expected>)`
- EXPECT_* 做正常验证（非致命），ASSERT_* 做前提条件检查（致命）
- 使用 TEST_F 定义 fixture 测试，共享测试数据
