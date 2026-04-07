# 图解 Claude Code 完全指南 - 细纲

## 文件信息
- **原文件**: 07-history.md
- **类型**: 第 7 课：History 会话历史 —— 缓冲写入与分级存储
- **难度**: ★★☆☆☆

---

## 一、文档结构概览

### 1.1 学习目标
1. 理解 History 系统的"缓冲区 + 磁盘"双层架构
2. 掌握 JSONL 追加写入模式的优势
3. 学会缓冲写入和延迟刷盘的设计思路
4. 了解大段粘贴内容的哈希外置存储
5. 认识会话隔离、反向读取和撤销机制

### 1.2 章节结构
| 章节 | 主题 | 核心内容 |
|------|------|---------|
| 一、History 系统概览 | 概念入门 | 日记本类比 |
| 二、核心数据结构 | 类型定义 | LogEntry、StoredPastedContent |
| 三、写入流程 | 缓冲+延迟 | addToHistory、flush |
| 四、读取流程 | 反向读取 | makeLogEntryReader |
| 五、撤销机制 | 删除逻辑 | removeLastFromHistory |
| 六、粘贴内容引用 | 哈希存储 | formatPastedTextRef |

---

## 二、关键知识点

### 2.1 存储位置
```
~/.claude/history.jsonl     ← 全局历史文件（所有项目共享）
```

**JSONL 格式**: 每行一条独立的 JSON 记录

### 2.2 LogEntry 数据结构
```typescript
type LogEntry = {
  display: string                           // 显示文本
  pastedContents: Record<number, StoredPastedContent>  // 粘贴内容
  timestamp: number                         // 时间戳
  project: string                           // 所属项目路径
  sessionId?: string                        // 所属会话 ID
}
```

### 2.3 StoredPastedContent 两种存储方式
```typescript
type StoredPastedContent = {
  id: number
  type: 'text' | 'image'
  content?: string      // 小内容直接存（≤1024 字符）
  contentHash?: string  // 大内容存哈希引用
  mediaType?: string
  filename?: string
}
```

**阈值**: `MAX_PASTED_CONTENT_LENGTH = 1024`

### 2.4 写入流程：缓冲 + 延迟刷盘
```typescript
export function addToHistory(command: HistoryEntry | string): void {
  // 跳过测试/验证会话
  if (isEnvTruthy(process.env.CLAUDE_CODE_SKIP_PROMPT_HISTORY)) {
    return
  }
  
  // 注册清理回调
  if (!cleanupRegistered) {
    cleanupRegistered = true
    registerCleanup(async () => {
      if (currentFlushPromise) {
        await currentFlushPromise
      }
      if (pendingEntries.length > 0) {
        await immediateFlushHistory()
      }
    })
  }
  
  void addToPromptHistory(command)  // 非阻塞
}
```

### 2.5 flushPromptHistory 带重试
```typescript
async function flushPromptHistory(retries: number): Promise<void> {
  if (isWriting || pendingEntries.length === 0) return
  if (retries > 5) return  // 最多重试 5 次
  
  isWriting = true
  try {
    await immediateFlushHistory()
  } finally {
    isWriting = false
    if (pendingEntries.length > 0) {
      await sleep(500)  // 避免热循环
      void flushPromptHistory(retries + 1)
    }
  }
}
```

### 2.6 immediateFlushHistory 实际写磁盘
```typescript
async function immediateFlushHistory(): Promise<void> {
  if (pendingEntries.length === 0) return
  
  let release
  try {
    const historyPath = join(getClaudeConfigHomeDir(), 'history.jsonl')
    
    // 确保文件存在
    await writeFile(historyPath, '', { encoding: 'utf8', mode: 0o600, flag: 'a' })
    
    // 获取文件锁（防止多进程并发写入）
    release = await lock(historyPath, {
      stale: 10000,
      retries: { retries: 3, minTimeout: 50 },
    })
    
    // 批量序列化并写入
    const jsonLines = pendingEntries.map(entry => jsonStringify(entry) + '\n')
    pendingEntries = []  // 清空缓冲区
    
    await appendFile(historyPath, jsonLines.join(''), { mode: 0o600 })
  } finally {
    if (release) await release()
  }
}
```

**关键细节**:
| 特性 | 实现 | 为什么 |
|------|------|--------|
| 文件锁 | `lock()` | 多个进程可能同时运行 |
| 追加模式 | `appendFile` | 不读取整个文件，只追加尾部 |
| 权限 `0o600` | 仅所有者可读写 | 历史可能包含敏感信息 |
| 批量写入 | `jsonLines.join('')` | 减少 I/O 次数 |

