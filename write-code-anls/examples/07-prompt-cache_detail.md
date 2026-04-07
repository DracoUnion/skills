# 第7课：Prompt 缓存优化 —— 减少 API 调用成本 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第7课：Prompt 缓存优化 —— 减少 API 调用成本

### 1.2 二级标题
- 学习目标
- 生活类比：续讲故事
- 真实源码解析
- 缓存的成本影响
- 缓存友好的设计原则
- Token 估算
- 动手练习
- 本课小结
- 下节预告

### 1.3 三级标题
- 1. 缓存中断检测系统
- 2. 缓存感知的设计决策
- 3. 压缩后的缓存保护
- 4. 压缩时的缓存前缀共享
- 5. 缓存共享成功率追踪
- 原则1：保持前缀稳定
- 原则2：避免不必要的变更
- 原则3：预期内的中断要通知
- 原则4：不要为了缓存牺牲正确性

---

## 2. 关键知识点

### 2.1 Prompt Cache 基本原理
- API 服务器缓存已处理的 prompt 前缀
- 缓存命中时处理成本降至 1/10
- 前缀变化导致缓存失效

### 2.2 缓存中断检测字段
| 字段 | 说明 |
|------|------|
| `systemHash` | 系统 prompt 的 hash |
| `toolsHash` | 工具 schema 的 hash |
| `cacheControlHash` | 缓存控制参数的 hash |
| `toolNames` | 工具名称列表 |
| `perToolHashes` | 每个工具的 schema hash |
| `model` | 模型名称 |
| `fastMode` | 快速模式 |
| `globalCacheStrategy` | 全局缓存策略 |
| `betas` | beta 头列表 |
| `effortValue` | 努力值 |

### 2.3 缓存友好的设计原则
1. **保持前缀稳定** - 系统 prompt 和工具定义不变
2. **避免不必要的变更** - 使用内容 hash 而非随机 UUID
3. **预期内的中断要通知** - `notifyCompaction()`
4. **不要为了缓存牺牲正确性** - beta 头、effort 值等必须改变缓存键

### 2.4 缓存共享策略
- 压缩 fork 复用主线程的 prompt 缓存
- 需要发送相同的缓存键参数（system、tools、model、messages 前缀、thinking 配置）
- 设置 `skipCacheWrite: true`

### 2.5 缓存命中率计算
```
cacheHitRate = cache_read_input_tokens / 
  (cache_read_input_tokens + cache_creation_input_tokens + input_tokens)
```

---

## 3. 涉及的源码文件路径

### 3.1 核心源码文件
- `services/api/promptCacheBreakDetection.ts` - 缓存中断检测
- `services/compact/compact.ts` - 压缩时的缓存共享
- `main.tsx` - 内容 hash 生成临时文件路径
- `utils/tokens.js` - token 估算

---

## 4. 类名、函数名、接口名

### 4.1 类型/接口
- `PreviousState` - 缓存中断检测的前一状态
- `PendingChanges` - 待处理的缓存变化

### 4.2 函数
- `notifyCompaction()` - 通知压缩（重置缓存读取基线）
- `runForkedAgent()` - 运行 fork 代理
- `generateTempFilePath(prefix: string, ext: string, options: { contentHash: string })` - 生成临时文件路径
- `roughTokenCountEstimation(text: string)` - 粗略 token 估算
- `logEvent(event: string, data: object)` - 事件日志

### 4.3 常量
- `TOKEN_COUNT_THINKING_BUDGET = 1024` - token 计数思考预算
- `TOKEN_COUNT_MAX_TOKENS = 2048` - token 计数最大 token

---

## 5. 代码片段重点

### 5.1 缓存中断检测系统（promptCacheBreakDetection.ts）
```typescript
type PreviousState = {
  systemHash: number;
  toolsHash: number;
  cacheControlHash: number;
  toolNames: string[];
  perToolHashes: Record<string, number>;
  systemCharCount: number;
  model: string;
  fastMode: boolean;
  globalCacheStrategy: string;
  betas: string[];
  effortValue: string;
  extraBodyHash: number;
  callCount: number;
  prevCacheReadTokens: number | null;
  cacheDeletionsPending: boolean;
};

type PendingChanges = {
  systemPromptChanged: boolean;
  toolSchemasChanged: boolean;
  modelChanged: boolean;
  fastModeChanged: boolean;
  cacheControlChanged: boolean;
  globalCacheStrategyChanged: boolean;
  betasChanged: boolean;
  addedToolCount: number;
  removedToolCount: number;
  changedToolSchemas: string[];
};
```

### 5.2 缓存感知的设计决策（main.tsx 第446-457行）
```typescript
// 使用基于内容 hash 的路径，而非随机 UUID
// 设置路径出现在 Bash 工具的沙盒拒绝列表中，属于发送给 API 的
// 工具描述的一部分。每个子进程使用随机 UUID 会改变工具描述，
// 导致缓存前缀失效，造成 12 倍的输入 token 成本惩罚。
// 内容 hash 确保相同设置在不同进程间产生相同路径。
settingsPath = generateTempFilePath('claude-settings', '.json', {
  contentHash: trimmedSettings
});
```

### 5.3 压缩后的缓存保护（compact.ts 第698-703行）
```typescript
// 重置缓存读取基线，使压缩后的缓存下降不被标记为中断
if (feature('PROMPT_CACHE_BREAK_DETECTION')) {
  notifyCompaction(
    context.options.querySource ?? 'compact',
    context.agentId,
  );
}
```

### 5.4 压缩时的缓存前缀共享（compact.ts 第1178-1199行）
```typescript
if (promptCacheSharingEnabled) {
  try {
    // 不要在这里设置 maxOutputTokens。fork 借用主线程的
    // prompt 缓存，需要发送相同的缓存键参数（system、tools、
    // model、messages 前缀、thinking 配置）。设置 maxOutputTokens
    // 会修改 thinking 配置，造成缓存键不匹配而失效。
    const result = await runForkedAgent({
      promptMessages: [summaryRequest],
      cacheSafeParams,
      canUseTool: createCompactCanUseTool(),
      querySource: 'compact',
      forkLabel: 'compact',
      maxTurns: 1,
      skipCacheWrite: true,
    });
    // ...
  }
}
```

### 5.5 缓存共享成功率追踪（compact.ts）
```typescript
logEvent('tengu_compact_cache_sharing_success', {
  preCompactTokenCount,
  outputTokens: result.totalUsage.output_tokens,
  cacheReadInputTokens: result.totalUsage.cache_read_input_tokens,
  cacheCreationInputTokens: result.totalUsage.cache_creation_input_tokens,
  cacheHitRate:
    result.totalUsage.cache_read_input_tokens > 0
      ? result.totalUsage.cache_read_input_tokens /
        (result.totalUsage.cache_read_input_tokens +
         result.totalUsage.cache_creation_input_tokens +
         result.totalUsage.input_tokens)
      : 0,
});
```

### 5.6 Token 估算（services/tokenEstimation.ts）
```typescript
const TOKEN_COUNT_THINKING_BUDGET = 1024;
const TOKEN_COUNT_MAX_TOKENS = 2048;

function roughTokenCountEstimation(text: string): number {
  return Math.ceil(text.length / 4);
}
```
