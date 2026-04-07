# 01-what-is-bridge.md 细纲

## 一、标题层级结构

### 1. 什么是 Bridge？为什么 CLI 需要连接 IDE？
- 学习目标（4点）
- 什么是 Bridge？
  - 生活类比：同声传译
  - 一句话定义
- 为什么需要 Bridge？
  - 两个独立的进程
  - 没有 Bridge 会怎样？
  - Bridge 解决了什么？
- Bridge 的核心架构
  - 整体架构图
  - BridgeConfig 类型定义
  - 三种工作模式（SpawnMode）
- Bridge 的生命周期
  - 从启动到退出
  - 启动入口：bridgeMain.ts
- Bridge 的核心文件清单
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **Bridge 定义**
   - CLI 和 IDE 之间的通信桥梁
   - 通过网络协议（WebSocket/SSE/HTTP）实现跨进程通信

2. **三种工作模式**
   - single-session: 一对一私教
   - worktree: 多间教室（独立 Git worktree）
   - same-dir: 共享教室（共享工作目录）

3. **BridgeConfig 核心字段**
   - dir: 工作目录
   - machineName: 机器名
   - branch: Git 分支
   - maxSessions: 最大并发会话数
   - spawnMode: 工作模式
   - bridgeId: Bridge 唯一标识

4. **生命周期流程**
   - 注册环境（registerBridgeEnvironment）
   - 轮询工作（pollForWork）
   - 生成子进程（spawn）
   - 注销环境（deregisterEnvironment）

## 三、源码文件路径

- `bridge/types.ts` - Bridge 类型定义
- `bridge/bridgeMain.ts` - 主循环入口
- `bridge/bridgeApi.ts` - API 客户端
- `bridge/bridgeConfig.ts` - 配置解析

## 四、类名、函数名、接口名

### 类型
- `BridgeConfig` - Bridge 配置类型
- `SpawnMode` - 工作模式类型（single-session/worktree/same-dir）
- `BridgeApiClient` - API 客户端类型
- `SessionSpawner` - 会话生成器类型
- `BridgeLogger` - 日志记录器类型

### 核心函数
- `runBridgeLoop()` - Bridge 主循环
- `registerBridgeEnvironment()` - 注册 Bridge 环境
- `deregisterEnvironment()` - 注销 Bridge 环境
- `pollForWork()` - 轮询工作

### 常量
- `DEFAULT_BACKOFF` - 默认退避配置
