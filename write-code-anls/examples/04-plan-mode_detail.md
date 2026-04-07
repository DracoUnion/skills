# 04-plan-mode.md 细纲

## 一、标题层级结构

### 1. Plan 模式——只读规划的设计思路
- 学习目标（5点）
- 生活类比：建筑蓝图审查
- 源码直击：Plan 模式的配置
  - PAUSE_ICON
  - color: 'planMode'
- Plan 模式的工作原理
- Plan + Bypass 的特殊组合
  - isBypassPermissionsModeAvailable
- Plan 模式与 Auto 模式的交互
- 进入/退出 Plan 模式的工具
  - EnterPlanModeTool
  - ExitPlanModeTool
- prePlanMode：记住回去的路
- Plan 模式的典型使用场景
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **Plan 模式核心理念**
   - 只看不动——让 AI 先规划，用户审查后再执行
   - 暂停图标 ⏸ 提醒用户当前是规划状态

2. **Plan 模式行为**
   - 只读操作：允许（读文件、搜索、分析）
   - 写操作：拒绝（编辑、创建、删除）
   - 命令执行：拒绝（除了只读命令）
   - 规划工具：允许（EnterPlanMode/ExitPlanMode）

3. **Plan + Bypass 特殊组合**
   - 从 Bypass 切换到 Plan 时保留 Bypass 状态
   - `isBypassPermissionsModeAvailable = true`
   - 退出 Plan 后恢复到之前的模式

4. **prePlanMode 状态保存**
   - 保存进入 Plan 前的模式
   - 退出 Plan 时恢复到该模式
   - 避免重新配置 Bypass 的麻烦

5. **与 Auto 模式的交互**
   - Plan 模式的只读限制优先于 Auto 分类器
   - 即使分类器判断安全，Plan 仍拒绝写操作

6. **典型使用场景**
   - 第一步：Plan 模式读取代码库、分析依赖、提出方案
   - 第二步：用户审查方案
   - 第三步：切换到执行模式实施方案

## 三、源码文件路径

- `src/utils/permissions/PermissionMode.ts` - 模式配置
- `src/types/permissions.ts` - ToolPermissionContext 类型
- `src/utils/permissions/permissions.ts` - 权限检查中的 Plan 处理

## 四、类名、函数名、接口名

### 常量
- `PAUSE_ICON` - 暂停图标
- `PERMISSION_MODE_CONFIG.plan` - Plan 模式配置

### 类型
- `ToolPermissionContext` - 权限上下文
  - `mode: PermissionMode`
  - `prePlanMode?: PermissionMode`
  - `isBypassPermissionsModeAvailable: boolean`

### 工具
- `EnterPlanModeTool` - 进入 Plan 模式工具
- `ExitPlanModeTool` - 退出 Plan 模式工具
- `ENTER_PLAN_MODE_TOOL_NAME` - 工具名常量
- `EXIT_PLAN_MODE_TOOL_NAME` - 工具名常量

### 辅助函数
- `shouldBypassPermissions` - 判断是否应绕过权限
- `createDisabledBypassPermissionsContext()` - 创建禁用的 Bypass 上下文
