# 第10课：综合实战 —— 性能优化检查清单 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第10课：综合实战 —— 性能优化检查清单

### 1.2 二级标题
- 学习目标
- 生活类比：装修一栋房子
- 检查清单一：启动优化
- 检查清单二：运行时代码加载
- 检查清单三：上下文与内存管理
- 检查清单四：API 调用优化
- 检查清单五：前端渲染优化
- 检查清单六：流式处理与并发
- 综合案例分析：一次完整的用户交互
- 优化优先级决策树
- 动手练习
- 全课程总结
- 课后阅读推荐

### 1.3 三级标题
- 第一优先级：关键路径加速
- Claude Code 的启动优化实例
- 第二优先级：按需加载
- 实战案例：commands.ts 的分层加载
- 第三优先级：控制资源增长
- 三级压缩体系
- 第四优先级：降低成本与延迟
- 缓存一致性检查
- 第五优先级：流畅的用户体验
- 第六优先级：高效的数据处理管道
- 各阶段的优化贡献
- 核心原则回顾
- 10 节课的知识地图

---

## 2. 关键知识点

### 2.1 六大检查清单

#### 检查清单一：启动优化
| # | 检查项 | 来源课程 | 相关源码 |
|---|--------|----------|----------|
| 1.1 | 是否有可以**并行执行**的启动任务？ | 第2课 | `Promise.all([getSkills(), getPluginCommands()])` |
| 1.2 | 启动时是否加载了**暂时不需要**的模块？ | 第3课 | `await import('./commands/insights.js')` |
| 1.3 | 是否有**编译时可消除**的死代码？ | 第4课 | `feature('PROACTIVE') ? require(...) : null` |
| 1.4 | 是否在入口点尽早启动了**异步预取**？ | 第2课 | `startKeychainPrefetch()` 在 import 之前 |
| 1.5 | 是否设置了**性能检查点**来追踪启动耗时？ | 第1课 | `profileCheckpoint('main_tsx_entry')` |

#### 检查清单二：运行时代码加载
| # | 检查项 | 来源课程 |
|---|--------|----------|
| 2.1 | 是否有**只在特定条件**下才用到的模块？ | 第5课 |
| 2.2 | 是否有**只在特定功能**被触发时才需要的重量级模块？ | 第3课 |
| 2.3 | 是否利用了 **feature flag** 在编译时消除不需要的代码？ | 第4课 |
| 2.4 | 条件加载时是否保留了**类型安全**？ | 第5课 |

#### 检查清单三：上下文与内存管理
| # | 检查项 | 来源课程 |
|---|--------|----------|
| 3.1 | 是否有**自动压缩**机制防止上下文无限增长？ | 第6课 |
| 3.2 | 是否有**增量压缩**减少不必要的全量操作？ | 第6课 |
| 3.3 | 是否有**熔断器**防止失败操作反复重试？ | 第6课 |
| 3.4 | 是否使用 **WeakMap** 避免对象缓存导致内存泄漏？ | 第8课 |
| 3.5 | 是否在压缩后**只恢复必要的文件**而非全部？ | 第6课 |
| 3.6 | 恢复是否有 **token 预算**约束？ | 第6课 |

#### 检查清单四：API 调用优化
| # | 检查项 | 来源课程 |
|---|--------|----------|
| 4.1 | 是否**保持 prompt 前缀稳定**以利用缓存？ | 第7课 |
| 4.2 | 是否有**缓存中断检测**机制？ | 第7课 |
| 4.3 | 压缩 fork 是否**复用主线程缓存**？ | 第7课 |
| 4.4 | 是否在修改 prompt 前缀时**通知缓存系统**？ | 第7课 |
| 4.5 | 是否使用**流式 API**而非批量等待？ | 第9课 |

