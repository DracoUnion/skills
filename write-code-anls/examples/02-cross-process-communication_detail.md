# 02-cross-process-communication.md 细纲

## 一、标题层级结构

### 1. 跨进程通信基础——WebSocket / SSE / HTTP
- 学习目标（4点）
- 三种通信方式的生活类比
  - HTTP：写信
  - WebSocket：打电话
  - SSE：听广播
  - 三者对比
- Bridge 中的通信协议
  - 整体通信架构
  - HTTP 用在哪里？
  - WebSocket 用在哪里？
  - SSE 用在哪里？
- 轮询 vs 推送
  - 轮询（Polling）
  - 推送（Push）
  - 为什么同时使用两种？
- 传输层抽象：统一接口
  - 为什么需要抽象？
  - 适配器模式
- v1 vs v2 的区别
  - v1：WebSocket + HTTP POST
  - v2：SSE + CCRClient
  - 对比表
- 错误处理与重试
  - HTTP 请求的 401 重试
  - 连接退避策略
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **三种通信协议对比**
   - HTTP: 一问一答，短连接，无状态
   - WebSocket: 双向实时，长连接，有状态
   - SSE: 服务器单向推送，长连接，自动重连

2. **Bridge 协议使用场景**
   - HTTP: 管理操作（注册、轮询、确认）
   - WebSocket: v1 传输层读取通道
   - SSE: v2 传输层读取通道

3. **轮询 vs 推送**
   - 等待新任务: 轮询（简单可靠）
   - 会话消息: 推送（实时性要求高）

4. **传输层抽象**
   - ReplBridgeTransport 统一接口
   - 适配器模式隔离 v1/v2 差异

5. **v1 vs v2 对比**
   - v1: WebSocket 读 + POST 写
   - v2: SSE 读 + CCRClient POST 写
   - v2 支持断线恢复（序列号）、交付确认

6. **退避策略**
   - 指数退避: 2秒 → 4秒 → 8秒 → ... → 120秒
   - 10分钟后放弃

## 三、源码文件路径

- `bridge/bridgeApi.ts` - HTTP API 客户端
- `bridge/replBridgeTransport.ts` - 传输层抽象
- `bridge/bridgeMain.ts` - 退避配置

## 四、类名、函数名、接口名

### 类型
- `ReplBridgeTransport` - 传输层统一接口
- `HybridTransport` - v1 混合传输
- `SSETransport` - SSE 传输
- `CCRClient` - CCR v2 客户端

### 核心函数
- `createV1ReplTransport()` - 创建 v1 传输层
- `createV2ReplTransport()` - 创建 v2 传输层
- `withOAuthRetry()` - 401 重试包装
- `pollForWork()` - 轮询工作

### 常量
- `DEFAULT_BACKOFF` - 默认退避配置
  - connInitialMs: 2000
  - connCapMs: 120000
  - connGiveUpMs: 600000