### 2.7 读取流程：反向读取 + 缓冲优先
```typescript
async function* makeLogEntryReader(): AsyncGenerator<LogEntry> {
  const currentSession = getSessionId()
  
  // 第一步：先从缓冲区读（最新的）
  for (let i = pendingEntries.length - 1; i >= 0; i--) {
    yield pendingEntries[i]!
  }
  
  // 第二步：从磁盘文件反向读取
  const historyPath = join(getClaudeConfigHomeDir(), 'history.jsonl')
  for await (const line of readLinesReverse(historyPath)) {
    try {
      const entry = deserializeLogEntry(line)
      // 跳过已被撤销的条目
      if (entry.sessionId === currentSession && skippedTimestamps.has(entry.timestamp)) {
        continue
      }
      yield entry
    } catch (error) {
      logForDebugging(`Failed to parse history line: ${error}`)
    }
  }
}
```

### 2.8 撤销机制
```typescript
export function removeLastFromHistory(): void {
  if (!lastAddedEntry) return
  const entry = lastAddedEntry
  lastAddedEntry = null
  
  const idx = pendingEntries.lastIndexOf(entry)
  if (idx !== -1) {
    pendingEntries.splice(idx, 1)    // 快速路径：还在缓冲区
  } else {
    skippedTimestamps.add(entry.timestamp)  // 慢速路径：已写入磁盘
  }
}
```

### 2.9 粘贴内容引用
```typescript
export function formatPastedTextRef(id: number, numLines: number): string {
  if (numLines === 0) return `[Pasted text #${id}]`
  return `[Pasted text #${id} +${numLines} lines]`
}

export function expandPastedTextRefs(
  input: string,
  pastedContents: Record<number, PastedContent>,
): string {
  // 从后往前替换，保持前面的偏移量正确
}
```

---

## 三、关联文件索引

### 3.1 前置阅读
- [06-memory-types.md](06-memory-types.md) - 四种记忆分类法

### 3.2 后续课程
- [08-migrations.md](08-migrations.md) - Migrations 版本迁移

### 3.3 核心源码文件
| 文件路径 | 职责 | 行数 |
|---------|------|------|
| `history.ts` | 命令历史系统 | 465 行 |

---

## 四、源码对应关系

### 4.1 核心类型
| 名称 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `LogEntry` | type | `history.ts` | 磁盘上的记录 |
| `StoredPastedContent` | type | `history.ts` | 粘贴内容存储 |
| `HistoryEntry` | type | `history.ts` | 历史条目 |
| `PastedContent` | type | `history.ts` | 粘贴内容 |

### 4.2 核心函数
| 函数名 | 位置 | 功能 |
|--------|------|------|
| `addToHistory()` | `history.ts` | 添加到历史 |
| `addToPromptHistory()` | `history.ts` | 处理粘贴内容 |
| `flushPromptHistory()` | `history.ts` | 带重试的刷盘 |
| `immediateFlushHistory()` | `history.ts` | 实际写磁盘 |
| `makeLogEntryReader()` | `history.ts` | 生成读取器 |
| `getHistory()` | `history.ts` | 获取历史 |
| `removeLastFromHistory()` | `history.ts` | 撤销最后一条 |
| `formatPastedTextRef()` | `history.ts` | 格式化粘贴引用 |
| `expandPastedTextRefs()` | `history.ts` | 展开粘贴引用 |

### 4.3 常量
| 常量名 | 值 | 说明 |
|--------|-----|------|
| `MAX_PASTED_CONTENT_LENGTH` | 1024 | 小内容阈值 |
| `MAX_HISTORY_ITEMS` | 100 | 最多返回条数 |

---

## 五、本课小结

| 概念 | 解释 |
|------|------|
| JSONL 格式 | 每行一条 JSON——追加友好、反向读取高效 |
| 双层存储 | 内存缓冲区 + 磁盘文件，缓冲优先读取 |
| 文件锁 | `lock()` 防止多进程并发写入冲突 |
| 会话隔离 | 当前会话的记录排在前面 |
| 粘贴外置 | 大段粘贴内容用哈希引用，存在独立文件中 |
| 撤销机制 | 缓冲区直接删除，已刷盘的加入跳过集合 |
| 异步非阻塞 | 写入不阻塞用户交互，`registerCleanup` 保证退出前刷盘 |

---

*此细纲由 Claude Code 自动生成，用于快速导航和内容概览*
