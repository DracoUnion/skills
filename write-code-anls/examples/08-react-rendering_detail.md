# 第8课：React 渲染优化 —— 虚拟滚动与 Memo - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第8课：React 渲染优化 —— 虚拟滚动与 Memo

### 1.2 二级标题
- 学习目标
- 生活类比：超长菜单的餐厅
- 核心概念一：虚拟滚动（Virtual Scrolling）
- 核心概念二：OffscreenFreeze —— 冻结不可见内容
- 核心概念三：WeakMap 缓存与 GC 压力
- 核心概念四：React.memo 与 MessageRow
- 核心概念五：增量搜索优化
- 动手练习
- 本课小结
- 下节预告

### 1.3 三级标题
- 问题：为什么需要虚拟滚动？
- Claude Code 的解决方案：VirtualMessageList
- Mermaid 流程图：虚拟滚动工作流
- 高度缓存与终端宽度
- 问题：滚出视口的内容还在更新？
- Claude Code 的巧妙方案
- 为什么要 `'use no memo'`？
- 问题：频繁计算消耗大量内存
- Claude Code 的 WeakMap 缓存策略
- 为什么选择 WeakMap 而不是 Map？
- 另一个例子：Sticky Prompt 缓存
- 问题：父组件更新导致子组件无效重渲染
- Claude Code 的 MessageRow 优化
- Mermaid 图：有/无 memo 的渲染对比
- 问题：全文搜索在大量消息中很慢
- Claude Code 的两阶段策略

---

## 2. 关键知识点

### 2.1 虚拟滚动（Virtual Scrolling）
- 只渲染可见区域的消息
- 上下不可见区域用占位符填充
- `columns` 变化时清除高度缓存（文字换行导致高度变化）

### 2.2 OffscreenFreeze 模式
- 不可见时返回缓存的旧 ReactElement 引用
- React 跳过 diff，零开销
- 使用 `'use no memo'` 禁用 React Compiler 的自动 memo

### 2.3 WeakMap vs Map
| 特性 | Map | WeakMap |
|------|-----|---------|
| 键类型 | 任意 | 只能是对象 |
| GC 行为 | 键被删除后缓存仍存在（泄漏） | 键被 GC 后缓存自动清除 |
| 遍历 | 可遍历 | 不可遍历 |
| 适用场景 | 需要持久缓存 | 对象生命周期绑定的缓存 |

### 2.4 React.memo 优化技巧
- 传布尔值而非数组：`hasContentAfter: boolean`
- 避免传递完整数组引用到子组件
- 防止 React Compiler 把数组 pin 到 fiber 的 memoCache

### 2.5 增量搜索优化
- **阶段一：预热（Warm）** - 后台遍历所有消息，执行 `toLowerCase()`，结果存入 WeakMap
- **阶段二：搜索（Search）** - 遍历缓存的小写文本，零 `toLowerCase` 分配

---

## 3. 涉及的源码文件路径

### 3.1 核心源码文件
- `components/VirtualMessageList.tsx` - 虚拟消息列表
- `components/OffscreenFreeze.tsx` - 不可见内容冻结
- `components/MessageRow.tsx` - 消息行组件
- `hooks/useVirtualScroll.js` - 虚拟滚动 Hook
- `hooks/useTerminalViewport.ts` - 终端视口 Hook

### 3.2 相关工具
- `ink/components/Box.tsx` - 盒子布局组件
- `ink/components/ScrollBox.tsx` - 滚动容器组件

---

## 4. 类名、函数名、接口名

### 4.1 组件
- `VirtualMessageList` - 虚拟消息列表组件
- `OffscreenFreeze` - 不可见内容冻结组件
- `MessageRow` - 消息行组件
- `Box` - 盒子布局组件
- `ScrollBox` - 滚动容器组件

### 4.2 Hooks
- `useVirtualScroll()` - 虚拟滚动 Hook
- `useTerminalViewport()` - 终端视口 Hook
- `useContext()` - React 上下文 Hook
- `useRef()` - React ref Hook

### 4.3 函数
- `defaultExtractSearchText(msg: RenderableMessage)` - 默认搜索文本提取
- `renderableSearchText(msg: RenderableMessage)` - 渲染搜索文本
- `stickyPromptText(msg: RenderableMessage)` - 粘性提示文本
- `computeStickyPromptText(msg: RenderableMessage)` - 计算粘性提示文本
- `hasContentAfterIndex(messages: RenderableMessage[], index: number)` - 检查后面是否有内容

### 4.4 类型/接口
- `Props` - VirtualMessageList 属性
- `RenderableMessage` - 可渲染消息类型
- `JumpHandle` - 跳转句柄
- `ScrollBoxHandle` - 滚动框句柄

### 4.5 常量
- `fallbackLowerCache` - 搜索文本缓存 WeakMap
- `promptTextCache` - 提示文本缓存 WeakMap
- `InVirtualListContext` - 虚拟列表上下文

---

## 5. 代码片段重点

### 5.1 VirtualMessageList 组件定义
```typescript
type Props = {
  messages: RenderableMessage[];
  scrollRef: RefObject<ScrollBoxHandle | null>;
  columns: number;
  itemKey: (msg: RenderableMessage) => string;
  renderItem: (msg: RenderableMessage, index: number) => React.ReactNode;
  extractSearchText?: (msg: RenderableMessage) => string;
  trackStickyPrompt?: boolean;
};
```

### 5.2 OffscreenFreeze 组件
```typescript
export function OffscreenFreeze({ children }: Props): React.ReactNode {
  'use no memo'

  const inVirtualList = useContext(InVirtualListContext);
  const [ref, { isVisible }] = useTerminalViewport();
  const cached = useRef(children);

  if (isVisible || inVirtualList) {
    cached.current = children;
  }

  return <Box ref={ref}>{cached.current}</Box>;
}
```

### 5.3 WeakMap 缓存策略
```typescript
const fallbackLowerCache = new WeakMap<RenderableMessage, string>();

function defaultExtractSearchText(msg: RenderableMessage): string {
  const cached = fallbackLowerCache.get(msg);
  if (cached !== undefined) return cached;

  const lowered = renderableSearchText(msg);
  fallbackLowerCache.set(msg, lowered);
  return lowered;
}
```

### 5.4 Sticky Prompt 缓存
```typescript
const promptTextCache = new WeakMap<RenderableMessage, string | null>();

function stickyPromptText(msg: RenderableMessage): string | null {
  const cached = promptTextCache.get(msg);
  if (cached !== undefined) return cached;

  const result = computeStickyPromptText(msg);
  promptTextCache.set(msg, result);
  return result;
}
```

### 5.5 MessageRow Props 设计
```typescript
export type Props = {
  message: RenderableMessage;
  isUserContinuation: boolean;
  hasContentAfter: boolean;
  tools: Tools;
  commands: Command[];
  verbose: boolean;
  inProgressToolUseIDs: Set<string>;
  streamingToolUseIDs: Set<string>;
};
```

### 5.6 JumpHandle 接口
```typescript
export type JumpHandle = {
  warmSearchIndex: () => Promise<number>;
  setSearchQuery: (q: string) => void;
  nextMatch: () => void;
  prevMatch: () => void;
};
```
