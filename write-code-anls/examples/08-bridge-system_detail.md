# 第八课：双向传送门 —— IDE 桥接系统详解 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第八课：双向传送门 —— IDE 桥接系统详解

### 1.2 二级标题
- 学习目标
- 一、生活类比：翻译官
- 二、Bridge 系统架构
- 三、ReplBridge：单会话桥接
- 四、BridgeMain：多会话管理
- 五、认证与安全
- 六、消息处理
- 七、传输层
- 八、Capacity Wake：容量唤醒
- 九、会话运行器
- 十、权限桥接
- 十一、动手练习
- 十二、本课小结
- 下节预告

### 1.3 三级标题
- 2.1 核心模块
- 2.2 通信架构
- 3.1 桥接句柄
- 3.2 消息写入
- 4.1 核心设计
- 4.2 会话生命周期
- 4.3 退避重连
- 5.1 JWT 令牌管理
- 5.2 可信设备
- 5.3 工作密钥
- 5.4 认证流程
- 6.1 入站消息处理
- 6.2 消息去重
- 6.3 入站附件
- 7.1 V1 与 V2 传输
- 7.2 混合传输
- 9.1 SessionRunner
- 9.2 多会话管理

---

## 2. 关键知识点

### 2.1 Bridge 系统核心模块
| 文件 | 功能 |
|------|------|
| `bridgeMain.ts` | 主入口，多会话管理 |
| `replBridge.ts` | REPL 桥接，单会话管理 |
| `bridgeApi.ts` | API 客户端 |
| `bridgeMessaging.ts` | 消息处理 |
| `bridgeConfig.ts` | 配置管理 |
| `jwtUtils.ts` | JWT 认证 |
| `capacityWake.ts` | 容量唤醒 |
| `sessionRunner.ts` | 会话运行器 |

### 2.2 通信架构
```
IDE (VS Code/Cursor) ↔ Bridge 服务 ↔ CLI (Claude Code)
```

### 2.3 ReplBridge 句柄
| 方法 | 功能 |
|------|------|
| `writeMessages(messages)` | 发送消息 |
| `writeSdkMessages(messages)` | 发送 SDK 消息 |
| `sendControlRequest(request)` | 发送控制请求 |
| `sendControlResponse(response)` | 发送控制响应 |
| `sendResult()` | 发送结果 |
| `teardown()` | 清理 |

### 2.4 会话生命周期
```
Connecting → Connected → Polling → SessionStarted → SessionRunning → SessionCompleted/SessionFailed → Polling
```

### 2.5 退避配置
- `connInitialMs: 2_000` - 首次重连等待 2 秒
- `connCapMs: 120_000` - 最大等待 2 分钟
- `connGiveUpMs: 600_000` - 10 分钟后放弃

### 2.6 传输协议
- **V1** - 基于 HTTP 轮询
- **V2** - 基于 WebSocket（更低延迟）
- **混合传输** - WebSocket 用于实时消息，HTTP 用于大数据传输

### 2.7 Capacity Wake
- 当 Bridge 服务器繁忙时，CLI 进入等待状态
- 有可用容量时唤醒等待的客户端

---

## 3. 涉及的源码文件路径

### 3.1 Bridge 核心
- `bridge/bridgeMain.ts` - 多会话管理
- `bridge/replBridge.ts` - 单会话桥接
- `bridge/bridgeApi.ts` - API 客户端
- `bridge/bridgeMessaging.ts` - 消息处理
- `bridge/bridgeConfig.ts` - 配置管理
- `bridge/bridgePermissionCallbacks.ts` - 权限回调
- `bridge/bridgeUI.ts` - UI 日志
- `bridge/bridgeStatusUtil.ts` - 状态工具
- `bridge/types.ts` - 类型定义

### 3.2 Bridge 认证与安全
- `bridge/jwtUtils.ts` - JWT 认证
- `bridge/workSecret.ts` - 工作密钥
- `bridge/trustedDevice.ts` - 可信设备

### 3.3 Bridge 传输与会话
- `bridge/sessionRunner.ts` - 会话运行器
- `bridge/capacityWake.ts` - 容量唤醒
- `bridge/replBridgeTransport.ts` - 传输层
- `bridge/inboundAttachments.ts` - 入站附件

