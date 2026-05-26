### Rust 编码规范

- 项目结构：`src/lib.rs` 或 `src/main.rs`，测试 `#[cfg(test)]` 模块
- 使用 `cargo fmt` 格式化代码，`cargo clippy` 静态检查
- 命名：模块 snake_case、类型 PascalCase、函数/变量 snake_case、常量 SCREAMING_SNAKE_CASE
- 公共 API 必须有 `///` 文档注释
- 错误处理使用 `Result<T, E>`，避免 `unwrap()` 和 `expect()` 在生产代码
