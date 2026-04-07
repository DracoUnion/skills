# 第8课：Agent Swarm 多代理协作架构 - 细纲

## 文件信息
- **原文件**: part02-architecture/08-agent-swarm.md
- **类型**: 架构全景
- **难度**: ★★★★☆

---

## 一、为什么需要多代理

### 1.1 生活类比：项目经理和团队
- **单人模式**：自己写代码、测试、部署——效率低下
- **团队模式**：分配任务给不同的人，每人负责一块——并行高效

### 1.2 单代理 vs 多代理
```
单代理（串行）
读文件A → 改文件A → 读文件B → 改文件B → 运行测试

多代理（并行）
        主代理（协调）
        ├── Agent 1: 改文件A
        ├── Agent 2: 改文件B
        └── Agent 3: 运行测试
                ↓
            全部完成 ✅
```

---

## 二、AgentTool：子代理的入口

### 2.1 AgentTool 定义
**文件**: `src/tools/AgentTool/AgentTool.tsx`

```typescript
import { buildTool } from 'src/Tool.js'

// 基础输入 Schema
const baseInputSchema = lazySchema(() => z.object({
  description: z.string().describe('A short (3-5 word) description of the task'),
  prompt: z.string().describe('The task for the agent to perform'),
  subagent_type: z.string().optional()
    .describe('The type of specialized agent to use'),
  model: z.enum(['sonnet', 'opus', 'haiku']).optional()
    .describe('Optional model override for this agent'),
  run_in_background: z.boolean().optional()
    .describe('Set to true to run in the background'),
}))

// 完整 Schema（含多代理参数）
const fullInputSchema = lazySchema(() => {
  const multiAgentInputSchema = z.object({
    name: z.string().optional()
      .describe('Name for the spawned agent'),
    team_name: z.string().optional()
      .describe('Team name for spawning'),
    mode: permissionModeSchema().optional()
      .describe('Permission mode for spawned teammate'),
  })
  return baseInputSchema().merge(multiAgentInputSchema).extend({
    isolation: z.enum(['worktree']).optional()
      .describe('Isolation mode for the agent'),
    cwd: z.string().optional()
      .describe('Working directory for the agent'),
  })
})
```

### 2.2 AgentTool 关键特性
| 参数 | 说明 | 示例 |
|------|------|------|
| `prompt` | 子代理要执行的任务 | "修复 login.ts 中的 bug" |
| `subagent_type` | 代理类型 | "generalPurpose", "explore" |
| `model` | 使用的模型 | "sonnet", "haiku" |
| `run_in_background` | 是否后台运行 | true |
| `isolation` | 隔离模式 | "worktree" |
| `name` | 代理名称（可通信） | "frontend-worker" |

---

## 三、代理的生命周期

### 3.1 生命周期流程
```
主代理 → 调用 AgentTool(prompt)
            ↓
        验证输入参数
            ↓
        选择代理类型
            ↓
        创建子代理
            ↓
    前台模式？
    ├── 是 → 发送查询 → 流式响应 → 执行工具调用 → 返回结果 → 返回任务结果
    └── 否 → 注册为后台任务 → 返回任务 ID → 主代理继续其他工作 → 异步执行 → 完成通知
```

---

## 四、代理隔离机制

### 4.1 Worktree 隔离
**文件**: `src/tools/AgentTool/AgentTool.tsx`

```typescript
import { createAgentWorktree, removeAgentWorktree } from '../../utils/worktree.js'

// 创建隔离的 worktree
// 子代理在自己的 worktree 中工作
// 完成后可以合并更改或丢弃
```

### 4.2 Worktree 隔离流程
```
主仓库 (/project)
    ├── git worktree add → Worktree 1 (/tmp/agent-abc/)
    └── git worktree add → Worktree 2 (/tmp/agent-def/)
            ↓
    Agent 1（修改文件不影响主仓库）
    Agent 2（独立的工作副本）
```

### 4.3 工具权限隔离
**文件**: `src/constants/tools.ts`

