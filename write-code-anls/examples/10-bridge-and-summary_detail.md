# 第10课：Bridge 桥接系统与全架构总结 - 细纲

## 文件信息
- **原文件**: part02-architecture/10-bridge-and-summary.md
- **类型**: 架构全景
- **难度**: ★★★★☆

---

## 一、什么是 Bridge 桥接系统

### 1.1 生活类比：远程操控无人机
- **以前**：亲自开车去（只能在本地运行 Claude Code）
- **现在**：用无人机远程查看（Bridge 让你远程控制 Claude Code）

### 1.2 Bridge 功能
- 在**云端服务器**上运行
- 通过**Web 浏览器**或**手机**控制
- 保持**长时间运行**的会话

### 1.3 Bridge 架构
```
用户（Web/Mobile/Desktop）
    ←→ HTTPS / WebSocket ←→
Bridge API（中间层服务）
    ←→ 轮询 / WebSocket ←→
Claude Code（远程运行实例）
```

---

## 二、Bridge 架构详解

### 2.1 bridge/ 目录结构
| 文件 | 作用 |
|------|------|
| `bridgeMain.ts` | 桥接主入口 |
| `bridgeConfig.ts` | 配置管理 |
| `bridgeApi.ts` | API 客户端 |
| `bridgeMessaging.ts` | 消息传递 |
| `bridgeUI.ts` | UI 日志 |
| `bridgePermissionCallbacks.ts` | 权限回调 |
| `pollConfig.ts` | 轮询配置 |
| `sessionRunner.ts` | 会话管理 |
| `createSession.ts` | 会话创建 |
| `replBridge.ts` | REPL 桥接 |
| `replBridgeTransport.ts` | 传输层 |
| `jwtUtils.ts` | JWT 认证 |
| `trustedDevice.ts` | 设备信任 |
| `capacityWake.ts` | 容量唤醒 |
| `types.ts` | 类型定义 |

### 2.2 bridgeMain.ts 的核心
**文件**: `src/bridge/bridgeMain.ts`

```typescript
import { createBridgeApiClient } from './bridgeApi.js'
import { createSessionSpawner } from './sessionRunner.js'
import { getPollIntervalConfig } from './pollConfig.js'
import { getTrustedDeviceToken } from './trustedDevice.js'
import { createCapacityWake } from './capacityWake.js'

// 默认退避配置
const DEFAULT_BACKOFF: BackoffConfig = {
  connInitialMs: 2_000,       // 初始重连间隔
  connCapMs: 120_000,         // 最大重连间隔（2分钟）
  connGiveUpMs: 600_000,      // 放弃重连时间（10分钟）
  generalInitialMs: 500,
  generalCapMs: 30_000,
  generalGiveUpMs: 600_000,
}

const STATUS_UPDATE_INTERVAL_MS = 1_000  // 状态更新间隔
const SPAWN_SESSIONS_DEFAULT = 32        // 默认最大会话数
```

---

## 三、Bridge 的工作流程

### 3.1 工作流程序列
```
Bridge 进程启动
    ↓
注册 Worker → Bridge API
    ← 环境 ID + 令牌
    ↓
轮询等待任务
    ↓
用户（浏览器）→ 创建会话请求 → Bridge API
    ← 会话 URL
    ↓
Bridge 获取待处理任务 ← 新会话任务！
    ↓
启动 Claude Code 实例
    ← 实例就绪
    ↓
用户发送消息 "帮我修改代码"
    ↓
Bridge API 转发消息 → Bridge
    ↓
传递用户输入 → Claude Code 实例
    ↓
流式响应 → Bridge
    ↓
传回响应 → Bridge API
    ↓
显示 AI 回复 → 用户
```

---

## 四、REPL Bridge：交互式桥接

### 4.1 REPL Bridge 架构
```
本地 REPL（React/Ink UI）
    ↓
Bridge 组件（replBridge.ts）
    ↓
├── 📤 出站事件（响应、工具调用、状态）
└── 📥 入站消息（用户输入、控制命令）
    ↓
远程客户端
```

### 4.2 安全的命令过滤
**文件**: `src/commands.ts`

