# 02-default-mode.md 细纲

## 一、标题层级结构

### 1. Default 模式——每次询问的安全哲学
- 学习目标（5点）
- 生活类比：谨慎的新管家
- 源码直击：Default 模式的配置
  - PERMISSION_MODE_CONFIG
- 核心函数：hasPermissionsToUseTool
  - 内层函数执行流程图
- 核心源码解析
  - hasPermissionsToUseToolInner 在 Default 模式下的行为
- 只读命令：自动放行的白名单
  - READONLY_COMMANDS
  - COMMAND_ALLOWLIST
- Default 模式下的典型工作流
- Accept Edits 模式：文件系统命令的快速通道
  - ACCEPT_EDITS_ALLOWED_COMMANDS
- 模式切换：Shift+Tab 循环
  - getNextPermissionMode
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **Default 模式核心理念**
   - 默认不信任，操作前先问
   - 宁可多问一次，不可多做一步

2. **hasPermissionsToUseTool 执行流程**
   - Step 1a: 整个工具 Deny 规则检查
   - Step 1b: 整个工具 Ask 规则检查
   - Step 1c: 工具自检 checkPermissions
   - Step 1d: 工具自检结果为 deny
   - Step 1g: 安全检查
   - Step 2a: Bypass 模式检查
   - Step 2b: 整个工具 Allow 规则
   - Step 3: passthrough → ask 转换

3. **只读命令白名单**
   - `ls`, `cat`, `head`, `tail`, `wc`, `stat`
   - `id`, `uname`, `free`, `df`, `du`
   - `basename`, `dirname`, `realpath`
   - `cut`, `paste`, `tr`, `column`, `diff`
   - `sleep`, `which`, `type`, `true`, `false`

4. **Flag 解析白名单**
   - `grep`: `-i`, `-r`, `-n`, `-c` 等安全 flag
   - `git diff`: 安全 flag 集合

5. **Accept Edits 模式**
   - 对文件系统命令自动放行
   - `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, `sed`

6. **模式切换循环**
   - Default → AcceptEdits → Plan → Bypass → Default
   - Shift+Tab 快捷键切换

## 三、源码文件路径

- `src/utils/permissions/PermissionMode.ts` - 模式配置
- `src/utils/permissions/permissions.ts` - 权限检查核心
- `src/tools/BashTool/readOnlyValidation.ts` - 只读命令验证
- `src/tools/BashTool/modeValidation.ts` - 模式约束验证
- `src/utils/permissions/getNextPermissionMode.ts` - 模式切换

## 四、类名、函数名、接口名

### 核心函数
- `hasPermissionsToUseTool()` - 权限检查入口
- `hasPermissionsToUseToolInner()` - 内层权限检查
- `getNextPermissionMode()` - 获取下一个权限模式

### 常量
- `PERMISSION_MODE_CONFIG` - 模式配置对象
- `READONLY_COMMANDS` - 只读命令数组
- `COMMAND_ALLOWLIST` - 命令 Flag 白名单
- `ACCEPT_EDITS_ALLOWED_COMMANDS` - Accept Edits 允许命令

### 辅助函数
- `getDenyRuleForTool()` - 获取 Deny 规则
- `getAskRuleForTool()` - 获取 Ask 规则
- `toolAlwaysAllowedRule()` - 获取 Allow 规则
- `isCommandReadOnly()` - 判断命令是否只读
- `isCommandSafeViaFlagParsing()` - Flag 解析验证

### 类型
- `PermissionMode` - 权限模式类型
- `PermissionModeConfig` - 模式配置类型
