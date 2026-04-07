# 04-bash-tool.md 细纲

## 一、标题层级结构

### 1. BashTool 深度解析 —— Shell 命令安全执行
- 学习目标（5点）
- 生活类比：银行的安全柜台
- BashTool 模块地图
- 输入参数与命令解析
  - 输入 Schema
  - 命令分类体系
- 安全检查的多层防御
  - 第 1 层：AST 解析
  - 第 2 层：安全包装器剥离
  - 第 3 层：子命令分割与逐一检查
- 权限检查的优先级
- 沙箱机制
- 超时与后台执行
- 命令安全拦截示例
  - 危险的 cd + git 组合
  - 子命令数量上限
  - 危险 Shell 前缀黑名单
- isReadOnly 判断逻辑
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **BashTool 模块结构**
   - `BashTool.tsx` - 主入口
   - `bashSecurity.ts` - 安全检查
   - `bashPermissions.ts` - 权限检查
   - `readOnlyValidation.ts` - 只读验证

2. **命令分类**
   - `BASH_SEARCH_COMMANDS`: find, grep, rg, ag 等
   - `BASH_READ_COMMANDS`: cat, head, tail, less 等
   - `BASH_LIST_COMMANDS`: ls, tree, du
   - `BASH_SILENT_COMMANDS`: mv, cp, rm, mkdir 等

3. **AST 解析三种结果**
   - `simple`: 命令结构清晰
   - `too-complex`: 含有命令替换、扩展等复杂结构
   - `parse-unavailable`: tree-sitter 不可用

4. **安全环境变量白名单**
   - SAFE: NODE_ENV, RUST_LOG, GO111MODULE, NO_COLOR, TERM
   - UNSAFE: PATH, LD_PRELOAD, PYTHONPATH, NODE_OPTIONS

## 三、源码文件路径

- `src/tools/BashTool/BashTool.tsx` - 主入口（第 60-120 行）
- `src/tools/BashTool/bashPermissions.ts` - 权限检查（第 1050-1178 行）
- `src/tools/BashTool/bashSecurity.ts` - 安全检查
- `src/tools/BashTool/readOnlyValidation.ts` - 只读验证
- `src/tools/BashTool/shouldUseSandbox.ts` - 沙箱判断

## 四、类名、函数名、接口名

### 函数
- `bashToolHasPermission()` - Bash 工具权限检查入口
- `bashToolCheckPermission()` - 权限检查核心（第 1050-1178 行）
- `bashToolCheckExactMatchPermission()` - 精确匹配检查
- `stripSafeWrappers()` - 剥离安全包装器（第 524 行）
- `parseCommandRaw()` - AST 解析命令
- `parseForSecurityFromAst()` - AST 安全分析
- `isSearchOrReadBashCommand()` - 只读命令判断（第 95-120 行）

### 常量
- `BASH_SEARCH_COMMANDS` - 搜索类命令集合（第 76-78 行）
- `BASH_READ_COMMANDS` - 读取类命令集合（第 81-85 行）
- `BASH_LIST_COMMANDS` - 列表类命令集合（第 88 行）
- `BASH_SILENT_COMMANDS` - 静默命令集合（第 91-94 行）
- `SAFE_ENV_VARS` - 安全环境变量白名单（第 378-430 行）
- `BARE_SHELL_PREFIXES` - 危险 Shell 前缀黑名单（第 196-226 行）
- `MAX_SUBCOMMANDS_FOR_SECURITY_CHECK` - 子命令数量上限（第 103 行）= 50

### 类型
- `BashCommand` - Bash 命令类型
- `BashPermissionResult` - Bash 权限检查结果
