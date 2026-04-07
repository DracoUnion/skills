# 第六课：终端魔法屏 —— React+Ink 终端 UI 解析 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第六课：终端魔法屏 —— React+Ink 终端 UI 解析

### 1.2 二级标题
- 学习目标
- 一、生活类比：在画布上作画
- 二、技术架构总览
- 三、Ink 核心模块
- 四、核心组件库
- 五、Yoga 布局引擎
- 六、事件处理系统
- 七、Hooks 系统
- 八、应用层组件
- 九、渲染优化
- 十、ANSI 渲染细节
- 十一、动手练习
- 十二、本课小结
- 下节预告

### 1.3 三级标题
- 3.1 自定义 Reconciler
- 3.2 DOM 节点
- 3.3 渲染管线
- 4.1 基础组件
- 4.2 Box 组件：终端中的 Flexbox
- 4.3 ScrollBox 组件
- 5.1 什么是 Yoga？
- 5.2 布局计算流程
- 6.1 键盘输入
- 6.2 事件分发
- 6.3 焦点管理
- 7.1 核心 Hooks
- 7.2 动画 Hook
- 8.1 App 组件
- 8.2 Claude Code 的业务组件
- 8.3 终端尺寸上下文
- 9.1 差异渲染
- 9.2 节点缓存
- 9.3 文本宽度计算
- 9.4 渲染流程
- 10.1 颜色与样式
- 10.2 边框渲染
- 10.3 超链接

---

## 2. 关键知识点

### 2.1 技术栈
- **React** - 声明式 UI
- **Ink** - 终端渲染器
- **Yoga** - 弹性布局引擎（CSS Flexbox 的 C 实现）

### 2.2 渲染管线
```
React 组件更新 → Reconciler 差异 → DOM 树更新 → Yoga 布局计算 → 渲染到 Output → 差异比较 → ANSI 输出到终端
```

### 2.3 核心组件
| 组件 | 功能 |
|------|------|
| `Box` | 弹性盒子布局（类似 CSS Flexbox） |
| `Text` | 文本渲染（颜色、粗体、下划线） |
| `ScrollBox` | 可滚动容器 |
| `Button` | 可点击按钮 |
| `Link` | 超链接 |
| `Spacer` | 间距占位 |
| `Newline` | 换行 |

### 2.4 Yoga 布局
- 支持：`flexDirection`, `justifyContent`, `alignItems`, `padding`, `margin`
- 将终端的行列坐标映射到 Yoga 的布局系统

### 2.5 事件系统
- `parse-keypress.ts` - 解析终端原始输入
- `emitter.ts` - 事件发射器
- `dispatcher.ts` - 事件分发器
- `focus.ts` - 焦点管理

### 2.6 核心 Hooks
| Hook | 功能 |
|------|------|
| `useInput` | 监听键盘输入 |
| `useTerminalViewport` | 获取终端尺寸 |
| `useStdin` | 原始标准输入 |
| `useSelection` | 文本选择 |
| `useTerminalFocus` | 终端窗口焦点状态 |
| `useAnimationFrame` | 动画帧（类似 requestAnimationFrame） |

### 2.7 渲染优化
- **差异渲染** - 不是每次都清屏重绘，只更新变化部分
- **节点缓存** - 缓存 DOM 节点的渲染结果
- **文本宽度计算** - 处理 CJK 字符（宽度 2）、emoji、ANSI 转义序列

---

## 3. 涉及的源码文件路径

### 3.1 Ink 核心模块
- `ink/reconciler.ts` - 自定义 React Reconciler
- `ink/dom.ts` - 终端 DOM 节点
- `ink/output.ts` - 输出处理
- `ink/node-cache.ts` - 节点缓存

### 3.2 Ink 组件
- `ink/components/Box.tsx` - 盒子布局组件
- `ink/components/Text.tsx` - 文本组件
- `ink/components/ScrollBox.tsx` - 滚动容器
- `ink/components/Button.tsx` - 按钮组件
- `ink/components/Link.tsx` - 链接组件
- `ink/components/App.tsx` - 顶层应用组件
- `ink/components/TerminalSizeContext.tsx` - 终端尺寸上下文

### 3.3 Ink 布局
- `ink/layout/yoga.ts` - Yoga 集成
- `ink/layout/engine.ts` - 布局引擎
- `ink/layout/geometry.ts` - 几何计算

