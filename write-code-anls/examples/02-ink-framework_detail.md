# 02-ink-framework.md 细纲

## 一、标题层级结构

### 1. Ink 框架入门——React 渲染到终端
- 学习目标（5点）
- Ink 是什么？React 的"终端渲染器"
  - 生活类比：翻译官
- `<Box>` 组件：终端中的 `<div>`
  - flexDirection / flexWrap / flexGrow
- `<Text>` 组件：终端中的"画笔"
  - 样式映射到 ANSI
- 自定义 Reconciler：Ink 的核心引擎
  - createInstance
  - createTextInstance
  - resetAfterCommit
  - commitUpdate
- Yoga 布局引擎：终端中的 Flexbox
- Ink DOM：虚拟的"终端 DOM"
- 事件系统：键盘、鼠标、焦点
  - handleReadable
  - processInput
  - parseMultipleKeypresses
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **Ink 定位**
   - React 的终端渲染器
   - 将 JSX 翻译为字符网格
   - Claude Code 使用深度定制版本

2. **Box 组件**
   - 等价于 `<div style="display:flex">`
   - 支持 flexDirection, flexWrap, flexGrow, gap
   - 支持 borderStyle, padding, margin

3. **Text 组件**
   - color, backgroundColor
   - bold, dim, italic, underline, strikethrough, inverse
   - wrap 模式
   - bold 和 dim 互斥

4. **自定义 Reconciler**
   - createInstance: 创建 DOM 节点
   - createTextInstance: 创建文本节点
   - resetAfterCommit: 提交后重置，触发 Yoga 布局和渲染
   - commitUpdate: 更新节点属性

5. **Yoga 布局引擎**
   - Facebook 的跨平台 Flexbox 引擎
   - 计算每个元素在字符网格中的位置
   - 处理换行、中文字符、Emoji 宽度

6. **Ink DOM 结构**
   - nodeName: 'ink-box' | 'ink-text'
   - style: Styles
   - yogaNode: YogaNode
   - parentNode / childNodes

7. **事件系统**
   - stdin readable 事件
   - parseMultipleKeypresses 解析按键
   - discreteUpdates 批量处理

## 三、源码文件路径

- `ink/reconciler.ts` - 自定义 Reconciler
- `ink/components/Box.tsx` - Box 组件
- `ink/components/Text.tsx` - Text 组件
- `ink/dom.ts` - DOM 节点结构
- `ink/components/App.tsx` - 事件处理

## 四、类名、函数名、接口名

### 核心函数
- `createReconciler()` - 创建 Reconciler
- `createNode()` - 创建 DOM 节点
- `createTextNode()` - 创建文本节点
- `applyProp()` - 应用属性
- `setStyle()` - 设置样式
- `setAttribute()` - 设置属性

### 组件
- `Box` - 布局容器
- `Text` - 文本组件

### 类型
- `DOMElement` - DOM 元素
- `TextNode` - 文本节点
- `Styles` - 样式类型
- `TextStyles` - 文本样式

### Reconciler 配置
- `createInstance` - 创建实例
- `createTextInstance` - 创建文本实例
- `resetAfterCommit` - 提交后重置
- `commitUpdate` - 提交更新
