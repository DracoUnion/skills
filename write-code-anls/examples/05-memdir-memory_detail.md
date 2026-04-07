# 图解 Claude Code 完全指南 - 细纲

## 文件信息
- **原文件**: 05-memdir-memory.md
- **类型**: 第 5 课：Memdir 记忆魔法 —— 基于文件系统的长期记忆
- **难度**: ★★☆☆☆

---

## 一、文档结构概览

### 1.1 学习目标
1. 理解 Memdir 的设计理念——为什么选择文件系统而非数据库
2. 掌握记忆目录的路径计算和文件组织方式
3. 学会 `MEMORY.md` 入口文件的索引机制
4. 了解记忆的扫描、截断和新鲜度管理
5. 理解 `findRelevantMemories` 的智能召回流程

### 1.2 章节结构
| 章节 | 主题 | 核心内容 |
|------|------|---------|
| 一、为什么需要记忆？ | 概念入门 | 医生病历本类比 |
| 二、为什么用文件系统？ | 技术选型 | 对比数据库/内存 |
| 三、记忆目录路径 | 路径计算 | 优先级、安全验证 |
| 四、MEMORY.md | 索引机制 | 截断保护 |
| 五、扫描与读取 | 性能优化 | 只读 frontmatter |
| 六、智能召回 | AI 召回 | Sonnet 模型选择 |

---

## 二、关键知识点

### 2.1 为什么用文件系统？
| 方案 | 优点 | 缺点 |
|------|------|------|
| 数据库 (SQLite) | 查询快、结构化 | 需要额外依赖、迁移复杂 |
| 内存 (Map) | 最快 | 进程结束就没了 |
| **文件系统** | 零依赖、人类可读、git 友好 | 扫描慢（但记忆文件不多） |

### 2.2 路径计算
```typescript
// 源码文件：memdir/paths.ts
export const getAutoMemPath = memoize(
  (): string => {
    const override = getAutoMemPathOverride() ?? getAutoMemPathSetting()
    if (override) {
      return override
    }
    const projectsDir = join(getMemoryBaseDir(), 'projects')
    return (
      join(projectsDir, sanitizePath(getAutoMemBase()), AUTO_MEM_DIRNAME) + sep
    ).normalize('NFC')
  },
  () => getProjectRoot(),
)
```

**路径解析优先级：**
1. 环境变量覆盖 `CLAUDE_COWORK_MEMORY_PATH_OVERRIDE`
2. settings.json 覆盖 `autoMemoryDirectory`
3. 默认路径 `~/.claude/projects/{sanitized-path}/memory/`

### 2.3 Git 仓库共享记忆
```typescript
function getAutoMemBase(): string {
  return findCanonicalGitRoot(getProjectRoot()) ?? getProjectRoot()
}
```
多个 git worktree 共享同一个记忆目录。

### 2.4 安全验证
```typescript
function validateMemoryPath(raw: string | undefined, expandTilde: boolean): string | undefined {
  if (
    !isAbsolute(normalized) ||
    normalized.length < 3 ||
    /^[A-Za-z]:$/.test(normalized) ||
    normalized.startsWith('\\\\') ||
    normalized.startsWith('//') ||
    normalized.includes('\0')
  ) {
    return undefined
  }
  return (normalized + sep).normalize('NFC')
}
```

### 2.5 MEMORY.md 截断保护
```typescript
export const MAX_ENTRYPOINT_LINES = 200
export const MAX_ENTRYPOINT_BYTES = 25_000

export function truncateEntrypointContent(raw: string): EntrypointTruncation {
  // 先按行截断，再按字节截断
  // 在换行符处切断，不会把一行切成两半
}
```

### 2.6 scanMemoryFiles
```typescript
export async function scanMemoryFiles(
  memoryDir: string,
  signal: AbortSignal,
): Promise<MemoryHeader[]> {
  const entries = await readdir(memoryDir, { recursive: true })
  const mdFiles = entries.filter(
    f => f.endsWith('.md') && basename(f) !== 'MEMORY.md',
  )
  
  // 只读每个文件的前 30 行（frontmatter）
  // 用 Promise.allSettled 一个失败不影响其他
  // 上限 200 个文件
}
```

