# 第 4 课：React 与 Ink——终端 UI 框架 - 细纲

## 文件信息
- **原文件**: part01-basics/04-react-and-ink.md
- **类型**: 基础入门
- **难度**: ★★☆☆☆

---

## 一、React 核心概念

### 1.1 组件化思想
- **核心理念**: 把界面拆分成独立的、可复用的"组件"
- **类比**: 乐高积木——每块积木是一个组件，可组合、可复用
- **Claude Code 应用**: 144 个 UI 组件

### 1.2 组件层次结构示例
```
App 组件（整个应用）
├── Header 组件
├── Spinner 组件
├── MessageList 组件
│   ├── Message 组件
│   └── Message 组件
└── InputBox 组件
```

### 1.3 传统思维 vs React 思维
| 传统思维 | React 思维 |
|----------|-----------|
| 直接操作页面元素 | 描述"界面应该长什么样" |
| 手动更新界面 | 数据变了，界面自动更新 |

---

## 二、JSX 语法

### 2.1 什么是 JSX
- JSX = JavaScript/TypeScript 中写类似 HTML 的标签
- 编译后变成 `React.createElement()` 调用

### 2.2 JSX 基本规则
| 规则 | 示例 | 说明 |
|------|------|------|
| 标签必须关闭 | `<Text>内容</Text>` | 有开始和结束标签 |
| 自关闭标签 | `<Box />` | 无子内容时使用 |
| 嵌入表达式 | `{name}` | 花括号内写 JavaScript |
| 属性赋值 | `width={80}` | 等号赋值 |
| 条件渲染 | `{isLoading ? <A/> : <B/>}` | 三元运算符 |

### 2.3 文件后缀区别
| 后缀 | 含义 | 示例 |
|------|------|------|
| `.ts` | 纯 TypeScript | `Tool.ts` |
| `.tsx` | TypeScript + JSX | `main.tsx`, `Spinner.tsx` |

---

## 三、组件的 Props 和 State

### 3.1 Props（属性）
- **定义**: 从父组件传入的只读数据
- **类比**: 函数的参数

```typescript
type GreetingProps = {
  name: string
  color?: string  // 可选属性
}

function Greeting({ name, color = "white" }: GreetingProps) {
  return <Text color={color}>你好，{name}！</Text>
}
```

### 3.2 Claude Code 中的真实 Props
```typescript
// Spinner.tsx
type Props = {
  mode: SpinnerMode                    // 必填
  loadingStartTimeRef: React.RefObject<number>
  spinnerTip?: string                  // 可选（?）
  overrideColor?: keyof Theme | null   // 可选
  verbose: boolean                     // 必填
  hasActiveTools?: boolean             // 可选
}
```
- **源码来源**: `src/components/Spinner.tsx`

```typescript
// SearchBox.tsx
type Props = {
  query: string
  placeholder?: string
  isFocused: boolean
  isTerminalFocused: boolean
  prefix?: string
  width?: number | string
  cursorOffset?: number
  borderless?: boolean
}
```
- **源码来源**: `src/components/SearchBox.tsx`

### 3.3 State（状态）
- **定义**: 组件内部的可变数据
- **特点**: State 改变时，组件自动重新渲染

```typescript
import { useState } from 'react'

function Counter() {
  const [count, setCount] = useState(0)
  return <Text>计数：{count}</Text>
}
```

### 3.4 Props vs State 对比
| | Props | State |
|---|-------|-------|
| 来源 | 父组件传入 | 组件内部创建 |
| 能否修改 | 不能（只读） | 能（通过 setter） |
| 变化效果 | 重新渲染 | 重新渲染 |

---

## 四、React Hooks

### 4.1 什么是 Hooks
- Hooks = 以 `use` 开头的特殊函数
- 让函数组件拥有状态和其他 React 功能

### 4.2 useState — 管理状态
```typescript
const [value, setValue] = useState(初始值)
const [name, setName] = useState("Claude")
const [count, setCount] = useState(0)
```

