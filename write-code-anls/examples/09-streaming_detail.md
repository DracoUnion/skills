# 第9课：流式处理 —— 异步生成器与背压控制 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第9课：流式处理 —— 异步生成器与背压控制

### 1.2 二级标题
- 学习目标
- 生活类比：流水线与传送带
- 核心概念一：异步生成器基础
- 核心概念二：Claude Code 的 Query 循环
- 核心概念三：StreamingToolExecutor
- 核心概念四：并发生成器执行器 all()
- 核心概念五：背压控制
- 动手练习
- 本课小结
- 下节预告

### 1.3 三级标题
- 普通函数 vs 生成器函数
- yield vs yield*
- 整体架构
- Query 循环的流式管道
- 关键设计：状态机 + 流式输出
- 问题：等模型说完再执行工具太慢
- 优化流程
- Claude Code 的 StreamingToolExecutor
- 并发安全控制
- 问题：如何同时运行多个异步生成器？
- 工作原理图解
- 关键点：Promise.race
- 什么是背压（Backpressure）？
- 异步生成器的天然背压
- Claude Code 中的背压

---

## 2. 关键知识点

### 2.1 异步生成器基础
- `async function*` 定义异步生成器
- `yield` 吐出一个值
- `yield*` 透传子生成器的所有值
- 可以在 yield 之间做异步操作

### 2.2 yield vs yield*
| 语法 | 行为 |
|------|------|
| `yield 42` | 消费者收到: 42 |
| `yield* otherGen()` | 消费者收到: otherGen 的每一个值 |

### 2.3 Query 循环架构
- 外层 `query()` 函数使用 `yield* queryLoop()`
- `queryLoop()` 内部是 `while(true)` 循环
- 状态机管理：`state` 对象记录迭代状态
- 流式推送：`yield message` 立刻推送给消费者

### 2.4 StreamingToolExecutor
- 模型流式返回 tool_use 块时立刻调用 `addTool()`
- 并发安全标记：`isConcurrencySafe`
- 并发安全的工具可以并行执行
- 非安全的工具需要独占执行

### 2.5 并发生成器执行器 all()
- 使用 `Promise.race` 驱动多个生成器
- 哪个先完成就先处理哪个
- 实现"来一个处理一个"的流式效果
- 不会阻塞——不需要等所有生成器都产出才继续

### 2.6 背压控制
- 异步生成器自带背压机制
- 生产者在 `yield` 后暂停，直到消费者调用 `next()`
- 消费者处理完才触发下一个 `next()`
- 自然地控制速率，内存恒定

---

## 3. 涉及的源码文件路径

### 3.1 核心源码文件
- `query.ts` - Query 循环实现
- `services/tools/StreamingToolExecutor.ts` - 流式工具执行器
- `utils/generators.ts` - 并发生成器执行器

---

## 4. 类名、函数名、接口名

### 4.1 函数
- `query(params: QueryParams)` - Query 主函数
- `queryLoop(params: QueryParams, consumedCommandUuids: string[])` - Query 循环
- `callModel(options: CallModelOptions)` - 调用模型
- `addTool(block: ToolUseBlock, assistantMessage: AssistantMessage)` - 添加工具
- `getRemainingResults()` - 获取剩余结果
- `all<A>(generators: AsyncGenerator<A, void>[], concurrencyCap = Infinity)` - 并发生成器执行器

### 4.2 类
- `StreamingToolExecutor` - 流式工具执行器类

### 4.3 类型/接口
- `QueryParams` - Query 参数
- `State` - Query 循环状态
- `StreamEvent` - 流式事件
- `RequestStartEvent` - 请求开始事件
- `Message` - 消息类型
- `TombstoneMessage` - 墓碑消息
- `ToolUseSummaryMessage` - 工具使用摘要消息
- `Terminal` - 终止原因
- `ToolStatus` - 工具状态（'queued' | 'executing' | 'completed' | 'yielded'）
- `TrackedTool` - 追踪的工具
- `ToolUseBlock` - 工具使用块
- `AssistantMessage` - 助手消息
- `MessageUpdate` - 消息更新

