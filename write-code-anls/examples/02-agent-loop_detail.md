# 02-agent-loop.md 细纲

## 一、标题层级结构

### 1. Agent Loop 核心循环详解
- 学习目标（5点）
- 生活类比：Agent Loop 就像厨师做菜
- Agent Loop 整体架构
  - 流程图
- 源码解析：queryLoop 函数
  - 入口函数 query()（第219-239行）
  - 循环状态 State 对象（第204-217行）
  - 循环主体 while(true) 的秘密（第241-307行）
- 循环的六个阶段
  - 阶段1：上下文压缩
  - 阶段2：调用 AI 模型（流式响应）
  - 阶段3：判断是否需要执行工具
  - 阶段4：执行工具
  - 阶段5：添加附件和检查
  - 阶段6：构建下一轮状态
- 状态转换图
- QueryParams — 循环的输入参数
- 错误处理
- maxTurns — 安全阀
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **Agent Loop 核心流程**
   - while(true) 循环驱动
   - 终止条件：模型完成、达到 maxTurns、用户中止、模型错误、预算耗尽

2. **State 对象结构**
   - `messages`: 当前消息列表
   - `toolUseContext`: 工具执行上下文
   - `autoCompactTracking`: 压缩追踪
   - `turnCount`: 当前轮次
   - `transition`: 上一次的转换原因

3. **六个阶段循环**
   - 压缩检查（autocompact）
   - 调用 AI 模型（流式 Streaming）
   - 判断 needsFollowUp（是否有工具调用）
   - 执行工具
   - 添加附件
   - 构建下一轮状态

4. **终止条件类型**
   - `completed`: 模型完成回复
   - `max_turns`: 达到最大轮次
   - `aborted`: 用户中止
   - `model_error`: 模型错误
   - `max_budget_usd`: 预算耗尽

5. **transition reason 类型**
   - `next_turn`: 正常下一轮
   - `stop_hook_blocking`: 停止钩子阻塞
   - `max_output_tokens_recovery`: 输出超限恢复
   - `reactive_compact_retry`: 反应式压缩重试

## 三、源码文件路径

- `src/query.ts` - queryLoop 核心循环

## 四、类名、函数名、接口名

### 核心函数
- `query()` - 查询入口（第219-239行）
- `queryLoop()` - 核心循环函数（第241-307行）

### 类型
- `QueryParams` - 查询参数（第181-199行）
- `State` - 循环状态（第204-217行）
- `Terminal` - 终止结果
- `Continue` - 继续原因

### 辅助函数
- `buildQueryConfig()` - 构建查询配置
- `startRelevantMemoryPrefetch()` - 预取记忆

### 常量
- `DEFAULT_MAX_TURNS` - 默认最大轮次
