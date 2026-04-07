# 第1课：什么是多 Agent 系统？ - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第1课：什么是多 Agent 系统？

### 1.2 二级标题
- 学习目标
- 通俗讲解：从生活类比说起
- Claude Code 的多 Agent 架构全貌
- 初探源码：Agent 的"出生证明"
- 两种协作模式：Coordinator vs Swarm
- 为什么需要多 Agent？
- 动手练习
- 本课小结
- 下节预告

### 1.3 三级标题
- 一个人 vs 一个团队
- 什么是 Agent？
- 什么是多 Agent 系统？
- 核心组件一览
- 从源码看 Agent 的定义
- Agent 的三种来源
- Coordinator 模式（指挥官模式）
- Swarm 模式（蜂群模式）
- 单 Agent 的局限
- 多 Agent 的优势

---

## 2. 关键知识点

### 2.1 Agent 定义
- 拥有特定能力的独立 AI 工作者
- 有自己的系统提示词、工具集、上下文和生命周期

### 2.2 多 Agent 系统
- 多个 Agent 协同工作，共同完成复杂任务
- 每个 Agent 有独立的对话上下文
- Agent 之间通过消息通信协作

### 2.3 核心组件
| 组件 | 源码位置 | 作用 |
|------|---------|------|
| AgentTool | `tools/AgentTool/` | 创建和管理子 Agent |
| TeamCreateTool | `tools/TeamCreateTool/` | 组建 Swarm 团队 |
| TeamDeleteTool | `tools/TeamDeleteTool/` | 解散团队、清理资源 |
| SendMessageTool | `tools/SendMessageTool/` | Agent 之间发送消息 |
| coordinatorMode | `coordinator/` | Coordinator 编排模式 |

### 2.4 Agent 的三种来源
| 类型 | 说明 |
|------|------|
| BuiltIn | 内置 Agent（系统自带） |
| Custom | 自定义 Agent（用户创建） |
| Plugin | 插件 Agent（第三方提供） |

### 2.5 两种协作模式对比
| 特性 | Coordinator 模式 | Swarm 模式 |
|------|-----------------|-----------|
| 拓扑 | 星形 | 网状 |
| 通信 | Worker 只与 Coordinator 通信 | 队友可直接通信 |
| 适用场景 | 明确的工程任务 | 复杂的协作任务 |

### 2.6 多 Agent 的优势
- 并行执行
- 职责分离
- 最小权限
- 独立上下文
- 容错性

---

## 3. 涉及的源码文件路径

### 3.1 Agent 系统
- `tools/AgentTool/loadAgentsDir.ts` - Agent 定义加载
- `coordinator/coordinatorMode.ts` - Coordinator 模式判断
- `tools/AgentTool/built-in/` - 内置 Agent 定义

---

## 4. 类名、函数名、接口名

### 4.1 类型/接口
- `BaseAgentDefinition` - Agent 基础定义
- `BuiltInAgentDefinition` - 内置 Agent 定义
- `CustomAgentDefinition` - 自定义 Agent 定义
- `PluginAgentDefinition` - 插件 Agent 定义
- `AgentDefinition` - Agent 定义联合类型

### 4.2 函数
- `isCoordinatorMode()` - 判断是否 Coordinator 模式
- `feature()` - 功能开关检查
- `isEnvTruthy()` - 环境变量 truthy 检查

### 4.3 常量
- `BUILTIN_AGENTS` - 内置 Agent 映射

---

## 5. 代码片段重点

### 5.1 BaseAgentDefinition 类型（loadAgentsDir.ts）
```typescript
type BaseAgentDefinition = {
  agentType: string
  whenToUse: string
  tools?: string[]
  disallowedTools?: string[]
  model?: string
  maxTurns?: number
  permissionMode?: string
}
```

### 5.2 AgentDefinition 联合类型（loadAgentsDir.ts）
```typescript
type AgentDefinition =
  | BuiltInAgentDefinition
  | CustomAgentDefinition
  | PluginAgentDefinition
```

### 5.3 isCoordinatorMode 函数（coordinatorMode.ts）
```typescript
export function isCoordinatorMode(): boolean {
  if (feature('COORDINATOR_MODE')) {
    return isEnvTruthy(process.env.CLAUDE_CODE_COORDINATOR_MODE)
  }
  return false
}
```

---
