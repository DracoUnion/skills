# 06-tool-execution.md 细纲

## 一、标题层级结构

### 1. 工具执行：串行 vs 并发策略
- 学习目标（5点）
- 生活类比：工厂流水线 vs 多工位并行
- 两种执行器对比
  - toolOrchestration.ts vs StreamingToolExecutor.ts
- 源码解析：partitionToolCalls — 智能分批（第91-116行）
- runToolsSerially — 串行执行（第118-150行）
- runToolsConcurrently — 并发执行（第152-177行）
  - 并发限制 getMaxToolUseConcurrency
- runTools — 统一入口（第19-82行）
- 在 queryLoop 中的选择
- contextModifier — 工具改变世界
- 执行策略对比总结
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **两种执行器对比**
   - toolOrchestration: AI 说完后统一执行，预先分批
   - StreamingToolExecutor: AI 说话过程中就开始，实时调度

2. **partitionToolCalls 分批逻辑**
   - 连续的并发安全工具合并为一批
   - 非并发安全工具单独成批
   - 示例：ReadFile→ReadFile→Bash→Grep→ReadFile→Write
     - 批次1: ReadFile+ReadFile（并行）
     - 批次2: Bash（串行）
     - 批次3: Grep+ReadFile（并行）
     - 批次4: Write（串行）

3. **串行执行特点**
   - 逐个执行，前一个完成后才执行下一个
   - 支持 contextModifier——工具可以修改上下文
   - 确保写操作的顺序性

4. **并发执行特点**
   - 批量并行，受并发限制保护
   - 默认最多 10 个工具并发
   - 可通过环境变量调整

5. **并发限制**
   - `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY` 环境变量
   - 默认值为 10

6. **contextModifier 处理差异**
   - 串行模式：立即应用
   - 并行模式：延迟到批次结束后统一应用
   - 原因：避免多个工具同时修改上下文导致冲突

7. **queryLoop 中的选择**
   - `config.gates.streamingToolExecution` 开关控制
   - 启用 → StreamingToolExecutor
   - 禁用 → toolOrchestration

## 三、源码文件路径

- `src/services/tools/toolOrchestration.ts` - 传统工具编排
- `src/services/tools/StreamingToolExecutor.ts` - 流式工具执行器

## 四、类名、函数名、接口名

### 核心函数
- `runTools()` - 工具执行统一入口（第19-82行）
- `partitionToolCalls()` - 智能分批（第91-116行）
- `runToolsSerially()` - 串行执行（第118-150行）
- `runToolsConcurrently()` - 并发执行（第152-177行）

### 辅助函数
- `getMaxToolUseConcurrency()` - 获取并发限制（第8-11行）
- `findToolByName()` - 根据名称查找工具
- `markToolUseAsComplete()` - 标记工具完成

### 类型
- `Batch` - 工具批次类型
- `MessageUpdate` - 消息更新类型
- `MessageUpdateLazy` - 延迟消息更新类型

### 常量
- `MAX_TOOL_USE_CONCURRENCY` - 默认并发限制 10
