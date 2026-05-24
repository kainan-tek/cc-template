## API 设计

- URL 使用名词复数：`/users`、`/orders`
- HTTP 方法语义：GET（查询）、POST（创建）、PUT（全量更新）、PATCH（部分更新）、DELETE（删除）
- 使用 HTTP 状态码：200（成功）、201（创建）、400（请求错误）、404（未找到）、500（服务器错误）
- 分页：`?page=1&page_size=20`
- 版本控制：URL 路径 `/api/v1/` 或 Header `Accept: application/vnd.api.v1+json`
- 所有 API 必须有 OpenAPI 文档
- 请求/响应必须定义 Schema
- 示例值必须提供
