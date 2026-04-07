# 07-permissions.md 细纲

## 一、标题层级结构

### 1. 权限守门人 —— checkPermissions 全流程
- 学习目标（5点）
- 生活类比：机场安检系统
- 权限规则的三种行为
- 权限规则来源与优先级
  - 规则来源层次
  - 规则的收集方式
- hasPermissionsToUseTool 七步流程
  - 步骤 1a：整体工具 Deny 检查
  - 步骤 1b：整体工具 Ask 检查
  - 步骤 1c-1g：工具自身权限检查
  - 步骤 2a：Bypass 模式检查
  - 步骤 2b：Always Allow 规则匹配
  - 步骤 3：最终 Passthrough → Ask 转换
- Auto 模式：AI 分类器
  - 三级快速通道
  - 拒绝追踪与兜底
- 权限规则匹配：工具级 vs 内容级
- 权限模式全览
- ToolPermissionContext 数据结构
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **权限三种行为**
   - `allow`: 直接放行
   - `deny`: 直接拒绝
   - `ask`: 询问用户
   - `passthrough`: 交给上层处理

2. **七步检查流程**
   - 1a: Deny 规则检查
   - 1b: Ask 规则检查
   - 1c: 工具自检
   - 1d: 工具拒绝检查
   - 1e: 用户交互检查
   - 1f: 内容级 Ask 规则
   - 1g: Safety Check（不可绕过）
   - 2a: Bypass 模式
   - 2b: Allow 规则
   - 3: passthrough → ask

3. **规则来源优先级**
   - policySettings > flagSettings > userSettings > projectSettings > localSettings > cliArg > session

4. **Safety Check 不可绕过**
   - `.git/`, `.claude/`, `.vscode/` 等敏感路径
   - 即使 bypassPermissions 模式也要询问

## 三、源码文件路径

- `src/utils/permissions/permissions.ts` - 权限检查核心
- `src/types/permissions.ts` - 权限类型定义
- `src/utils/permissions/PermissionResult.ts` - 权限结果

## 四、类名、函数名、接口名

### 函数
- `hasPermissionsToUseTool()` - 权限检查入口（第 1169-1310 行）
- `hasPermissionsToUseToolInner()` - 内层权限检查
- `getDenyRuleForTool()` - 获取 Deny 规则
- `getAskRuleForTool()` - 获取 Ask 规则
- `toolAlwaysAllowedRule()` - 获取 Allow 规则
- `getAllowRules()` - 获取所有 Allow 规则（第 122-132 行）
- `getDenyRules()` - 获取所有 Deny 规则
- `filterToolsByDenyRules()` - 过滤被禁止的工具

### 类型
- `PermissionBehavior` = 'allow' | 'deny' | 'ask'
- `PermissionDecision` - 权限决策类型
- `PermissionDecisionReason` - 决策原因类型
- `ToolPermissionContext` - 权限上下文（第 123-138 行）
- `PermissionRule` - 权限规则
- `PermissionRuleSource` - 规则来源类型

### 常量
- `PERMISSION_RULE_SOURCES` - 规则来源数组（第 109-114 行）
- `SETTING_SOURCES` - 设置来源

### 决策原因类型
- `{ type: 'rule', rule: PermissionRule }`
- `{ type: 'mode', mode: PermissionMode }`
- `{ type: 'safetyCheck', reason: string }`
- `{ type: 'classifier', classifier: string }`
- `{ type: 'hook', hookName: string }`