### 3.4 相关传输
- `cli/transports/HybridTransport.ts` - 混合传输

---

## 4. 类名、函数名、接口名

### 4.1 类型/接口
- `ReplBridgeHandle` - 桥接句柄
- `BackoffConfig` - 退避配置
- `CapacitySignal` - 容量信号
- `SessionSpawner` - 会话生成器
- `BoundedUUIDSet` - 有限大小 UUID 集合

### 4.2 函数
- `createReplBridgeHandle()` - 创建桥接句柄
- `handleIngressMessage(message)` - 处理入站消息
- `isEligibleBridgeMessage(message)` - 检查消息是否可桥接
- `extractTitleText(message)` - 提取消息标题
- `createTokenRefreshScheduler()` - 创建令牌刷新调度器
- `getTrustedDeviceToken()` - 获取可信设备令牌
- `decodeWorkSecret(secret)` - 解码工作密钥
- `buildSdkUrl(config)` - 构建 SDK URL
- `createCapacityWake()` - 创建容量唤醒
- `createSessionSpawner()` - 创建会话生成器
- `safeFilenameId(id)` - 安全文件名 ID
- `createV1ReplTransport()` - 创建 V1 传输
- `createV2ReplTransport()` - 创建 V2 传输

### 4.3 常量
- `DEFAULT_BACKOFF` - 默认退避配置
- `SPAWN_SESSIONS_DEFAULT = 32` - 默认最大并发会话数

---

## 5. 代码片段重点

### 5.1 ReplBridge 句柄（replBridge.ts）
```typescript
export type ReplBridgeHandle = {
  bridgeSessionId: string;
  environmentId: string;
  sessionIngressUrl: string;
  writeMessages(messages: Message[]): void;
  writeSdkMessages(messages: SDKMessage[]): void;
  sendControlRequest(request): void;
  sendControlResponse(response): void;
  sendResult(): void;
  teardown(): Promise<void>;
};
```

### 5.2 退避配置（bridgeMain.ts）
```typescript
const DEFAULT_BACKOFF: BackoffConfig = {
  connInitialMs: 2_000,
  connCapMs: 120_000,
  connGiveUpMs: 600_000,
  generalInitialMs: 500,
  generalCapMs: 30_000,
  generalGiveUpMs: 600_000,
};
```

### 5.3 JWT 令牌管理（jwtUtils.ts）
```typescript
export function createTokenRefreshScheduler() {
  // 定期检查令牌有效期
  // 在过期前自动刷新
}
```

### 5.4 工作密钥（workSecret.ts）
```typescript
export function decodeWorkSecret(secret: string) {
  // 解码工作密钥
  // 用于安全地传递会话信息
}

export function buildSdkUrl(config) {
  // 构建 SDK 连接 URL
  // 包含认证信息
}
```

### 5.5 消息去重（bridgeMessaging.ts）
```typescript
export class BoundedUUIDSet {
  // 有限大小的 UUID 集合
  // 用于消息去重
  // 防止同一消息被处理多次
}
```

### 5.6 传输层（replBridgeTransport.ts）
```typescript
export function createV1ReplTransport() {
  // V1 传输：基于 HTTP 轮询
}

export function createV2ReplTransport() {
  // V2 传输：基于 WebSocket（更低延迟）
}
```

### 5.7 容量唤醒（capacityWake.ts）
```typescript
export function createCapacityWake(): CapacitySignal {
  // 创建容量信号
  // 当服务端有空闲容量时触发
  // CLI 被唤醒并开始处理
}
```

### 5.8 会话运行器（sessionRunner.ts）
```typescript
export function createSessionSpawner(): SessionSpawner {
  // 创建会话生成器
  // 管理会话的创建和销毁
}

export function safeFilenameId(id: string): string {
  // 将会话 ID 转换为安全的文件名
  // 用于日志和临时文件
}
```

### 5.9 多会话管理（bridgeMain.ts）
```typescript
const SPAWN_SESSIONS_DEFAULT = 32;
// 默认最多同时运行 32 个会话
```
