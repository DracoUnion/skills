# 第6课：QueryEngine 查询引擎核心原理 - 细纲

## 文件信息
- **原文件**: part02-architecture/06-query-engine.md
- **类型**: 架构全景
- **难度**: ★★★★☆

---

## 一、QueryEngine 的角色

### 1.1 生活类比：指挥家
QueryEngine 是 Claude Code 的"指挥家"：
- 不演奏任何乐器（不执行具体工具）
- 决定**何时谁演奏什么**（调度消息和工具）
- 追踪**整首曲子的进度**（管理对话状态）
- 处理**意外情况**（错误恢复、超限处理）

### 1.2 核心职责
| 职责 | 说明 |
|------|------|
| 接收用户输入 | 处理用户消息和斜杠命令 |
| 构建系统提示 | 组合工具定义、上下文信息 |
| 调用 AI 模型 | 与 Claude API 通信 |
| 执行工具调用 | 调度各种工具执行 |
| 管理对话历史 | 维护消息列表 |
| 处理错误和恢复 | 超限重试、模型降级 |
| 追踪使用量和成本 | Token 统计、预算控制 |

---

## 二、QueryEngine 类结构

### 2.1 类定义
**文件**: `src/QueryEngine.ts`

```typescript
export class QueryEngine {
  private config: QueryEngineConfig
  private mutableMessages: Message[]
  private abortController: AbortController
  private permissionDenials: SDKPermissionDenial[]
  private totalUsage: NonNullableUsage
  private hasHandledOrphanedPermission = false
  private readFileState: FileStateCache
  private discoveredSkillNames = new Set<string>()

  constructor(config: QueryEngineConfig) {
    this.config = config
    this.mutableMessages = config.initialMessages ?? []
    this.abortController = config.abortController ?? createAbortController()
    this.permissionDenials = []
    this.readFileState = config.readFileCache
    this.totalUsage = EMPTY_USAGE
  }

  // 核心方法：提交消息并获取流式响应
  async *submitMessage(
    prompt: string | ContentBlockParam[],
    options?: { uuid?: string; isMeta?: boolean },
  ): AsyncGenerator<SDKMessage, void, unknown> {
    // ...1000+ 行的核心逻辑
  }

  interrupt(): void { this.abortController.abort() }
  getMessages(): readonly Message[] { return this.mutableMessages }
  getSessionId(): string { return getSessionId() }
  setModel(model: string): void { this.config.userSpecifiedModel = model }
}
```

### 2.2 关键属性解读
| 属性 | 用途 | 类比 |
|------|------|------|
| `mutableMessages` | 对话历史 | 聊天记录 |
| `abortController` | 中断控制 | 紧急停止按钮 |
| `permissionDenials` | 权限拒绝记录 | 安全日志 |
| `totalUsage` | API 使用量统计 | 账单 |
| `readFileState` | 文件读取缓存 | 记忆库 |

---

## 三、submitMessage：一次查询的完整旅程

### 3.1 流程图
```
用户 → submitMessage("帮我读取文件")
    ↓
fetchSystemPromptParts() → 系统提示 + 用户上下文
    ↓
processUserInput() → 处理后的消息
    ↓
query({ messages, systemPrompt, tools... })
    ↓
循环：
├── 调用 Claude API → 流式响应
├── 执行工具调用 → BashTool, FileReadTool...
└── yield 结果
    ↓
返回最终结果
```

### 3.2 submitMessage 关键步骤
```typescript
async *submitMessage(prompt, options) {
  // 步骤1：初始化
  setCwd(cwd)
  const startTime = Date.now()

  // 步骤2：获取系统提示
  const { defaultSystemPrompt, userContext, systemContext } =
    await fetchSystemPromptParts({ tools, mainLoopModel, mcpClients })

  // 步骤3：处理用户输入（斜杠命令等）
  const { messages, shouldQuery, allowedTools } =
    await processUserInput({ input: prompt, mode: 'prompt' })

  this.mutableMessages.push(...messages)

  // 步骤4：如果不需要查询（如 /help），直接返回
  if (!shouldQuery) {
    yield { type: 'result', subtype: 'success', result: resultText }
    return
  }

  // 步骤5：进入查询循环
  for await (const message of query({
    messages, systemPrompt, userContext, canUseTool, toolUseContext
  })) {
    // 处理每个流式消息...
    switch (message.type) {
      case 'assistant':
        this.mutableMessages.push(message)
        yield* normalizeMessage(message)
        break
      case 'user':
        this.mutableMessages.push(message)
        yield* normalizeMessage(message)
        break
    }
  }

  // 步骤6：返回最终结果
  yield { type: 'result', subtype: 'success', result: textResult }
}
```

