### C++ 编码规范

- 构建目标命名加项目前缀（如 `<project>_<library>`），避免冲突
- 依赖管理使用构建系统的标准方式（CMake: `FetchContent` / Android: `android_library deps`）
- 命名遵循 Google C++ Style Guide
- 前向声明优先于 `#include`
