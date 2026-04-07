# 06-permission-pipeline.md 细纲

## 一、标题层级结构

### 1. 权限检查完整流水线源码解析
- 学习目标（5点）
- 生活类比：机场登机的完整流程
- 完整流水线架构
  - 内层 10 步检查 + 外层模式变换
- 逐步源码解析
  - Step 1a-1b: 规则检查
  - Step 1c-1d: 工具自检
  - Step 1e-1g: 特殊情况处理
  - Step 2a-2b: 模式和规则放行
  - Step 3: passthrough → ask 转换
- 实战追踪：npm install 在 Default 模式下
- 权限建议（Suggestions）的生成
- 外层函数的模式变换
- 完整流水线总览表
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **权限检查流水线 10 步**
   - Step 1a: 整个工具 Deny 规则检查
   - Step 1b: 整个工具 Ask 规则检查
   - Step 1c: 工具自检 checkPermissions
   - Step 1d: 工具自检结果为 deny
   - Step 1e: 需要用户交互
   - Step 1f: 内容级 Ask 规则
   - Step 1g: 安全检查（safetyCheck）
   - Step 2a: Bypass 模式检查
   - Step 2b: 整个工具 Allow 规则
   - Step 3: passthrough → ask 转换

2. **短路机制**
   - 任何步骤返回明确结果就终止
   - Deny 规则最高优先级

3. **passthrough 行为**
   - 工具说"我不确定"，交给上层决定
   - Default 模式下转为 ask

4. **外层模式变换**
   - dontAsk 模式: ask → deny
   - Auto 模式: 运行分类器
   - 无头模式: 运行 Hooks 或 auto-deny

5. **权限建议系统**
   - ask 结果附带 suggestions
   - 用户可一键添加 allow 规则
   - 保存到 localSettings

6. **双层架构**
   - 内层: hasPermissionsToUseToolInner - 处理规则/工具/模式
   - 外层: hasPermissionsToUseTool - 处理 dontAsk/auto/无头

## 三、源码文件路径

- `src/utils/permissions/permissions.ts` - 权限检查流水线

## 四、类名、函数名、接口名

### 核心函数
- `hasPermissionsToUseTool()` - 权限检查入口（外层）
- `hasPermissionsToUseToolInner()` - 内层权限检查

### 辅助函数
- `getDenyRuleForTool()` - 获取 Deny 规则
- `getAskRuleForTool()` - 获取 Ask 规则
- `toolAlwaysAllowedRule()` - 获取 Allow 规则
- `getUpdatedInputOrFallback()` - 获取更新后的输入
- `createPermissionRequestMessage()` - 创建权限请求消息

### 常量
- `DONT_ASK_REJECT_MESSAGE` - dontAsk 拒绝消息
- `AUTO_REJECT_MESSAGE` - 无头模式自动拒绝消息

### 类型
- `PermissionDecision` - 权限决策类型
- `ToolPermissionContext` - 工具权限上下文
- `CanUseToolFn` - 工具权限检查函数类型
