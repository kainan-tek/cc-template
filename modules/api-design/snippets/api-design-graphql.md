## API 设计

- Query 只做查询，Mutation 只做变更
- 使用 Input Type 区分创建和更新
- 分页使用 Relay Connection 规范
- 错误处理使用标准 error 格式
- Schema 按领域分模块
- 命名：类型 PascalCase、字段 camelCase、枚举值 SCREAMING_SNAKE_CASE