```typescript
// 子代理不能使用的工具
export const ALL_AGENT_DISALLOWED_TOOLS = new Set([
  TASK_OUTPUT_TOOL_NAME,          // 防止递归
  EXIT_PLAN_MODE_V2_TOOL_NAME,   // 计划模式是主线程概念
  ENTER_PLAN_MODE_TOOL_NAME,
  ASK_USER_QUESTION_TOOL_NAME,   // 子代理不能直接问用户
  TASK_STOP_TOOL_NAME,           // 需要主线程任务状态
])
```

**类比**:
- **Worktree 隔离** → 每个厨师有自己的工作台，互不干扰
- **工具权限隔离** → 实习厨师不能用炸锅（危险工具）

---

## 五、协调器模式（Coordinator Mode）

### 5.1 协调器模式定义
**文件**: `src/coordinator/coordinatorMode.ts`

```typescript
export function isCoordinatorMode(): boolean {
  if (feature('COORDINATOR_MODE')) {
    return isEnvTruthy(process.env.CLAUDE_CODE_COORDINATOR_MODE)
  }
  return false
}

export function getCoordinatorUserContext(
  mcpClients: ReadonlyArray<{ name: string }>,
  scratchpadDir?: string,
): { [k: string]: string } {
  if (!isCoordinatorMode()) return {}

  const workerTools = isEnvTruthy(process.env.CLAUDE_CODE_SIMPLE)
    ? [BASH_TOOL_NAME, FILE_READ_TOOL_NAME, FILE_EDIT_TOOL_NAME]
        .sort().join(', ')
    : Array.from(ASYNC_AGENT_ALLOWED_TOOLS)
        .filter(name => !INTERNAL_WORKER_TOOLS.has(name))
        .sort().join(', ')

  let content = `Workers spawned via the ${AGENT_TOOL_NAME} tool ` +
    `have access to these tools: ${workerTools}`

  return { coordinator_context: content }
}
```

### 5.2 协调器 vs 普通模式
```
普通模式
    主代理
    ├── 自己执行 BashTool
    ├── 自己执行 FileEditTool
    └── 偶尔派子代理

协调器模式
    协调器（主代理）— 只能用 3 个工具
    ├── AgentTool → 派子代理
    ├── TaskStopTool → 停止任务
    └── SendMessageTool → 通信
            ↓
    Worker 1: 改前端
    Worker 2: 改后端
    Worker 3: 写测试
```

### 5.3 协调器允许的工具
**文件**: `src/constants/tools.ts`

```typescript
export const COORDINATOR_MODE_ALLOWED_TOOLS = new Set([
  AGENT_TOOL_NAME,       // 创建子代理
  TASK_STOP_TOOL_NAME,   // 停止任务
  SEND_MESSAGE_TOOL_NAME, // 发送消息
  SYNTHETIC_OUTPUT_TOOL_NAME,
])
```

---

## 六、代理间通信

### 6.1 SendMessageTool
```
协调器
    ├── SendMessage(to: 'frontend', msg: '更新 API 接口') → Worker 1 (name: 'frontend')
    └── SendMessage(to: 'backend', msg: '新接口格式如下...') ← Worker 1 → Worker 2 (name: 'backend')
            ↓
    任务完成通知 ← Worker 2
```

### 6.2 代理名称注册
**文件**: `src/state/AppStateStore.ts`

```typescript
// AppState 中维护代理名称注册表
agentNameRegistry: Map<string, AgentId>
// name → AgentId 映射，用于 SendMessage 路由
```

---

## 七、后台任务管理

### 7.1 后台任务生命周期
```
创建任务（registerAsyncAgent()）
    ↓
运行中（updateAsyncAgentProgress()）
    ↓
完成通知（completeAgentTask()）
    ↓
查看结果（foregroundedTaskId）
```

### 7.2 自动后台机制
**文件**: `src/tools/AgentTool/AgentTool.tsx`

