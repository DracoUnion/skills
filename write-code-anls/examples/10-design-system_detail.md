# 10-design-system.md 细纲

## 一、标题层级结构

### 1. 设计系统与主题——构建统一的 UI 风格
- 学习目标（5点）
- 终端设计系统的挑战
  - 生活类比：黑白照片上色
- Theme 类型：颜色的"字典"
  - 品牌色 / 功能色 / 语义色 / Diff 色 / 界面色
- 可用的主题
  - dark / light / daltonized / ansi
- 颜色解析链
- ThemedText：语义化文本
  - 颜色优先级
- ThemedBox：语义化容器
  - resolveColor
- ThemeProvider：主题状态管理
  - 自动主题检测（OSC 11）
- 设计系统组件一览
- color() 工具函数
- 设计原则总结
- 动手练习
- 课程完结

## 二、关键知识点

1. **Theme 类型结构**
   - 品牌色: claude, claudeShimmer, permission, planMode
   - 功能色: text, inverseText, inactive, subtle, suggestion, background
   - 语义色: success, error, warning
   - Diff 色: diffAdded, diffRemoved, diffAddedDimmed, diffRemovedDimmed, diffAddedWord, diffRemovedWord
   - 界面色: promptBorder, bashBorder, selectionBg, userMessageBackground

2. **可用主题**
   - dark: 深色
   - light: 浅色
   - light-daltonized / dark-daltonized: 色盲友好
   - light-ansi / dark-ansi: 16色兼容

3. **颜色解析链**
   - ThemedText → useTheme → getTheme → resolveColor → Text → ANSI

4. **ThemedText 优先级**
   - 明确 color > hoverColor > dimColor ? 'inactive' : undefined

5. **resolveColor 函数**
   - 原始颜色值 → 直接返回
   - 主题 key → 查表返回

6. **自动主题检测**
   - OSC 11 查询终端背景色
   - 判断亮度 → light/dark
   - 监听终端主题变化

7. **设计系统组件**
   - 基础: ThemedText, ThemedBox, Divider
   - 反馈: StatusIcon, ProgressBar, LoadingState
   - 交互: ListItem, Tabs, Dialog, FuzzyPicker
   - 布局: Pane, KeyboardShortcutHint, Byline
   - 特殊: Ratchet

8. **设计原则**
   - 语义化颜色
   - 主题可切换
   - 无障碍（daltonized）
   - 兼容性（ansi）
   - 自动检测
   - 实时预览
   - 渐进增强

## 三、源码文件路径

- `utils/theme.ts` - 主题定义
- `components/design-system/ThemedText.tsx` - 主题文本
- `components/design-system/ThemedBox.tsx` - 主题容器
- `components/design-system/ThemeProvider.tsx` - 主题 Provider
- `components/design-system/color.ts` - 颜色工具

## 四、类名、函数名、接口名

### 类型
- `Theme` - 主题类型
- `ThemeName` - 主题名称
- `ThemeSetting` - 主题设置

### 核心函数
- `getTheme()` - 获取主题
- `resolveColor()` - 解析颜色
- `color()` - 颜色工具函数
- `useTheme()` - 使用主题 Hook

### 组件
- `ThemeProvider` - 主题 Provider
- `ThemedText` - 主题文本
- `ThemedBox` - 主题容器
- `Divider` - 分隔线
- `StatusIcon` - 状态图标
- `ProgressBar` - 进度条
- `LoadingState` - 加载状态
- `ListItem` - 列表项
- `Tabs` - 标签页
- `Dialog` - 对话框
- `FuzzyPicker` - 模糊选择器
- `Pane` - 面板
- `KeyboardShortcutHint` - 快捷键提示
- `Byline` - 署名行
- `Ratchet` - 棘轮动画

### 常量
- `THEME_NAMES` - 主题名称数组
- `DEFAULT_THEME` - 默认主题

### 辅助函数
- `getSystemThemeName()` - 获取系统主题
- `colorize()` - 着色函数
- `parseRGB()` - 解析 RGB
