# 第2课：技术栈全解析：TypeScript + Bun + React/Ink - 细纲

## 文件信息
- **原文件**: part02-architecture/02-tech-stack.md
- **类型**: 架构全景
- **难度**: ★★☆☆☆

---

## 一、TypeScript：给 JavaScript 穿上铠甲

### 1.1 生活类比：标签化的收纳箱
- JavaScript = 所有东西扔在一起
- TypeScript = 给每个箱子贴上标签

### 1.2 真实源码中的类型
**文件**: `src/QueryEngine.ts`

```typescript
export type QueryEngineConfig = {
  cwd: string
  tools: Tools
  commands: Command[]
  mcpClients: MCPServerConnection[]
  agents: AgentDefinition[]
  canUseTool: CanUseToolFn
  getAppState: () => AppState
  setAppState: (f: (prev: AppState) => AppState) => void
  initialMessages?: Message[]
  readFileCache: FileStateCache
  customSystemPrompt?: string
  maxTurns?: number
  maxBudgetUsd?: number
  verbose?: boolean
}
```

### 1.3 TypeScript 在 Claude Code 中的价值
| 价值 | 说明 |
|------|------|
| 类型安全 | 1300+ 行的 QueryEngine，没有类型就是噩梦 |
| 接口契约 | Tool 接口定义每个工具必须实现什么 |
| 重构信心 | 改名函数，编译器告诉你哪里要改 |
| 团队协作 | 新人看类型定义就知道怎么用 |

---

## 二、Bun：闪电般的 JavaScript 运行时

### 2.1 生活类比：高铁 vs 绿皮火车
- Node.js = 可靠的绿皮火车
- Bun = 高铁，速度快好几倍

### 2.2 Bun 的独特用法：feature() 函数
**文件**: `src/tools.ts`

```typescript
import { feature } from 'bun:bundle'

const SleepTool = feature('PROACTIVE') || feature('KAIROS')
  ? require('./tools/SleepTool/SleepTool.js').SleepTool
  : null

const coordinatorModeModule = feature('COORDINATOR_MODE')
  ? require('./coordinator/coordinatorMode.js') as typeof import('./coordinator/coordinatorMode.js')
  : null

const SnipTool = feature('HISTORY_SNIP')
  ? require('./tools/SnipTool/SnipTool.js').SnipTool
  : null
```

### 2.3 feature() 编译时特性门控
```
源代码中的 feature('X')
    ↓
Bun 打包时判断
    ↓
X 开启 → 包含这段代码
X 关闭 → 完全删除这段代码（Dead Code Elimination）
```

**好处**:
- 更小的产物体积
- 内部功能不泄露
- 更快的启动速度

### 2.4 Bun vs Node.js
| 特性 | Node.js | Bun |
|------|---------|-----|
| 启动速度 | ~40ms | ~6ms |
| 包管理 | npm/yarn | 内置，更快 |
| TypeScript | 需要编译 | 原生支持 |
| 打包 | 需要 webpack | 内置 bundler |
| 测试 | 需要 jest | 内置测试运行器 |

---

## 三、React/Ink：让终端也能用 React

### 3.1 生活类比：乐高积木
- 传统 CLI = 用纸笔画画
- React/Ink = 用乐高积木拼出丰富界面

### 3.2 Ink 是什么
- 让 React 组件能在终端中渲染的库
- Claude Code 内置了定制的 Ink 版本

### 3.3 Ink 核心组件
**文件**: `src/ink/components/`

| 组件 | 作用 | 类比 |
|------|------|------|
| `Box.tsx` | 布局容器 | `<div>` |
| `Text.tsx` | 文本组件 | `<span>` |
| `ScrollBox.tsx` | 可滚动容器 | 带滚动的 div |

### 3.4 为什么用 React 做 CLI
| 传统 CLI | React/Ink CLI |
|----------|---------------|
| `console.log('Loading...')` | `<Text color='green'>Loading...</Text>` |
| 手动管理光标位置 | 自动布局，像写网页一样 |
| 手动处理窗口大小变化 | 响应式设计，自动适配 |