#### 检查清单五：前端渲染优化
| # | 检查项 | 来源课程 |
|---|--------|----------|
| 5.1 | 长列表是否使用了**虚拟滚动**？ | 第8课 |
| 5.2 | 不可见内容是否**冻结更新**？ | 第8课 |
| 5.3 | 组件 props 是否避免了**不必要的引用变化**？ | 第8课 |
| 5.4 | 搜索是否做了**预热缓存**？ | 第8课 |
| 5.5 | 是否正确使用了 `React.memo` / `useMemo`？ | 第8课 |
| 5.6 | 是否使用了**流式渲染**而非等待完整数据？ | 第9课 |

#### 检查清单六：流式处理与并发
| # | 检查项 | 来源课程 |
|---|--------|----------|
| 6.1 | 是否使用**异步生成器**构建流式管道？ | 第9课 |
| 6.2 | 是否利用 **yield*** 组合子管道？ | 第9课 |
| 6.3 | 是否在**等待期间并行**执行其他工作？ | 第9课 |
| 6.4 | 并发是否有**安全控制**？ | 第9课 |
| 6.5 | 是否有**自然的背压**机制？ | 第9课 |
| 6.6 | 并行预取是否在**不阻塞主流程**的情况下运行？ | 第2课 |

### 2.2 三级压缩体系
1. **Microcompact**：轻量级，清理旧工具结果
2. **AutoCompact**：中量级，API 调用生成总结
3. **ReactiveCompact**：重量级，应急响应 prompt-too-long 错误

### 2.3 核心原则回顾
| 原则 | 解释 | 课程 |
|------|------|------|
| **不做无用功** | 死代码消除、条件加载 | 第3、4、5课 |
| **并行而非串行** | Promise.all、并行预取 | 第2课 |
| **渐进式处理** | 流式、增量压缩 | 第6、9课 |
| **空间换时间** | 缓存、预计算 | 第7、8课 |
| **按需而非预备** | 懒加载、虚拟滚动 | 第3、8课 |
| **设定预算** | token 预算、文件数量限制 | 第6课 |
| **有兜底方案** | 熔断器、多级降级 | 第6、7课 |

---

## 3. 涉及的源码文件路径

### 3.1 核心源码文件
- `main.tsx` - 启动优化、并行预取、feature flag
- `query.ts` - 流式处理、异步生成器、query 循环
- `commands.ts` - 条件 require、懒加载、命令系统
- `services/compact/compact.ts` - 全量压缩算法
- `services/compact/autoCompact.ts` - 自动压缩触发逻辑
- `services/compact/microCompact.ts` - 增量微压缩
- `services/api/promptCacheBreakDetection.ts` - Prompt 缓存中断检测
- `components/VirtualMessageList.tsx` - 虚拟滚动、搜索优化
- `components/OffscreenFreeze.tsx` - 不可见内容冻结
- `services/tools/StreamingToolExecutor.ts` - 流式工具执行
- `utils/generators.ts` - 并发生成器执行器

---

## 4. 类名、函数名、接口名

### 4.1 启动优化相关
- `profileCheckpoint(name: string)` - 性能检查点
- `startMdmRawRead()` - 启动 MDM 读取
- `startKeychainPrefetch()` - 启动钥匙串预取
- `startDeferredPrefetches()` - 延迟预取
- `logStartupTelemetry()` - 启动遥测日志
- `Promise.all()` - 并行执行

### 4.2 懒加载相关
- `import()` - 动态导入
- `require()` - 条件 require
- `feature(flag: string)` - Bun 特性标志
- `lazySchema(factory)` - 延迟 Schema 创建
- `memoize(fn)` - 函数结果缓存

### 4.3 压缩相关
- `autoCompactIfNeeded()` - 自动压缩
- `microcompactMessages()` - 微压缩
- `getAutoCompactThreshold(model: string)` - 获取自动压缩阈值
- `createPostCompactFileAttachments()` - 创建压缩后文件附件
- `stripImagesFromMessages()` - 剥离图片
- `MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES` - 最大连续自动压缩失败次数

### 4.4 缓存相关
- `notifyCompaction()` - 通知压缩
- `promptCacheSharingEnabled` - 缓存共享启用标志
- `runForkedAgent()` - 运行 fork 代理
- `generateTempFilePath()` - 生成临时文件路径

