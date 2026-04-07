# 06-send-message-tool.md 细纲

## 一、标题层级结构

### 1. SendMessageTool —— Agent 间通信详解
- 学习目标（5点）
- 通俗讲解：公司内部通信类比
- SendMessageTool 输入结构
  - 三种消息类型
  - 结构化消息的定义
- 消息路由：谁发给谁？
  - 路由 1：点对点消息
  - 路由 2：广播消息
  - 路由 3：发送给已注册的子 Agent（自动恢复）
- Shutdown 协议：优雅关闭
  - 阶段 1：发送关闭请求
  - 阶段 2：处理关闭确认
  - Shutdown 也可以被拒绝
  - 完整的 Shutdown 流程
- 方案审批机制
- 输入验证：安全守卫
- 消息路由总览
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **SendMessage 输入参数**
   - to: 接收者（队友名或 '*' 广播）
   - summary: 摘要（纯文本消息必填）
   - message: 消息内容（纯文本或结构化）

2. **三种消息类型**
   - 纯文本消息
   - shutdown_request/shutdown_response
   - plan_approval_response

3. **消息路由**
   - 点对点：writeToMailbox
   - 广播：给所有队友（排除自己）
   - 子 Agent：队列或自动恢复

4. **Shutdown 协议**
   - 两阶段握手：请求 → 确认/拒绝
   - 发送 shutdown_request
   - 回复 shutdown_response（approve: true/false）
   - 可以拒绝并给出理由

5. **自动恢复机制**
   - 给已停止的 Agent 发消息会 resumeAgentBackground
   - 运行中的 Agent 消息排队等待

6. **输入验证**
   - to 不能为空
   - to 不能包含 @
   - 纯文本消息必须有 summary
   - 结构化消息不能广播
   - shutdown_response 只能发给 team-lead

## 三、源码文件路径

- `tools/SendMessageTool/SendMessageTool.ts` - 发送消息工具
- `tools/SendMessageTool/prompt.ts` - 消息提示词

## 四、类名、函数名、接口名

### 核心函数
- `handleMessage()` - 处理点对点消息
- `handleBroadcast()` - 处理广播消息
- `handleShutdownRequest()` - 处理关闭请求
- `handleShutdownApproval()` - 处理关闭确认
- `writeToMailbox()` - 写入邮箱
- `queuePendingMessage()` - 队列待发送消息
- `resumeAgentBackground()` - 后台恢复 Agent

### 类型
- `SendMessageInput` - 发送消息输入
- `StructuredMessage` - 结构化消息
- `ShutdownRequest` - 关闭请求
- `ShutdownResponse` - 关闭响应

### 常量
- `TEAM_LEAD_NAME` - Team Lead 名称