### 4.4 常量
- `concurrencyCap` - 并发上限（默认 Infinity）

---

## 5. 代码片段重点

### 5.1 Query 主函数（query.ts）
```typescript
export async function* query(
  params: QueryParams,
): AsyncGenerator<
  | StreamEvent
  | RequestStartEvent
  | Message
  | TombstoneMessage
  | ToolUseSummaryMessage,
  Terminal
> {
  const consumedCommandUuids: string[] = [];
  const terminal = yield* queryLoop(params, consumedCommandUuids);
  for (const uuid of consumedCommandUuids) {
    notifyCommandLifecycle(uuid, 'completed');
  }
  return terminal;
}
```

### 5.2 Query 循环状态机
```typescript
let state: State = {
  messages: params.messages,
  toolUseContext: params.toolUseContext,
  autoCompactTracking: undefined,
  maxOutputTokensRecoveryCount: 0,
  hasAttemptedReactiveCompact: false,
  turnCount: 1,
  transition: undefined,
};

while (true) {
  // 1. 预处理（压缩、snip 等）
  // 2. 调用模型，流式接收
  for await (const message of deps.callModel({...})) {
    yield message;
    if (message.type === 'assistant') {
      // 检测到工具调用
    }
  }

  // 3. 没有工具调用 → 结束
  if (!needsFollowUp) {
    return { reason: 'completed' };
  }

  // 4. 执行工具，收集结果
  for await (const update of toolUpdates) {
    yield update.message;
  }

  // 5. 更新状态，进入下一轮
  state = { ...nextState };
}
```

### 5.3 StreamingToolExecutor 类
```typescript
type ToolStatus = 'queued' | 'executing' | 'completed' | 'yielded';

type TrackedTool = {
  id: string;
  block: ToolUseBlock;
  status: ToolStatus;
  isConcurrencySafe: boolean;
  promise?: Promise<void>;
  results?: Message[];
  pendingProgress: Message[];
};

export class StreamingToolExecutor {
  private tools: TrackedTool[] = [];

  addTool(block: ToolUseBlock, assistantMessage: AssistantMessage): void {
    // 1. 查找工具定义
    // 2. 判断是否可并发执行
    // 3. 如果可以，立刻开始执行
  }

  async *getRemainingResults(): AsyncGenerator<MessageUpdate> {
    // 等待所有工具执行完毕
    // 按接收顺序 yield 结果
  }
}
```

### 5.4 并发生成器执行器 all()（utils/generators.ts）
```typescript
export async function* all<A>(
  generators: AsyncGenerator<A, void>[],
  concurrencyCap = Infinity,
): AsyncGenerator<A, void> {
  const next = (generator: AsyncGenerator<A, void>) => {
    const promise = generator.next().then(({ done, value }) => ({
      done, value, generator, promise,
    }));
    return promise;
  };

  const waiting = [...generators];
  const promises = new Set<Promise<QueuedGenerator<A>>>();

  while (promises.size < concurrencyCap && waiting.length > 0) {
    promises.add(next(waiting.shift()!));
  }

  while (promises.size > 0) {
    const { done, value, generator, promise } = await Promise.race(promises);
    promises.delete(promise);

    if (!done) {
      promises.add(next(generator));
      if (value !== undefined) {
        yield value;
      }
    } else if (waiting.length > 0) {
      promises.add(next(waiting.shift()!));
    }
  }
}
```

### 5.5 背压控制示例
```typescript
async function* producer() {
  for (let i = 0; i < 1000; i++) {
    console.log(`生产: ${i}`);
    yield i; // 暂停！等待消费者消费
  }
}

async function consumer() {
  for await (const item of producer()) {
    console.log(`消费: ${item}`);
    await heavyProcessing(item); // 慢慢处理
    // 处理完才会触发下一个 next() → producer 才继续
  }
}
```

### 5.6 Query 循环中的背压
```typescript
for await (const message of deps.callModel({...})) {
  // 每收到一个 message：
  // 1. 做一些处理（检测 tool_use 等）
  // 2. yield 给消费者
  yield message;
  // ↑ 消费者处理完才会继续
  // 这自然地控制了速率
}
```
