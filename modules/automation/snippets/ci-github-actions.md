## 自动化

- Workflow 文件放在 `.github/workflows/`
- 命名：`ci.yml`、`release.yml`
- 触发条件明确：push 分支、PR、tag
- Job 间依赖通过 `needs` 声明
- 使用缓存加速构建