---

## 四、query.ts：查询循环的核心

### 4.1 while(true) 循环
**文件**: `src/query.ts`

```typescript
export async function* query(params: QueryParams) {
  let state: State = {
    messages: params.messages,
    toolUseContext: params.toolUseContext,
    turnCount: 1,
    // ...更多状态
  }

  while (true) {
    const { messages, toolUseContext, turnCount } = state

    // 1️⃣ 预处理：微压缩、自动压缩
    messagesForQuery = await deps.microcompact(messagesForQuery)
    const { compactionResult } = await deps.autocompact(messagesForQuery)

    // 2️⃣ 调用模型 API
    for await (const message of deps.callModel({
      messages, systemPrompt, tools, signal
    })) {
      yield message  // 流式输出
      if (message.type === 'assistant') {
        assistantMessages.push(message)
        if (hasToolUse) needsFollowUp = true
      }
    }

    // 3️⃣ 如果没有工具调用，结束
    if (!needsFollowUp) {
      return { reason: 'completed' }
    }

    // 4️⃣ 执行工具调用
    for await (const update of runTools(toolUseBlocks)) {
      yield update.message
      toolResults.push(update.message)
    }

    // 5️⃣ 检查终止条件
    if (maxTurns && turnCount + 1 > maxTurns) {
      return { reason: 'max_turns' }
    }

    // 6️⃣ 继续下一轮
    state = {
      messages: [...messagesForQuery, ...assistantMessages, ...toolResults],
      turnCount: turnCount + 1,
    }
  }
}
```

### 4.2 查询循环图解
```
开始新一轮
    ↓
预处理（微压缩 + 自动压缩）
    ↓
调用 Claude API（流式响应）
    ↓
有工具调用？
├── 否 → 完成 ✅
└── 是 → 执行工具（BashTool, FileReadTool...）
            ↓
        达到限制？（maxTurns / maxBudget）
        ├── 是 → 完成
        └── 否 → 准备下一轮 → 继续循环
```

---

## 五、流式工具执行：StreamingToolExecutor

### 5.1 流式执行原理
**文件**: `src/query.ts`

```typescript
const useStreamingToolExecution = config.gates.streamingToolExecution
let streamingToolExecutor = useStreamingToolExecution
  ? new StreamingToolExecutor(
      toolUseContext.options.tools,
      canUseTool,
      toolUseContext,
    )
  : null

// 在流式接收中，工具调用一出现就开始执行
if (streamingToolExecutor) {
  for (const toolBlock of msgToolUseBlocks) {
    streamingToolExecutor.addTool(toolBlock, message)
  }
}
```

### 5.2 流式执行流程
```
Claude API → 文本块 "让我读取文件..."
    ↓
Claude API → tool_use: FileRead(path)
    ↓
StreamingToolExecutor.addTool(FileRead) 🚀 立即开始
    ↓
Claude API → 文本块 "...然后搜索..."
    ↓
Claude API → tool_use: Grep(pattern)
    ↓
StreamingToolExecutor.addTool(Grep) 🚀 并行执行
    ↓
FileRead 完成 ✅
Grep 完成 ✅
    ↓
收集所有结果
```

**类比**: 厨师边看菜谱边做菜——不是读完整本菜谱才开始，而是看到"先烧水"就立刻去烧水。

---

## 六、自动压缩机制

### 6.1 自动压缩触发
**文件**: `src/query.ts`

```typescript
const { compactionResult } = await deps.autocompact(
  messagesForQuery,
  toolUseContext,
  { systemPrompt, userContext, systemContext },
  querySource,
  tracking,
  snipTokensFreed,
)

if (compactionResult) {
  const postCompactMessages = buildPostCompactMessages(compactionResult)
  for (const message of postCompactMessages) {
    yield message
  }
  messagesForQuery = postCompactMessages
}
```