### 3.4 Ink 事件
- `ink/parse-keypress.ts` - 按键解析
- `ink/events/emitter.ts` - 事件发射器
- `ink/events/dispatcher.ts` - 事件分发器
- `ink/events/keyboard-event.ts` - 键盘事件
- `ink/events/click-event.ts` - 点击事件
- `ink/events/focus-event.ts` - 焦点事件
- `ink/events/input-event.ts` - 输入事件
- `ink/focus.ts` - 焦点管理

### 3.5 Ink Hooks
- `ink/hooks/use-input.ts` - 输入 Hook
- `ink/hooks/use-terminal-viewport.ts` - 终端视口 Hook
- `ink/hooks/use-stdin.ts` - 标准输入 Hook
- `ink/hooks/use-selection.ts` - 选择 Hook
- `ink/hooks/use-terminal-focus.ts` - 终端焦点 Hook
- `ink/hooks/use-animation-frame.ts` - 动画帧 Hook

### 3.6 Ink 工具
- `ink/colorize.ts` - 颜色转换
- `ink/render-border.ts` - 边框渲染
- `ink/stringWidth.ts` - 字符串宽度计算
- `ink/wrapAnsi.ts` - ANSI 感知换行
- `ink/supports-hyperlinks.ts` - 超链接支持检测

### 3.7 业务组件
- `components/App.tsx` - 主应用
- `components/CompactSummary.tsx` - 压缩摘要显示
- `components/ContextVisualization.tsx` - 上下文可视化
- `components/CoordinatorAgentStatus.tsx` - 协调者代理状态
- `components/Spinner.tsx` - 加载动画
- `components/PermissionDialog.tsx` - 权限确认弹窗
- `components/DiagnosticsDisplay.tsx` - 诊断信息

---

## 4. 类名、函数名、接口名

### 4.1 组件
- `Box` - 盒子布局组件
- `Text` - 文本组件
- `ScrollBox` - 滚动容器组件
- `Button` - 按钮组件
- `Link` - 链接组件
- `Spacer` - 间距组件
- `Newline` - 换行组件
- `App` - 顶层应用组件

### 4.2 Hooks
- `useInput(handler)` - 输入 Hook
- `useTerminalViewport()` - 终端视口 Hook
- `useStdin()` - 标准输入 Hook
- `useSelection()` - 选择 Hook
- `useTerminalFocus()` - 终端焦点 Hook
- `useAnimationFrame(callback)` - 动画帧 Hook

### 4.3 类型/接口
- `ScrollBoxHandle` - 滚动框句柄
- `TerminalSize` - 终端尺寸

---

## 5. 代码片段重点

### 5.1 Box 组件使用示例
```tsx
<Box flexDirection="column" padding={1} borderStyle="round">
  <Box flexDirection="row" justifyContent="space-between">
    <Text bold color="green">Claude Code</Text>
    <Text dimColor>v1.0.0</Text>
  </Box>
  <Box marginTop={1}>
    <Text>正在分析代码...</Text>
  </Box>
</Box>
```

### 5.2 useInput Hook
```typescript
useInput((input, key) => {
  if (key.return) handleSubmit();
  if (key.escape) handleCancel();
});
```

### 5.3 useTerminalViewport Hook
```typescript
const { columns, rows } = useTerminalViewport();
```

### 5.4 useAnimationFrame Hook
```typescript
useAnimationFrame(() => {
  setFrame(prev => prev + 1);
});
```

### 5.5 渲染管线
```typescript
// 源码：ink/output.ts（概念）
// 不是每次都清屏重绘
// 而是计算本次渲染和上次的差异
// 只更新变化的部分 → 减少闪烁
```

### 5.6 文本宽度计算
```typescript
// 源码：ink/stringWidth.ts
// 精确计算字符串显示宽度
// 处理：CJK 字符（宽度 2）、emoji、ANSI 转义序列
```

### 5.7 ANSI 感知换行
```typescript
// 源码：ink/wrapAnsi.ts
// ANSI 感知的文本换行
// 换行时保持颜色和样式的连续性
```

### 5.8 边框渲染
```typescript
// 源码：ink/render-border.ts
// 使用 Unicode 字符绘制边框
// 支持样式：single, double, round, bold, classic
// ╭──╮  ┌──┐  ╔══╗
// │  │  │  │  ║  ║
// ╰──╯  └──┘  ╚══╝
```
