# 03-dual-app-architecture.md 细纲

## 一、标题层级结构

### 1. 双层 App 架构——业务 App + Ink App
- 学习目标（5点）
- 为什么需要两层 App？
  - 生活类比：酒店的前台与后勤
- 业务层 App：Context Provider 的洋葱
  - FpsMetricsProvider
  - StatsProvider
  - AppStateProvider
- 基础设施层 Ink App：终端的"管家"
  - 生命周期管理
  - 输入处理
- 完整启动流程
- Context 数据流示例
  - ThemeProvider → ThemedText
- 为什么不合并成一个 App？
- React Compiler 优化
  - _c() 和 $[0] 缓存
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **双层架构**
   - 业务层: `components/App.tsx` - 应用状态、FPS、统计
   - 基础设施层: `ink/components/App.tsx` - 终端 I/O、光标、渲染

2. **Provider 洋葱模型**
   - FpsMetricsProvider（最外层）
   - StatsProvider（中间层）
   - AppStateProvider（最内层）
   - children（实际界面组件）

3. **基础设施层职责**
   - 终端控制：隐藏/恢复光标、设置 raw 模式
   - 输入处理：读取 stdin → 解析按键 → 分发事件
   - 渲染管理：触发 React 更新 → Yoga 布局 → Diff 输出

4. **Context 数据流**
   - ThemeProvider → useTheme() → ThemedText
   - resolveColor: 主题 key → 实际颜色

5. **分层好处**
   - 关注点分离
   - 可测试性
   - 复用性
   - 渲染优化
   - 代码可读性

6. **React Compiler 优化**
   - 自动 useMemo/useCallback
   - $ 数组是缓存槽位
   - 依赖项变化时才重新计算

## 三、源码文件路径

- `components/App.tsx` - 业务层 App
- `ink/components/App.tsx` - 基础设施层 App
- `components/design-system/ThemedText.tsx` - 主题文本
- `components/design-system/ThemeProvider.tsx` - 主题 Provider

## 四、类名、函数名、接口名

### 业务层
- `App` - 业务层 App 组件
- `FpsMetricsProvider` - FPS 监控 Provider
- `StatsProvider` - 统计 Provider
- `AppStateProvider` - 应用状态 Provider
- `useTheme()` - 使用主题 Hook

### 基础设施层
- `InkApp` - Ink App 类组件
- `handleReadable` - 可读事件处理
- `processInput` - 输入处理
- `discreteUpdates` - 离散更新

### 辅助函数
- `resolveColor()` - 解析颜色
- `getTheme()` - 获取主题
- `_c()` - React Compiler 缓存函数
