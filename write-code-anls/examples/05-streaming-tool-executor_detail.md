# 05-streaming-tool-executor.md 细纲

## 一、标题层级结构

### 1. StreamingToolExecutor 并行工具执行
- 学习目标（5点）
- 生活类比：餐厅的多口炒锅
- 架构概览
- 源码解析：核心数据结构
  - TrackedTool 类型（第19-32行）
  - StreamingToolExecutor 类（第40-62行）
- addTool — 工具入队（第76-124行）
- processQueue — 队列调度（第129-151行）
- executeTool — 工具执行（第265-405行）
- 错误级联 — Bash 出错，全部取消
- 结果产出 — 保持顺序
  - getCompletedResults（第412-440行）
  - getRemainingResults（第453-490行）
- discard — 回退时的清理
- 完整执行时序
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **TrackedTool 状态机**
   - `queued`: 等待执行
   - `executing`: 正在运行
   - `completed`: 结果就绪
   - `yielded`: 结果已产出

2. **并发安全判断**
   - `isConcurrencySafe` 由每个工具自己决定
   - FileReadTool: 并发安全（只读）
   - FileWriteTool: 不安全（修改文件）
   - BashTool: 取决于命令内容

3. **调度规则**
   - 队列为空 → 立即执行
   - 执行中的全部并发安全 + 新工具并发安全 → 并行执行
   - 执行中的全部并发安全 + 新工具非并发安全 → 等待
   - 有非并发安全在执行 → 等待

4. **错误级联机制**
   - 只有 BashTool 的错误会取消兄弟工具
   - 原因：Bash 命令常有隐式依赖链
   - `siblingAbortController.abort('sibling_error')`

5. **结果产出顺序**
   - 按照工具入队顺序产出
   - 不按完成顺序
   - 非并发安全工具在执行中时停止遍历

6. **进度消息即时传递**
   - `pendingProgress` 数组存储待产出的进度消息
   - `progressAvailableResolve` 通知有新进度

7. **discard 机制**
   - 流式回退时丢弃整个 executor
   - 标记 `discarded = true`
   - 创建新的 StreamingToolExecutor

## 三、源码文件路径

- `src/services/tools/StreamingToolExecutor.ts` - 流式工具执行器

## 四、类名、函数名、接口名

### 核心类
- `StreamingToolExecutor` - 流式工具执行器类（第40-62行）

### 类型
- `TrackedTool` - 被跟踪的工具（第19-32行）
- `ToolStatus` - 工具状态类型

### 核心方法
- `addTool()` - 添加工具到队列（第76-124行）
- `processQueue()` - 处理队列（第129-151行）
- `executeTool()` - 执行单个工具（第265-405行）
- `getCompletedResults()` - 获取已完成结果（第412-440行）
- `getRemainingResults()` - 获取剩余结果（第453-490行）
- `discard()` - 丢弃执行器（第69-71行）

### 辅助函数
- `canExecuteTool()` - 判断是否可以执行
- `createChildAbortController()` - 创建子中止控制器
- `createSyntheticErrorMessage()` - 创建合成错误消息

### 常量
- `BASH_TOOL_NAME` - Bash 工具名称
