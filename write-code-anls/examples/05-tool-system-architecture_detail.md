# 第5课：工具系统架构：40+ 工具如何组织 - 细纲

## 文件信息
- **原文件**: part02-architecture/05-tool-system-architecture.md
- **类型**: 架构全景
- **难度**: ★★★☆☆

---

## 一、什么是"工具"

### 1.1 生活类比：瑞士军刀
Claude Code 的工具系统就像一把瑞士军刀：
- **BashTool** — 像一把刀，可以执行任何命令
- **FileReadTool** — 像放大镜，查看文件内容
- **FileEditTool** — 像笔，修改文件
- **GrepTool** — 像搜索引擎，在代码中搜索
- **WebFetchTool** — 像浏览器，获取网页内容
- **AgentTool** — 像助手，派出子代理执行任务

---

## 二、工具大全览

### 2.1 工具分类
| 分类 | 工具 | 作用 |
|------|------|------|
| 文件操作 | FileReadTool, FileEditTool, FileWriteTool, NotebookEditTool | 读写文件 |
| 搜索工具 | GrepTool, GlobTool, WebSearchTool | 内容/文件名搜索 |
| 执行工具 | BashTool, PowerShellTool | 执行命令 |
| 网络工具 | WebFetchTool, LSPTool | 获取网页/语言服务 |
| 代理工具 | AgentTool, TaskOutputTool, TaskStopTool | 子代理管理 |
| 辅助工具 | TodoWriteTool, SkillTool, AskUserQuestionTool, EnterPlanModeTool | 待办/技能/询问 |

---

## 三、工具注册中心：tools.ts

### 3.1 getAllBaseTools 函数
**文件**: `src/tools.ts`

```typescript
export function getAllBaseTools(): Tools {
  return [
    AgentTool,
    TaskOutputTool,
    BashTool,
    ...(hasEmbeddedSearchTools() ? [] : [GlobTool, GrepTool]),
    ExitPlanModeV2Tool,
    FileReadTool,
    FileEditTool,
    FileWriteTool,
    NotebookEditTool,
    WebFetchTool,
    TodoWriteTool,
    WebSearchTool,
    TaskStopTool,
    AskUserQuestionTool,
    SkillTool,
    EnterPlanModeTool,
    ...(isEnvTruthy(process.env.ENABLE_LSP_TOOL) ? [LSPTool] : []),
    ...(isWorktreeModeEnabled() ? [EnterWorktreeTool, ExitWorktreeTool] : []),
    getSendMessageTool(),
    ...(isAgentSwarmsEnabled()
      ? [getTeamCreateTool(), getTeamDeleteTool()]
      : []),
    BriefTool,
    ListMcpResourcesTool,
    ReadMcpResourceTool,
    ...(isToolSearchEnabledOptimistic() ? [ToolSearchTool] : []),
  ]
}
```

### 3.2 条件加载设计
```typescript
// 模式：条件包含工具
...(条件 ? [工具] : [])

// 编译时条件
...(feature('COORDINATOR_MODE') ? [coordinatorModeTools] : [])

// 运行时条件
...(isEnvTruthy(process.env.X) ? [SomeTool] : [])

// 用户类型条件
...(process.env.USER_TYPE === 'ant' ? [InternalTool] : [])
```

### 3.3 工具加载决策树
```
getAllBaseTools()
├── 始终加载（BashTool, FileReadTool...）
├── feature() 门控（编译时决定）
│   ├── COORDINATOR_MODE → 协调器工具
│   └── HISTORY_SNIP → 历史剪裁工具
├── 环境变量控制（运行时决定）
│   └── ENABLE_LSP_TOOL → LSP 工具
└── 用户类型（ant vs external）
    └── ant → 内部工具（REPLTool, ConfigTool）
```

---

## 四、工具过滤管道

### 4.1 从注册到可用的流程
```
getAllBaseTools() [40+ 工具]
    ↓
filterToolsByDenyRules() [权限过滤]
    ↓
isEnabled() 检查 [启用状态过滤]
    ↓
模式过滤 [REPL/Simple模式]
    ↓
最终可用工具 [~20-30 个]
```

### 4.2 getTools 函数
**文件**: `src/tools.ts`

```typescript
export const getTools = (permissionContext: ToolPermissionContext): Tools => {
  // 简单模式：只有 Bash、Read 和 Edit
  if (isEnvTruthy(process.env.CLAUDE_CODE_SIMPLE)) {
    const simpleTools: Tool[] = [BashTool, FileReadTool, FileEditTool]
    return filterToolsByDenyRules(simpleTools, permissionContext)
  }

  // 获取所有基础工具并过滤特殊工具
  const tools = getAllBaseTools().filter(tool => !specialTools.has(tool.name))

  // 按权限规则过滤
  let allowedTools = filterToolsByDenyRules(tools, permissionContext)

  // 检查每个工具是否启用
  const isEnabled = allowedTools.map(_ => _.isEnabled())
  return allowedTools.filter((_, i) => isEnabled[i])
}
```

### 4.3 权限过滤详解
```typescript
export function filterToolsByDenyRules<T extends {
  name: string
  mcpInfo?: { serverName: string; toolName: string }
}>(tools: readonly T[], permissionContext: ToolPermissionContext): T[] {
  return tools.filter(tool => !getDenyRuleForTool(permissionContext, tool))
}
```

**类比**: 机场安检——工具先通过"安全名单"检查，被禁止的工具直接拦下来。

---

## 五、工具池组装：内置工具 + MCP 工具

