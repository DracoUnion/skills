# 图解 Claude Code 完全指南 - 细纲

## 文件信息
- **原文件**: 01-what-is-state-management.md
- **类型**: 第1课：什么是状态管理？为什么需要它？
- **难度**: ★☆☆☆☆

---

## 一、文档结构概览

### 1.1 学习目标
1. 理解什么是"状态"，以及它在程序中的含义
2. 明白为什么复杂应用需要统一的状态管理方案
3. 了解 Claude Code 中状态管理面临的挑战
4. 认识 Claude Code 的三层状态架构概览
5. 建立对后续课程的整体认知地图

### 1.2 章节结构
| 章节 | 主题 | 核心内容 |
|------|------|---------|
| 一、什么是"状态"？ | 状态概念入门 | 生活类比（书桌）、代码示例 |
| 二、为什么需要"管理"状态？ | 状态管理必要性 | 团队工作类比、三大问题解决 |
| 三、Claude Code 面临的状态挑战 | 实际场景分析 | 种类繁多、生命周期不同、AppState 概览 |
| 四、Claude Code 的三层状态架构 | 架构分层 | 内存状态、文件持久化、版本迁移 |
| 五、为什么不用 Redux / Zustand / MobX？ | 技术选型 | 34行自研 Store 的优势 |

---

## 二、关键知识点

### 2.1 状态（State）概念
- **定义**: 程序在某一时刻所有"记住"的东西的总和
- **生活类比**: 书桌上的物品（打开的书、咖啡温度、抽屉文件夹、脑中计划）
- **代码示例**: `let userName = "小明"`、`let isLoggedIn = false`

### 2.2 状态管理解决的三大问题
```
🔍 可追踪 - 谁在什么时候改了什么
🔒 可控制 - 只能通过指定方式修改
📢 可通知 - 状态变了自动通知相关方
```

### 2.3 Claude Code 的三层状态架构
| 层次 | 职责 | 生命周期 | 对应课程 | 源码文件 |
|------|------|---------|---------|---------|
| 内存状态 | 运行时所有数据 | 进程生命周期 | 第 2-4 课 | `state/store.ts`, `state/AppStateStore.ts` |
| 文件持久化 | 跨会话保存的数据 | 跨会话/永久 | 第 5-7 课 | `memdir/`, `history.ts` |
| 版本迁移 | 数据格式升级 | 升级时一次性 | 第 8 课 | `migrations/*.ts` |

### 2.4 AppState 核心类型
```typescript
// 来自 state/AppStateStore.ts
export type AppState = DeepImmutable<{
  settings: SettingsJson           // 用户设置
  verbose: boolean                 // 是否详细输出
  mainLoopModel: ModelSetting      // 主循环使用的模型
  statusLineText: string | undefined  // 状态栏文字
  thinkingEnabled: boolean | undefined // 是否启用思考
  toolPermissionContext: ToolPermissionContext  // 工具权限
}> & {
  tasks: { [taskId: string]: TaskState }    // 任务列表
  mcp: { clients: MCPServerConnection[]; tools: Tool[]; ... }  // MCP 插件
  fileHistory: FileHistoryState             // 文件历史
}
```

### 2.5 createStore 极简实现
```typescript
// 来自 state/store.ts（完整 34 行）
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

---

## 三、关联文件索引

### 3.1 前置阅读
- 无（本课为系列起点）

### 3.2 后续课程
- [02-create-store.md](02-create-store.md) - createStore 源码解析
- [03-app-state.md](03-app-state.md) - AppState 500+ 字段的组织之道
- [04-side-effects.md](04-side-effects.md) - 副作用同步

### 3.3 核心源码文件
| 文件路径 | 职责 | 行数 |
|---------|------|------|
| `state/store.ts` | 极简 Store 实现 | 34 行 |
| `state/AppStateStore.ts` | AppState 类型定义 | 570 行 |
| `state/onChangeAppState.ts` | 副作用收口 | 172 行 |

---

## 四、源码对应关系

### 4.1 核心类型与接口
| 名称 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `Store<T>` | interface | `state/store.ts` | Store 接口定义 |
| `createStore` | function | `state/store.ts` | Store 工厂函数 |
| `AppState` | type | `state/AppStateStore.ts` | 应用状态类型 |
| `DeepImmutable` | type | `state/AppStateStore.ts` | 深度不可变类型 |
| `Listener` | type | `state/store.ts` | 监听器类型 |
| `OnChange<T>` | type | `state/store.ts` | 变更回调类型 |

### 4.2 关键函数
| 函数名 | 位置 | 功能 |
|--------|------|------|
| `getState()` | `state/store.ts` | 获取当前状态 |
| `setState(updater)` | `state/store.ts` | 更新状态 |
| `subscribe(listener)` | `state/store.ts` | 订阅状态变更 |
| `getDefaultAppState()` | `state/AppStateStore.ts` | 获取默认状态 |

---

## 五、本课小结

| 关键概念 | 一句话解释 |
|---------|-----------|
| 状态（State） | 程序在某一时刻"记住"的所有东西 |
| 状态管理 | 用统一的方式管理状态的读取、修改和通知 |
| 可追踪 | 知道谁在什么时候改了什么 |
| 可控制 | 只能通过指定方式修改状态 |
| 可通知 | 状态变了自动通知关心的人 |
| DeepImmutable | Claude Code 中确保状态不被直接修改的类型约束 |

---

*此细纲由 Claude Code 自动生成，用于快速导航和内容概览*