### 2.7 记忆文件格式
```markdown
---
name: 用户角色
description: 用户是高级后端工程师，偏好函数式编程风格
type: user
---

用户在 Anthropic 工作，主要使用 TypeScript 和 Go。
```

### 2.8 findRelevantMemories
```typescript
export async function findRelevantMemories(
  query: string,
  memoryDir: string,
  signal: AbortSignal,
  recentTools: readonly string[] = [],
  alreadySurfaced: ReadonlySet<string> = new Set(),
): Promise<RelevantMemory[]> {
  const memories = (await scanMemoryFiles(memoryDir, signal))
    .filter(m => !alreadySurfaced.has(m.filePath))
  
  if (memories.length === 0) return []
  
  const selectedFilenames = await selectRelevantMemories(
    query, memories, signal, recentTools,
  )
  // ...
}
```

### 2.9 记忆新鲜度
```typescript
export function memoryAgeDays(mtimeMs: number): number {
  return Math.max(0, Math.floor((Date.now() - mtimeMs) / 86_400_000))
}

export function memoryFreshnessText(mtimeMs: number): string {
  const d = memoryAgeDays(mtimeMs)
  if (d <= 1) return ''
  return (
    `This memory is ${d} days old. ` +
    `Memories are point-in-time observations, not live state...`
  )
}
```

---

## 三、关联文件索引

### 3.1 前置阅读
- [04-side-effects.md](04-side-effects.md) - 副作用同步

### 3.2 后续课程
- [06-memory-types.md](06-memory-types.md) - 四种记忆分类法

### 3.3 核心源码文件
| 文件路径 | 职责 | 行数 |
|---------|------|------|
| `memdir/memdir.ts` | 记忆系统主模块 | 508 行 |
| `memdir/paths.ts` | 记忆路径计算 | 279 行 |
| `memdir/memoryScan.ts` | 记忆文件扫描 | 95 行 |
| `memdir/findRelevantMemories.ts` | AI 智能召回 | 142 行 |
| `memdir/memoryAge.ts` | 新鲜度计算 | 54 行 |

---

## 四、源码对应关系

### 4.1 核心函数
| 函数名 | 位置 | 功能 |
|--------|------|------|
| `getAutoMemPath()` | `memdir/paths.ts` | 获取记忆目录路径 |
| `scanMemoryFiles()` | `memdir/memoryScan.ts` | 扫描记忆文件 |
| `findRelevantMemories()` | `memdir/findRelevantMemories.ts` | 智能召回 |
| `truncateEntrypointContent()` | `memdir/memdir.ts` | 截断索引文件 |
| `memoryAgeDays()` | `memdir/memoryAge.ts` | 计算记忆年龄 |
| `ensureMemoryDirExists()` | `memdir/memdir.ts` | 确保目录存在 |

### 4.2 常量
| 常量名 | 值 | 说明 |
|--------|-----|------|
| `MAX_ENTRYPOINT_LINES` | 200 | MEMORY.md 最大行数 |
| `MAX_ENTRYPOINT_BYTES` | 25_000 | MEMORY.md 最大字节数 |
| `MAX_MEMORY_FILES` | 200 | 最多扫描文件数 |
| `FRONTMATTER_MAX_LINES` | 30 | 只读前 30 行 |

---

## 五、本课小结

| 概念 | 解释 |
|------|------|
| Memdir | 基于文件系统的持久化记忆目录 |
| MEMORY.md | 记忆索引文件，每行一个指针，不超过 200 行 |
| Frontmatter | 记忆文件头部的 YAML 元数据（name, description, type） |
| scanMemoryFiles | 扫描目录，只读 frontmatter，按时间排序 |
| findRelevantMemories | 用 Sonnet 模型从记忆清单中选择最相关的（≤5个） |
| memoryAge | 人类可读的新鲜度标签，帮助 AI 判断记忆是否过时 |
| 路径安全 | 拒绝危险路径，projectSettings 不能覆盖记忆目录 |

---

*此细纲由 Claude Code 自动生成，用于快速导航和内容概览*
