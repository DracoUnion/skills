# 第2课：AgentTool 源码解析 —— 子 Agent 的创建 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第2课：AgentTool 源码解析 —— 子 Agent 的创建

### 1.2 二级标题
- 学习目标
- 通俗讲解：招聘流程类比
- AgentTool 目录结构
- 核心源码解析：runAgent 函数
- 同步 vs 异步 Agent
- 特殊机制：Fork 子 Agent
- 动手练习
- 本课小结
- 下节预告

### 1.3 三级标题
- 第一步：确定模型和身份
- 第二步：准备上下文（布置工位）
- 第三步：构建系统提示词（写岗位手册）
- 第四步：配置权限（发门禁卡）
- 第五步：解析可用工具（打开工具箱）
- 第六步：进入工作循环（正式干活）
- 第七步：清理资源（办理离职）
- 关键区别
- 为什么要 Fork？
- 防止递归 Fork

---

## 2. 关键知识点

### 2.1 AgentTool 目录结构
| 文件 | 职责 |
|------|------|
| `AgentTool.tsx` | 主入口 |
| `runAgent.ts` | 核心运行逻辑 |
| `prompt.ts` | 提示词描述 |
| `constants.ts` | 常量定义 |
| `builtInAgents.ts` | 内置 Agent 注册表 |
| `loadAgentsDir.ts` | 加载自定义 Agent |
| `agentToolUtils.ts` | 工具解析辅助函数 |
| `forkSubagent.ts` | Fork 模式逻辑 |
| `resumeAgent.ts` | 恢复已暂停的 Agent |

### 2.2 runAgent 函数流程
1. 确定模型和身份（agentId）
2. 准备上下文（forkContextMessages）
3. 构建系统提示词（systemPrompt）
4. 配置权限（toolPermissionContext）
5. 解析可用工具（resolveAgentTools）
6. 进入查询循环（query）
7. 清理资源（finally 块）

### 2.3 同步 vs 异步 Agent 对比
| 特性 | 同步 Agent | 异步 Agent |
|------|-----------|-----------|
| 父 Agent 是否等待 | 等待完成 | 立即继续 |
| AbortController | 共享父的 | 独立新建的 |
| 权限弹窗 | 可以弹出 | 不能弹出 |
| 状态共享 | 共享 setAppState | 独立 |
| 结果返回 | 直接返回 | task-notification |

### 2.4 Fork Agent 特点
- 继承父 Agent 的完整对话上下文
- `tools: ['*']` 继承所有工具
- `model: 'inherit'` 继承父的模型
- `permissionMode: 'bubble'` 权限提示冒泡到父
- Fork 的孩子不能再 Fork

---

## 3. 涉及的源码文件路径

### 3.1 Agent 工具
- `tools/AgentTool/runAgent.ts` - 核心运行逻辑
- `tools/AgentTool/agentToolUtils.ts` - 工具过滤
- `tools/AgentTool/forkSubagent.ts` - Fork 模式
- `tools/AgentTool/constants.ts` - 常量定义

---

## 4. 类名、函数名、接口名

### 4.1 函数
- `runAgent()` - 运行子 Agent
- `resolveAgentTools()` - 解析 Agent 工具
- `filterToolsForAgent()` - 过滤 Agent 工具
- `createSubagentContext()` - 创建子 Agent 上下文
- `isInForkChild()` - 检查是否在 Fork 子进程中

### 4.2 常量
- `ALL_AGENT_DISALLOWED_TOOLS` - 所有 Agent 禁用的工具
- `CUSTOM_AGENT_DISALLOWED_TOOLS` - 自定义 Agent 额外禁用的工具
- `ASYNC_AGENT_ALLOWED_TOOLS` - 异步 Agent 允许的工具白名单
- `ONE_SHOT_BUILTIN_AGENT_TYPES` - 一次性内置 Agent 类型

### 4.3 类型
- `SessionSpawnerDeps` - 会话生成器依赖
- `SessionHandle` - 会话控制句柄

---

## 5. 代码片段重点

### 5.1 runAgent 函数签名（runAgent.ts）
```typescript
export async function* runAgent({
  agentDefinition,
  promptMessages,
  toolUseContext,
  canUseTool,
  isAsync,
  model,
  // ... 更多参数
})
```

### 5.2 工具过滤（agentToolUtils.ts）
```typescript
export function filterToolsForAgent({
  tools, isBuiltIn, isAsync, permissionMode
}) {
  return tools.filter(tool => {
    if (tool.name.startsWith('mcp__')) return true
    if (ALL_AGENT_DISALLOWED_TOOLS.has(tool.name)) return false
    if (!isBuiltIn && CUSTOM_AGENT_DISALLOWED_TOOLS.has(tool.name))
      return false
    if (isAsync && !ASYNC_AGENT_ALLOWED_TOOLS.has(tool.name))
      return false
    return true
  })
}
```

### 5.3 Fork Agent 定义（forkSubagent.ts）
```typescript
export const FORK_AGENT = {
  agentType: 'fork',
  tools: ['*'],
  maxTurns: 200,
  model: 'inherit',
  permissionMode: 'bubble',
  source: 'built-in',
  getSystemPrompt: () => '',
}
```

### 5.4 防止递归 Fork（forkSubagent.ts）
```typescript
export function isInForkChild(messages: MessageType[]): boolean {
  return messages.some(m => {
    if (m.type !== 'user') return false
    const content = m.message.content
    if (!Array.isArray(content)) return false
    return content.some(
      block =>
        block.type === 'text' &&
        block.text.includes(`<${FORK_BOILERPLATE_TAG}>`),
    )
  })
}
```

### 5.5 finally 块资源清理（runAgent.ts）
```typescript
finally {
  await mcpCleanup()
  clearSessionHooks(rootSetAppState, agentId)
  agentToolUseContext.readFileState.clear()
  initialMessages.length = 0
  unregisterPerfettoAgent(agentId)
  rootSetAppState(prev => {
    const { [agentId]: _removed, ...todos } = prev.todos
    return { ...prev, todos }
  })
  killShellTasksForAgent(agentId, ...)
}
```

---
