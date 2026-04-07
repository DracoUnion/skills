# 图解 Claude Code 完全指南 - 细纲

## 文件信息
- **原文件**: 09-feature-flags-telemetry.md
- **类型**: 第 9 课：特性标志与遥测系统
- **难度**: ★★★☆☆

---

## 一、文档结构概览

### 1.1 学习目标
1. 理解特性标志（Feature Flags）的概念和在 Claude Code 中的用途
2. 掌握 GrowthBook 集成的三种读取模式
3. 学会事件日志系统的队列架构和安全约束
4. 了解 Datadog 日志上报和采样策略

### 1.2 章节结构
| 章节 | 主题 | 核心内容 |
|------|------|---------|
| 一、"遥控器"的比喻 | 概念入门 | 特性标志与遥测类比 |
| 二、事件日志 | 核心实现 | 最小依赖原则、队列架构 |
| 三、GrowthBook 特性标志 | 核心实现 | 三种读取模式 |
| 四、Datadog 日志上报 | 实现细节 | 白名单、批量发送 |
| 五、实验曝光记录 | 实现细节 | 曝光去重 |
| 六、认证变更后的刷新 | 特殊处理 | 客户端重建 |

---

## 二、关键知识点

### 2.1 概念类比
| 概念 | 类比 | 作用 |
|------|------|------|
| Feature Flag | 电灯开关 | 远程控制功能启用/禁用 |
| A/B 测试 | 药物临床试验 | 将用户分组测试效果 |
| 遥测事件 | 心电监测仪 | 实时监控运行状态 |
| 采样 | 抽样调查 | 降低数据量和成本 |

### 2.2 事件日志设计理念
```typescript
// services/analytics/index.ts
/**
 * DESIGN: This module has NO dependencies to avoid import cycles.
 * Events are queued until attachAnalyticsSink() is called during app initialization.
 */
```

analytics 模块被设计为**零依赖** —— 它可以被任何其他模块安全导入，不会形成循环依赖。

### 2.3 核心 API
```typescript
// 同步日志（fire-and-forget）
export function logEvent(
  eventName: string,
  metadata: LogEventMetadata,  // 不允许字符串类型！
): void {
  if (sink === null) {
    eventQueue.push({ eventName, metadata, async: false })
    return
  }
  sink.logEvent(eventName, metadata)
}

// 异步日志（等待确认）
export async function logEventAsync(
  eventName: string,
  metadata: LogEventMetadata,
): Promise<void> {
  if (sink === null) {
    eventQueue.push({ eventName, metadata, async: true })
    return
  }
  await sink.logEventAsync(eventName, metadata)
}
```

### 2.4 安全类型约束
```typescript
// 防止意外记录代码或文件路径
type LogEventMetadata = {
  [key: string]: boolean | number | undefined
  // 注意：不允许 string 类型！
}

// 需要字符串时，必须显式标记已验证
type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS = never

// 使用时必须强制类型转换
logEvent('tengu_error', {
  error: errorMsg as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
})
```

### 2.5 GrowthBook 三种读取模式
- `_CACHED_MAY_BE_STALE`：磁盘缓存 · 非阻塞 · 可能过时
- `_BLOCKS_ON_INIT`：等待初始化 · 阻塞 · 最新值
- `_CACHED_OR_BLOCKING`：缓存优先 · 降级阻塞

### 2.6 覆盖优先级
```
环境变量覆盖 > 本地配置覆盖 > 内存值 > 磁盘缓存 > 默认值
```

### 2.7 周期性刷新
```typescript
// 内部员工：每 20 分钟刷新
// 外部用户：每 6 小时刷新
const GROWTHBOOK_REFRESH_INTERVAL_MS =
  process.env.USER_TYPE !== 'ant'
    ? 6 * 60 * 60 * 1000  // 6 hours
    : 20 * 60 * 1000       // 20 min
```

### 2.8 Datadog 日志上报

#### 事件白名单
```typescript
// services/analytics/datadog.ts
const DATADOG_ALLOWED_EVENTS = new Set([
  'tengu_api_error',
  'tengu_api_success',
  'tengu_compact_failed',
  'tengu_exit',
  'tengu_init',
  'tengu_oauth_error',
  'tengu_tool_use_error',
  'tengu_uncaught_exception',
  // ... 只有明确列出的事件才会上报
])
```

