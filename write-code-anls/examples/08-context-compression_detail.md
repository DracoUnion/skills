# 图解 Claude Code 完全指南 - 细纲

## 文件信息
- **原文件**: 08-context-compression.md
- **类型**: 第 8 课：上下文压缩 —— 三层递进算法详解
- **难度**: ★★★☆☆

---

## 一、文档结构概览

### 1.1 学习目标
1. 理解上下文压缩的必要性（Token 窗口限制）
2. 掌握三层压缩体系：微压缩 → 自动压缩 → 完整压缩
3. 学会自动压缩的阈值计算和触发逻辑
4. 了解压缩后的上下文恢复（文件重建、计划保留、技能注入）

### 1.2 章节结构
| 章节 | 主题 | 核心内容 |
|------|------|---------|
| 一、"笔记本空间"的比喻 | 概念入门 | 三层压缩类比 |
| 二、压缩阈值计算 | 核心算法 | 有效窗口、触发点 |
| 三、第一层：微压缩 | 压缩策略 | 清理旧工具结果 |
| 四、第二层：自动压缩 | 压缩策略 | AI 生成摘要 |
| 五、第三层：完整压缩 | 压缩策略 | 用户触发压缩 |
| 六、Prompt-Too-Long 恢复 | 容错设计 | 递归裁剪 |

---

## 二、关键知识点

### 2.1 三层压缩类比
| 策略 | 对应压缩层 | 做法 |
|------|-----------|------|
| 擦掉旧的草稿 | 微压缩 (MicroCompact) | 清理旧工具结果 |
| 把前面的内容缩写成摘要 | 自动压缩 (AutoCompact) | 用 AI 生成对话摘要 |
| 手动整理，保留关键笔记 | 完整压缩 (Manual Compact) | 用户主动触发 /compact |

### 2.2 有效上下文窗口
```typescript
// services/compact/autoCompact.ts
export function getEffectiveContextWindowSize(model: string): number {
  const reservedTokensForSummary = Math.min(
    getMaxOutputTokensForModel(model),
    20_000,  // 摘要最多 20K tokens
  )
  let contextWindow = getContextWindowForModel(model)

  // 支持自定义窗口大小
  const autoCompactWindow = process.env.CLAUDE_CODE_AUTO_COMPACT_WINDOW
  if (autoCompactWindow) {
    contextWindow = Math.min(contextWindow, parseInt(autoCompactWindow))
  }

  return contextWindow - reservedTokensForSummary
}
```

### 2.3 自动压缩触发点
```typescript
const AUTOCOMPACT_BUFFER_TOKENS = 13_000

export function getAutoCompactThreshold(model: string): number {
  return getEffectiveContextWindowSize(model) - AUTOCOMPACT_BUFFER_TOKENS
}
```

### 2.4 第一层：微压缩 (MicroCompact)
```typescript
// services/compact/microCompact.ts
const COMPACTABLE_TOOLS = new Set([
  'Read',        // 文件读取结果
  'Bash',        // Shell 命令输出
  'Grep',        // 搜索结果
  'Glob',        // 文件匹配结果
  'WebSearch',   // 网页搜索结果
  'WebFetch',    // 网页抓取结果
  'Edit',        // 编辑确认
  'Write',       // 写入确认
])

// 清理消息：[Old tool result content cleared]
const TIME_BASED_MC_CLEARED_MESSAGE = '[Old tool result content cleared]'
```

**原理**：对话中最老的工具调用结果通常不再需要。例如，30 分钟前读取的文件内容已经过时了，可以安全地用一个占位符替代。

### 2.5 第二层：自动压缩 (AutoCompact)

#### 触发条件
```typescript
export async function shouldAutoCompact(
  messages: Message[],
  model: string,
  querySource?: QuerySource,
): Promise<boolean> {
  // 递归保护：压缩/记忆提取不触发自身的压缩
  if (querySource === 'session_memory' || querySource === 'compact') {
    return false
  }

  if (!isAutoCompactEnabled()) return false

  const tokenCount = tokenCountWithEstimation(messages)
  const threshold = getAutoCompactThreshold(model)

  return tokenCount >= threshold
}
```

#### 熔断器机制
```typescript
const MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3

// 连续失败 3 次后停止尝试
if (tracking?.consecutiveFailures >= MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES) {
  return { wasCompacted: false }
}
```

### 2.6 第三层：完整压缩 (Full Compact)

#### 压缩提示词
```typescript
// services/compact/prompt.ts
const BASE_COMPACT_PROMPT = `Your task is to create a detailed summary of the conversation so far...

