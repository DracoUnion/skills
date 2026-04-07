# 08-transport-layer.md 细纲

## 一、标题层级结构

### 1. 传输层抽象——v1/v2 双模式设计
- 学习目标（4点）
- 为什么需要传输层抽象？
  - 生活类比：USB-C 统一接口
  - 对比没有抽象 vs 有抽象
- ReplBridgeTransport 接口详解
  - 完整接口定义
  - 接口分层图
- v1 传输层：WebSocket + POST
  - v1 架构图
  - v1 适配器实现
- v2 传输层：SSE + CCRClient
  - v2 架构图
  - v2 创建过程
  - 认证机制差异
- Epoch 机制
  - 什么是 Epoch？
  - Epoch 不匹配的处理
  - Worker 注册
- SSE 序列号与断线恢复
  - 序列号的作用
  - 传输层交换时的序列号传递
  - v1 vs v2 断线恢复对比
- v2 的连接初始化
  - SSE 和 CCR 并行启动
  - 连接时序图
  - outboundOnly 模式
- 事件交付确认
  - 交付状态
  - 自动双重确认
- 自定义关闭码
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **适配器模式**
   - ReplBridgeTransport 统一接口
   - V1Transport / V2Transport 分别实现
   - 上层代码无需关心底层协议

2. **v1 传输层**
   - WebSocket 读取
   - HTTP POST 写入
   - getLastSequenceNum() 返回 0

3. **v2 传输层**
   - SSE 读取（/worker/events/stream）
   - CCRClient POST 写入（/worker/events）
   - 支持序列号断线恢复

4. **Epoch 机制**
   - Worker 纪元号，每次注册递增
   - 旧实例收到 409 Conflict 自动关闭
   - 防止旧 Worker 干扰新 Worker

5. **序列号恢复**
   - SSE 事件带递增序列号
   - 断线重连时发送 from_sequence_num
   - 服务器从断点继续推送

6. **交付确认**
   - received: 已收到
   - processed: 已处理
   - 自动双重确认避免重复投递

## 三、源码文件路径

- `bridge/replBridgeTransport.ts` - 传输层抽象
- `bridge/workSecret.ts` - Worker 注册

## 四、类名、函数名、接口名

### 类型
- `ReplBridgeTransport` - 传输层统一接口
- `SSETransport` - SSE 传输
- `CCRClient` - CCR v2 客户端
- `HybridTransport` - v1 混合传输

### 核心函数
- `createV1ReplTransport()` - 创建 v1 传输层
- `createV2ReplTransport()` - 创建 v2 传输层
- `registerWorker()` - 注册 Worker 获取 Epoch
- `buildSdkUrl()` - 构建 SDK URL
- `buildCCRv2SdkUrl()` - 构建 CCR v2 URL

### 方法
- `write()` / `writeBatch()` - 写入消息
- `connect()` - 建立连接
- `close()` - 关闭连接
- `getLastSequenceNum()` - 获取最后序列号
- `reportState()` - 报告状态（v2）
- `reportDelivery()` - 报告交付状态（v2）

### 常量
- 关闭码 4090: Epoch 不匹配
- 关闭码 4091: 初始化失败
- 关闭码 4092: SSE 重连预算耗尽
