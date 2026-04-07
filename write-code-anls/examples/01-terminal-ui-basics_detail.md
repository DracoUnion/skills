# 01-terminal-ui-basics.md 细纲

## 一、标题层级结构

### 1. 终端 UI 基础——从 console.log 到 React
- 学习目标（5点）
- 终端不是"黑底白字"那么简单
  - 生活类比：打字机 vs 画板
  - 终端的本质：字符网格（80×24）
- ANSI 转义码：终端的"画笔"
  - 颜色控制
  - 光标控制
  - HIDE_CURSOR / SHOW_CURSOR
- 从 console.log 到 React：思维跃迁
  - 传统方式：命令式
  - React 方式：声明式
- 架构全景图
- Ink 渲染器：字符网格的"画家"
  - createRenderer
  - Output 对象
- 双缓冲与 Diff：消除闪烁
  - frontFrame / backFrame
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **终端本质**
   - 二维字符网格（80列 × 24行）
   - 每个格子可以放一个字符+样式

2. **ANSI 转义码**
   - 颜色: `\x1b[31m`（红色）
   - 光标移动: `\x1b[5;10H`
   - 清除行: `\x1b[2K`
   - 隐藏光标: `\x1b[?25l`
   - 显示光标: `\x1b[?25h`

3. **声明式 vs 命令式**
   - 命令式: 告诉终端"怎么做"
   - 声明式: 描述"想要什么"，React 计算变更

4. **Ink 渲染管线**
   - React 组件树 → Reconciler → Yoga 布局 → Output → Diff → 终端

5. **双缓冲策略**
   - frontFrame: 当前显示
   - backFrame: 后台计算
   - 只写入变化部分，避免闪烁

6. **Output 对象**
   - 维护字符网格（screen buffer）
   - renderNodeToOutput 递归写入

## 三、源码文件路径

- `ink/termio/dec.ts` - DEC 私有模式控制
- `ink/termio/csi.ts` - CSI 序列
- `ink/termio/sgr.ts` - SGR 样式控制
- `ink/renderer.ts` - 渲染器核心
- `ink/components/App.tsx` - App 组件

## 四、类名、函数名、接口名

### 核心函数
- `createRenderer()` - 创建渲染器
- `renderNodeToOutput()` - 渲染节点到输出

### 常量
- `HIDE_CURSOR` = `'\x1b[?25l'`
- `SHOW_CURSOR` = `'\x1b[?25h'`

### 类型
- `Renderer` - 渲染器类型
- `Output` - 输出对象
- `DOMElement` - DOM 元素类型

### 类
- `App` - Ink App 组件
- `Output` - 字符网格管理
