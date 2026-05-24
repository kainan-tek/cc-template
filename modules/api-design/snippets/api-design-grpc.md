## API 设计

### gRPC 规范

- 使用 Protocol Buffers v3
- Service 命名 PascalCase
- RPC 方法命名 PascalCase
- Message 命名 PascalCase
- 字段命名 snake_case

### Proto 文件组织

- 每个 Service 一个 proto 文件
- 公共 Message 放在 common.proto
- 使用 package 避免命名冲突
