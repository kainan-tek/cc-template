### C++ 编码规范

#### CMake 约定

- 使用 `CMakePresets.json` 管理构建配置
- 目标命名：`<project>_<library>`
- 使用 `FetchContent` 管理第三方依赖

#### 命名规范

- 类/结构体：PascalCase
- 函数/方法：snake_case
- 变量：snake_case
- 常量：kUpperCamelCase
- 宏：UPPER_SNAKE_CASE

#### 头文件

- 使用 `#pragma once` 作为 include guard
- 头文件自包含
- 前向声明优先于 `#include`

#### RAII 原则

- 资源获取即初始化
- 智能指针优先：`unique_ptr` > `shared_ptr`
- 禁止裸 `new`/`delete`

#### const 正确性

- 能用 `const` 就用 `const`
- 参数传递：基本类型按值，其他按 const 引用
- 成员函数：不修改状态则标记 `const`
