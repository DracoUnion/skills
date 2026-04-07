# 图解 Claude Code 完全指南 - 细纲

## 文件信息
- **原文件**: 10-auto-memory-extraction.md
- **类型**: 第 10 课：自动记忆提取与持久化
- **难度**: ★★★★☆

---

## 一、文档结构概览

### 1.1 学习目标
1. 理解自动记忆提取的设计理念和架构
2. 掌握 Forked Agent 模式的工作原理
3. 学会记忆文件的组织方式和安全约束
4. 了解记忆提取的触发时机、频率控制和互斥机制

### 1.2 章节结构
| 章节 | 主题 | 核心内容 |
|------|------|---------|
| 一、"日记本"的比喻 | 概念入门 | 自动记忆提取类比 |
| 二、系统架构概览 | 全局视图 | 架构流程图 |
| 三、初始化与闭包状态 | 实现细节 | initExtractMemories |
| 四、工具权限控制 | 安全设计 | createAutoMemCanUseTool |
| 五、互斥与合并机制 | 并发控制 | 与主代理互斥、请求合并 |
| 六、提取提示词 | 核心实现 | buildExtractAutoOnlyPrompt |
| 七、Forked Agent 模式 | 核心机制 | runForkedAgent |
| 八、写入结果追踪 | 实现细节 | extractWrittenPaths |

---

## 二、关键知识点

### 2.1 自动记忆提取类比
```
聪明的助手每天下班后自动帮你：
1. 回顾今天的对话："老板说了什么重要的事？"
2. 判断是否值得记录："这个项目偏好用 TypeScript，值得记住"
3. 写入日记本：分类归档到不同的主题文件
4. 更新目录：在目录页添加索引
```

### 2.2 初始化与闭包状态
```typescript
// services/extractMemories/extractMemories.ts
export function initExtractMemories(): void {
  // 闭包内的私有状态
  const inFlightExtractions = new Set<Promise<void>>()
  let lastMemoryMessageUuid: string | undefined  // 游标
  let inProgress = false                          // 互斥锁
  let turnsSinceLastExtraction = 0                // 节流计数
  let pendingContext: { ... } | undefined         // 暂存上下文

  // 内部提取逻辑
  async function runExtraction({ context, appendSystemMessage }) {
    // ...
  }

  // 公开入口
  extractor = async (context, appendSystemMessage) => {
    const p = executeExtractMemoriesImpl(context, appendSystemMessage)
    inFlightExtractions.add(p)
    try { await p }
    finally { inFlightExtractions.delete(p) }
  }

  // 等待所有提取完成
  drainer = async (timeoutMs = 60_000) => {
    await Promise.race([
      Promise.all(inFlightExtractions),
      new Promise(r => setTimeout(r, timeoutMs).unref()),
    ])
  }
}
```

### 2.3 工具权限控制
```typescript
export function createAutoMemCanUseTool(memoryDir: string): CanUseToolFn {
  return async (tool, input) => {
    // 允许：读取任意文件
    if (tool.name === 'Read' || tool.name === 'Grep' || tool.name === 'Glob') {
      return { behavior: 'allow', updatedInput: input }
    }

    // 允许：只读的 Shell 命令
    if (tool.name === 'Bash') {
      if (tool.isReadOnly(input)) {
        return { behavior: 'allow', updatedInput: input }
      }
      return deny('Only read-only shell commands are permitted')
    }

    // 允许：只在记忆目录内写入
    if ((tool.name === 'Edit' || tool.name === 'Write') &&
        isAutoMemPath(input.file_path)) {
      return { behavior: 'allow', updatedInput: input }
    }

    // 拒绝：其他所有工具
    return deny(`Only read tools and memory-dir writes are allowed`)
  }
}
```

允许的工具：Read（任意文件）、Grep（任意搜索）、Bash（只读命令）、Write/Edit（仅记忆目录）
禁止的工具：Agent、MCP、Bash（写入命令）、Write（其他目录）

### 2.4 与主代理的互斥
```typescript
function hasMemoryWritesSince(messages, sinceUuid): boolean {
  // 如果主代理已经写入了记忆文件
  // → 跳过后台提取，推进游标
  for (const message of messages) {
    for (const block of message.content) {
      const filePath = getWrittenFilePath(block)
      if (filePath && isAutoMemPath(filePath)) {
        return true  // 主代理已处理，后台不重复
      }
    }
  }
  return false
}
```