Your summary should include:
1. Primary Request and Intent
2. Key Technical Concepts
3. Files and Code Sections
4. Errors and fixes
5. All user messages
6. Pending Tasks
7. Current Work
8. Optional Next Step
`
```

#### 压缩后的上下文恢复预算
```typescript
// 文件恢复的预算限制
export const POST_COMPACT_MAX_FILES_TO_RESTORE = 5
export const POST_COMPACT_TOKEN_BUDGET = 50_000
export const POST_COMPACT_MAX_TOKENS_PER_FILE = 5_000
export const POST_COMPACT_MAX_TOKENS_PER_SKILL = 5_000
export const POST_COMPACT_SKILLS_TOKEN_BUDGET = 25_000
```

### 2.7 Prompt-Too-Long 的自动恢复
```typescript
export function truncateHeadForPTLRetry(
  messages: Message[],
  ptlResponse: AssistantMessage,
): Message[] | null {
  const groups = groupMessagesByApiRound(messages)
  if (groups.length < 2) return null

  // 解析需要裁剪的 Token 数
  const tokenGap = getPromptTooLongTokenGap(ptlResponse)

  let dropCount: number
  if (tokenGap !== undefined) {
    // 精确裁剪：删除足够覆盖差值的最老消息组
    let acc = 0
    dropCount = 0
    for (const g of groups) {
      acc += roughTokenCountEstimationForMessages(g)
      dropCount++
      if (acc >= tokenGap) break
    }
  } else {
    // 模糊裁剪：删除 20% 的消息组
    dropCount = Math.max(1, Math.floor(groups.length * 0.2))
  }

  return groups.slice(dropCount).flat()
}
```

---

## 三、关联文件索引

### 3.1 前置阅读
- [07-oauth-authentication.md](07-oauth-authentication.md) - OAuth 认证

### 3.2 后续课程
- [09-feature-flags-telemetry.md](09-feature-flags-telemetry.md) - 特性标志与遥测

### 3.3 核心源码文件
| 文件路径 | 职责 | 行数 |
|---------|------|------|
| `services/compact/autoCompact.ts` | 自动压缩逻辑 | ~200 行 |
| `services/compact/microCompact.ts` | 微压缩逻辑 | ~100 行 |
| `services/compact/prompt.ts` | 压缩提示词 | ~100 行 |

---

## 四、源码对应关系

### 4.1 核心函数
| 函数名 | 位置 | 功能 |
|--------|------|------|
| `getEffectiveContextWindowSize()` | `services/compact/autoCompact.ts` | 获取有效窗口大小 |
| `getAutoCompactThreshold()` | `services/compact/autoCompact.ts` | 获取自动压缩阈值 |
| `shouldAutoCompact()` | `services/compact/autoCompact.ts` | 判断是否应自动压缩 |
| `calculateTokenWarningState()` | `services/compact/autoCompact.ts` | 计算 Token 警告状态 |
| `stripImagesFromMessages()` | `services/compact/prompt.ts` | 剥离图片 |
| `truncateHeadForPTLRetry()` | `services/compact/autoCompact.ts` | PTL 自动恢复 |

### 4.2 核心常量
| 常量名 | 值 | 说明 |
|--------|-----|------|
| `AUTOCOMPACT_BUFFER_TOKENS` | 13_000 | 自动压缩缓冲 Token 数 |
| `MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES` | 3 | 最大连续失败次数 |
| `POST_COMPACT_MAX_FILES_TO_RESTORE` | 5 | 压缩后恢复文件数上限 |
| `POST_COMPACT_TOKEN_BUDGET` | 50_000 | 压缩后 Token 预算 |
| `POST_COMPACT_MAX_TOKENS_PER_FILE` | 5_000 | 每文件最大 Token 数 |

---

## 五、本课小结

| 概念 | 解释 |
|------|------|
| 三层压缩 | 微压缩 → 自动压缩 → 完整压缩 |
| 有效窗口 | 模型窗口 - 摘要预留（最多 20K） |
| 自动压缩阈值 | 有效窗口 - 13K 缓冲 |
| 微压缩 | 清理旧工具结果，最轻量 |
| 自动压缩 | Token 达到阈值时自动触发，生成 AI 摘要 |
| 完整压缩 | 用户主动触发或作为自动压缩的后备 |
| 熔断器 | 连续 3 次失败后停止尝试 |
| PTL 恢复 | 压缩请求本身超长时自动裁剪 |

---

*此细纲由 Claude Code 自动生成，用于快速导航和内容概览*