```typescript
import {
  completeAgentTask as completeAsyncAgent,
  createProgressTracker,
  registerAsyncAgent,
  updateAgentProgress as updateAsyncAgentProgress,
  failAgentTask as failAsyncAgent,
} from '../../tasks/LocalAgentTask/LocalAgentTask.js'

// 自动后台：超过 120 秒自动转入后台
function getAutoBackgroundMs(): number {
  if (isEnvTruthy(process.env.CLAUDE_AUTO_BACKGROUND_TASKS) ||
      getFeatureValue_CACHED_MAY_BE_STALE('tengu_auto_background_agents', false)) {
    return 120_000  // 2分钟
  }
  return 0
}
```

---

## 八、团队创建（Team/Swarm）

### 8.1 团队架构
```
Team Leader（teamContext.isLeader = true）
    ├── Teammate 1（tmux pane）→ Git Worktree 1
    ├── Teammate 2（tmux pane）→ Git Worktree 2
    └── Teammate 3（tmux pane）→ Git Worktree 3
```

### 8.2 TeamContext
**文件**: `src/state/AppStateStore.ts`

```typescript
teamContext?: {
  teamName: string
  teamFilePath: string
  leadAgentId: string
  selfAgentId?: string
  selfAgentName?: string
  isLeader?: boolean
  selfAgentColor?: string
  teammates: {
    [teammateId: string]: {
      name: string
      agentType?: string
      color?: string
      tmuxSessionName: string
      tmuxPaneId: string
      cwd: string
      worktreePath?: string
      spawnedAt: number
    }
  }
}
```

---

## 九、多代理系统的设计原则

| 原则 | 说明 |
|------|------|
| 🔒 最小权限 | 子代理只有必要的工具 |
| 🏠 隔离性 | Worktree 保证互不干扰 |
| 📡 通信 | SendMessage 进行协调 |
| 📊 可观测 | 进度跟踪和通知 |
| 🛡️ 安全 | 递归保护，防止无限嵌套 |

---

## 十、动手练习

### 练习1：理解代理类型
阅读 `tools/AgentTool/AgentTool.tsx` 的 `inputSchema`：
- [ ] `subagent_type` 有哪些可能的值？
- [ ] `isolation` 模式有哪些选项？
- [ ] 哪些参数只在多代理模式下可用？

### 练习2：追踪代理工具限制
对比 `ASYNC_AGENT_ALLOWED_TOOLS` 和 `COORDINATOR_MODE_ALLOWED_TOOLS`：
- [ ] 普通子代理能用多少个工具？
- [ ] 协调器能用多少个工具？
- [ ] 为什么协调器不能直接使用 BashTool？

### 思考题
1. 子代理为什么不能使用 `AskUserQuestionTool`？
2. Worktree 隔离和 Docker 容器隔离有什么区别？
3. 如果两个子代理修改了同一个文件，会发生什么？

---

## 十一、小结

| 组件 | 职责 | 文件 |
|------|------|------|
| AgentTool | 创建和管理子代理 | `tools/AgentTool/AgentTool.tsx` |
| CoordinatorMode | 纯指挥模式 | `coordinator/coordinatorMode.ts` |
| SendMessageTool | 代理间通信 | `tools/SendMessageTool/` |
| TeamCreateTool | 团队创建 | `tools/TeamCreateTool/` |
| LocalAgentTask | 后台任务管理 | `tasks/LocalAgentTask/` |
| Worktree | 代码隔离 | `utils/worktree.ts` |

### 关键设计
- **分层权限**：不同类型的代理有不同的工具集
- **隔离执行**：Worktree 保证代码修改不冲突
- **异步协调**：后台任务 + 进度通知
- **递归保护**：限制嵌套深度，防止无限递归

---

## 十二、关联文件

### 12.1 上一章
- [07-permission-system.md](07-permission-system.md) - 权限系统

### 12.2 下一章
- [09-mcp-extension.md](09-mcp-extension.md) - MCP 扩展系统

---

*此细纲由 Claude Code 自动生成*
