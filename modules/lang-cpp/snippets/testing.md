### C++ 测试规范

- 测试目录：`tests/`
- 测试文件命名：`test_<module>.cpp`
- 测试函数命名：`Test<Feature>_<Scenario>_<Expected>`
- 使用 TEST 宏定义测试用例
- EXPECT 断言（非致命）优先于 ASSERT（致命）
- 使用 fixture 共享测试数据
