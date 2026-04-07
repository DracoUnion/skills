# 06-jwt-authentication.md 细纲

## 一、标题层级结构

### 1. JWT 认证详解——Token 解码与自动刷新
- 学习目标（5点）
- JWT 是什么？
  - 生活类比：电影票
  - JWT 的编码格式
- Token 解码源码解析
  - 解码 JWT 载荷
  - 图解解码过程
  - 获取过期时间
- 自动刷新机制
  - 为什么需要自动刷新？
  - 刷新调度器的配置
  - createTokenRefreshScheduler 函数
  - schedule 方法详解
  - 刷新时间线
- 代际（Generation）防竞态
  - 竞态问题是什么？
  - 代际号解决方案
  - 代际号的工作流程
- 失败重试与连锁刷新
  - 失败重试
  - 连锁刷新
- 两种 Token 的区别
  - OAuth Token vs Session Ingress Token
  - 从源码看 Token 获取
  - Token 在 API 请求中的使用
- Bridge 中的 Token 刷新实践
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **JWT 结构**
   - Header: 类型和加密方式
   - Payload: 实际信息（sub, exp, iat）
   - Signature: 签名
   - Base64URL 编码

2. **Token 解码**
   - `decodeJwtPayload()` - 解码 Payload
   - `decodeJwtExpiry()` - 获取过期时间
   - 不验证签名，只读取信息

3. **自动刷新配置**
   - TOKEN_REFRESH_BUFFER_MS: 5 分钟（提前刷新）
   - FALLBACK_REFRESH_INTERVAL_MS: 30 分钟（无法获取过期时间）
   - MAX_REFRESH_FAILURES: 3（最多重试次数）

4. **代际号防竞态**
   - `nextGeneration()` - 递增代际号
   - 旧回调检测到代际号变化则跳过
   - 避免异步回调竞态条件

5. **两种 Token 区别**
   - OAuth Token: 调用 Bridge API，小时级有效期
   - Session Ingress Token: 会话级别，较短有效期

6. **v1 vs v2 刷新策略**
   - v1: 直接替换子进程 Token
   - v2: 触发 reconnectSession 重新分发

## 三、源码文件路径

- `bridge/jwtUtils.ts` - JWT 工具函数
- `bridge/bridgeConfig.ts` - Token 获取
- `bridge/bridgeApi.ts` - API 请求头

## 四、类名、函数名、接口名

### 核心函数
- `decodeJwtPayload()` - 解码 JWT Payload
- `decodeJwtExpiry()` - 获取过期时间
- `createTokenRefreshScheduler()` - 创建刷新调度器
- `base64URLEncode()` - Base64URL 编码
- `nextGeneration()` - 获取下一代际号

### 类型
- `TokenRefreshScheduler` - 刷新调度器类型
  - `schedule()` - 安排刷新
  - `scheduleFromExpiresIn()` - 根据 TTL 安排
  - `cancel()` - 取消刷新
  - `cancelAll()` - 取消所有刷新

### 常量
- `TOKEN_REFRESH_BUFFER_MS = 5 * 60 * 1000` - 提前 5 分钟刷新
- `FALLBACK_REFRESH_INTERVAL_MS = 30 * 60 * 1000` - 回退刷新间隔
- `MAX_REFRESH_FAILURES = 3` - 最大失败次数
- `REFRESH_RETRY_DELAY_MS = 60_000` - 重试延迟
