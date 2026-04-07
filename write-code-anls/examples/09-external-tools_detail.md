# 09-external-tools.md 细纲

## 一、标题层级结构

### 1. MCP / LSP / WebFetch —— 外部工具集成
- 学习目标（5点）
- 生活类比：三种连接外界的方式
- MCP 工具：万能插头
  - MCPTool 的"骨架"设计
  - MCP 工具的命名规则
  - MCP 与内置工具的融合
- LSP 工具：代码智能
  - LSP 的九种操作
  - 条件启用 + 延迟加载
  - 安全过滤：排除 gitignore 文件
  - 文件大小保护
- WebFetch 工具：网页抓取
  - 核心流程
  - 域名级别的权限控制
  - 权限建议（suggestions）
  - 重定向安全处理
  - Prompt 中的认证警告
- 三种外部工具对比
- 注册中心的外部工具管理
- 外部工具的安全边界汇总
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **MCP 工具特点**
   - 三段式命名：`mcp__服务器名__工具名`
   - `isMcp: true` 标记
   - `checkPermissions` 返回 `passthrough`
   - 运行时动态覆盖属性

2. **LSP 九种操作**
   - `goToDefinition`, `findReferences`, `hover`
   - `documentSymbol`, `workspaceSymbol`
   - `goToImplementation`, `prepareCallHierarchy`
   - `incomingCalls`, `outgoingCalls`

3. **WebFetch 权限控制**
   - 按域名而非 URL 级别
   - 预审批域名直接放行
   - 跨域重定向不自动跟随
   - 建议添加域名规则

4. **assembleToolPool 排序**
   - 内置工具按字母排序
   - MCP 工具按字母排序
   - 内置工具在前保护 prompt cache

## 三、源码文件路径

- `src/tools/MCPTool/MCPTool.ts` - MCP 工具
- `src/tools/LSPTool/LSPTool.ts` - LSP 工具
- `src/tools/WebFetchTool/WebFetchTool.ts` - WebFetch 工具
- `src/tools/WebFetchTool/preapproved.ts` - 预审批域名
- `src/tools.ts` - 工具注册中心

## 四、类名、函数名、接口名

### MCP
- `MCPTool` - MCP 工具定义（第 27-77 行）
- `isMcp: true` - MCP 标记
- `checkPermissions()` - 返回 passthrough

### LSP
- `LSPTool` - LSP 工具定义（第 127-139 行）
- `isLsp: true` - LSP 标记
- `shouldDefer: true` - 延迟加载
- `isEnabled()` - 运行时检查 LSP 连接
- `MAX_LSP_FILE_SIZE_BYTES` = 10MB（第 53 行）

### WebFetch
- `WebFetchTool` - WebFetch 工具
- `checkPermissions()` - 域名级权限检查（第 104-180 行）
- `webFetchToolInputToPermissionRuleContent()` - 提取域名（第 50-64 行）
- `buildSuggestions()` - 构建权限建议（第 309-318 行）

### 函数
- `assembleToolPool()` - 组装工具池（第 345-367 行）
- `uniqBy('name')` - 按名称去重
- `filterGitIgnoredLocations()` - 过滤 gitignore 文件

### 常量
- `MCP_TOOL_NAME_PREFIX` - MCP 工具名前缀
- `LSP_TOOL_NAME` - LSP 工具名
- `WEB_FETCH_TOOL_NAME` - WebFetch 工具名
