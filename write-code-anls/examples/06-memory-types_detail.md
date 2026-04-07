# 图解 Claude Code 完全指南 - 细纲

## 文件信息
- **原文件**: 06-memory-types.md
- **类型**: 第 6 课：四种记忆分类法详解
- **难度**: ★★☆☆☆

---

## 一、文档结构概览

### 1.1 学习目标
1. 掌握四种记忆类型（user / feedback / project / reference）的定义和区别
2. 理解每种类型的"何时存"和"如何用"
3. 学会判断什么信息**不该**存为记忆
4. 了解 Frontmatter 格式的设计意义
5. 认识个人模式与团队模式的差异

### 1.2 章节结构
| 章节 | 主题 | 核心内容 |
|------|------|---------|
| 一、为什么需要分类？ | 概念入门 | 图书馆分类系统类比 |
| 二、四种类型定义 | 核心知识 | user/feedback/project/reference |
| 三-六、各类型详解 | 逐个讲解 | 定义、示例、原则 |
| 七、什么不该存？ | 排除规则 | 决策树 |
| 八、Frontmatter | 格式规范 | YAML 头部 |
| 九、个人 vs 团队 | 模式对比 | 范围标记 |

---

## 二、关键知识点

### 2.1 四种记忆类型定义
```typescript
// 源码文件：memdir/memoryTypes.ts
export const MEMORY_TYPES = [
  'user',
  'feedback',
  'project',
  'reference',
] as const

export type MemoryType = (typeof MEMORY_TYPES)[number]
```

### 2.2 User（用户记忆）
**定义**: 关于用户的角色、目标、职责和知识水平的信息

**什么时候存？**
- 了解到用户的身份、技能、偏好时

**示例**:
```markdown
---
name: 用户技术背景
description: 用户是高级 Go 工程师，React 新手
type: user
---

- 10年 Go 经验，擅长并发和微服务
- 首次接触 React，不熟悉 hooks
```

**关键原则**: 目标是**帮助用户**。避免写负面评价或与工作无关的记忆。

### 2.3 Feedback（反馈记忆）
**定义**: 用户关于工作方式的指导——包括要避免什么和要继续做什么

**什么时候存？**
- 用户**纠正**你时：「不要这样做」「别用 mock」
- 用户**确认**非显而易见的做法时：「对，就是这样」

**结构要求**:
```
rule → Why → How to apply
```

**示例**:
```markdown
---
name: 不要 mock 数据库
description: 集成测试必须使用真实数据库
type: feedback
---

集成测试必须使用真实数据库，不使用 mock。

**Why:** 上个季度 mock 测试通过了但生产环境迁移失败...

**How to apply:** 在写测试时，即使 mock 看起来更简单...
```

### 2.4 Project（项目记忆）
**定义**: 关于正在进行的工作、目标、计划、bug 或事件的信息，**不能从代码或 git 历史中推导出来**

**日期转换规则**:
```typescript
'Always convert relative dates in user messages to absolute dates ' +
'when saving (e.g., "Thursday" → "2026-03-05")'
```

### 2.5 Reference（引用记忆）
**定义**: 指向外部系统中信息位置的指针

**示例**:
- Linear 项目 "INGEST" 跟踪 pipeline bugs
- Grafana 面板 grafana.internal/d/api-latency

### 2.6 什么不该存？
```typescript
export const WHAT_NOT_TO_SAVE_SECTION: readonly string[] = [
  '## What NOT to save in memory',
  '',
  '- Code patterns, conventions, architecture, file paths...',
  '- Git history, recent changes, or who-changed-what...',
  '- Debugging solutions or fix recipes...',
  '- Anything already documented in CLAUDE.md files.',
  '- Ephemeral task details: in-progress work...',
]
```

### 2.7 决策树
```
用户说了信息 → 能从代码/git推导？ → 是 → ❌ 不存
                    ↓ 否
              已在 CLAUDE.md？ → 是 → ❌ 不存
                    ↓ 否
              只对当前会话有用？ → 是 → ❌ 不存
                    ↓ 否
              是什么类型？ → user/feedback/project/reference → ✅ 存入
```

### 2.8 Frontmatter 格式
```markdown
---
name: {{memory name}}
description: {{one-line description}}
type: {{user, feedback, project, reference}}
---

{{memory content}}
```

### 2.9 个人 vs 团队模式
| | 个人模式 (INDIVIDUAL) | 团队模式 (COMBINED) |
|---|---|---|
| 目录 | 一个 memory/ | memory/ + memory/team/ |
| 范围标记 | 无 `<scope>` | 有 `<scope>` 标签 |
| feedback 默认 | 全部个人 | 默认个人，除非是项目级规范 |
| project 默认 | 全部个人 | 偏向 team |

### 2.10 记忆信任与验证
```typescript
export const TRUSTING_RECALL_SECTION: readonly string[] = [
  '## Before recommending from memory',
  '',
  'A memory that names a specific function, file, or flag is a claim...',
  '',
  '- If the memory names a file path: check the file exists.',
  '- If the memory names a function or flag: grep for it.',
  '- If the user is about to act on your recommendation, verify first.',
]
```

---

## 三、关联文件索引

### 3.1 前置阅读
- [05-memdir-memory.md](05-memdir-memory.md) - Memdir 记忆系统

### 3.2 后续课程
- [07-history.md](07-history.md) - History 会话历史

### 3.3 核心源码文件
| 文件路径 | 职责 | 行数 |
|---------|------|------|
| `memdir/memoryTypes.ts` | 四种记忆类型定义 | 272 行 |

---

## 四、源码对应关系

### 4.1 核心类型与常量
| 名称 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `MEMORY_TYPES` | const | `memdir/memoryTypes.ts` | 四种类型数组 |
| `MemoryType` | type | `memdir/memoryTypes.ts` | 记忆类型联合类型 |
| `TYPES_SECTION_INDIVIDUAL` | const | `memdir/memoryTypes.ts` | 个人模式指导文本 |
| `WHAT_NOT_TO_SAVE_SECTION` | const | `memdir/memoryTypes.ts` | 不该存的内容 |
| `TRUSTING_RECALL_SECTION` | const | `memdir/memoryTypes.ts` | 使用前验证指导 |
| `MEMORY_FRONTMATTER_EXAMPLE` | const | `memdir/memoryTypes.ts` | Frontmatter 示例 |

### 4.2 核心函数
| 函数名 | 位置 | 功能 |
|--------|------|------|
| `parseMemoryType()` | `memdir/memoryTypes.ts` | 解析记忆类型 |

---

## 五、本课小结

| 类型 | 核心问题 | 存什么 | 不存什么 |
|------|---------|--------|---------|
| user | 用户是谁？ | 角色、技能、偏好 | 负面评价 |
| feedback | 怎么工作？ | 纠正+确认+原因 | 不含 Why 的规则 |
| project | 在做什么？ | 计划、期限、决策 | 可从 git 推导的 |
| reference | 去哪找？ | 外部系统链接 | 代码内的路径 |

**黄金法则**: 不存能从代码推导的东西，即使用户要求也要追问"值得记的非显而易见的部分"。

---

*此细纲由 Claude Code 自动生成，用于快速导航和内容概览*
