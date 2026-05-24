## API 设计

- 使用 Protocol Buffers v3
- 命名：Service/RPC/Message PascalCase、字段 snake_case
- 每个 Service 一个 proto 文件
- 公共 Message 放在 common.proto
- 使用 package 避免命名冲突
