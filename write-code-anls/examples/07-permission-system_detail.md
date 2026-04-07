# 第7课：权限系统的分层设计 - 细纲

## 文件信息
- **原文件**: part02-architecture/07-permission-system.md
- **类型**: 架构全景
- **难度**: ★★★☆☆

---

## 一、为什么需要权限系统

### 1.1 生活类比：门禁系统
- **大门保安**（全局权限模式）：决定来访者能否进入
- **楼栋门禁**（项目级权限）：只有住户能进自己的楼
- **房间钥匙**（工具级权限）：每个房间有自己的锁
- **保险箱密码**（敏感操作权限）：最机密的东西额外保护

### 1.2 权限系统层次
```
全局权限模式（default / plan / auto）
    ↓
权限规则集（allow / deny / ask）
    ↓
工具级权限（每个工具的具体检查）
    ↓
文件级权限（哪些目录可以写入）
```

---

## 二、权限模式（Permission Mode）

### 2.1 权限模式对比
| 模式 | 说明 | 适用场景 |
|------|------|---------|
| `default` | 每次操作前都询问用户 | 日常使用，最安全 |
| `plan` | 只允许读取，修改需要批准 | 代码审查 |
| `auto` / `bypassPermissions` | 自动批准符合规则的操作 | 自动化脚本 |

### 2.2 权限规则的数据结构
```typescript
type PermissionBehavior = 'allow' | 'deny' | 'ask'

type PermissionRule = {
  tool: string          // 工具名称或模式
  behavior: PermissionBehavior
  ruleContent?: string  // 可选的细粒度匹配内容
  source: PermissionRuleSource
}

type PermissionRuleSource =
  | 'global-config'     // ~/.claude/settings.json
  | 'project-config'    // 项目目录的 .claude/settings.json
  | 'enterprise'        // 企业管理策略
  | 'session'           // 会话内临时规则
```

---

## 三、权限决策流程

### 3.1 核心决策逻辑
**文件**: `src/utils/permissions/permissions.ts`

```typescript
// 1. 先检查是否有"全面拒绝"规则
export function filterToolsByDenyRules(tools, permissionContext) {
  return tools.filter(tool => !getDenyRuleForTool(permissionContext, tool))
}

// 2. 运行时权限检查（在工具执行前）
// canUseTool 函数 → 决定 allow / deny / ask
```

### 3.2 完整决策流程
```
工具调用请求（例：BashTool('rm file.txt')）
    ↓
步骤1：全面拒绝检查
├── 有 deny 规则 → ❌ 直接拒绝（工具对模型不可见）
└── 没有 → 步骤2：权限模式检查
                ↓
            plan 模式？
            ├── 是 → 是只读操作？
            │       ├── 是 → ✅ 允许
            │       └── 否 → ❓ 询问用户
            └── 否 → 步骤3：匹配权限规则
                            ↓
                        有 allow 规则 → ✅ 允许
                        有 ask 规则 → ❓ 询问用户
                        无匹配规则 → ❓ 询问用户

            auto 模式？
            └── 步骤3：分类器检查
                    ↓
                安全操作 → ✅ 自动允许
                危险操作 → ❓ 询问用户

询问用户
    ↓
用户决定
├── 允许 → 执行工具
├── 拒绝 → 拒绝执行
└── 始终允许 → 保存规则 + 执行
```

---

## 四、权限上下文（ToolPermissionContext）

### 4.1 AppState 中的权限上下文
**文件**: `src/state/AppStateStore.ts`

```typescript
toolPermissionContext: {
  mode: 'default',              // 权限模式
  alwaysAllowRules: {           // 始终允许的规则
    command: allowedTools,
  },
  additionalWorkingDirectories: new Map(),  // 额外的工作目录
}
```

### 4.2 权限规则的来源层次（优先级从高到低）
```
🏢 企业策略 (Enterprise) — 最高优先级，不可覆盖
    ↓
🌐 全局配置 (~/.claude/settings.json) — 用户级设置
    ↓
📁 项目配置 (.claude/settings.json) — 项目级设置
    ↓
💬 会话规则 — 临时规则，会话内有效
```

### 4.3 权限来源示例
```typescript
// 企业策略可能禁止某些命令：
{ tool: 'Bash', behavior: 'deny', ruleContent: 'curl*', source: 'enterprise' }

// 全局配置允许 git 操作：
{ tool: 'Bash', behavior: 'allow', ruleContent: 'git *', source: 'global-config' }

// 项目配置允许运行测试：
{ tool: 'Bash', behavior: 'allow', ruleContent: 'npm test', source: 'project-config' }

// 会话中用户临时允许：
{ tool: 'Bash', behavior: 'allow', ruleContent: 'rm temp*', source: 'session' }
```

