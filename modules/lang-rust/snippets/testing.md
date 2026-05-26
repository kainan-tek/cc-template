### Rust 测试规范

- 测试位置：`#[cfg(test)] mod tests` 在同文件底部，或 `tests/` 目录集成测试
- 测试函数命名：`test_<function>_<scenario>_<expected>`
- 使用 `#[test]` 标记测试，`#[should_panic]` 标记预期失败
- 断言：`assert!`（布尔）、`assert_eq!`/`assert_ne!`（相等比较）
- 常用：`cargo test` | `cargo test <name>` | `cargo test -- --nocapture`
