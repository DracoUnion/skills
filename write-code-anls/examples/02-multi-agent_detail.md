# 第二课：多代理军团 —— Agent Swarm 协同机制 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第二课：多代理军团 —— Agent Swarm 协同机制

### 1.2 二级标题
- 学习目标
- 一、生活类比：建筑工地的项目经理
- 二、协调者模式的开启
- 三、AgentTool：子代理的诞生
- 四、代理的工具池：Worker 能用什么？
- 五、代理通信协议：task-notification
- 六、四阶段工作流
- 七、runAgent：代理运行引擎
- 八、续写对话：SendMessage
- 九、Scratchpad：跨 Worker 共享知识
- 十、动手练习
- 十一、本课小结
- 下节预告

### 1.3 三级标题
- 协调者的系统提示词
- 3.1 输入参数设计
- 3.2 代理运行流程
- 工具分配示意
- 三种任务状态
- 阶段 1：Research（研究）
- 阶段 2：Synthesis（综合）
- 阶段 3：Implementation（实施）
- 阶段 4：Verification（验证）
- Worktree 隔离
- 何时续写 vs 新建？

---

## 2. 关键知识点

### 2.1 Coordinator 模式
- Coordinator（协调者）负责分工与综合
- Worker（工人）负责执行
- 通过 `isCoordinatorMode()` 判断是否启用
- 环境变量：`CLAUDE_CODE_COORDINATOR_MODE`

### 2.2 AgentTool 输入参数
| 参数 | 类型 | 说明 |
|------|------|------|
| `description` | string | 任务简短描述（3-5词） |
| `prompt` | string | 代理执行的任务 |
| `subagent_type` | string | 专业代理类型（可选） |
| `model` | enum | 模型选择：sonnet/opus/haiku（可选） |
| `run_in_background` | boolean | 是否在后台运行（可选） |
| `isolation` | enum | 隔离模式：worktree/remote（可选） |

### 2.3 工具分配
| 角色 | 可用工具 | 不可用工具 |
|------|----------|------------|
| Coordinator | AgentTool, SendMessage, TaskStop | Bash, FileEdit 等执行工具 |
| Worker | Bash, FileRead, FileEdit, Grep... | AgentTool（不能再派子代理） |

### 2.4 代理通信协议（task-notification）
```xml
<task-notification>
  <task-id>agent-a1b</task-id>
  <status>completed</status>
  <summary>Agent "Investigate auth bug" completed</summary>
  <result>Found null pointer in src/auth/validate.ts:42...</result>
  <usage>
    <total_tokens>15000</total_tokens>
    <tool_uses>8</tool_uses>
    <duration_ms>45000</duration_ms>
  </usage>
</task-notification>
```

### 2.5 四阶段工作流
1. **Research（研究）** - 并行度高，只读操作
2. **Synthesis（综合）** - Coordinator 自己执行，阅读 Worker 汇报
3. **Implementation（实施）** - 并行度低，同一文件区域一次一个 Worker
4. **Verification（验证）** - 新的 Worker 验证，新鲜视角

### 2.6 续写 vs 新建决策
| 场景 | 选择 | 原因 |
|------|------|------|
| 研究后实施同一区域 | 续写 | Worker 已有文件上下文 |
| 修复刚失败的尝试 | 续写 | Worker 知道错误详情 |
| 验证别人写的代码 | 新建 | 需要新鲜视角 |
| 完全不相关的任务 | 新建 | 没有上下文可复用 |
| 之前方向完全错误 | 新建 | 错误上下文会干扰 |

---

## 3. 涉及的源码文件路径

### 3.1 核心源码文件
- `coordinator/coordinatorMode.ts` - 协调者模式定义
- `tools/AgentTool/AgentTool.tsx` - AgentTool 定义
- `tools/AgentTool/runAgent.ts` - 代理运行引擎
- `tools/SendMessageTool/SendMessageTool.ts` - 续写对话工具

### 3.2 相关配置
- 环境变量：`CLAUDE_CODE_COORDINATOR_MODE`
- 环境变量：`CLAUDE_CODE_SIMPLE`

---

## 4. 类名、函数名、接口名

