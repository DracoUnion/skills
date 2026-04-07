# 07-session-runner.md 细纲

## 一、标题层级结构

### 1. sessionRunner 会话管理——子进程生命周期
- 学习目标（5点）
- 子进程的生活类比
  - 餐厅模型
  - 三个通道
- SessionSpawner 核心结构
  - 依赖注入
  - SessionHandle：进程控制手柄
- 子进程的创建
  - 构建启动参数
  - 环境变量设置
  - 实际创建进程
- stdout 解析：NDJSON 流
  - 什么是 NDJSON？
  - stdout 读取逻辑
  - 消息处理流程
- 活动追踪
  - 工具名称映射
  - 活动摘要生成
  - 活动类型
- stderr 处理
- 进程退出处理
  - 退出状态判定
  - 退出状态流程
- kill 与 forceKill
  - 优雅终止（SIGTERM）
  - 强制终止（SIGKILL）
  - 两阶段终止
- Token 热更新
- 文件名安全处理
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **三通道模型**
   - stdin: 父进程 → 子进程（指令/Token 更新）
   - stdout: 子进程 → 父进程（NDJSON 消息流）
   - stderr: 子进程 → 父进程（错误/调试信息）

2. **NDJSON 格式**
   - Newline Delimited JSON
   - 每行一个 JSON 对象
   - 适合流式处理

3. **SessionHandle 方法**
   - kill(): 发送 SIGTERM
   - forceKill(): 发送 SIGKILL
   - writeStdin(): 写入 stdin
   - updateAccessToken(): 更新 Token

4. **活动追踪**
   - TOOL_VERBS: 工具名到动词映射
   - toolSummary(): 生成活动摘要
   - 环形缓冲：最多保留 10 条活动

5. **退出状态**
   - completed: 正常完成（code === 0）
   - interrupted: 被中断（SIGTERM/SIGINT）
   - failed: 异常退出

6. **两阶段终止**
   - SIGTERM: 请求优雅退出
   - 等待 30 秒
   - SIGKILL: 强制终止

## 三、源码文件路径

- `bridge/sessionRunner.ts` - 会话运行器
- `bridge/types.ts` - SessionHandle 类型

## 四、类名、函数名、接口名

### 类型
- `SessionSpawner` - 会话生成器类型
- `SessionHandle` - 会话控制柄
- `SessionActivity` - 会话活动
- `SessionDoneStatus` - 会话完成状态

### 核心函数
- `createSessionSpawner()` - 创建会话生成器
- `safeSpawn()` - 安全生成子进程
- `toolSummary()` - 生成工具活动摘要
- `extractActivities()` - 提取活动信息
- `safeFilenameId()` - 安全文件名处理

### 常量
- `MAX_ACTIVITIES = 10` - 最大活动记录数
- `MAX_STDERR_LINES = 10` - 最大 stderr 保留行数

### 方法
- `kill()` - 优雅终止
- `forceKill()` - 强制终止
- `writeStdin()` - 写入标准输入
- `updateAccessToken()` - 热更新 Token
