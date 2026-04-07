# 08-agent-tool.md 细纲

## 一、标题层级结构

### 1. AgentTool —— 子 Agent 的诞生与隔离
- 学习目标（5点）
- 生活类比：公司的项目外包
- AgentTool 架构全景
- 内置 Agent 类型
  - 一次性 Agent 优化
- 工具隔离：子 Agent 能用什么
  - 工具过滤逻辑
  - 工具解析（resolveAgentTools）
- runAgent：子 Agent 的生命周期
  - 初始化阶段
  - 权限隔离
  - AbortController 策略
  - 系统提示优化
- 资源清理：Agent 的善后
- Agent 专属 MCP 服务器
- 不完整消息过滤
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **内置 Agent 类型**
   - `GENERAL_PURPOSE_AGENT`: 通用多步任务
   - `EXPLORE_AGENT`: 代码探索（只读）
   - `PLAN_AGENT`: 任务规划（只读）
   - `ONE_SHOT_BUILTIN_AGENT_TYPES`: Explore 和 Plan 是一次性的

2. **工具隔离**
   - `ALL_AGENT_DISALLOWED_TOOLS`: 所有 Agent 禁用的工具
   - `CUSTOM_AGENT_DISALLOWED_TOOLS`: 自定义 Agent 额外禁用
   - `ASYNC_AGENT_ALLOWED_TOOLS`: 异步 Agent 白名单
   - MCP 工具始终允许

3. **权限隔离**
   - cliArg 规则保留
   - session 规则替换
   - 异步 Agent 不能显示权限弹窗

4. **资源清理 8 步**
   - 关闭 MCP 服务器
   - 清理 Session Hooks
   - 清理 Prompt Cache 追踪
   - 释放文件状态缓存
   - 释放上下文消息引用
   - 清理 Perfetto 追踪
   - 清理 Todo 条目
   - 终止后台 Shell 任务

## 三、源码文件路径

- `src/tools/AgentTool/AgentTool.ts` - Agent 工具入口
- `src/tools/AgentTool/runAgent.ts` - 子 Agent 运行（第 248-329 行）
- `src/tools/AgentTool/agentToolUtils.ts` - 工具过滤（第 70-116 行）
- `src/tools/AgentTool/builtInAgents.ts` - 内置 Agent 定义
- `src/tools/AgentTool/constants.ts` - 常量定义

## 四、类名、函数名、接口名

### 函数
- `runAgent()` - 运行子 Agent（第 248-329 行）
- `filterToolsForAgent()` - 过滤 Agent 可用工具（第 70-116 行）
- `resolveAgentTools()` - 解析 Agent 工具（第 122-225 行）
- `initializeAgentMcpServers()` - 初始化 Agent MCP 服务器
- `filterIncompleteToolCalls()` - 过滤不完整消息（第 866-904 行）

### 常量
- `ONE_SHOT_BUILTIN_AGENT_TYPES` - 一次性 Agent 类型（第 6-12 行）
- `ALL_AGENT_DISALLOWED_TOOLS` - 全局禁用工具集合
- `CUSTOM_AGENT_DISALLOWED_TOOLS` - 自定义 Agent 禁用
- `ASYNC_AGENT_ALLOWED_TOOLS` - 异步 Agent 白名单

### 类型
- `AgentDefinition` - Agent 定义
- `ResolvedAgentTools` - 解析后的工具
- `AgentPermissionMode` - Agent 权限模式

### 类
- `AgentTool` - Agent 工具类
- `ToolUseContext` - 工具使用上下文