---

## 五、权限跟踪：canUseTool 包装

### 5.1 wrappedCanUseTool
**文件**: `src/QueryEngine.ts`

```typescript
const wrappedCanUseTool: CanUseToolFn = async (
  tool, input, toolUseContext, assistantMessage, toolUseID, forceDecision,
) => {
  const result = await canUseTool(
    tool, input, toolUseContext, assistantMessage, toolUseID, forceDecision,
  )

  // 跟踪拒绝情况，用于 SDK 报告
  if (result.behavior !== 'allow') {
    this.permissionDenials.push({
      tool_name: sdkCompatToolName(tool.name),
      tool_use_id: toolUseID,
      tool_input: input,
    })
  }

  return result
}
```

### 5.2 好处
1. **审计追踪**——知道哪些操作被拒绝了
2. **SDK 报告**——外部集成可以看到权限拒绝
3. **不侵入原始逻辑**——装饰器模式，优雅扩展

---

## 六、沙箱机制

### 6.1 沙箱保护
**文件**: `src/utils/permissions/permissions.ts`

```typescript
import { shouldUseSandbox } from '../../tools/BashTool/shouldUseSandbox.js'
import { SandboxManager } from '../sandbox/sandbox-adapter.js'
```

### 6.2 沙箱流程
```
执行命令请求
    ↓
需要沙箱？
├── 是 → 在隔离环境中执行
│       ├── 限制文件系统访问
│       └── 限制网络访问
└── 否 → 直接执行
    ↓
返回结果
```

---

## 七、自动模式的安全机制

### 7.1 拒绝跟踪和回退
**文件**: `src/utils/permissions/permissions.ts`

```typescript
import {
  createDenialTrackingState,
  DENIAL_LIMITS,
  recordDenial,
  recordSuccess,
  shouldFallbackToPrompting,
} from './PermissionResult.js'
```

### 7.2 自动模式安全网
```
自动模式运行
    ↓
分类器评估操作
    ↓
安全操作 → ✅ 自动允许
危险操作 → 自动拒绝
                ↓
            记录拒绝
                ↓
            连续拒绝次数超过限制？
            ├── 是 → 回退到手动模式（开始询问用户）
            └── 否 → 继续自动模式
```

---

## 八、权限在工具执行中的应用

### 8.1 query.ts 中的权限检查
**文件**: `src/query.ts`

```typescript
const toolUpdates = streamingToolExecutor
  ? streamingToolExecutor.getRemainingResults()
  : runTools(toolUseBlocks, assistantMessages, canUseTool, toolUseContext)

for await (const update of toolUpdates) {
  if (update.message) {
    yield update.message

    // 如果 Hook 阻止了继续执行
    if (
      update.message.type === 'attachment' &&
      update.message.attachment.type === 'hook_stopped_continuation'
    ) {
      shouldPreventContinuation = true
    }
  }
}
```

---

## 九、动手练习

### 练习1：权限配置文件
查看本机的 Claude Code 权限配置：
```bash
# 全局配置
cat ~/.claude/settings.json

# 项目配置（如果有）
cat .claude/settings.json
```

### 练习2：权限流程追踪
在 `utils/permissions/permissions.ts` 中找到：
- [ ] `getDenyRuleForTool` 函数——它如何匹配工具名？
- [ ] 权限规则的应用和持久化逻辑
- [ ] `PermissionResult` 的三种类型：allow / deny / ask

### 思考题
1. 为什么企业策略的优先级最高？
2. 如果一个工具同时匹配了 allow 和 deny 规则，应该怎么处理？
3. 自动模式为什么需要"拒绝跟踪"和"回退到手动"机制？

---

## 十、小结

| 层级 | 机制 | 文件 |
|------|------|------|
| 模式层 | default / plan / auto | `PermissionMode.ts` |
| 规则层 | allow / deny / ask 规则 | `permissions.ts` |
| 过滤层 | filterToolsByDenyRules | `tools.ts` |
| 执行层 | canUseTool 运行时检查 | `QueryEngine.ts` |
| 追踪层 | 拒绝记录和回退 | `permissions.ts` |
| 沙箱层 | 隔离执行环境 | `sandbox-adapter.ts` |

### 核心设计原则
- **纵深防御**：多层保护，不依赖单一机制
- **最小权限**：默认拒绝，需要显式授权
- **可审计**：所有权限决策可追踪
- **优雅降级**：自动模式遇到危险时回退到手动

---

## 十一、关联文件

### 11.1 上一章
- [06-query-engine.md](06-query-engine.md) - QueryEngine 查询引擎

### 11.2 下一章
- [08-agent-swarm.md](08-agent-swarm.md) - Agent Swarm 多代理

---

*此细纲由 Claude Code 自动生成*
