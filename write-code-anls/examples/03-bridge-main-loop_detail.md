# 03-bridge-main-loop.md 细纲

## 一、标题层级结构

### 1. bridgeMain.ts 主循环源码解析
- 学习目标（5点）
- 主循环的生活类比
  - Bridge 像一个快递站
- `runBridgeLoop()` 全景图
  - 函数签名
  - 内部状态管理
  - 主循环流程图
- 轮询阶段详解
  - 轮询节奏控制
  - 退避过程的可视化
  - 睡眠检测
- 会话生成阶段
  - 安全生成
  - 会话生成的完整流程
  - 工作密钥解码
- 多会话管理
  - 容量控制
  - 会话完成回调
- 心跳机制
  - 为什么需要心跳？
  - 心跳认证过期后的恢复
- 优雅关闭
  - 关闭流程
  - SIGTERM → SIGKILL 升级
- Token 刷新调度
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **主循环流程**
   - 检查停止信号
   - 检查容量
   - 轮询工作
   - 生成会话
   - 清理完成会话

2. **内部状态管理**
   - activeSessions: 活跃会话 Map
   - sessionStartTimes: 会话开始时间
   - completedWorkIds: 已完成工作 ID
   - timedOutSessions: 已超时会话

3. **退避策略配置**
   - connInitialMs: 2000（连接错误初始）
   - connCapMs: 120000（最多 2 分钟）
   - generalInitialMs: 500（一般错误初始）

4. **睡眠检测**
   - 阈值 = connCapMs × 2
   - 检测时间跳跃判断系统睡眠

5. **会话生成流程**
   - pollForWork() 获取任务
   - decodeWorkSecret() 解码密钥
   - spawner.spawn() 创建子进程
   - acknowledgeWork() 确认工作

6. **优雅关闭**
   - SIGTERM（请求退出）
   - 等待 30 秒（shutdownGraceMs）
   - SIGKILL（强制终止）
   - deregisterEnvironment() 注销环境

## 三、源码文件路径

- `bridge/bridgeMain.ts` - 主循环
- `bridge/workSecret.ts` - 工作密钥解码
- `bridge/pollConfig.ts` - 轮询配置

## 四、类名、函数名、接口名

### 类型
- `BackoffConfig` - 退避配置
- `SessionHandle` - 会话控制柄
- `WorkResponse` - 工作响应
- `WorkSecret` - 工作密钥

### 核心函数
- `runBridgeLoop()` - Bridge 主循环
- `safeSpawn()` - 安全生成会话
- `heartbeatActiveWorkItems()` - 心跳活跃工作项
- `decodeWorkSecret()` - 解码工作密钥
- `pollSleepDetectionThresholdMs()` - 睡眠检测阈值

### 常量
- `DEFAULT_BACKOFF` - 默认退避配置
- `shutdownGraceMs` - 优雅关闭等待时间（30秒）
