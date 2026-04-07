# 第1课：什么是软件架构？Claude Code 的分层蛋糕 - 细纲

## 文件信息
- **原文件**: part02-architecture/01-what-is-software-architecture.md
- **类型**: 架构全景
- **难度**: ★★☆☆☆

---

## 一、什么是软件架构

### 1.1 生活类比：建一栋大楼
- **地基** → 基础设施层
- **承重墙** → 核心逻辑层
- **电梯和楼梯** → 通信/路由层
- **每层楼** → 功能模块层
- **外墙装饰** → 用户界面层

### 1.2 软件架构定义
> 软件架构 = 系统的组织方式 + 各部分如何协作 + 关键的设计决策

### 1.3 为什么架构重要
| 没有架构 | 有好的架构 |
|---------|-----------|
| 代码堆成一团 | 职责清晰，各司其职 |
| 改一处，坏十处 | 修改局部，不影响整体 |
| 新人看不懂 | 新人快速上手 |
| 扩展困难 | 轻松添加新功能 |

---

## 二、Claude Code 的五层架构

### 2.1 分层蛋糕模型
```
第5层：用户界面层 (React/Ink 终端 UI)
第4层：命令与交互层 (CLI 解析 + 斜杠命令)
第3层：查询引擎层 (QueryEngine + query 循环)
第2层：工具与服务层 (40+ 工具 + MCP + 权限)
第1层：状态与基础层 (AppState + Store + 配置)
```

### 2.2 分层架构核心规则
- 每一层只和相邻的层交互
- 上层依赖下层，下层不依赖上层

---

## 三、从真实源码看分层

### 3.1 第1层：状态与基础层
**文件**: `src/state/store.ts`

```typescript
export type Store<T> = {
  getState: () => T
  setState: (updater: (prev: T) => T) => void
  subscribe: (listener: Listener) => () => void
}

export function createStore<T>(
  initialState: T,
  onChange?: OnChange<T>,
): Store<T> {
  let state = initialState
  const listeners = new Set<Listener>()

  return {
    getState: () => state,
    setState: (updater: (prev: T) => T) => {
      const prev = state
      const next = updater(prev)
      if (Object.is(next, prev)) return
      state = next
      onChange?.({ newState: next, oldState: prev })
      for (const listener of listeners) listener()
    },
    subscribe: (listener: Listener) => {
      listeners.add(listener)
      return () => listeners.delete(listener)
    },
  }
}
```

**类比**: 公告板——任何人都可以看（`getState`），授权的人可以更新（`setState`），关心变化的人可以订阅通知（`subscribe`）。

### 3.2 第2层：工具与服务层
**文件**: `src/tools.ts`

```typescript
export function getAllBaseTools(): Tools {
  return [
    AgentTool,
    TaskOutputTool,
    BashTool,
    ...(hasEmbeddedSearchTools() ? [] : [GlobTool, GrepTool]),
    FileReadTool,
    FileEditTool,
    FileWriteTool,
    NotebookEditTool,
    WebFetchTool,
    TodoWriteTool,
    WebSearchTool,
    // ...更多工具
  ]
}
```

**类比**: 工具箱——不同的工具完成不同的任务。

### 3.3 第3层：查询引擎层
**文件**: `src/QueryEngine.ts`

```typescript
export class QueryEngine {
  private config: QueryEngineConfig
  private mutableMessages: Message[]
  private abortController: AbortController
  private totalUsage: NonNullableUsage

  constructor(config: QueryEngineConfig) {
    this.config = config
    this.mutableMessages = config.initialMessages ?? []
    this.abortController = config.abortController ?? createAbortController()
    this.totalUsage = EMPTY_USAGE
  }

  async *submitMessage(
    prompt: string | ContentBlockParam[],
    options?: { uuid?: string; isMeta?: boolean },
  ): AsyncGenerator<SDKMessage, void, unknown> {
    // 处理用户输入 → 调用 API → 执行工具 → 返回结果
  }
}
```

**类比**: 翻译官——接收你说的话，翻译给 Claude AI，再把 AI 的回答翻译回来。

### 3.4 第4层：命令与交互层
**文件**: `src/commands.ts`

```typescript
const COMMANDS = memoize((): Command[] => [
  addDir, advisor, agents, branch, clear,
  color, compact, config, copy, desktop,
  context, cost, diff, doctor, effort,
  exit, fast, files, help, ide,
  init, keybindings, mcp, memory, model,
  permissions, plan, review, session, skills,
  status, theme, vim,
  // ...更多命令
])
```

**类比**: 餐厅菜单——`/help` 看帮助，`/compact` 压缩对话，`/mcp` 管理外部工具。

### 3.5 第5层：用户界面层
**目录**: `src/ink/`
- 基于 React/Ink 构建的终端界面
- 让命令行有丰富的交互体验

---

## 四、目录结构全景图

### 4.1 关键文件说明
| 文件/目录 | 职责 | 层级 |
|----------|------|------|
| `main.tsx` | 程序入口，CLI 解析 | 第4层 |
| `tools.ts` | 工具注册中心 | 第2层 |
| `QueryEngine.ts` | 查询生命周期管理 | 第3层 |
| `query.ts` | 核心查询循环 | 第3层 |
| `commands.ts` | 斜杠命令注册 | 第4层 |
| `state/store.ts` | 状态管理 | 第1层 |
| `bridge/` | 远程桥接 | 第2层 |
| `services/mcp/` | MCP 扩展 | 第2层 |
| `ink/` | 终端 UI | 第5层 |

---

## 五、分层架构的好处

### 5.1 四大优势
| 优势 | 说明 |
|------|------|
| 可替换性 | 换掉 UI 层不影响查询引擎 |
| 可测试性 | 每层可以独立测试 |
| 团队协作 | 不同团队负责不同层 |
| 可扩展性 | 新增工具只需在工具层添加 |

### 5.2 真实例子：添加新工具
1. 在 `tools/` 目录下创建新工具文件
2. 在 `tools.ts` 的 `getAllBaseTools()` 中注册
3. 完成！其他层完全不需要改动

**核心思想**: 关注点分离

---

## 六、动手练习

### 练习1：找到关键文件
找到以下文件并记录行数：
- [ ] `main.tsx` — 入口文件
- [ ] `tools.ts` — 工具导入数量
- [ ] `QueryEngine.ts` — QueryEngine 类方法
- [ ] `state/store.ts` — Store 接口方法

### 练习2：画出你的理解
画出 Claude Code 的五层架构，标注每层的核心职责和关键文件。

### 思考题
1. 为什么 `state/store.ts` 要用 `Object.is(next, prev)` 判断状态变化？
2. 如果把所有代码都写在一个文件里会怎样？
3. 其他软件（微信、淘宝）是否也是分层架构？

---

## 七、小结

| 要点 | 内容 |
|------|------|
| 软件架构 | 系统的组织方式和设计决策 |
| 分层架构 | 各层职责明确，只与相邻层交互 |
| Claude Code 五层 | 状态层 → 工具层 → 引擎层 → 命令层 → UI 层 |
| 核心文件 | main.tsx, tools.ts, QueryEngine.ts, query.ts, commands.ts |
| 核心思想 | 关注点分离，高内聚低耦合 |

---

## 八、关联文件

### 8.1 上一章
- [../part01-basics/04-react-and-ink.md](../part01-basics/04-react-and-ink.md) - React 与 Ink

### 8.2 下一章
- [02-tech-stack.md](02-tech-stack.md) - 技术栈全解析

---

*此细纲由 Claude Code 自动生成*