### 4.3 useEffect — 处理副作用
```typescript
useEffect(() => {
  // 组件挂载后执行
  const timer = setInterval(...)
  
  // 返回清理函数（组件卸载时执行）
  return () => clearInterval(timer)
}, [])  // 空数组 = 只执行一次
```

### 4.4 useMemo — 缓存计算结果
```typescript
const sortedItems = useMemo(() => {
  return items.sort((a, b) => a.name.localeCompare(b.name))
}, [items])  // items 变化时才重新计算
```

### 4.5 Claude Code 的自定义 Hooks（85 个）
| Hook 名称 | 作用 | 源码位置 |
|-----------|------|----------|
| `useTerminalSize` | 获取终端窗口宽高 | `src/hooks/` |
| `useCanUseTool` | 检查工具使用权限 | `src/hooks/` |
| `useSettings` | 获取用户设置 | `src/hooks/` |
| `useBlink` | 光标闪烁效果 | `src/hooks/` |
| `useCancelRequest` | 处理取消请求 | `src/hooks/` |
| `useTasksV2` | 管理任务列表 | `src/hooks/` |

---

## 五、Ink：React 的终端渲染器

### 5.1 Ink 是什么
- **定义**: 让 React 组件能在终端中渲染的库
- **原理**: React + Ink → 终端文字界面

### 5.2 浏览器 vs 终端
| 环境 | React 渲染目标 | 组件 |
|------|----------------|------|
| 浏览器 | HTML 元素 | `<div>`, `<span>`, `<button>` |
| 终端 | 终端字符 | `<Box>`, `<Text>`, `<Link>` |

### 5.3 Ink 核心组件
| Ink 组件 | 作用 | 类比 HTML |
|----------|------|----------|
| `<Box>` | 容器/布局 | `<div>` |
| `<Text>` | 文字 | `<span>` |
| `<Link>` | 可点击链接 | `<a>` |
| `<Ansi>` | ANSI 转义序列 | - |

### 5.4 Box 组件布局属性
```typescript
// 水平排列（默认）
<Box flexDirection="row">
  <Text>左</Text>
  <Text>右</Text>
</Box>

// 垂直排列
<Box flexDirection="column">
  <Text>上</Text>
  <Text>下</Text>
</Box>

// 带边框和内边距
<Box borderStyle="round" padding={1} width={30}>
  <Text>内容</Text>
</Box>
```

### 5.5 Text 组件样式属性
```typescript
<Text bold>粗体</Text>
<Text italic>斜体</Text>
<Text underline>下划线</Text>
<Text color="green">绿色</Text>
<Text color="red">红色</Text>
<Text dimColor>暗淡</Text>
<Text inverse>反色</Text>
<Text strikethrough>删除线</Text>
```

---

## 六、为什么选择 React + Ink

### 6.1 传统终端 UI 方案的问题
| 方案 | 问题 |
|------|------|
| `ncurses`（C 库） | 需要写 C 语言，非常底层 |
| `blessed`（Node.js） | 已停止维护，API 复杂 |
| 手动输出字符 | 只适合简单输出，布局困难 |

### 6.2 React + Ink 的优势
| 优势 | 解释 |
|------|------|
| 声明式 UI | 描述"界面应该是什么样子" |
| 组件复用 | 写一次，到处使用 |
| 状态管理 | 数据变了，UI 自动更新 |
| 团队熟悉 | 前端开发者都会 React |
| TypeScript 友好 | 完美支持类型检查 |

### 6.3 Claude Code 的 Ink 定制
Claude Code 在 `src/ink/` 目录维护了一套**深度定制的 Ink 实现**（96 个文件）：

| 文件/模块 | 功能 |
|-----------|------|
| `reconciler.ts` | 自定义渲染器 |
| `layout/` | 自定义布局引擎 |
| `selection.ts` | 终端文本选择 |
| `searchHighlight.ts` | 搜索高亮 |
| `hooks/use-input.ts` | 键盘输入处理 |
| `terminal-querier.ts` | 终端能力查询 |

---

## 七、Claude Code 的组件结构

### 7.1 组件目录概览
`src/components/` 包含 **144 个组件文件**