#### 批量发送
```typescript
const DEFAULT_FLUSH_INTERVAL_MS = 15000  // 每 15 秒批量发送
const MAX_BATCH_SIZE = 100                // 每批最多 100 个事件
const NETWORK_TIMEOUT_MS = 5000           // 网络超时 5 秒
```

### 2.9 实验曝光记录
```typescript
// 记录用户看到了哪个实验的哪个变体
function logExposureForFeature(feature: string): void {
  if (loggedExposures.has(feature)) return  // 每个特性只记录一次

  const expData = experimentDataByFeature.get(feature)
  if (expData) {
    loggedExposures.add(feature)
    logGrowthBookExperimentTo1P({
      experimentId: expData.experimentId,
      variationId: expData.variationId,
      userAttributes: getUserAttributes(),
    })
  }
}
```

### 2.10 认证变更后的刷新
```typescript
export function refreshGrowthBookAfterAuthChange(): void {
  // 必须销毁和重建客户端
  // 因为 apiHostRequestHeaders 创建后不可变
  resetGrowthBook()

  // 通知订阅者值可能已变
  refreshed.emit()

  // 异步重新初始化
  reinitializingPromise = initializeGrowthBook()
    .catch(error => logError(error))
    .finally(() => { reinitializingPromise = null })
}
```

---

## 三、关联文件索引

### 3.1 前置阅读
- [08-context-compression.md](08-context-compression.md) - 上下文压缩

### 3.2 后续课程
- [10-auto-memory-extraction.md](10-auto-memory-extraction.md) - 自动记忆提取

### 3.3 核心源码文件
| 文件路径 | 职责 | 行数 |
|---------|------|------|
| `services/analytics/index.ts` | 事件日志核心 | ~200 行 |
| `services/analytics/datadog.ts` | Datadog 上报 | ~150 行 |
| `services/analytics/growthbook.ts` | GrowthBook 集成 | ~300 行 |

---

## 四、源码对应关系

### 4.1 核心函数
| 函数名 | 位置 | 功能 |
|--------|------|------|
| `logEvent()` | `services/analytics/index.ts` | 同步记录事件 |
| `logEventAsync()` | `services/analytics/index.ts` | 异步记录事件 |
| `stripProtoFields()` | `services/analytics/index.ts` | 隔离 PII 字段 |
| `getFeatureValue_CACHED_MAY_BE_STALE()` | `services/analytics/growthbook.ts` | 非阻塞读取特性值 |
| `setupPeriodicGrowthBookRefresh()` | `services/analytics/growthbook.ts` | 设置周期性刷新 |
| `logExposureForFeature()` | `services/analytics/growthbook.ts` | 记录实验曝光 |
| `refreshGrowthBookAfterAuthChange()` | `services/analytics/growthbook.ts` | 认证变更后刷新 |

### 4.2 核心常量
| 常量名 | 值 | 说明 |
|--------|-----|------|
| `GROWTHBOOK_REFRESH_INTERVAL_MS` | 6h / 20min | 特性标志刷新间隔 |
| `DEFAULT_FLUSH_INTERVAL_MS` | 15000 | Datadog 批量发送间隔 |
| `MAX_BATCH_SIZE` | 100 | 每批最大事件数 |
| `NETWORK_TIMEOUT_MS` | 5000 | 网络超时 |

---

## 五、本课小结

| 概念 | 解释 |
|------|------|
| 零依赖设计 | analytics 模块无依赖，避免循环依赖 |
| 事件队列 | 启动前缓冲，初始化后批量排空 |
| 安全类型约束 | `LogEventMetadata` 禁止直接传入字符串 |
| 三种读取模式 | _CACHED_MAY_BE_STALE / _BLOCKS_ON_INIT / _CACHED_OR_BLOCKING |
| 5 级覆盖优先级 | 环境变量 > 配置 > 内存 > 磁盘 > 默认 |
| Datadog 白名单 | 只有明确列出的事件才会上报 |
| 实验曝光 | 每个特性只记录一次曝光 |
| 认证刷新 | 认证变更后完全重建 GrowthBook 客户端 |

---

*此细纲由 Claude Code 自动生成，用于快速导航和内容概览*
