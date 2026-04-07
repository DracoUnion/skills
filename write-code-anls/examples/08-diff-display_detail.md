# 08-diff-display.md 细纲

## 一、标题层级结构

### 1. 代码 Diff 展示——Rust NAPI 高亮
- 学习目标（5点）
- 终端中的代码 Diff
  - 生活类比：报纸的校对标记
- 为什么用 Rust？
  - Rust NAPI 模块
  - 性能对比
- StructuredDiff 组件架构
- WeakMap 缓存：精巧的内存管理
  - RENDER_CACHE
  - 为什么用 WeakMap
  - 缓存容量限制
- Gutter 宽度计算
- 双列分割渲染
  - NoSelect
  - RawAnsi
  - sliceAnsi
- 回退方案
- 渲染管线总结
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **Rust NAPI 优势**
   - JS 高亮: 1000行 ≈ 50-200ms
   - Rust NAPI: 1000行 ≈ 2-10ms
   - 快 10-50 倍，不占用 JS GC

2. **StructuredDiff 组件**
   - patch: StructuredPatchHunk
   - filePath: 语言检测
   - width: 终端宽度
   - skipHighlighting: 跳过高亮

3. **WeakMap 缓存**
   - RENDER_CACHE: WeakMap<patch, Map<key, CachedRender>>
   - patch 被 GC 时自动清理
   - 模块级缓存，组件卸载后仍在
   - 每 patch 最多 4 个变体

4. **缓存 key**
   - `${theme}|${width}|${dim}|${gutterWidth}|${firstLine}|${filePath}`

5. **Gutter 宽度计算**
   - maxLineNumber = max(oldStart+oldLines, newStart+newLines)
   - gutterWidth = digits + 3

6. **双列分割**
   - Gutter 列: NoSelect（不可选中）
   - Content 列: RawAnsi（直接输出）
   - sliceAnsi 按字符位置分割

7. **回退方案**
   - Rust NAPI 不可用时
   - 纯 JS 简单 Diff
   - 无语法高亮，只有行级标记

## 三、源码文件路径

- `components/StructuredDiff.tsx` - Diff 组件
- `components/StructuredDiffFallback.tsx` - 回退组件
- `napi-rs/` - Rust NAPI 模块

## 四、类名、函数名、接口名

### 核心组件
- `StructuredDiff` - Diff 展示组件
- `StructuredDiffFallback` - 回退组件
- `RawAnsi` - 原始 ANSI 输出
- `NoSelect` - 不可选中包装

### 缓存
- `RENDER_CACHE` - WeakMap 缓存
- `CachedRender` - 缓存条目类型

### 辅助函数
- `renderColorDiff()` - 渲染彩色 Diff
- `computeGutterWidth()` - 计算 Gutter 宽度
- `sliceAnsi()` - 分割 ANSI 字符串

### 常量
- `MAX_CACHE_VARIANTS` = 4

### 类型
- `StructuredPatchHunk` - Diff 补丁块
- `CachedRender` - 缓存渲染结果
  - lines: string[]
  - gutterWidth: number
  - gutters: string[] | null
  - contents: string[] | null
