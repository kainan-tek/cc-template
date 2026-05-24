### Shell 编码规范

#### POSIX 兼容性

- Shebang：`#!/usr/bin/env bash`
- 错误处理：`set -euo pipefail`
- 变量引用：始终使用双引号 `"$var"`

#### 最佳实践

- 使用 `printf` 代替 `echo`
- 函数命名：snake_case
- 使用 `local` 声明局部变量
- 使用 `[[ ]]` 代替 `[ ]`
- 使用 `$()` 代替反引号
