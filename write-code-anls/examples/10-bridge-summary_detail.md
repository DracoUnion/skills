# 10-bridge-summary.md 细纲

## 一、标题层级结构

### 1. Bridge 架构总结与扩展思路
- 学习目标（5点）
- Bridge 全景回顾
  - 完整架构图
  - 数据流全景
- 核心知识速查表
  - 按课程汇总
  - 消息类型速查
- 设计模式总结
  - 适配器模式（Adapter）
  - 观察者模式（Observer）
  - 环形缓冲区（Ring Buffer）
  - 依赖注入（Dependency Injection）
  - 代际号防竞态（Generation Counter）
  - 两阶段终止（Two-Phase Shutdown）
- 设计权衡分析
  - 轮询 vs 推送
  - v1 vs v2
  - 内存 vs 准确性
  - 安全 vs 便利
- 错误处理总结
  - 错误分类
  - 错误恢复策略
- 可扩展性分析
  - 当前架构的优势
  - 潜在扩展方向
- 从 Bridge 学到的通用工程经验
- 综合练习
- 文件与概念速查索引
  - 按文件名查
  - 按概念查
- 课程完结语

## 二、关键知识点

1. **核心设计模式**
   - 适配器模式：ReplBridgeTransport 统一 v1/v2
   - 观察者模式：事件回调机制
   - 环形缓冲区：BoundedUUIDSet
   - 依赖注入：createSessionSpawner(deps)
   - 代际号防竞态：Token 刷新调度
   - 两阶段终止：SIGTERM → SIGKILL

2. **设计权衡**
   - 轮询：简单可靠，适合低频任务
   - 推送：实时性高，适合会话消息
   - v1：简单，可观测性差
   - v2：复杂，可观测性好

3. **错误恢复策略**
   - 网络断连：指数退避重连
   - Token 过期：自动刷新
   - 401：刷新 OAuth Token
   - Epoch 不匹配：关闭重连

4. **工程经验**
   - 接口优于实现
   - 防御性编程
   - 优雅降级
   - 可观测性
   - 渐进式发布
   - 内存安全

## 三、源码文件路径

- `bridge/types.ts` - 类型定义
- `bridge/bridgeMain.ts` - 主循环
- `bridge/bridgeMessaging.ts` - 消息路由
- `bridge/jwtUtils.ts` - JWT 工具
- `bridge/sessionRunner.ts` - 会话管理
- `bridge/replBridgeTransport.ts` - 传输层
- `bridge/bridgeEnabled.ts` - 功能开关
- `bridge/bridgeApi.ts` - API 客户端
- `bridge/workSecret.ts` - 密钥解码
- `bridge/bridgeConfig.ts` - 配置

## 四、类名、函数名、接口名

### 核心类型
- `BridgeConfig` - Bridge 配置
- `SessionHandle` - 会话控制柄
- `ReplBridgeTransport` - 传输层接口
- `BackoffConfig` - 退避配置
- `BoundedUUIDSet` - 有界 UUID 集合

### 核心函数
- `runBridgeLoop()` - 主循环
- `createV1ReplTransport()` / `createV2ReplTransport()` - 传输层
- `createTokenRefreshScheduler()` - Token 刷新
- `createSessionSpawner()` - 会话生成器
- `isBridgeEnabled()` - 功能开关
- `decodeWorkSecret()` - 密钥解码

### 设计模式相关
- 适配器模式：V1Transport / V2Transport
- 观察者模式：setOnData / setOnClose / setOnConnect
- 环形缓冲区：BoundedUUIDSet
- 代际号：nextGeneration()
