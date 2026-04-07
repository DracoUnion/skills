# 01-tool-system-overview.md 细纲

## 一、标题层级结构

### 1. 工具系统概览 —— AI 的百宝袋
- 学习目标（5点）
- 生活类比：AI 的百宝袋
- 架构全景图
- 工具系统的四大支柱
  - 注册中心（Registry）
  - 统一接口（Interface）
  - 权限系统（Permissions）
  - 执行引擎（Execution）
- 工具分类一览
- 一次完整的工具调用旅程
- 三级过滤管道
- 关键设计理念
  - 安全优先（Fail-Closed）
  - 统一构建（buildTool）
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **工具系统四大支柱**
   - 注册中心：`tools.ts` 中的 `getAllBaseTools()`
   - 统一接口：`Tool.ts` 中的 `Tool` 类型定义
   - 权限系统：`permissions/` 目录
   - 执行引擎：`toolExecution.ts`

2. **三级过滤管道**
   - 第一级：环境过滤（`getAllBaseTools()`）
   - 第二级：权限 deny 规则过滤（`filterToolsByDenyRules()`）
   - 第三级：启用检查（`isEnabled()`）

3. **工具分类**
   - Shell: BashTool
   - 文件: FileReadTool, FileEditTool, FileWriteTool
   - 搜索: GrepTool, GlobTool
   - Agent: AgentTool
   - 网络: WebFetchTool
   - 扩展: MCPTool

4. **安全设计原则**
   - Fail-Closed: 默认值保守
   - `isConcurrencySafe`: 默认 false
   - `isReadOnly`: 默认 false

## 三、源码文件路径

- `src/tools.ts` - 工具注册中心
- `src/Tool.ts` - Tool 接口定义
- `src/tools/` - 内置工具目录
- `src/utils/permissions/` - 权限系统

## 四、类名、函数名、接口名

### 接口
- `Tool<Input, Output, P>` - 工具统一接口
- `ToolUseContext` - 工具执行上下文

### 函数
- `getAllBaseTools()` - 获取所有基础工具
- `getTools()` - 三级过滤后获取工具
- `buildTool()` - 工具工厂函数
- `filterToolsByDenyRules()` - deny 规则过滤

### 类/类型
- `Tools` - 工具数组类型
- `PermissionResult` - 权限检查结果
- `ToolResult` - 工具执行结果

### 常量
- `TOOL_DEFAULTS` - 工具安全默认值
