# 09-thinking-mode.md 细纲

## 一、标题层级结构

### 1. Thinking 扩展思维三种模式
- 学习目标（5点）
- 生活类比：考试中的思考时间
- 三种模式对比
  - disabled / enabled / adaptive
- 源码解析：ThinkingConfig 类型（第10-13行）
  - 默认配置 shouldEnableThinkingByDefault（第146-162行）
  - QueryEngine 中的配置
- Thinking 的传递路径
- 模型支持矩阵
  - modelSupportsThinking（第90-110行）
  - modelSupportsAdaptiveThinking（第113-144行）
- Ultrathink — 深度思考关键词
  - isUltrathinkEnabled（第19-24行）
  - hasUltrathinkKeyword（第29-31行）
  - 彩虹色显示
- Thinking 对 Token 消耗的影响
  - Thinking 块的 Token 计数
  - Token 计数时的 Thinking 处理
- Thinking 的"规则"
- Thinking 流程图
- 配置优先级
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **三种 Thinking 模式**
   - `disabled`: 不使用扩展思维，直接回答
   - `enabled`: 使用固定预算的思维 Token
   - `adaptive`: AI 自行决定是否需要深度思考

2. **ThinkingConfig 类型**
   - 联合类型: `{ type: 'adaptive' } | { type: 'enabled'; budgetTokens: number } | { type: 'disabled' }`

3. **默认配置逻辑**
   - 环境变量 `MAX_THINKING_TOKENS` 最高优先级
   - 用户设置 `alwaysThinkingEnabled` 次优先级
   - 默认启用 adaptive 模式

4. **模型支持矩阵**
   - Claude 3 系列: 不支持 Thinking
   - Claude 4 Haiku: 支持（1P），不支持 Adaptive
   - Claude 4 Sonnet: 支持 Thinking，不支持 Adaptive
   - Claude 4.6 Sonnet/Opus: 支持 Thinking 和 Adaptive

5. **Ultrathink 彩蛋**
   - 关键词: `ultrathink`
   - 激活深度思维模式
   - UI 显示彩虹色 thinking 指示器
   - 使用正则 `/\bultrathink\b/i` 检测

6. **Thinking 三条规则**
   - 规则1: 包含 thinking/redacted_thinking 的消息必须用 max_thinking_length > 0
   - 规则2: thinking 块不能是消息的最后一个块
   - 规则3: thinking 块必须在整个工具调用链中保留

7. **Token 计数处理**
   - thinking 块: 按文本内容计数
   - redacted_thinking 块: 按 data 内容计数
   - 包含 thinking 的请求需要特殊处理

8. **配置优先级**
   - 环境变量 > 用户设置 > SDK 传入 > 默认值

## 三、源码文件路径

- `src/utils/thinking.ts` - Thinking 模式配置
- `src/services/tokenEstimation.ts` - Thinking Token 计数

## 四、类名、函数名、接口名

### 核心类型
- `ThinkingConfig` - Thinking 配置类型（第10-13行）

### 核心函数
- `shouldEnableThinkingByDefault()` - 默认启用判断（第146-162行）
- `modelSupportsThinking()` - 模型是否支持 Thinking（第90-110行）
- `modelSupportsAdaptiveThinking()` - 是否支持 Adaptive（第113-144行）
- `isUltrathinkEnabled()` - 是否启用 ultrathink（第19-24行）
- `hasUltrathinkKeyword()` - 检测 ultrathink 关键词（第29-31行）
- `findThinkingTriggerPositions()` - 查找关键词位置（第36-58行）

### 辅助函数
- `getRainbowColor()` - 获取彩虹色（第60-86行）
- `hasThinkingBlocks()` - 检查是否包含 thinking 块

### 常量
- `RAINBOW_COLORS` - 彩虹色数组
- `TOKEN_COUNT_THINKING_BUDGET` - thinking 计数预算
- `MAX_THINKING_TOKENS` - 环境变量名

### 类型
- `ThinkingBlock` - thinking 块类型
- `RedactedThinkingBlock` - 编辑过的 thinking 块
