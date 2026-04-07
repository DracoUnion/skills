# 03-tool-interface.md 细纲

## 一、标题层级结构

### 1. Tool 接口 DNA —— 统一接口设计详解
- 学习目标（5点）
- 生活类比：员工档案模板
- Tool 接口全景（类图）
- 核心身份属性
  - name —— 唯一标识
  - aliases —— 历史兼容
  - searchHint —— 搜索线索
- 输入输出定义
  - inputSchema —— 用 Zod 定义参数
  - lazySchema —— 延迟初始化
- 工具生命周期
  - validateInput —— 入口安检
  - call —— 核心执行
- 权限与安全属性
  - isReadOnly —— 是否只读
  - isDestructive —— 是否有破坏性
  - isConcurrencySafe —— 并发安全
- buildTool —— 工具工厂
- UI 渲染方法
- 高级特性
  - interruptBehavior —— 中断策略
  - maxResultSizeChars —— 结果大小限制
  - preparePermissionMatcher —— 权限匹配器
- ToolUseContext —— 执行上下文
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **Tool 接口核心属性**
   - `name`: 工具唯一标识
   - `inputSchema`: Zod 输入参数定义
   - `outputSchema`: Zod 输出结构定义
   - `call()`: 核心执行逻辑
   - `checkPermissions()`: 权限检查

2. **工具生命周期**
   - backfillObservableInput → validateInput → checkPermissions → call → mapResult → Render

3. **安全默认值（Fail-Closed）**
   - `isConcurrencySafe`: 默认 false
   - `isReadOnly`: 默认 false
   - `isDestructive`: 默认 false
   - `checkPermissions`: 默认 allow

4. **Zod Schema 设计**
   - 使用 `z.strictObject` 拒绝未定义字段
   - `lazySchema` 延迟初始化避免性能开销

## 三、源码文件路径

- `src/Tool.ts` - Tool 接口定义（第 362-695 行）
- `src/utils/lazySchema.ts` - 延迟 Schema 工具
- `src/tools/GrepTool/GrepTool.ts` - inputSchema 示例

## 四、类名、函数名、接口名

### 接口
- `Tool<Input, Output, P>` - 工具统一接口（第 362-456 行）
- `ToolUseContext` - 工具执行上下文（第 158-300 行）
- `ToolResult<Output>` - 工具执行结果
- `ValidationResult` - 输入验证结果
- `PermissionResult` - 权限检查结果

### 函数
- `buildTool<D extends AnyToolDef>()` - 工具工厂函数（第 783-792 行）
- `toolMatchesName()` - 工具名称匹配（第 348-353 行）

### 常量
- `TOOL_DEFAULTS` - 工具安全默认值（第 757-769 行）
  - `isEnabled: () => true`
  - `isConcurrencySafe: () => false`
  - `isReadOnly: () => false`

### 类型
- `AnyToolDef` - 任意工具定义类型
- `BuiltTool<D>` - 构建后的工具类型
- `CanUseToolFn` - 工具使用权限检查函数类型

### UI 渲染方法
- `renderToolUseMessage()` - 渲染工具调用信息
- `renderToolResultMessage()` - 渲染工具执行结果
- `mapToolResultToToolResultBlockParam()` - 结果映射到 API 格式
