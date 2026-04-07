# 10-design-your-own.md 细纲

## 一、标题层级结构

### 1. 实战——如何设计你自己的多 Agent 系统
- 学习目标（5点）
- 设计方法论：五步法
- 第一步：任务分析
  - 提出正确的问题
  - 实战案例：设计一个"全栈功能开发"系统
- 第二步：角色设计
  - 自定义 Agent 定义文件
  - Agent 定义的完整属性
  - 为"评论功能"设计 Agent
- 第三步：通信设计
  - 选择模式
  - 消息流设计
- 第四步：安全设计
  - 安全审查清单
  - 为不同角色配置安全策略
- 第五步：优化迭代
  - Token 优化策略
  - 源码中的优化启发
  - 错误处理最佳实践
- 完整设计模板
- 实战练习
- 知识体系回顾
- 课程总结：十个核心原则
- 你的下一步

## 二、关键知识点

1. **五步法**
   - 任务分析：拆解任务，识别并行机会
   - 角色设计：定义 Agent，编写提示词
   - 通信设计：选择模式，设计消息流
   - 安全设计：最小权限，隔离策略
   - 优化迭代：Token 优化，错误处理

2. **自定义 Agent**
   - 在 .claude/agents/ 目录下创建 Markdown 文件
   - Frontmatter 定义属性
   - 正文编写系统提示词

3. **Agent 定义属性**
   - name, description, tools, disallowedTools
   - model, effort, permissionMode, maxTurns
   - skills, background, memory, isolation
   - color, hooks, mcpServers

4. **Token 优化策略**
   - omitClaudeMd: 只读 Agent 省略规则
   - 省略 gitStatus: Explore/Plan 自己查
   - ONE_SHOT: 省略 agentId/SendMessage 提示
   - Fork 共享 prompt cache

5. **十个核心原则**
   - 最小权限、职责单一、不委托理解
   - 并行是超能力、安全是多层的
   - 清理必须可靠、通信要精确
   - 优雅退出、Token 效率、从简单开始

## 三、源码文件路径

- `tools/AgentTool/loadAgentsDir.ts` - 加载自定义 Agent
- `tools/AgentTool/built-in/*.ts` - 内置 Agent 示例
- `.claude/agents/` - 自定义 Agent 目录（用户创建）

## 四、类名、函数名、接口名

### 核心函数
- `loadAgentsDir()` - 加载 Agent 目录
- `parseAgentDefinition()` - 解析 Agent 定义
- `validateAgentDefinition()` - 验证 Agent 定义

### 类型
- `CustomAgentDefinition` - 自定义 Agent 定义
- `AgentDefinition` - Agent 定义联合类型

### 常量
- `AGENT_SECURITY_PROFILES` - 安全配置示例
- `DEFAULT_MAX_TURNS` - 默认最大轮数
