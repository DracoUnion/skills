# 07-spinner-animation.md 细纲

## 一、标题层级结构

### 1. Spinner 加载动画的性能设计
- 学习目标（5点）
- 终端动画的挑战
  - 生活类比：老式翻页钟 vs 数字钟
- Spinner 字符动画
  - DEFAULT_CHARACTERS
  - SPINNER_FRAMES
- 共享时钟：useAnimationFrame
  - ClockContext
  - keepAlive
- 卡顿检测：颜色渐变反馈
  - ERROR_RED
  - interpolateColor
- 减弱动效（Reduced Motion）
  - REDUCED_MOTION_DOT
  - 2秒周期
- 性能对比
- 动画系统架构
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **终端动画挑战**
   - 每帧需要: React reconcile + Yoga 布局 + 字符网格 + Diff + stdout 写入
   - 成本远高于浏览器
   - 核心原则: 尽可能少触发重渲染

2. **Spinner 帧动画**
   - DEFAULT_CHARACTERS: Braille 图案
   - SPINNER_FRAMES: 正序+反序
   - frame % length 取当前帧

3. **共享时钟 ClockContext**
   - 所有动画从同一时钟读取
   - 保持同步旋转
   - 按需驱动: keepAlive 订阅者

4. **useAnimationFrame**
   - isVisible: 离屏暂停
   - intervalMs: 节流控制
   - 失焦减速

5. **卡顿检测**
   - stalledIntensity: 0-1
   - 从主题色渐变到 ERROR_RED
   - 线性插值: `base * (1-t) + red * t`

6. **减弱动效**
   - prefersReducedMotion 设置
   - 慢闪烁圆点 ●
   - 2秒周期: 1秒亮 + 1秒暗

7. **性能优化**
   - 120ms 间隔（约 8fps）
   - 共享时钟
   - 离屏暂停
   - 失焦减速

## 三、源码文件路径

- `components/Spinner/SpinnerGlyph.tsx` - Spinner 组件
- `ink/hooks/use-animation-frame.ts` - 动画帧 Hook
- `components/Spinner/utils.ts` - Spinner 工具函数

## 四、类名、函数名、接口名

### 核心 Hook
- `useAnimationFrame()` - 动画帧 Hook
- `useTerminalViewport()` - 终端视口

### 组件
- `SpinnerGlyph` - Spinner 组件

### 常量
- `DEFAULT_CHARACTERS` - 默认 Spinner 字符
- `SPINNER_FRAMES` - 帧数组
- `ERROR_RED` = { r: 171, g: 43, b: 63 }
- `REDUCED_MOTION_DOT` = '●'
- `REDUCED_MOTION_CYCLE_MS` = 2000

### 辅助函数
- `interpolateColor()` - 颜色插值
- `parseRGB()` - 解析 RGB
- `toRGBColor()` - 转为 RGB 颜色
- `hueToRgb()` - HUE 转 RGB
- `getDefaultCharacters()` - 获取默认字符

### 类型
- `ClockContext` - 时钟上下文
- `AnimationFrameOptions` - 动画帧选项