### 4.1 函数
- `isCoordinatorMode()` - 判断是否协调者模式
- `getCoordinatorSystemPrompt()` - 获取协调者系统提示词
- `getCoordinatorUserContext(mcpClients, scratchpadDir)` - 获取协调者用户上下文
- `runAgent(params)` - 运行代理
- `createSubagentContext(...)` - 创建代理上下文
- `buildEffectiveSystemPrompt(...)` - 构建有效系统提示词
- `assembleToolPool(permissionContext, mcpTools)` - 组装工具池
- `recordSidechainTranscript(...)` - 记录旁链对话

### 4.2 常量
- `ASYNC_AGENT_ALLOWED_TOOLS` - 异步代理允许的工具集合
- `INTERNAL_WORKER_TOOLS` - 内部 Worker 工具集合
- `BASH_TOOL_NAME` - Bash 工具名称
- `FILE_READ_TOOL_NAME` - 文件读取工具名称
- `FILE_EDIT_TOOL_NAME` - 文件编辑工具名称

### 4.3 类型/接口
- `AgentToolInput` - AgentTool 输入类型
- `SubagentContext` - 子代理上下文
- `TaskNotification` - 任务通知类型

---

## 5. 代码片段重点

### 5.1 协调者模式判断（coordinatorMode.ts）
```typescript
export function isCoordinatorMode(): boolean {
  if (feature('COORDINATOR_MODE')) {
    return isEnvTruthy(process.env.CLAUDE_CODE_COORDINATOR_MODE);
  }
  return false;
}
```

### 5.2 协调者系统提示词（coordinatorMode.ts）
```typescript
export function getCoordinatorSystemPrompt(): string {
  return `You are Claude Code, an AI assistant that orchestrates
software engineering tasks across multiple workers.

## 1. Your Role
You are a **coordinator**. Your job is to:
- Help the user achieve their goal
- Direct workers to research, implement and verify code changes
- Synthesize results and communicate with the user
- Answer questions directly when possible

## 2. Your Tools
- **Task** - Spawn a new worker
- **SendMessage** - Continue an existing worker
- **TaskStop** - Stop a running worker
...`;
}
```

### 5.3 AgentTool 输入 Schema（AgentTool.tsx）
```typescript
const baseInputSchema = lazySchema(() => z.object({
  description: z.string()
    .describe('A short (3-5 word) description of the task'),
  prompt: z.string()
    .describe('The task for the agent to perform'),
  subagent_type: z.string().optional()
    .describe('The type of specialized agent to use'),
  model: z.enum(['sonnet', 'opus', 'haiku']).optional()
    .describe("Optional model override for this agent"),
  run_in_background: z.boolean().optional()
    .describe('Set to true to run this agent in the background'),
  isolation: z.enum(['worktree', 'remote']).optional()
    .describe('Isolation mode. "worktree" creates a temporary git worktree...'),
}));
```

### 5.4 Worker 工具池过滤（coordinatorMode.ts）
```typescript
export function getCoordinatorUserContext(
  mcpClients: ReadonlyArray<{ name: string }>,
  scratchpadDir?: string,
): { [k: string]: string } {
  const workerTools = isEnvTruthy(process.env.CLAUDE_CODE_SIMPLE)
    ? [BASH_TOOL_NAME, FILE_READ_TOOL_NAME, FILE_EDIT_TOOL_NAME]
        .sort().join(', ')
    : Array.from(ASYNC_AGENT_ALLOWED_TOOLS)
        .filter(name => !INTERNAL_WORKER_TOOLS.has(name))
        .sort().join(', ');

  let content = `Workers spawned via the Task tool have access
    to these tools: ${workerTools}`;

  if (mcpClients.length > 0) {
    content += `\n\nWorkers also have access to MCP tools
      from connected MCP servers: ${serverNames}`;
  }

  return { workerToolsContext: content };
}
```

### 5.5 runAgent 核心流程（runAgent.ts）
```typescript
export async function runAgent(params) {
  // 1. 创建代理上下文
  const subagentContext = createSubagentContext(...);

  // 2. 获取系统提示词
  const systemPrompt = await buildEffectiveSystemPrompt(...);

  // 3. 组装工具池
  const tools = assembleToolPool(permissionContext, mcpTools);

  // 4. 执行查询循环
  const result = await query({
    messages,
    systemPrompt,
    tools,
    model: agentModel,
    // ...
  });

  // 5. 记录结果、清理资源
  await recordSidechainTranscript(...);
}
```

### 5.6 SendMessage 使用示例
```typescript
SendMessage({
  to: "agent-a1b",
  message: "Fix the null pointer in src/auth/validate.ts:42..."
});
```
