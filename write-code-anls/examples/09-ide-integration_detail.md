# 09-ide-integration.md 细纲

## 一、标题层级结构

### 1. VS Code / JetBrains 集成实践
- 学习目标（5点）
- IDE 集成的全景图
  - 生活类比：手机遥控空调
  - 完整集成架构
- 功能开关：谁能用 Bridge？
  - 多层门禁
  - 基础开关：isBridgeEnabled
  - 阻塞式开关：isBridgeEnabledBlocking
  - 诊断信息：getBridgeDisabledReason
- 版本兼容性检查
  - 最低版本要求
- REPL Bridge 初始化
  - 初始化选项
  - 初始化流程
  - 信息收集
- SDK URL 构建
  - v1 WebSocket URL
  - v2 HTTP URL
  - 本地 vs 生产环境
- v1 vs v2 桥接路径
  - 环境选择
  - 会话 ID 兼容性
- IDE 中的用户体验
  - Worker 类型标识
  - 自动连接
  - 镜像模式
- 安全考虑
  - Token 隔离
  - 路径安全
  - 设备信任
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **功能开关多层检查**
   - 构建时开关（BRIDGE_MODE）
   - claude.ai 订阅检查
   - GrowthBook 灰度开关（tengu_ccr_bridge）
   - 版本检查

2. **两种检查方式**
   - isBridgeEnabled(): 缓存值，快速但可能过时
   - isBridgeEnabledBlocking(): 阻塞检查，准确但慢

3. **SDK URL 构建**
   - 本地: ws:// + /v2/（直连）
   - 生产: wss:// + /v1/（经 Envoy 代理）

4. **会话 ID 兼容**
   - session_* 前缀（v1）
   - cse_* 前缀（v2）
   - sameSessionId() 比较后缀

5. **Worker 类型**
   - claude_code: 普通代码任务
   - claude_code_assistant: 助手面板任务

6. **安全机制**
   - Token 隔离：子进程使用独立 Session Token
   - 路径验证：validateBridgeId 防止路径遍历
   - 设备信任：X-Trusted-Device-Token

## 三、源码文件路径

- `bridge/bridgeEnabled.ts` - 功能开关
- `bridge/initReplBridge.ts` - 初始化
- `bridge/workSecret.ts` - SDK URL 构建
- `bridge/bridgeConfig.ts` - Token 获取

## 四、类名、函数名、接口名

### 核心函数
- `isBridgeEnabled()` - 检查 Bridge 是否启用（缓存）
- `isBridgeEnabledBlocking()` - 检查 Bridge 是否启用（阻塞）
- `getBridgeDisabledReason()` - 获取禁用原因
- `checkBridgeMinVersion()` - 检查最低版本
- `initReplBridge()` - 初始化 REPL Bridge
- `buildSdkUrl()` - 构建 v1 SDK URL
- `buildCCRv2SdkUrl()` - 构建 v2 SDK URL
- `sameSessionId()` - 比较会话 ID

### 类型
- `InitBridgeOptions` - 初始化选项
- `BridgeWorkerType` - Worker 类型
- `BridgeState` - Bridge 状态

### 常量
- `tengu_ccr_bridge` - Bridge 功能开关
- `tengu_bridge_repl_v2` - v2 路径开关
- `tengu_cobalt_harbor` - 自动连接开关
- `tengu_ccr_mirror` - 镜像模式开关
