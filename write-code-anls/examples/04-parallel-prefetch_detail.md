# 第4课：并行预取机制：MDM/Keychain/GrowthBook - 细纲

## 文件信息
- **原文件**: part02-architecture/04-parallel-prefetch.md
- **类型**: 架构全景
- **难度**: ★★★☆☆

---

## 一、为什么需要并行预取

### 1.1 生活类比：做早餐
| 任务 | 耗时 |
|------|------|
| 烧水泡咖啡 | 3分钟 |
| 煎鸡蛋 | 4分钟 |
| 烤面包 | 2分钟 |

- **串行做法**: 3 + 4 + 2 = **9 分钟**
- **并行做法**: max(3, 4, 2) = **4 分钟**

### 1.2 核心思想
能同时做的事情，绝不排队做。

---

## 二、main.tsx 中的并行预取

### 2.1 前21行代码
**文件**: `src/main.tsx`

```typescript
// 这些副作用必须在所有其他 import 之前运行：
// 1. profileCheckpoint 在模块加载前标记时间点
// 2. startMdmRawRead 启动 MDM 子进程（plutil/reg query），
//    让它们和后续 ~135ms 的 import 并行运行
// 3. startKeychainPrefetch 启动 macOS 钥匙串读取——
//    isRemoteManagedSettingsEligible() 否则会通过同步 spawn
//    串行读取两个钥匙串（每次 macOS 启动 ~65ms）
import { profileCheckpoint } from './utils/startupProfiler.js';
profileCheckpoint('main_tsx_entry');

import { startMdmRawRead } from './utils/settings/mdm/rawRead.js';
startMdmRawRead();

import { ensureKeychainPrefetchCompleted, startKeychainPrefetch }
  from './utils/secureStorage/keychainPrefetch.js';
startKeychainPrefetch();
```

### 2.2 启动时间线
```
0ms     模块加载开始 (~135ms)
5ms     MDM 配置读取开始 (~40ms)
10ms    Keychain 读取开始 (~65ms)
15ms    GrowthBook 初始化开始 (~50ms)
135ms   模块加载完成
150ms   CLI 解析
160ms   AppState 创建
180ms   REPL 启动
```

**关键洞察**: MDM 和 Keychain 的读取在 135ms 内完成，用户完全感受不到等待。

---

## 三、三大预取系统详解

### 3.1 系统一：MDM（Mobile Device Management）配置读取

#### 流程
```
startMdmRawRead()
    ↓
什么操作系统？
├── macOS → plutil 读取 plist（子进程）
├── Windows → reg query 读取注册表（子进程）
└── Linux → 跳过（不需要）
    ↓
缓存结果
```

#### 用途
- 读取企业管理策略
- 是否允许使用某些工具
- API 端点配置
- 安全策略设置

#### 为什么要预取
`plutil`（macOS）和 `reg query`（Windows）是外部命令，需要启动子进程，耗时 ~40ms。预取让这个等待"消失"。

### 3.2 系统二：Keychain（钥匙串）预取

#### 流程
```
startKeychainPrefetch()
    ↓
├── OAuth Token 读取 ──┐
└── Legacy API Key 读取 ├─并行执行→ 两个结果都准备好
                        ↓
              后续认证检查直接使用缓存值
```

#### 效果对比
| 方式 | 耗时 |
|------|------|
| 不预取（串行） | 35ms + 30ms = 65ms |
| 预取（并行） | 0ms（已在后台完成） |

**类比**: 提前把钥匙从口袋里拿出来——到了家门口不用再翻口袋。

### 3.3 系统三：GrowthBook 特性标志

#### 系统架构
```
GrowthBook 服务
    ↓
获取特性标志
    ↓
├── tengu_auto_compact（自动压缩）
├── tengu_streaming_tool（流式工具执行）
├── tengu_fast_mode（快速模式）
└── tengu_ccr_bridge（远程桥接）
    ↓
运行时 feature gate（控制功能开关）
```

#### 用途
- 灰度发布新功能
- 针对不同用户群开放不同特性
- 远程控制功能开关

#### 代码示例
```typescript
import { getFeatureValue_CACHED_MAY_BE_STALE }
  from './services/analytics/growthbook.js'

const capEnabled = getFeatureValue_CACHED_MAY_BE_STALE(
  'tengu_otk_slot_v1',
  false,  // 默认值
)
```

---

## 四、并行预取的设计模式

### 4.1 模式一：Import 间隙预取
```typescript
// 利用 import 语句之间的时间执行预取
import { startMdmRawRead } from './mdm.js';
startMdmRawRead();  // 立即启动，不等结果

// 继续加载其他模块（~135ms）
import { React } from 'react';
import { Commander } from 'commander';

// 等到真正需要时，结果已经准备好了
const mdmConfig = await getMdmResult();  // 瞬间返回
```

### 4.2 模式二：Promise.all 并行
**文件**: `src/commands.ts`

```typescript
const [skills, { enabled: enabledPlugins }] = await Promise.all([
  getSlashCommandToolSkills(getCwd()),
  loadAllPluginsCacheOnly(),
])
```

```
开始
├── 任务A: 加载技能 (50ms)
└── 任务B: 加载插件 (80ms)
    ↓
全部完成（耗时 80ms，而非 130ms）
```

