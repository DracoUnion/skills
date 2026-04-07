# 04-streaming.md 细纲

## 一、标题层级结构

### 1. 流式响应 Streaming 源码解析
- 学习目标（5点）
- 生活类比：流式响应就像自来水
- 流式响应全景图
  - 序列图
- 流式事件的六种类型
  - message_start / content_block_start / content_block_delta
  - content_block_stop / message_delta / message_stop
- 源码解析：queryLoop 中的流式处理
  - 发起流式请求（第659-708行）
  - 处理流式消息（第747-863行）
  - 暂扣机制
- AsyncGenerator — 流式传输的语言基础
  - 什么是 AsyncGenerator
  - 在 Claude Code 中的应用
- 流式过程中的 Usage 追踪
  - QueryEngine 中的 usage 累积（第788-816行）
- 流式工具执行 — 边流边跑
- 流式回退机制
- 信号中止 — 紧急刹车
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **流式事件六种类型**
   - `message_start`: 新消息开始
   - `content_block_start`: 内容块开始
   - `content_block_delta`: 内容增量
   - `content_block_stop`: 内容块结束
   - `message_delta`: 消息元信息（stop_reason, usage）
   - `message_stop`: 消息结束

2. **AsyncGenerator 链条**
   - Claude API → query() → QueryEngine → 用户界面
   - 使用 `yield*` 透传内部生成器的值

3. **暂扣机制（Withhold）**
   - `prompt_too_long`: 上下文太长
   - `max_output_tokens`: 输出超限
   - `media_size_error`: 媒体大小错误
   - 暂扣等待恢复，避免显示虚假错误

4. **Usage 追踪流程**
   - `message_start`: 初始化 usage
   - `message_delta`: 累加 usage
   - `message_stop`: 合并到 totalUsage

5. **流式工具执行**
   - 边接收 AI 回复边开始执行工具
   - StreamingToolExecutor.addTool()
   - getCompletedResults() 产出已完成结果

6. **流式回退（Fallback）**
   - 主模型不可用时切换到备用模型
   - tombstone 标记作废已产出消息
   - 重建 StreamingToolExecutor

7. **中止处理**
   - AbortController 信号
   - 生成合成的 tool_result
   - 优雅退出循环

## 三、源码文件路径

- `src/query.ts` - queryLoop 流式处理
- `src/QueryEngine.ts` - Usage 追踪
- `src/services/api/claude.ts` - API 调用和流式处理

## 四、类名、函数名、接口名

### 核心函数
- `callModel()` - 调用模型（返回 AsyncGenerator）
- `deps.callModel()` - 依赖注入的模型调用

### 类型
- `StreamEvent` - 流式事件
- `RequestStartEvent` - 请求开始事件
- `TombstoneMessage` - 墓碑消息（回退时标记作废）

### 辅助函数
- `isWithheldMaxOutputTokens()` - 检查是否暂扣输出超限
- `isWithheldPromptTooLong()` - 检查是否暂扣上下文太长
- `createUserInterruptionMessage()` - 创建用户中止消息

### 常量
- `PROMPT_TOO_LONG_ERROR_MESSAGE` - 上下文太长错误消息