### 6.2 压缩流程
```
长对话（100+ 条消息）
    ↓
超过 Token 阈值？
├── 否 → 继续对话
└── 是 → 压缩引擎（生成摘要）
            ↓
        压缩后（摘要 + 最近消息）
            ↓
        继续对话
```

---

## 七、错误恢复机制

### 7.1 max_output_tokens 恢复
**文件**: `src/query.ts`

```typescript
if (isWithheldMaxOutputTokens(lastMessage)) {
  if (maxOutputTokensRecoveryCount < MAX_OUTPUT_TOKENS_RECOVERY_LIMIT) {
    const recoveryMessage = createUserMessage({
      content:
        'Output token limit hit. Resume directly — no apology, no recap.',
      isMeta: true,
    })
    state = {
      messages: [...messagesForQuery, ...assistantMessages, recoveryMessage],
      maxOutputTokensRecoveryCount: maxOutputTokensRecoveryCount + 1,
    }
    continue  // 继续 while(true) 循环
  }
}
```

### 7.2 错误恢复策略
| 错误类型 | 恢复策略 |
|----------|----------|
| max_output_tokens | 注入恢复消息，最多重试 3 次 |
| prompt_too_long | 尝试上下文折叠、反应式压缩 |
| model_fallback | 切换到备用模型，通知用户 |

---

## 八、ask() 便捷包装

### 8.1 ask 函数
**文件**: `src/QueryEngine.ts`

```typescript
export async function* ask({
  prompt, cwd, tools, canUseTool, mutableMessages, ...config
}) {
  const engine = new QueryEngine({
    cwd, tools, commands, mcpClients,
    canUseTool, getAppState, setAppState,
    initialMessages: mutableMessages,
    readFileCache: cloneFileStateCache(getReadFileCache()),
  })

  try {
    yield* engine.submitMessage(prompt, { uuid: promptUuid })
  } finally {
    setReadFileCache(engine.getReadFileState())
  }
}
```

### 8.2 QueryEngine vs ask()
| 特性 | QueryEngine | ask() |
|------|------------|-------|
| 生命周期 | 长期存在，多轮对话 | 单次查询 |
| 状态管理 | 自己管理状态 | 自动创建和清理 |
| 适用场景 | SDK/交互模式 | 非交互/一次性 |

---

## 九、动手练习

### 练习1：追踪一次查询
阅读 `QueryEngine.ts` 的 `submitMessage` 方法，画出：
1. 从 `prompt` 参数开始
2. 经过哪些处理步骤
3. 在哪里调用 `query()`
4. 最终 yield 什么类型的结果

### 练习2：理解查询循环
在 `query.ts` 中找到 `while (true)` 循环，列出所有可能导致循环退出的条件：
- [ ] `return { reason: 'completed' }` — 正常完成
- [ ] `return { reason: 'max_turns' }` — 超过最大轮数
- [ ] 还有哪些？

### 思考题
1. 为什么 `submitMessage` 用 `async *`（AsyncGenerator）而不是普通 `async`？
2. 流式工具执行相比等待模型输出完成再执行，有什么优势和风险？
3. 自动压缩时如何确保不丢失重要的对话上下文？

---

## 十、小结

| 概念 | 文件 | 职责 |
|------|------|------|
| QueryEngine | `QueryEngine.ts` | 查询生命周期管理 |
| submitMessage() | `QueryEngine.ts` | 单轮对话的完整处理 |
| query() | `query.ts` | 核心查询循环（while true） |
| StreamingToolExecutor | `query.ts` | 流式工具执行 |
| autocompact | `query.ts` | 自动压缩长对话 |
| ask() | `QueryEngine.ts` | 一次性查询的便捷包装 |

---

## 十一、关联文件

### 11.1 上一章
- [05-tool-system-architecture.md](05-tool-system-architecture.md) - 工具系统架构

### 11.2 下一章
- [07-permission-system.md](07-permission-system.md) - 权限系统

---

*此细纲由 Claude Code 自动生成*