### 3.5 真实的 React 在 CLI 中的用法
```typescript
// 概念示例：Agent 工具的 UI 渲染
function renderToolUseProgressMessage(
  toolName: string,
  description: string,
) {
  return <Text color="blue">{`🔄 ${toolName}: ${description}`}</Text>
}
```

---

## 四、三者如何协同工作

### 4.1 技术栈协作流程
```
TypeScript（类型安全）
    ↓
Bun（运行时 + 打包）
    ↓
feature() 门控 → Dead Code Elimination
    ↓
最终可执行文件

React/Ink（渲染 UI）→ 终端界面
```

### 4.2 main.tsx 中的协作体现
**文件**: `src/main.tsx`

```typescript
import { feature } from 'bun:bundle'          // Bun 特性
import React from 'react'                       // React
import { Command as CommanderCommand } from '@commander-js/extra-typings'  // TS 类型
import { createStore } from './state/store.js'   // TS 状态管理
import { type AppState, getDefaultAppState } from './state/AppStateStore.js'  // TS 类型

// feature() 控制编译时包含哪些模块
const coordinatorModeModule = feature('COORDINATOR_MODE')
  ? require('./coordinator/coordinatorMode.js')
  : null

const assistantModule = feature('KAIROS')
  ? require('./assistant/index.js')
  : null
```

---

## 五、Dead Code Elimination 深度解析

### 5.1 条件导入示例
**文件**: `src/commands.ts`

```typescript
const proactive =
  feature('PROACTIVE') || feature('KAIROS')
    ? require('./commands/proactive.js').default
    : null

const bridge = feature('BRIDGE_MODE')
  ? require('./commands/bridge/index.js').default
  : null

const voiceCommand = feature('VOICE_MODE')
  ? require('./commands/voice/index.js').default
  : null
```

### 5.2 编译前后对比
| 编译前（源码） | 编译后（外部版本） |
|----------------|-------------------|
| `feature('VOICE_MODE') ? require(voice) : null` | `null`（voice 被移除） |
| `feature('BRIDGE_MODE') ? require(bridge) : null` | `null`（bridge 被移除） |
| 核心功能代码 | 核心功能代码（保留） |

---

## 六、动手练习

### 练习1：TypeScript 类型体验
仿照 Claude Code 的 Store 类型：
```typescript
type MyStore<T> = {
  getState: () => T
  setState: (updater: (prev: T) => T) => void
}

type CounterState = { count: number; name: string }
```

### 练习2：理解 feature() 门控
阅读 `tools.ts` 源码，回答：
- [ ] 有多少个 `feature()` 调用？
- [ ] 哪些工具只有内部用户能使用？（`USER_TYPE === 'ant'`）
- [ ] 如果 `feature('COORDINATOR_MODE')` 返回 false，会发生什么？

### 思考题
1. 为什么 Claude Code 不直接用 JavaScript，而要用 TypeScript？
2. `feature()` 和运行时的 `if` 判断有什么区别？
3. 为什么要在终端里用 React？直接 `console.log` 不好吗？

---

## 七、小结

| 技术 | 作用 | 类比 |
|------|------|------|
| TypeScript | 类型安全，防止错误 | 给箱子贴标签 |
| Bun | 快速运行时 + 打包 | 高铁 vs 绿皮火车 |
| React/Ink | 终端 UI 框架 | 乐高积木 |
| feature() | 编译时代码消除 | 书的不同版本 |

### 关键文件
| 文件 | 技术体现 |
|------|---------|
| `QueryEngine.ts` | TypeScript 类型的大规模应用 |
| `tools.ts` | `feature()` + 条件导入 |
| `ink/components/` | React/Ink 组件 |
| `main.tsx` | 三种技术的交汇点 |

---

## 八、关联文件

### 8.1 上一章
- [01-what-is-software-architecture.md](01-what-is-software-architecture.md) - 软件架构

### 8.2 下一章
- [03-startup-process.md](03-startup-process.md) - 启动流程详解

---

*此细纲由 Claude Code 自动生成*
