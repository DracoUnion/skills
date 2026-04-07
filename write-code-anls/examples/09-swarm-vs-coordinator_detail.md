# 09-swarm-vs-coordinator.md 细纲

## 一、标题层级结构

### 1. Swarm 模式 vs Coordinator 模式对比
- 学习目标（5点）
- 通俗讲解：两种管理风格
  - Coordinator 模式 = 军队指挥
  - Swarm 模式 = 创业团队
- 架构差异
- 启用方式
  - Coordinator 模式
  - Swarm 模式
  - 互斥关系
- 多维度对比
  - 1. 工具可用性
  - 2. 通信机制
  - 3. Worker/队友管理
  - 4. 任务管理
  - 5. Token 消耗
- 场景选择指南
  - 什么时候用 Coordinator？
  - 什么时候用 Swarm？
- 综合对比表
- 融合使用的可能性
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **架构差异**
   - Coordinator: 星形拓扑，单点瓶颈
   - Swarm: 网状拓扑，无单点瓶颈

2. **启用方式**
   - Coordinator: CLAUDE_CODE_COORDINATOR_MODE=1
   - Swarm: TeamCreateTool 自然触发
   - Fork 和 Coordinator 互斥

3. **工具可用性**
   - Coordinator 主 Agent: 3 个工具（Agent/SendMessage/TaskStop）
   - Swarm Team Lead: 所有标准工具 + Swarm 工具

4. **通信机制**
   - Coordinator: task-notification，XML 格式，自动注入
   - Swarm: Mailbox，JSON 格式，自动轮询

5. **任务管理**
   - Coordinator: 隐式，在 prompt 中
   - Swarm: 显式，TaskCreate/Update/List

6. **选择策略**
   - Coordinator: 明确的工程任务，2-5 个 Worker，单向通信
   - Swarm: 复杂协作任务，5+ 个队友，多向通信

7. **关键问题**
   - 成员之间是否需要直接对话？
   - 是 → Swarm，否 → Coordinator

## 三、源码文件路径

- `coordinator/coordinatorMode.ts` - Coordinator 模式
- `tools/TeamCreateTool/TeamCreateTool.ts` - Swarm 模式
- `tools/AgentTool/forkSubagent.ts` - Fork 与 Coordinator 互斥

## 四、类名、函数名、接口名

### 核心函数
- `isCoordinatorMode()` - 检查 Coordinator 模式
- `isAgentSwarmsEnabled()` - 检查 Swarm 是否启用
- `isForkSubagentEnabled()` - 检查 Fork 是否启用（与 Coordinator 互斥）

### 类型
- `CoordinatorModeConfig` - Coordinator 模式配置
- `SwarmConfig` - Swarm 配置

### 常量
- `COORDINATOR_MODE` - Coordinator 功能开关
- `AGENT_SWARMS` - Swarm 功能开关
- `FORK_SUBAGENT` - Fork 功能开关
