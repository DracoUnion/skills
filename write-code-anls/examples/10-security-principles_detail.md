# 10-security-principles.md 细纲

## 一、标题层级结构

### 1. 安全设计五原则与实战应用
- 学习目标（5点）
- 生活类比：一座安全的大楼
- 原则一：Fail-Closed（故障时关闭）
  - AST 解析失败 → 询问
  - 分类器出错 → 不自动允许
  - 拒绝次数超限 → 回退到用户询问
  - 变量展开无法验证 → 拒绝自动允许
- 原则二：Defense-in-Depth（纵深防御）
  - 权限检查的防御层次
  - Bypass 模式不是万能的
- 原则三：Least Privilege（最小权限）
  - 模式设计的权限阶梯
  - Default 模式的只读白名单
  - 危险 Allow 规则的自动清理
- 原则四：Separation of Concerns（关注点分离）
  - 权限系统的模块职责
  - 替换一个模块不影响其他
- 原则五：Auditability（可审计性）
  - PermissionDecisionReason 完整追踪
  - 决策日志记录
  - 用户可见的决策链
- 五原则的协同作用
- 全系统源码结构回顾
- 动手练习
- 全课程总结

## 二、关键知识点

1. **Fail-Closed 原则**
   - 不确定时默认拒绝或询问
   - 不是默认允许
   - 体现在 AST 解析、分类器、变量展开等各处

2. **Defense-in-Depth 原则**
   - 不依赖单一防线
   - 五层防御：Deny 规则 → Ask 规则 → 工具检查 → 模式检查 → 安全兜底
   - Bypass 模式下仍有 Deny/工具 deny/安全检查三层

3. **Least Privilege 原则**
   - 默认给予最小权限
   - 权限阶梯：Plan → Default → AcceptEdits → Auto → Bypass
   - 只读白名单最小集
   - 危险规则自动清理

4. **Separation of Concerns 原则**
   - 每个模块只负责一个安全维度
   - 类型定义层 / 规则引擎 / 工具特定安全 / AI 分类器 / 交互层
   - 替换模块不影响其他

5. **Auditability 原则**
   - 每个决策必须可追溯
   - PermissionDecisionReason 十种类型
   - 决策日志记录
   - 用户可见决策链

6. **五原则协同**
   - Fail-Closed → Defense-in-Depth → Least Privilege → Auditability
   - 贯穿整个权限系统

7. **源码结构**
   - types/permissions.ts - 核心类型
   - utils/permissions/ - 权限工具
   - tools/BashTool/ - Bash 安全
   - hooks/toolPermission/ - 交互处理

## 三、源码文件路径

- `src/types/permissions.ts` - 核心类型定义
- `src/utils/permissions/permissions.ts` - 权限检查流水线
- `src/utils/permissions/PermissionMode.ts` - 模式定义
- `src/utils/permissions/PermissionRule.ts` - 规则结构
- `src/utils/permissions/yoloClassifier.ts` - 分类器
- `src/utils/permissions/classifierDecision.ts` - 分类器白名单
- `src/utils/permissions/bypassPermissionsKillswitch.ts` - Bypass 开关
- `src/utils/permissions/dangerousPatterns.ts` - 危险模式
- `src/tools/BashTool/bashPermissions.ts` - Bash 权限
- `src/tools/BashTool/readOnlyValidation.ts` - 只读验证
- `src/hooks/toolPermission/PermissionContext.ts` - 竞争锁
- `src/hooks/toolPermission/handlers/interactiveHandler.ts` - 赛跑调度

## 四、类名、函数名、接口名

### 核心概念
- `Fail-Closed` - 故障时关闭
- `Defense-in-Depth` - 纵深防御
- `Least Privilege` - 最小权限
- `Separation of Concerns` - 关注点分离
- `Auditability` - 可审计性

### 决策原因类型
- `PermissionDecisionReason` - 决策原因
  - `type: 'rule' | 'mode' | 'classifier' | 'safetyCheck' | ...`

### 日志记录
- `logPermissionDecision()` - 记录权限决策
- `logEvent('permission_decision', {...})` - 事件日志
- `logEvent('tengu_auto_mode_decision', {...})` - 分类器决策日志

### 核心函数
- `hasPermissionsToUseTool()` - 权限检查入口
- `createResolveOnce()` - 竞争锁
- `executeAsyncClassifierCheck()` - 分类器检查

### 全课程知识地图
- 第1课：为什么需要权限控制
- 第2-5课：五种权限模式
- 第6-7课：权限检查流水线 + 规则系统
- 第8-9课：Bash AST 分析 + 交互式权限赛跑
- 第10课：五大安全设计原则
