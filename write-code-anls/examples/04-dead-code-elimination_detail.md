# 第4课：死代码消除 —— Bun feature() 编译时优化 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第4课：死代码消除 —— Bun feature() 编译时优化

### 1.2 二级标题
- 学习目标
- 生活类比：精装房 vs 毛坯房
- 真实源码解析
- 编译时消除 vs 运行时判断
- Claude Code 的 Feature Flag 架构
- 与传统环境变量判断的混合使用
- 死代码消除的三个层次
- 动手练习
- 本课小结
- 下节预告

### 1.3 三级标题
- Bun 的 `feature()` 函数
- 案例一：PROACTIVE 功能的条件编译
- 案例二：大量 feature flag 守护的命令
- 案例三：query.ts 中的编译时优化
- 案例四：compact.ts 中的条件逻辑
- Feature Flag 的命名规范

---

## 2. 关键知识点

### 2.1 Bun feature() 函数
- `import { feature } from 'bun:bundle'`
- 编译时求值（不是运行时！）
- 返回 `true` 或 `false`
- 打包器看到 `false` 分支后直接删除整个分支代码

### 2.2 编译时消除 vs 运行时判断
| 特性 | 编译时消除 (`feature()`) | 运行时判断 (`process.env`) |
|------|------------------------|--------------------------|
| 代码在产物中 | 不存在 | 存在 |
| 依赖的模块 | 不被打包 | 仍被打包 |
| 包体积影响 | 减小 | 不变 |
| 灵活性 | 编译时固定 | 运行时可变 |
| 性能开销 | 零 | 极小（一次判断） |

### 2.3 Feature Flag 命名规范
| Feature Flag | 功能描述 |
|-------------|---------|
| `PROACTIVE` | 主动式建议功能 |
| `KAIROS` | 助手模式 |
| `VOICE_MODE` | 语音模式 |
| `BRIDGE_MODE` | 桥接远程模式 |
| `HISTORY_SNIP` | 历史裁剪 |
| `REACTIVE_COMPACT` | 响应式压缩 |
| `CACHED_MICROCOMPACT` | 缓存微压缩 |
| `EXPERIMENTAL_SKILL_SEARCH` | 实验性技能搜索 |
| `TOKEN_BUDGET` | Token 预算控制 |

### 2.4 死代码消除的三个层次
1. **层次1：Tree Shaking** - 打包器自动移除未引用的导出
2. **层次2：Feature Flag DCE** - 编译时条件消除整块代码
3. **层次3：构建级排除** - 不同构建配置产出不同包

---

## 3. 涉及的源码文件路径

### 3.1 核心源码文件
- `commands.ts` - feature flag 守护的命令加载
- `query.ts` - 响应式压缩、上下文折叠条件编译
- `services/compact/compact.ts` - PROMPT_CACHE_BREAK_DETECTION、KAIROS 条件逻辑
- `main.tsx` - 环境变量条件加载

---

## 4. 类名、函数名、接口名

### 4.1 函数
- `feature(flag: string): boolean` - Bun 特性标志函数
- `require(path: string)` - 条件 require

### 4.2 常量
- `proactive` - PROACTIVE/KAIROS 功能命令
- `briefCommand` - KAIROS_BRIEF 功能命令
- `assistantCommand` - KAIROS 助手命令
- `bridge` - BRIDGE_MODE 桥接命令
- `voiceCommand` - VOICE_MODE 语音命令
- `forceSnip` - HISTORY_SNIP 历史裁剪命令
- `workflowsCmd` - WORKFLOW_SCRIPTS 工作流命令
- `webCmd` - CCR_REMOTE_SETUP 远程设置命令
- `reactiveCompact` - REACTIVE_COMPACT 响应式压缩模块
- `contextCollapse` - CONTEXT_COLLAPSE 上下文折叠模块
- `agentsPlatform` - 内部用户代理平台

---

## 5. 代码片段重点

### 5.1 feature() 导入
```typescript
import { feature } from 'bun:bundle';
```

### 5.2 PROACTIVE 功能条件编译（commands.ts 第62-65行）
```typescript
const proactive =
  feature('PROACTIVE') || feature('KAIROS')
    ? require('./commands/proactive.js').default
    : null;
```

### 5.3 大量 feature flag 守护的命令（commands.ts 第62-122行）
```typescript
const proactive = feature('PROACTIVE') || feature('KAIROS')
  ? require('./commands/proactive.js').default : null;

const briefCommand = feature('KAIROS') || feature('KAIROS_BRIEF')
  ? require('./commands/brief.js').default : null;

const assistantCommand = feature('KAIROS')
  ? require('./commands/assistant/index.js').default : null;

const bridge = feature('BRIDGE_MODE')
  ? require('./commands/bridge/index.js').default : null;

const voiceCommand = feature('VOICE_MODE')
  ? require('./commands/voice/index.js').default : null;

const forceSnip = feature('HISTORY_SNIP')
  ? require('./commands/force-snip.js').default : null;

const workflowsCmd = feature('WORKFLOW_SCRIPTS')
  ? (require('./commands/workflows/index.js')).default : null;

const webCmd = feature('CCR_REMOTE_SETUP')
  ? (require('./commands/remote-setup/index.js')).default : null;
```

### 5.4 query.ts 中的编译时优化（query.ts 第15-21行）
```typescript
const reactiveCompact = feature('REACTIVE_COMPACT')
  ? (require('./services/compact/reactiveCompact.js'))
  : null;

const contextCollapse = feature('CONTEXT_COLLAPSE')
  ? (require('./services/contextCollapse/index.js'))
  : null;
```

### 5.5 query.ts 中的条件逻辑（query.ts 第401-410行）
```typescript
if (feature('HISTORY_SNIP')) {
  queryCheckpoint('query_snip_start');
  const snipResult = snipModule!.snipCompactIfNeeded(messagesForQuery);
  messagesForQuery = snipResult.messages;
  snipTokensFreed = snipResult.tokensFreed;
  if (snipResult.boundaryMessage) {
    yield snipResult.boundaryMessage;
  }
  queryCheckpoint('query_snip_end');
}
```

### 5.6 compact.ts 中的条件逻辑（compact.ts 第698行）
```typescript
if (feature('PROMPT_CACHE_BREAK_DETECTION')) {
  notifyCompaction(
    context.options.querySource ?? 'compact',
    context.agentId,
  );
}
```

### 5.7 环境变量条件加载（main.tsx 第48-52行）
```typescript
const agentsPlatform =
  process.env.USER_TYPE === 'ant'
    ? require('./commands/agents-platform/index.js').default
    : null;
```

### 5.8 命令列表展开（commands.ts）
```typescript
const COMMANDS = memoize((): Command[] => [
  addDir,
  advisor,
  ...(proactive ? [proactive] : []),
  ...(briefCommand ? [briefCommand] : []),
  ...(bridge ? [bridge] : []),
]);
```
