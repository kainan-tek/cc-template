### C++ 测试规范（Catch2）

- 测试目录：`tests/`
- 测试文件命名：`test_<module>.cpp`
- 测试用例命名：`TEST_CASE("<Feature>: <Scenario> <Expected>")`
- REQUIRE 断言（致命）用于关键验证，CHECK（非致命）用于软验证
- 使用 SECTION 组织测试内的子场景
- 使用 TEST_CASE_METHOD 绑定 fixture 共享测试数据
