# 08-token-counting.md 细纲

## 一、标题层级结构

### 1. Token 计数与成本控制
- 学习目标（5点）
- 生活类比：Token 就像超市的购物点数
- Token 计数架构
  - 粗估 / 精确计数 / Haiku 回退
- 粗估算法 — 快速但不精确
  - 基本粗估 roughTokenCountEstimation（第203-208行）
  - 文件类型感知 bytesPerTokenForFileType（第215-224行）
  - 消息级粗估
- 精确计数 — 调用 API
  - countMessagesTokensWithAPI（第140-201行）
  - Haiku 回退 countTokensViaHaikuFallback（第251-325行）
- Usage 流转 — Token 的"记账"
  - QueryEngine 中的 Usage 追踪（第788-816行）
  - Usage 的组成
- 预算控制 — maxBudgetUsd
  - 检查预算（第972-1002行）
  - 成本计算
- 自动压缩与 Token 的关系
  - Token 告警状态
  - queryLoop 中的阻塞检查（第637-648行）
- 结构化输出的重试限制
- Token Budget — 自动继续机制
- Token 计数完整流程
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **三种计数方式**
   - 粗估: 字符数 ÷ 4（JSON ÷ 2）
   - 精确计数: 调用 countTokens API
   - Haiku 回退: 用小模型间接计数

2. **粗估算法**
   - 标准文本: 字符数 ÷ 4
   - JSON: 字符数 ÷ 2（更多单字符 Token）
   - 图片/PDF: 固定 2000

3. **精确计数 API**
   - `anthropic.beta.messages.countTokens()`
   - 失败时返回 null，降级到粗估

4. **Haiku 回退**
   - 主模型 countTokens 不可用时使用
   - 用 max_tokens=1 发请求，只看 usage
   - 包含缓存 Token 计算

5. **Usage 组成**
   - `input_tokens`: 输入 Token
   - `output_tokens`: 输出 Token
   - `cache_creation_input_tokens`: 缓存创建 Token
   - `cache_read_input_tokens`: 缓存读取 Token

6. **预算控制**
   - `maxBudgetUsd` 配置
   - 每轮循环后检查
   - 超预算时返回 `error_max_budget_usd`

7. **Token 告警状态**
   - < 50%: 正常
   - 50-80%: 警告
   - 80-95%: 高危，触发自动压缩
   - > 95%: 阻塞，不允许新请求

8. **Token Budget 自动继续**
   - 预算内自动继续工作
   - `token_budget_continuation` transition

## 三、源码文件路径

- `src/services/tokenEstimation.ts` - Token 估算
- `src/QueryEngine.ts` - Usage 追踪和预算控制

## 四、类名、函数名、接口名

### 核心函数
- `roughTokenCountEstimation()` - 粗估 Token 数（第203-208行）
- `countMessagesTokensWithAPI()` - API 精确计数（第140-201行）
- `countTokensViaHaikuFallback()` - Haiku 回退计数（第251-325行）
- `bytesPerTokenForFileType()` - 文件类型感知（第215-224行）

### 辅助函数
- `roughTokenCountEstimationForBlock()` - 消息块粗估
- `hasThinkingBlocks()` - 检查是否包含 thinking 块
- `calculateTokenWarningState()` - 计算 Token 警告状态
- `checkTokenBudget()` - 检查 Token 预算

### 类型
- `Usage` - 用量类型
- `NonNullableUsage` - 非空用量类型

### 常量
- `BYTES_PER_TOKEN` = 4 - 每 Token 字节数
- `BYTES_PER_TOKEN_JSON` = 2 - JSON 每 Token 字节数
- `TOKEN_COUNT_THINKING_BUDGET` - thinking 计数预算
- `FLOOR_OUTPUT_TOKENS` = 3000 - 输出 Token 下限