### 7.2 UI 基础组件
| 组件 | 作用 |
|------|------|
| `Spinner.tsx` | 加载动画 |
| `SearchBox.tsx` | 搜索框 |
| `BaseTextInput.tsx` | 文本输入框 |
| `CompactSummary.tsx` | 紧凑摘要显示 |
| `HighlightedCode/` | 代码语法高亮 |

### 7.3 功能组件
| 组件 | 作用 |
|------|------|
| `App.tsx` | 顶层应用容器 |
| `MessageResponse.tsx` | AI 回复消息显示 |
| `ContextVisualization.tsx` | 上下文可视化 |
| `CostThresholdDialog.tsx` | 费用超限提醒 |
| `AutoUpdater.tsx` | 自动更新提示 |

### 7.4 对话框组件
| 组件 | 作用 |
|------|------|
| `AutoModeOptInDialog.tsx` | 自动模式确认 |
| `BypassPermissionsModeDialog.tsx` | 绕过权限确认 |
| `ClaudeMdExternalIncludesDialog.tsx` | 外部文件引用确认 |

### 7.5 设计系统
`src/components/design-system/` 下的主题组件：
| 组件 | 作用 |
|------|------|
| `ThemedBox` | 带主题的容器 |
| `ThemedText` | 带主题的文字 |
| `ThemeProvider` | 主题提供者 |

---

## 八、完整组件示例

### 8.1 SearchBox 组件简化版
```tsx
import React from 'react'
import { Box, Text } from '../ink.js'

type Props = {
  query: string
  placeholder?: string
  isFocused: boolean
}

export function SearchBox({ query, placeholder = "搜索...", isFocused }: Props) {
  return (
    <Box
      borderStyle="round"
      borderColor={isFocused ? "blue" : undefined}
      paddingX={1}
    >
      <Text dimColor={!isFocused}>
        {"⌕ "}
        {query
          ? <Text>{query}</Text>
          : <Text dimColor>{placeholder}</Text>
        }
      </Text>
    </Box>
  )
}
```

---

## 九、小结

| 要点 | 内容 |
|------|------|
| React | UI 构建库，核心思想是"组件化" |
| JSX | 在 TypeScript 中写类似 HTML 的标签 |
| Props | 从父组件传入的只读数据 |
| State | 组件内部的可变数据，变化时触发重新渲染 |
| Hooks | `useState`、`useEffect`、`useMemo` 等 |
| Ink | React 的终端渲染器，用 `<Box>` 和 `<Text>` |
| 为什么 React+Ink | 声明式、组件化、TypeScript 友好 |
| 组件数量 | 144 个组件文件 |

---

## 十、动手练习

### 练习 1：识别组件结构
```bash
ls src/components/ | head -30
```
1. 哪些文件名像是"对话框"组件？
2. 哪些文件名像是"显示/展示"组件？
3. 为什么有些是单个 `.tsx` 文件，有些是文件夹？

### 练习 2：阅读 Props 定义
打开 `src/components/Spinner.tsx`：
1. `Spinner` 接受哪些属性？
2. 哪些是必填的？哪些是可选的？
3. `SpinnerMode` 从哪里导入？

### 练习 3：理解 JSX
分析一段 JSX 代码，描述终端显示效果。

### 练习 4：探索 Ink 封装
```bash
ls src/ink/
ls src/ink/ | wc -l
```
1. 有多少个文件？
2. 从文件名猜功能？
3. 为什么自己维护 Ink 实现？

### 练习 5：追踪 ink.ts 导出
打开 `src/ink.ts`：
1. 从 `./ink/root.js` 导入了什么？
2. `withTheme` 函数的作用？
3. 这个文件的作用？

---

## 十一、关联文件

### 11.1 上一章
- [03-typescript-basics.md](03-typescript-basics.md) - TypeScript 基础

### 11.2 下一章
- [../part02-architecture/01-what-is-software-architecture.md](../part02-architecture/01-what-is-software-architecture.md) - 软件架构

---

*此细纲由 Claude Code 自动生成*