### 2.5 提取提示词结构
```typescript
// services/extractMemories/prompts.ts
export function buildExtractAutoOnlyPrompt(
  newMessageCount: number,
  existingMemories: string,
): string {
  return [
    // 角色定义
    `You are now acting as the memory extraction subagent.`,
    `Analyze the most recent ~${newMessageCount} messages above.`,

    // 工具限制
    `Available tools: Read, Grep, Glob, read-only Bash, Edit/Write for memory directory only.`,

    // 效率指导
    `You have a limited turn budget.`,
    `Turn 1: issue all Read calls in parallel`,
    `Turn 2: issue all Write/Edit calls in parallel`,

    // 内容限制
    `You MUST only use content from the last ~${newMessageCount} messages.`,
    `Do not waste turns investigating or verifying that content.`,

    // 已有记忆清单
    `## Existing memory files`,
    existingMemories,
    `Check this list before writing — update rather than creating a duplicate.`,

    // 记忆类型与排除规则...
  ].join('\n')
}
```

### 2.6 记忆文件格式
```markdown
---
type: preference
confidence: high
created: 2026-03-31
---

# 用户偏好：TypeScript 严格模式

用户总是要求在 TypeScript 项目中使用 strict 模式，
包括 noImplicitAny 和 strictNullChecks。
```

### 2.7 Forked Agent 模式
```typescript
const result = await runForkedAgent({
  promptMessages: [createUserMessage({ content: userPrompt })],
  cacheSafeParams,         // 共享主对话的缓存参数
  canUseTool,              // 受限的工具权限
  querySource: 'extract_memories',
  forkLabel: 'extract_memories',
  skipTranscript: true,    // 不记录到会话日志
  maxTurns: 5,             // 最多 5 轮工具调用
})
```

Forked Agent 共享 prompt cache，节省约 80% Token 成本。

### 2.8 写入结果追踪
```typescript
function extractWrittenPaths(agentMessages: Message[]): string[] {
  const paths: string[] = []
  for (const message of agentMessages) {
    if (message.type !== 'assistant') continue
    for (const block of message.content) {
      // 检查 Edit 和 Write 工具的 file_path
      const filePath = getWrittenFilePath(block)
      if (filePath) paths.push(filePath)
    }
  }
  return uniq(paths)  // 去重
}
```

写入的路径会被分类：
- **索引文件** (`MEMORY.md`)：机械更新，不算"记忆"
- **主题文件** (`user_role.md` 等)：真正的记忆

---

## 三、关联文件索引

### 3.1 前置阅读
- [09-feature-flags-telemetry.md](09-feature-flags-telemetry.md) - 特性标志与遥测

### 3.2 课程总结
| 课程 | 核心知识点 |
|------|-----------|
| 第1课 | 服务层整体架构，6大模块概览 |
| 第2课 | API 客户端工厂模式，指数退避重试 |
| 第3课 | 20+ 种错误分类，SSL 链遍历，用户提示设计 |
| 第4课 | MCP 协议概念，8种服务器类型，安全策略 |
| 第5课 | 5种传输方式，In-Process Transport，工具发现 |
| 第6课 | LSP 闭包模式，文件扩展名路由，生命周期通知 |
| 第7课 | OAuth 2.0 + PKCE，授权码流程，令牌刷新 |
| 第8课 | 三层压缩体系，阈值计算，PTL 自动恢复 |
| 第9课 | GrowthBook 特性标志，事件队列，安全类型约束 |
| 第10课 | Forked Agent 记忆提取，工具权限，互斥合并 |

### 3.3 核心源码文件
| 文件路径 | 职责 | 行数 |
|---------|------|------|
| `services/extractMemories/extractMemories.ts` | 记忆提取主逻辑 | ~300 行 |
| `services/extractMemories/prompts.ts` | 提取提示词 | ~100 行 |

---

## 四、源码对应关系

### 4.1 核心函数
| 函数名 | 位置 | 功能 |
|--------|------|------|
| `initExtractMemories()` | `services/extractMemories/extractMemories.ts` | 初始化记忆提取系统 |
| `createAutoMemCanUseTool()` | `services/extractMemories/extractMemories.ts` | 创建工具权限检查函数 |
| `buildExtractAutoOnlyPrompt()` | `services/extractMemories/prompts.ts` | 构建提取提示词 |
| `runForkedAgent()` | 外部 | 运行分叉代理 |
| `extractWrittenPaths()` | `services/extractMemories/extractMemories.ts` | 提取写入的文件路径 |
| `hasMemoryWritesSince()` | `services/extractMemories/extractMemories.ts` | 检查主代理是否已写入记忆 |

### 4.2 核心常量
| 常量名 | 值 | 说明 |
|--------|-----|------|
| `maxTurns` | 5 | Forked Agent 最大轮数 |
| `timeoutMs` | 60_000 | 等待提取完成超时 |

---

## 五、本课小结

| 概念 | 解释 |
|------|------|
| 自动记忆提取 | 后台运行的分叉代理，每轮对话结束时触发 |
| 闭包模式 | 管理状态：游标位置、互斥锁、节流计数 |
| 工具权限 | 只能读取任意文件，写入仅限记忆目录 |
| 互斥机制 | 主代理已写入则后台跳过；并发请求被合并 |
| Forked Agent | 共享 prompt cache，节省约 80% Token 成本 |
| 记忆文件格式 | frontmatter 格式，按主题组织 |

---

*此细纲由 Claude Code 自动生成，用于快速导航和内容概览*