```typescript
// 桥接安全命令——只有这些命令可以通过 Bridge 执行
export const BRIDGE_SAFE_COMMANDS: Set<Command> = new Set([
  compact,      // 压缩上下文
  clear,        // 清屏
  cost,         // 显示成本
  summary,      // 总结对话
  releaseNotes, // 显示更新日志
  files,        // 列出文件
])

// 判断命令是否可以通过 Bridge 执行
export function isBridgeSafeCommand(cmd: Command): boolean {
  if (cmd.type === 'local-jsx') return false    // JSX 命令不安全
  if (cmd.type === 'prompt') return true         // 提示类命令安全
  return BRIDGE_SAFE_COMMANDS.has(cmd)
}
```

---

## 五、会话管理和状态同步

### 5.1 AppState 中的 Bridge 状态
**文件**: `src/state/AppStateStore.ts`

```typescript
// Bridge 相关的状态字段
{
  replBridgeEnabled: boolean,       // 是否启用
  replBridgeExplicit: boolean,      // 是否显式启用
  replBridgeOutboundOnly: boolean,  // 仅出站模式
  replBridgeConnected: boolean,     // 环境已注册
  replBridgeSessionActive: boolean, // WebSocket 已连接
  replBridgeReconnecting: boolean,  // 正在重连
  replBridgeConnectUrl?: string,    // 连接 URL
  replBridgeSessionUrl?: string,    // 会话 URL
  replBridgeEnvironmentId?: string, // 环境 ID
  replBridgeSessionId?: string,     // 会话 ID
  replBridgeError?: string,         // 错误信息
}
```

### 5.2 连接状态机
```
[*] → Disconnected
Disconnected → Connecting（启用 Bridge）
Connecting → Connected（环境注册成功）
Connected → SessionActive（用户连接）
SessionActive → Connected（用户断开）
Connected → Reconnecting（连接中断）
Reconnecting → Connected（重连成功）
Reconnecting → Disconnected（重连失败）
SessionActive → Reconnecting（连接中断）
```

---

## 六、Bridge 的退避和容错

### 6.1 退避配置
**文件**: `src/bridge/bridgeMain.ts`

```typescript
const DEFAULT_BACKOFF: BackoffConfig = {
  connInitialMs: 2_000,      // 首次重试等待 2 秒
  connCapMs: 120_000,        // 最长等待 2 分钟
  connGiveUpMs: 600_000,     // 10 分钟后放弃
  generalInitialMs: 500,
  generalCapMs: 30_000,
  generalGiveUpMs: 600_000,
}
```

### 6.2 指数退避策略
```
重试1: 2秒
    ↓
重试2: 4秒
    ↓
重试3: 8秒
    ↓
重试4: 16秒
    ↓
...
    ↓
重试N: 120秒（上限）
    ↓
总时间 > 10分钟 → 放弃
```

---

## 七、全架构总结

### 7.1 完整架构图
```
🖥️ 用户界面层
├── CLI 解析（Commander.js）
├── React/Ink UI（终端渲染）
└── Bridge UI（远程控制）
    ↓
⌨️ 命令与交互层
├── 命令系统（commands.ts）— 50+ 斜杠命令
└── 斜杠命令处理（/help /compact /mcp）
    ↓
🧠 查询引擎层
├── QueryEngine（QueryEngine.ts）— 查询生命周期
├── 查询循环（query.ts）— while(true) 核心
├── 自动压缩（autoCompact）
└── 流式工具执行（StreamingToolExecutor）
    ↓
🔧 工具与服务层
├── 40+ 内置工具（tools.ts）
├── MCP 扩展（services/mcp/）
├── 权限系统（permissions/）
├── Agent Swarm（AgentTool）
└── Bridge 桥接（bridge/）
    ↓
💾 状态与基础层
├── Store（state/store.ts）
├── AppState（AppStateStore.ts）
├── 配置系统（settings）
└── 并行预取（MDM/Keychain/GB）
```

### 7.2 数据流全景
```
用户 → "帮我修复 bug"
    ↓
CLI/UI → submitMessage(prompt)
    ↓
QueryEngine → 读取当前状态（AppState）
    ↓
构建系统提示
    ↓
query({messages, tools})
    ↓
自动压缩（如需要）
    ↓
发送请求 → Claude API
    ← 流式响应
    ↓
工具调用循环
├── 检测 tool_use
├── canUseTool? ← allow ✅
├── 执行工具（Tools）
├── 工具结果
├── 更新状态（AppState）
└── 继续请求 → Claude API
    ← 下一轮响应
    ↓
QueryEngine ← 最终结果
    ↓
CLI/UI → 显示给用户
    ↓
用户 ← "Bug 已修复！"
```

---

## 八、十课知识地图

