# 10-queryengine-ecosystem.md 细纲

## 一、标题层级结构

### 1. QueryEngine 与其他系统的协作全景
- 学习目标（5点）
- 生活类比：QueryEngine 就像城市的交通枢纽
- 系统全景架构
- 入口层：三种使用方式
  - REPL（交互式终端）
  - SDK（编程接口）
  - CLI（命令行）
- 工具系统注册
  - 工具注册表 getAllBaseTools（第193-251行）
  - 工具过滤管道
  - assembleToolPool（第345-367行）
- Agent 子系统
  - AgentTool — 创建子代理
  - 子代理的限制
- MCP（Model Context Protocol）集成
- 会话持久化
  - Transcript 记录（第716-731行）
  - 会话恢复
- 权限系统
- 完整的请求生命周期
- 知识串联：10课回顾
- 核心设计原则总结
- 动手练习
- 本课小结
- 系列课程总结

## 二、关键知识点

1. **系统全景架构**
   - 用户入口层: REPL / SDK / CLI / IDE
   - 引擎核心层: QueryEngine / queryLoop / StreamingToolExecutor
   - AI 模型层: Claude API / withRetry / Thinking
   - 工具系统层: Bash / File / Grep / Glob / WebFetch / Agent / MCP
   - 上下文系统层: SystemPrompt / Context / CLAUDE.md / Git
   - 基础设施层: Session / TokenCount / CostTrack / Compact / Permissions

2. **三种使用方式**
   - REPL: 交互式终端，主要交互方式
   - SDK: 编程接口，`ask()` 是便捷包装
   - CLI: 命令行，非交互式使用

3. **工具注册流程**
   - `getAllBaseTools()`: 获取所有基础工具
   - `isEnabled()` 过滤
   - `filterToolsByDenyRules` 过滤
   - Simple 模式仅保留 Bash + Read + Edit
   - 合并 MCP 工具
   - 按名称排序（缓存稳定性）

4. **Agent 子系统**
   - 子代理有独立的消息历史、工具集、Token 预算、中止控制器
   - 工具限制: ALL_AGENT_DISALLOWED_TOOLS / CUSTOM_AGENT_DISALLOWED_TOOLS

5. **MCP 集成**
   - MCP 服务器提供的工具合并到工具池
   - `mcpClients: MCPServerConnection[]`

6. **会话持久化**
   - `recordTranscript()`: 记录会话
   - assistant 消息: 异步记录
   - user/system 消息: 同步记录
   - `--resume` 恢复会话

7. **权限系统流程**
   - 工具调用请求 → canUseTool()
   - Deny rules 检查 → 被禁止则拒绝
   - Auto Allow 检查 → YOLO 模式等直接允许
   - 否则询问用户

8. **五大设计原则**
   - 流式优先: 基于 AsyncGenerator
   - 韧性设计: withRetry + 指数退避 + 模型回退
   - 资源感知: Token 计数 + 预算控制 + 自动压缩
   - 安全可控: 权限系统 + maxTurns + maxBudgetUsd + abort
   - 可扩展: MCP 协议 + 插件系统 + Agent 子代理

## 三、源码文件路径

- `src/QueryEngine.ts` - 引擎主类
- `src/query.ts` - 核心查询循环
- `src/tools.ts` - 工具注册与过滤
- `src/context.ts` - Git 状态 + CLAUDE.md
- `src/utils/queryContext.ts` - 系统提示词构建
- `src/services/api/withRetry.ts` - 重试机制
- `src/services/tools/StreamingToolExecutor.ts` - 流式工具执行
- `src/services/tokenEstimation.ts` - Token 计数
- `src/utils/thinking.ts` - Thinking 模式
- `src/constants/prompts.ts` - 系统提示词内容

## 四、类名、函数名、接口名

### 核心类
- `QueryEngine` - 查询引擎主类
- `StreamingToolExecutor` - 流式工具执行器

### 核心函数
- `getAllBaseTools()` - 获取所有基础工具（第193-251行）
- `assembleToolPool()` - 组装工具池（第345-367行）
- `recordTranscript()` - 记录会话
- `ask()` - SDK 便捷包装（第1186-1295行）

### 工具相关常量
- `ALL_AGENT_DISALLOWED_TOOLS` - 所有子代理禁用工具
- `CUSTOM_AGENT_DISALLOWED_TOOLS` - 自定义子代理禁用工具
- `ASYNC_AGENT_ALLOWED_TOOLS` - 异步子代理允许工具

### 类型
- `MCPServerConnection` - MCP 服务器连接
- `ToolPermissionContext` - 工具权限上下文
- `CanUseToolFn` - 工具权限检查函数类型

### 公式总结
```
Claude Code = QueryEngine(
  入口层(REPL | SDK | CLI),
  上下文(系统提示词 + CLAUDE.md + Git),
  循环(
    while(true) {
      压缩(autoCompact) →
      调用(Claude API + Thinking + Retry) →
      执行(StreamingToolExecutor | toolOrchestration) →
      检查(预算 + 轮次 + 停止钩子) →
      continue | return
    }
  ),
  基础设施(Token计数 + 成本追踪 + 会话持久化 + 权限管理)
)
```
