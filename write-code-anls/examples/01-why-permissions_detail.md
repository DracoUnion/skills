# 01-why-permissions.md 细纲

## 一、标题层级结构

### 1. 为什么 AI Agent 需要权限控制？
- 学习目标（5点）
- 生活类比：AI 就像你请来的装修工人
- 源码直击：权限行为的三种结果
  - PermissionBehavior 类型定义
- 五种权限模式：从"全看紧"到"全放开"
  - EXTERNAL_PERMISSION_MODES
  - InternalPermissionMode
- 权限系统整体架构
  - 权限检查流水线图
- 权限决策的完整类型定义
  - PermissionAllowDecision
  - PermissionAskDecision
  - PermissionDenyDecision
- 决策原因：十种不同的判定来源
  - PermissionDecisionReason 类型
- AI Agent 的三类风险
  - 破坏性操作 / 信息泄露 / 连锁反应
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **三种权限行为**
   - `allow`: 直接放行
   - `deny`: 直接拒绝
   - `ask`: 询问用户

2. **五种权限模式**
   - `plan`: 只读模式（最严格）
   - `default`: 默认模式（每次询问）
   - `acceptEdits`: 接受编辑模式
   - `auto`: AI 分类器自动判断
   - `bypassPermissions`: 绕过权限模式（最宽松）

3. **十种决策原因类型**
   - `rule`: 被规则匹配
   - `mode`: 当前模式决定
   - `subcommandResults`: 子命令汇总
   - `hook`: Hook 钩子决定
   - `classifier`: AI 分类器判定
   - `safetyCheck`: 安全检查（不可绕过）
   - `workingDir`: 工作目录限制
   - `asyncAgent`: 异步代理限制
   - `sandboxOverride`: 沙箱覆盖
   - `other`: 其他原因

4. **三类风险**
   - 破坏性操作: rm -rf /, git push --force
   - 信息泄露: cat ~/.ssh/id_rsa, curl 发送敏感数据
   - 连锁反应: 修改 .bashrc 植入后门

5. **安全检查不可绕过**
   - `.git/`, `.claude/`, `.vscode/` 等敏感路径
   - 即使 bypassPermissions 模式也要询问

## 三、源码文件路径

- `src/types/permissions.ts` - 权限类型定义
- `src/utils/permissions/permissions.ts` - 权限检查核心

## 四、类名、函数名、接口名

### 类型定义
- `PermissionBehavior` = 'allow' | 'deny' | 'ask'
- `ExternalPermissionMode` - 外部权限模式
- `InternalPermissionMode` - 内部权限模式（含 auto/bubble）
- `PermissionAllowDecision` - 允许决策
- `PermissionAskDecision` - 询问决策
- `PermissionDenyDecision` - 拒绝决策
- `PermissionDecisionReason` - 决策原因类型

### 常量
- `EXTERNAL_PERMISSION_MODES` - 外部权限模式数组

### 决策原因类型
- `{ type: 'rule'; rule: PermissionRule }`
- `{ type: 'mode'; mode: PermissionMode }`
- `{ type: 'safetyCheck'; reason: string }`
- `{ type: 'classifier'; classifier: string }`
- `{ type: 'hook'; hookName: string }`
