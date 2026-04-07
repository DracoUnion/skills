# 07-retry-error-handling.md 细纲

## 一、标题层级结构

### 1. 重试与错误处理：指数退避详解
- 学习目标（5点）
- 生活类比：打电话占线的策略
- 重试架构全景
- 源码解析：withRetry 函数
  - 函数签名（第170-178行）
  - 主循环（第180-514行）
- 指数退避算法
  - 核心计算 getRetryDelay（第530-548行）
  - 延迟时间表
  - 随机抖动的作用
- 429 vs 529 — 两种过载的区别
  - 429 处理
  - 529 处理与模型回退
- 前台 vs 后台查询源
- 上下文溢出恢复
- 持久重试模式
- 重试通知链路
- shouldRetry — 重试决策树（第696-787行）
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **指数退避算法**
   - 基础延迟: 500ms
   - 公式: `min(500ms × 2^(attempt-1), 32000ms) + random(0, 25%)`
   - 第1次: 500ms, 第2次: 1s, 第3次: 2s, 第4次: 4s...
   - 封顶: 32秒

2. **随机抖动作用**
   - 避免重试风暴
   - 分散多个客户端的重试时间

3. **429 vs 529 处理**
   - 429 (Rate Limit): 尊重 retry-after 头 → 等待 → 重试
   - 529 (Overloaded): 指数退避 → 重试 → 3次后考虑回退

4. **模型回退机制**
   - 连续 3 次 529 错误后触发
   - `FallbackTriggeredError` 信号
   - queryLoop 捕获后切换到备用模型

5. **前台 vs 后台查询源**
   - 前台（repl_main_thread, sdk, agent 等）：重试
   - 后台（标题生成、摘要等）：不重试，减少压力

6. **上下文溢出恢复**
   - 解析 `max_tokens context overflow` 错误
   - 调整 max_tokens 后重试
   - 安全缓冲区: 1000 tokens

7. **持久重试模式**
   - `CLAUDE_CODE_UNATTENDED_RETRY` 环境变量
   - 最大退避: 5 分钟
   - 心跳间隔: 30 秒
   - 永不放弃

8. **shouldRetry 决策**
   - 模拟错误: 不重试
   - 持久模式下 429/529: 总是重试
   - 上下文溢出: 可以重试
   - 连接错误: 可以重试
   - 401/408/409/429/500+: 可以重试

## 三、源码文件路径

- `src/services/api/withRetry.ts` - 重试机制

## 四、类名、函数名、接口名

### 核心函数
- `withRetry()` - 重试包装函数（第170-178行）
- `getRetryDelay()` - 计算重试延迟（第530-548行）
- `shouldRetry()` - 重试决策（第696-787行）
- `getMaxRetries()` - 获取最大重试次数

### 错误类型
- `FallbackTriggeredError` - 触发模型回退
- `CannotRetryError` - 无法重试错误
- `APIUserAbortError` - 用户中止错误
- `APIError` - API 错误基类
- `APIConnectionError` - 连接错误

### 辅助函数
- `is529Error()` - 判断是否为 529 错误
- `isTransientCapacityError()` - 判断是否为容量错误
- `parseMaxTokensContextOverflowError()` - 解析上下文溢出错误
- `getRetryAfterMs()` - 获取 retry-after 时间

### 常量
- `BASE_DELAY_MS` = 500 - 基础延迟
- `MAX_529_RETRIES` = 3 - 529 错误最大重试次数
- `PERSISTENT_MAX_BACKOFF_MS` = 5 * 60 * 1000 - 持久模式最大退避
- `HEARTBEAT_INTERVAL_MS` = 30_000 - 心跳间隔

### 类型
- `RetryContext` - 重试上下文
- `RetryOptions` - 重试选项