### 5.1 assembleToolPool 函数
**文件**: `src/tools.ts`

```typescript
export function assembleToolPool(
  permissionContext: ToolPermissionContext,
  mcpTools: Tools,
): Tools {
  const builtInTools = getTools(permissionContext)

  // 过滤被禁止的 MCP 工具
  const allowedMcpTools = filterToolsByDenyRules(mcpTools, permissionContext)

  // 按名称排序以保持 prompt cache 稳定性
  const byName = (a: Tool, b: Tool) => a.name.localeCompare(b.name)
  return uniqBy(
    [...builtInTools].sort(byName).concat(allowedMcpTools.sort(byName)),
    'name',  // 按名称去重，内置工具优先
  )
}
```

### 5.2 工具池组装流程
```
内置工具（BashTool, FileReadTool...）
    ↓
权限过滤
    ↓
按名称排序 ──┐
              ├──→ 合并去重（uniqBy name）→ 最终工具池
MCP 工具 ────┘
    ↓
权限过滤
    ↓
按名称排序
```

### 5.3 为什么要排序
排序是为了 **Prompt Cache 稳定性**——如果工具列表的顺序变化，系统提示的哈希值就会改变，导致缓存失效。

---

## 六、Agent 的受限工具集

### 6.1 子代理禁用工具
**文件**: `src/constants/tools.ts`

```typescript
export const ALL_AGENT_DISALLOWED_TOOLS = new Set([
  TASK_OUTPUT_TOOL_NAME,          // 防止递归
  EXIT_PLAN_MODE_V2_TOOL_NAME,   // 计划模式是主线程概念
  ENTER_PLAN_MODE_TOOL_NAME,
  ASK_USER_QUESTION_TOOL_NAME,   // 子代理不能直接问用户
  TASK_STOP_TOOL_NAME,           // 需要主线程任务状态
])
```

### 6.2 异步代理允许的工具（白名单）
```typescript
export const ASYNC_AGENT_ALLOWED_TOOLS = new Set([
  FILE_READ_TOOL_NAME,
  WEB_SEARCH_TOOL_NAME,
  TODO_WRITE_TOOL_NAME,
  GREP_TOOL_NAME,
  WEB_FETCH_TOOL_NAME,
  GLOB_TOOL_NAME,
  ...SHELL_TOOL_NAMES,
  FILE_EDIT_TOOL_NAME,
  FILE_WRITE_TOOL_NAME,
  NOTEBOOK_EDIT_TOOL_NAME,
  SKILL_TOOL_NAME,
])
```

### 6.3 协调器模式允许的工具
```typescript
export const COORDINATOR_MODE_ALLOWED_TOOLS = new Set([
  AGENT_TOOL_NAME,       // 创建子代理
  TASK_STOP_TOOL_NAME,   // 停止任务
  SEND_MESSAGE_TOOL_NAME, // 发送消息
])
```

### 6.4 工具权限层级
```
主线程（所有工具可用）
    ↓
子代理（受限工具集）
├── ✅ 文件读写
├── ✅ 搜索工具
├── ✅ Shell 执行
├── ❌ AgentTool（防递归）
└── ❌ AskUser（不能问用户）

协调器（仅管理工具）
├── ✅ AgentTool（管理代理）
├── ✅ TaskStop
├── ✅ SendMessage
└── ❌ 其他所有工具
```

---

## 七、工具搜索：按需加载

### 7.1 ToolSearchTool
**文件**: `src/tools.ts`

```typescript
// 当工具搜索可能启用时，包含 ToolSearchTool
...(isToolSearchEnabledOptimistic() ? [ToolSearchTool] : []),
```

### 7.2 工具搜索机制
```
模型 → "我需要一个能读取 MCP 资源的工具"
    ↓
ToolSearchTool
    ↓
搜索匹配 → ListMcpResourcesTool, ReadMcpResourceTool
    ↓
添加到当前上下文 → 模型
```

---

## 八、动手练习

### 练习1：统计工具数量
打开 `tools.ts`，按分类统计：
- [ ] 始终加载的工具：___ 个
- [ ] `feature()` 门控的工具：___ 个
- [ ] 环境变量控制的工具：___ 个
- [ ] 用户类型限制的工具：___ 个

### 练习2：工具目录结构
浏览 `tools/` 目录，选择一个工具（如 `BashTool`）：
```
tools/BashTool/
├── BashTool.ts       ← 工具定义
├── toolName.ts       ← 工具名称常量
├── prompt.ts         ← 提示词
├── UI.tsx            ← React 渲染
└── shouldUseSandbox.ts ← 沙箱逻辑
```

### 思考题
1. 为什么要用 `uniqBy('name')` 确保工具名称唯一？
2. 协调器模式为什么只允许 AgentTool 和 SendMessage？
3. 工具排序对 Prompt Cache 有什么影响？

---

## 九、小结

| 概念 | 说明 |
|------|------|
| getAllBaseTools() | 所有工具的注册中心 |
| 条件加载 | `feature()`、环境变量、用户类型控制 |
| filterToolsByDenyRules() | 权限过滤管道 |
| assembleToolPool() | 内置 + MCP 工具合并 |
| Agent 工具限制 | 子代理只能用受限工具集 |
| ToolSearchTool | 按需搜索和加载工具 |

---

## 十、关联文件

### 10.1 上一章
- [04-parallel-prefetch.md](04-parallel-prefetch.md) - 并行预取机制

### 10.2 下一章
- [06-query-engine.md](06-query-engine.md) - QueryEngine 查询引擎

---

*此细纲由 Claude Code 自动生成*