| 课程 | 核心内容 |
|------|---------|
| 第1课 软件架构 | 分层设计、五层蛋糕、关注点分离 |
| 第2课 技术栈 | TypeScript 类型安全、Bun 运行时、React/Ink UI、feature() 门控 |
| 第3课 启动流程 | main.tsx 入口、CLI 解析、AppState 初始化 |
| 第4课 并行预取 | MDM 预取、Keychain 预取、GrowthBook 预取、Promise.all |
| 第5课 工具系统 | 40+ 工具、注册与发现、条件加载、工具池合并 |
| 第6课 查询引擎 | QueryEngine 类、query() 循环、流式执行、自动压缩 |
| 第7课 权限系统 | 权限模式、多层规则、运行时检查、沙箱保护 |
| 第8课 Agent Swarm | AgentTool、协调器模式、Worktree 隔离、团队协作 |
| 第9课 MCP 扩展 | 协议标准、多种传输、工具包装、安全模型 |
| 第10课 Bridge + 总结 | 远程桥接、会话管理、全架构回顾 |

---

## 九、架构设计原则总结

### 9.1 分层与模块化
```
每一层职责单一，通过接口通信
→ 添加新工具不需要改查询引擎
→ 换掉 UI 层不影响核心逻辑
```

### 9.2 并行优先
```
能并行的绝不串行
→ 启动时预取 MDM/Keychain/GrowthBook
→ 流式工具执行（边接收边执行）
→ Promise.all 并行加载技能和插件
```

### 9.3 安全纵深
```
多层防护，不依赖单点
→ 编译时门控 → 权限模式 → 规则匹配 → 运行时检查 → 沙箱
```

### 9.4 开放扩展
```
核心稳定，边缘灵活
→ MCP 协议让外部服务即插即用
→ 插件系统扩展命令和技能
→ Agent Swarm 实现多代理协作
```

### 9.5 优雅降级
```
失败不是终点，恢复才是
→ 自动压缩处理上下文过长
→ 模型降级处理服务不可用
→ 权限回退从自动模式到手动模式
→ Bridge 指数退避重连
```

---

## 十、动手练习

### 练习1：架构日记
用自己的话，写一篇 200 字的短文，描述 Claude Code 的整体架构。

### 练习2：设计一个新工具
假设要添加 `DocSearchTool`（文档搜索工具），思考：
- [ ] 工具定义文件放在哪个目录？
- [ ] 需要在 `tools.ts` 的哪里注册？
- [ ] 需要什么权限？
- [ ] 如何通过 MCP 提供给外部使用？

### 练习3：架构对比
选择一个熟悉的开源项目（如 VS Code、React），对比它和 Claude Code 的架构异同：
- [ ] 分层方式有什么不同？
- [ ] 插件/扩展机制有什么相似之处？
- [ ] 状态管理方案有何差异？

---

## 十一、课程总结

| 课程 | 核心收获 |
|------|---------|
| 第1课 | 架构就是"系统的设计图"，Claude Code 是五层蛋糕 |
| 第2课 | TypeScript 保安全，Bun 求速度，React/Ink 做界面 |
| 第3课 | 启动不是一步，而是精心编排的多步骤流水线 |
| 第4课 | 能并行就并行，135ms 的 import 时间不浪费 |
| 第5课 | 40+ 工具通过统一接口管理，条件加载很灵活 |
| 第6课 | QueryEngine 是大脑，query() 循环是心跳 |
| 第7课 | 安全靠纵深防御，权限不是一刀切 |
| 第8课 | 多代理并行协作，隔离和通信缺一不可 |
| 第9课 | MCP 让 Claude Code 成为开放平台 |
| 第10课 | Bridge 打破本地限制，架构设计有章可循 |

### 继续学习的方向
1. **动手实践**：尝试给 Claude Code 贡献代码或开发 MCP 服务器
2. **深入源码**：选择一个感兴趣的模块，完整阅读其源码
3. **架构思考**：在自己的项目中尝试应用学到的架构原则
4. **社区参与**：加入 Claude Code 社区，分享学习心得

> **架构不是记忆，而是理解。不是终点，而是起点。**
>
> 祝你在软件架构的世界里，越走越远！

---

## 十二、关联文件

### 12.1 上一章
- [09-mcp-extension.md](09-mcp-extension.md) - MCP 扩展系统

### 12.2 下一篇
- [../part03-tools/01-tool-system-overview.md](../part03-tools/01-tool-system-overview.md) - 工具系统详解

---

*此细纲由 Claude Code 自动生成*
