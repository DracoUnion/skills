# 10-build-your-own-tool.md 细纲

## 一、标题层级结构

### 1. 如何自己实现一个新工具（实战）
- 学习目标（5点）
- 回顾：Tool 接口全景
  - buildTool 的默认值
- 实战：实现一个 WordCountTool
  - 需求分析
  - 目录结构
- 第一步：定义常量和描述（prompt.ts）
- 第二步：定义 Schema（输入输出）
- 第三步：实现核心逻辑
- 第四步：注册工具
- 开发检查清单
- 常见模式与最佳实践
  - 权限模式选择
  - 错误处理模式
  - Token 优化模式
  - 并发安全判断
- 工具开发流程总结
- 课程系列总回顾
- 动手练习
- 本课小结
- 课程结语

## 二、关键知识点

1. **Tool 接口三层方法**
   - 必须：name, inputSchema, call, description, prompt, maxResultSizeChars, mapToolResultToToolResultBlockParam, renderToolUseMessage
   - 强烈建议：validateInput, checkPermissions, isReadOnly, isConcurrencySafe, userFacingName, getToolUseSummary, toAutoClassifierInput
   - 可选：outputSchema, searchHint, getActivityDescription, renderToolResultMessage, getPath, aliases, shouldDefer

2. **buildTool 安全默认值**
   - `isEnabled: () => true`
   - `isConcurrencySafe: () => false`
   - `isReadOnly: () => false`
   - `checkPermissions: (input) => Promise.resolve({ behavior: 'allow', updatedInput: input })`

3. **开发流程**
   - 需求分析 → 创建目录 → 定义 prompt.ts → 定义 Schema → 实现 buildTool → 实现 UI → 注册到 tools.ts → 编写测试 → 验证权限流程 → 优化 Token

4. **权限模式选择**
   - 只读操作：使用 `checkReadPermissionForTool`
   - 修改系统文件：自定义 checkPermissions + Safety Check
   - 按内容区分：使用 `getRuleByContentsForTool`
   - 默认：使用 buildTool 默认

## 三、源码文件路径

- `src/Tool.ts` - Tool 接口和 buildTool
- `src/tools.ts` - 工具注册
- `src/utils/lazySchema.ts` - 延迟 Schema
- `src/utils/permissions/filesystem.ts` - 文件权限检查

## 四、类名、函数名、接口名

### 核心函数
- `buildTool<D extends AnyToolDef>(def: D): BuiltTool<D>` - 工具工厂（第 783-792 行）
- `lazySchema(() => z.strictObject({...}))` - 延迟 Schema

### 类型
- `Tool<Input, Output, P>` - 工具接口
- `ToolDef<InputSchema, Output>` - 工具定义
- `BuiltTool<D>` - 构建后的工具
- `InputSchema` / `OutputSchema` - Schema 类型
- `Output` - 输出类型

### 权限相关
- `checkReadPermissionForTool()` - 读取权限检查
- `getRuleByContentsForTool()` - 内容级规则获取
- `PermissionDecision` - 权限决策
- `PermissionResult` - 权限结果

### UI 相关
- `renderToolUseMessage()` - 渲染工具调用
- `renderToolResultMessage()` - 渲染结果
- `mapToolResultToToolResultBlockParam()` - 结果映射

### 常量
- `TOOL_DEFAULTS` - 安全默认值（第 757-769 行）
- `DEFAULT_HEAD_LIMIT` = 250
- `Infinity` - FileReadTool 永不持久化
