### Shell 编码规范

- Shebang：`#!/usr/bin/env bash`
- 错误处理：`set -euo pipefail`
- 变量引用始终使用双引号 `"$var"`
- 使用 `printf` 代替 `echo`
- 函数命名 snake_case，使用 `local` 声明局部变量
- 使用 `[[ ]]` 代替 `[ ]`，`$()` 代替反引号