### 4.5 渲染优化相关
- `VirtualMessageList` - 虚拟消息列表组件
- `OffscreenFreeze` - 不可见内容冻结组件
- `useVirtualScroll()` - 虚拟滚动 Hook
- `WeakMap` - 弱引用缓存
- `fallbackLowerCache` - 搜索文本缓存
- `promptTextCache` - 提示文本缓存

### 4.6 流式处理相关
- `query(params: QueryParams)` - Query 主函数
- `queryLoop()` - Query 循环
- `StreamingToolExecutor` - 流式工具执行器
- `all(generators, concurrencyCap)` - 并发生成器执行器
- `yield` / `yield*` - 生成器产出
- `Promise.race()` - 竞速 Promise

---

## 5. 代码片段重点

### 5.1 启动优化实例（main.tsx）
```typescript
import { profileCheckpoint } from './utils/startupProfiler.js';
profileCheckpoint('main_tsx_entry');

import { startMdmRawRead } from './utils/settings/mdm/rawRead.js';
startMdmRawRead();

import { startKeychainPrefetch } from './utils/secureStorage/keychainPrefetch.js';
startKeychainPrefetch();
```

### 5.2 分层加载（commands.ts）
```typescript
// 第一层：始终需要的核心命令
import clear from './commands/clear/index.js';
import help from './commands/help/index.js';

// 第二层：条件存在的功能
const voiceCommand = feature('VOICE_MODE')
  ? require('./commands/voice/index.js').default
  : null;

// 第三层：很少使用的重量级功能
const usageReport: Command = {
  name: 'insights',
  async getPromptForCommand(args, context) {
    const real = (await import('./commands/insights.js')).default;
    return real.getPromptForCommand(args, context);
  },
};
```

### 5.3 三级压缩体系
```typescript
// 1. Microcompact
const COMPACTABLE_TOOLS = new Set([
  FILE_READ_TOOL_NAME,
  ...SHELL_TOOL_NAMES,
  GREP_TOOL_NAME,
  GLOB_TOOL_NAME,
]);

// 2. AutoCompact
export function getAutoCompactThreshold(model: string): number {
  return getEffectiveContextWindowSize(model) - AUTOCOMPACT_BUFFER_TOKENS;
}

// 3. ReactiveCompact - 当 API 返回 413 时触发
```

### 5.4 缓存共享（compact.ts）
```typescript
if (promptCacheSharingEnabled) {
  const result = await runForkedAgent({
    promptMessages: [summaryRequest],
    cacheSafeParams,
    canUseTool: createCompactCanUseTool(),
    querySource: 'compact',
    forkLabel: 'compact',
    maxTurns: 1,
    skipCacheWrite: true,
  });
}
```

### 5.5 虚拟滚动（VirtualMessageList.tsx）
```typescript
type Props = {
  messages: RenderableMessage[];
  scrollRef: RefObject<ScrollBoxHandle | null>;
  columns: number;
  itemKey: (msg: RenderableMessage) => string;
  renderItem: (msg: RenderableMessage, index: number) => React.ReactNode;
};
```

### 5.6 并发生成器执行器（utils/generators.ts）
```typescript
export async function* all<A>(
  generators: AsyncGenerator<A, void>[],
  concurrencyCap = Infinity,
): AsyncGenerator<A, void> {
  const waiting = [...generators];
  const promises = new Set<Promise<QueuedGenerator<A>>>();

  while (promises.size < concurrencyCap && waiting.length > 0) {
    promises.add(next(waiting.shift()!));
  }

  while (promises.size > 0) {
    const { done, value, generator, promise } = await Promise.race(promises);
    promises.delete(promise);

    if (!done) {
      promises.add(next(generator));
      if (value !== undefined) yield value;
    } else if (waiting.length > 0) {
      promises.add(next(waiting.shift()!));
    }
  }
}
```