### 4.3 模式三：预取 + 消费分离
**文件**: `src/query.ts`

```typescript
// 在查询循环中提前启动预取
using pendingMemoryPrefetch = startRelevantMemoryPrefetch(
  state.messages,
  state.toolUseContext,
)

// ... 模型流式输出和工具执行（5-30秒）...

// 消费预取结果（如果已经完成）
if (
  pendingMemoryPrefetch &&
  pendingMemoryPrefetch.settledAt !== null &&
  pendingMemoryPrefetch.consumedOnIteration === -1
) {
  const memoryAttachments = filterDuplicateMemoryAttachments(
    await pendingMemoryPrefetch.promise,
    toolUseContext.readFileState,
  )
}
```

**类比**: 等电梯的时候掏出钥匙——到了家门口直接开门。

---

## 五、性能测量：profileCheckpoint

### 5.1 检查点代码
**文件**: `src/QueryEngine.ts`

```typescript
headlessProfilerCheckpoint('before_getSystemPrompt')
const { defaultSystemPrompt, userContext, systemContext } =
  await fetchSystemPromptParts({ /* ... */ })
headlessProfilerCheckpoint('after_getSystemPrompt')

headlessProfilerCheckpoint('before_skills_plugins')
const [skills, { enabled: enabledPlugins }] = await Promise.all([
  getSlashCommandToolSkills(getCwd()),
  loadAllPluginsCacheOnly(),
])
headlessProfilerCheckpoint('after_skills_plugins')
```

### 5.2 性能检查点序列
```
main_tsx_entry
    ↓
before_getSystemPrompt
    ↓
after_getSystemPrompt
    ↓
before_skills_plugins
    ↓
after_skills_plugins
    ↓
system_message_yielded
    ↓
query_started
```

---

## 六、query.ts 中的查询级预取

### 6.1 技能发现预取
**文件**: `src/query.ts`

```typescript
// 技能发现预取——每次迭代启动
const pendingSkillPrefetch = skillPrefetch?.startSkillDiscoveryPrefetch(
  null,
  messages,
  toolUseContext,
)

// ... 模型调用 + 工具执行 ...

// 消费技能发现结果
if (skillPrefetch && pendingSkillPrefetch) {
  const skillAttachments =
    await skillPrefetch.collectSkillDiscoveryPrefetch(pendingSkillPrefetch)
  for (const att of skillAttachments) {
    const msg = createAttachmentMessage(att)
    yield msg
  }
}
```

---

## 七、并行预取的挑战与注意事项

### 7.1 优缺点
| ✅ 优点 | ⚠️ 挑战 |
|---------|---------|
| 减少总等待时间 | 依赖顺序要正确 |
| 提升用户体验 | 错误处理更复杂 |
| 充分利用 I/O 等待 | 调试难度增加 |
| | 资源竞争风险 |

### 7.2 Claude Code 的解决方案
- **依赖管理**: 确保预取在需要结果之前完成
- **优雅降级**: 预取失败时回退到同步方式
- **结果缓存**: 预取结果缓存起来，避免重复执行

---

## 八、动手练习

### 练习1：测量并行加速
写一个简单的 Bun 脚本，对比串行和并行执行：
```typescript
const taskA = () => new Promise(r => setTimeout(r, 100))
const taskB = () => new Promise(r => setTimeout(r, 200))
const taskC = () => new Promise(r => setTimeout(r, 150))

// 串行执行
console.time('serial')
await taskA(); await taskB(); await taskC();
console.timeEnd('serial')  // ~450ms

// 并行执行
console.time('parallel')
await Promise.all([taskA(), taskB(), taskC()])
console.timeEnd('parallel')  // ~200ms
```

### 练习2：追踪预取链
在 `main.tsx` 中找到所有的 "prefetch" 或 "preload" 调用：
- [ ] 每个预取操作预取什么数据？
- [ ] 预取结果在哪里被消费？
- [ ] 如果预取失败，会怎么处理？

### 思考题
1. 为什么预取操作放在 `import` 语句之间，而不是所有 `import` 完成之后？
2. `Promise.all` 中如果有一个 Promise 失败了，会怎样？Claude Code 如何处理？
3. 预取操作会不会造成资源浪费（比如预取了但没用上）？

---

## 九、小结

| 概念 | 说明 | 节省时间 |
|------|------|---------|
| Import 间隙预取 | 在模块加载的 135ms 内并行执行 I/O | ~65ms |
| MDM 预取 | 提前读取企业管理配置 | ~40ms |
| Keychain 预取 | 并行读取 OAuth + API Key | ~65ms |
| GrowthBook 预取 | 提前加载特性标志 | ~50ms |
| Promise.all | 并行执行多个异步操作 | 50%+ |
| 查询级预取 | 在模型推理期间预取附件 | 隐藏延迟 |

### 核心原则
> **预取的黄金法则**: 如果一个操作不依赖前一个操作的结果，就让它们并行执行。

---

## 十、关联文件

### 10.1 上一章
- [03-startup-process.md](03-startup-process.md) - 启动流程详解

### 10.2 下一章
- [05-tool-system-architecture.md](05-tool-system-architecture.md) - 工具系统架构

---

*此细纲由 Claude Code 自动生成*
