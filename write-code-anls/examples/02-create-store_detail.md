# 图解 Claude Code 完全指南 - 细纲

## 文件信息
- **原文件**: 02-create-store.md
- **类型**: 第 2 课：createStore 源码解析 —— 34 行极简 Store
- **难度**: ★★☆☆☆

---

## 一、文档结构概览

### 1.1 学习目标
1. 理解闭包如何实现私有状态存储
2. 掌握发布-订阅（Pub/Sub）模式的原理和实现
3. 搞懂 `Object.is` 短路优化的意义
4. 理解 `onChange` 回调如何架起"内存 → 磁盘"的桥梁
5. 能自己写出一个类似的极简 Store

### 1.2 章节结构
| 章节 | 主题 | 核心内容 |
|------|------|---------|
| 一、完整源码一览 | 整体概览 | 34 行完整代码展示 |
| 二、类型定义 | 先画图纸 | Listener、OnChange、Store 类型 |
| 三、createStore 逐行解析 | 核心实现 | 闭包、getState、setState、subscribe |
| 四、完整数据流图 | 流程梳理 | 状态更新完整流程 |
| 五、与 React useState 对比 | 横向对比 | 特性对比表 |
| 六、设计中的取舍 | 深入思考 | 为什么不用 middleware/selector |

---

## 二、关键知识点

### 2.1 类型定义详解

#### Listener 类型
```typescript
type Listener = () => void
```
- 不接收参数，只作为"状态变了"的信号
- 需要获取新状态时自行调用 `getState()`

#### OnChange 类型
```typescript
type OnChange<T> = (args: { newState: T; oldState: T }) => void
```
- 同时接收新旧状态，可做差异比较
- 实现副作用同步的关键（第 4 课 `onChangeAppState` 的基础）

#### Store 接口
```typescript
export type Store<T> = {
  getState: () => T                              // 读
  setState: (updater: (prev: T) => T) => void    // 写
  subscribe: (listener: Listener) => () => void  // 订阅
}
```

### 2.2 闭包：私有状态的秘密
```typescript
export function createStore<T>(initialState: T, onChange?: OnChange<T>): Store<T> {
  let state = initialState           // ← 闭包保护的私有状态
  const listeners = new Set<Listener>()  // ← 闭包保护的监听器集合
  
  return {
    getState: () => state,           // 只暴露访问方法
    setState: (updater) => { /* ... */ },
    subscribe: (listener) => { /* ... */ },
  }
}
```

**为什么用 `Set` 而不是数组？**
- 不会重复添加同一个 listener
- 删除操作是 O(1) 而非 O(n)

### 2.3 setState 核心逻辑
```typescript
setState: (updater: (prev: T) => T) => {
  const prev = state                 // ① 保存旧状态
  const next = updater(prev)         // ② 基于旧状态计算新状态
  if (Object.is(next, prev)) return  // ③ 没变？什么都不做（短路优化）
  state = next                       // ④ 更新状态
  onChange?.({ newState: next, oldState: prev })  // ⑤ 触发变更回调
  for (const listener of listeners) listener()    // ⑥ 通知所有订阅者
}
```

### 2.4 Object.is 短路优化
```typescript
if (Object.is(next, prev)) return
```

**Object.is vs ===**
```typescript
Object.is(NaN, NaN)   // true  ✅ （=== 返回 false）
Object.is(+0, -0)     // false ✅ （=== 返回 true）
```

**短路优化的收益：**
- 避免不必要的 onChange 调用
- 避免不必要的磁盘写入
- 避免不必要的 UI 重渲染
- 避免不必要的网络请求

### 2.5 subscribe 模式
```typescript
subscribe: (listener: Listener) => {
  listeners.add(listener)
  return () => listeners.delete(listener)  // 返回取消订阅函数
}
```

**使用示例：**
```typescript
const unsubscribe = store.subscribe(() => {
  console.log('状态更新了！', store.getState())
})

// 不再需要监听时
unsubscribe()
```

---

## 三、关联文件索引

### 3.1 前置阅读
- [01-what-is-state-management.md](01-what-is-state-management.md) - 状态管理基础概念

### 3.2 后续课程
- [03-app-state.md](03-app-state.md) - AppState 500+ 字段的组织之道
- [04-side-effects.md](04-side-effects.md) - 副作用同步

### 3.3 核心源码文件
| 文件路径 | 职责 | 行数 |
|---------|------|------|
| `state/store.ts` | 极简 Store 实现 | 34 行 |

---

## 四、源码对应关系

### 4.1 核心类型与接口
| 名称 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `Store<T>` | type | `state/store.ts` | Store 接口定义 |
| `Listener` | type | `state/store.ts` | 监听器类型 |
| `OnChange<T>` | type | `state/store.ts` | 变更回调类型 |

### 4.2 关键函数
| 函数名 | 位置 | 功能 | 参数 | 返回值 |
|--------|------|------|------|--------|
| `createStore<T>()` | `state/store.ts` | Store 工厂函数 | `initialState: T`, `onChange?: OnChange<T>` | `Store<T>` |
| `getState()` | `state/store.ts` | 获取当前状态 | 无 | `T` |
| `setState(updater)` | `state/store.ts` | 更新状态 | `(prev: T) => T` | `void` |
| `subscribe(listener)` | `state/store.ts` | 订阅变更 | `Listener` | `() => void`（取消函数） |

### 4.3 与 React useState 对比
| 特性 | React useState | Claude Code createStore |
|------|---------------|------------------------|
| 作用域 | 单个组件 | 整个应用 |
| 订阅机制 | 自动（React 调度） | 手动 subscribe |
| 更新方式 | `setState(newVal)` 或 `setState(prev => ...)` | 只有 `setState(prev => ...)` |
| 批量更新 | React 18 自动批量 | 每次 setState 立即生效 |
| 变更通知 | React 自动 re-render | 手动 onChange + listeners |

---

## 五、设计中的取舍

### 5.1 为什么没有 middleware？
- 副作用类型有限（写配置、通知远端、清缓存）
- 一个 `onChange` 回调搞定了所有副作用
- 一个函数比中间件链更容易理解和调试

### 5.2 为什么没有 selector？
- UI 组件直接 `getState()` 取需要的字段
- `Object.is` 短路已经避免了不必要的通知
- 34 行代码不值得为了优化而增加复杂度

---

## 六、本课小结

| 概念 | 解释 |
|------|------|
| 闭包存储 | `let state` 被闭包保护，外部只能通过暴露的方法访问 |
| 函数式更新 | `setState(prev => ...)` 保证基于最新状态计算 |
| Object.is 短路 | 状态没变就不触发后续操作，避免不必要的副作用 |
| onChange 回调 | 架起内存状态和磁盘持久化的桥梁 |
| subscribe 模式 | 发布-订阅模式，返回取消函数实现优雅清理 |
| Set 管理监听者 | 比数组更快地添加和删除监听者 |

---

*此细纲由 Claude Code 自动生成，用于快速导航和内容概览*
