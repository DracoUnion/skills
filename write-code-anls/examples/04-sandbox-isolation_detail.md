# 04-sandbox-isolation.md 细纲

## 一、标题层级结构

### 1. 沙箱隔离 —— 子 Agent 的安全边界
- 学习目标（5点）
- 通俗讲解：办公大楼门禁类比
- 第一层：全局工具禁用
  - 所有 Agent 都不能用的工具
  - 自定义 Agent 额外不能用的工具
- 第二层：Agent 类型工具限制
  - 白名单模式（Allowlist）
  - 黑名单模式（Denylist）
  - 工具解析流程
- 第三层：权限模式与弹窗控制
  - 权限模式继承
  - 异步 Agent 的特殊限制
  - 工具权限作用域
- 第四层：Worktree 隔离
  - Worktree 的工作原理
  - Fork Agent 中的 Worktree 通知
- 安全设计的多层防御
- 资源清理：安全退出
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **四层安全隔离**
   - 第一层：全局禁用（ALL_AGENT_DISALLOWED_TOOLS）
   - 第二层：类型限制（tools/disallowedTools）
   - 第三层：权限控制（permissionMode + 弹窗控制）
   - 第四层：环境隔离（Worktree/Remote）

2. **工具过滤流程**
   - MCP 工具始终允许
   - 全局黑名单检查
   - 自定义 Agent 额外黑名单
   - 异步 Agent 白名单检查

3. **权限模式**
   - 继承父 Agent 权限
   - 不能降级最高权限（bypass/acceptEdits）
   - 异步 Agent shouldAvoidPermissionPrompts

4. **Worktree 隔离**
   - isolation: 'worktree' 配置
   - 独立 Git 工作目录
   - 改动不影响主分支
   - buildWorktreeNotice 通知 Agent

5. **资源清理**
   - finally 块确保资源释放
   - mcpCleanup()
   - clearSessionHooks()
   - readFileState.clear()
   - killShellTasksForAgent()

## 三、源码文件路径

- `tools/AgentTool/agentToolUtils.ts` - 工具过滤
- `tools/AgentTool/runAgent.ts` - 权限配置和清理
- `tools/AgentTool/loadAgentsDir.ts` - isolation 配置
- `tools/AgentTool/forkSubagent.ts` - Worktree 通知

## 四、类名、函数名、接口名

### 核心函数
- `filterToolsForAgent()` - 过滤 Agent 工具
- `resolveAgentTools()` - 解析 Agent 工具
- `buildWorktreeNotice()` - 构建 Worktree 通知

### 常量
- `ALL_AGENT_DISALLOWED_TOOLS` - 全局禁用工具
- `CUSTOM_AGENT_DISALLOWED_TOOLS` - 自定义额外禁用
- `ASYNC_AGENT_ALLOWED_TOOLS` - 异步 Agent 白名单

### 类型
- `BaseAgentDefinition` - 包含 isolation 字段
- `ToolPermissionContext` - 工具权限上下文
