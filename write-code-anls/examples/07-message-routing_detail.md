# 07-message-routing.md 细纲

## 一、标题层级结构

### 1. 四种消息路由模式深入
- 学习目标（5点）
- 通俗讲解：快递配送类比
- 模式一：Task Notification（Coordinator 模式）
  - 通知的 XML 格式
  - 工作流程
  - 关键特点
- 模式二：Mailbox（Swarm 模式）
  - Mailbox 的工作原理
  - 消息投递的核心代码
  - Swarm 模式的消息流
  - 与 Coordinator 模式的关键区别
- 模式三：进程内消息队列
  - 消息排队
  - 自动恢复机制
  - 状态机
- 模式四：跨会话消息
  - UDS（Unix Domain Socket）模式
  - Bridge 模式
  - 跨会话消息的安全检查
- 四种路由模式全面对比
- 消息的投递保障
  - 自动投递 vs 手动检查
  - 空闲状态说明
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **四种消息路由模式**
   - Task Notification: Coordinator 模式，XML 格式，自动注入 user message
   - Mailbox: Swarm 模式，文件系统邮箱，JSON 格式
   - In-Process Queue: 进程内队列，内存操作，自动恢复
   - Cross-Session: UDS/Bridge，跨会话通信，需安全审批

2. **Task Notification**
   - XML 格式：task-id, status, summary, result, usage
   - 自动注入为 user message
   - Worker 不互相对话

3. **Mailbox 机制**
   - 基于文件系统：~/.claude/mailboxes/{team}/{agent}/inbox.json
   - writeToMailbox 写入
   - 自动轮询投递

4. **自动恢复机制**
   - running 状态：消息排队
   - stopped 状态：resumeAgentBackground
   - 支持从磁盘 transcript 恢复

5. **跨会话消息安全**
   - bridge 方案需要用户明确同意
   - classifierApprovable: false
   - 防止提示注入攻击

6. **四种模式对比**
   - Task Notification: 星形，低延迟，Coordinator 专用
   - Mailbox: 网状，中延迟，持久化
   - In-Process: 父→子，最低延迟，内存队列
   - Cross-Session: 点对点，高延迟，需审批

## 三、源码文件路径

- `coordinator/coordinatorMode.ts` - Task Notification 格式
- `tools/SendMessageTool/SendMessageTool.ts` - Mailbox 和跨会话消息
- `tools/TeamCreateTool/prompt.ts` - 消息投递说明

## 四、类名、函数名、接口名

### 核心函数
- `writeToMailbox()` - 写入邮箱
- `queuePendingMessage()` - 队列消息
- `resumeAgentBackground()` - 恢复 Agent
- `isLocalAgentTask()` - 检查是否为本地 Agent 任务
- `isMainSessionTask()` - 检查是否为主会话任务

### 类型
- `TaskNotification` - 任务通知
- `MailboxMessage` - 邮箱消息
- `CrossSessionMessage` - 跨会话消息

### 常量
- `UDS_SCHEME` - UDS 方案
- `BRIDGE_SCHEME` - Bridge 方案
