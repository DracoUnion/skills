# 第5课：条件 Require —— 运行时按需加载 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第5课：条件 Require —— 运行时按需加载

### 1.2 二级标题
- 学习目标
- 生活类比：按需购买 vs 囤货
- 真实源码解析
- 三种加载方式全面对比
- 为什么 Claude Code 更偏爱 require() 而非 import()？
- TypeScript 中安全使用条件 require 的模式
- 常见陷阱
- 动手练习
- 本课小结
- 下节预告

### 1.3 三级标题
- 模式一：feature() + require() 组合拳
- 模式二：环境变量 + require()
- 模式三：延迟函数包装
- 模式四：编译时守护的运行时模块
- 模式五：条件 require 在 compact prompt 中
- 类型标注技巧
- ESLint 配合
- 陷阱1：在循环中 require
- 陷阱2：忘记 null 检查
- 陷阱3：混淆编译时和运行时

---

## 2. 关键知识点

### 2.1 三种加载方式对比
| 特性 | 静态 import | 动态 import() | 条件 require |
|------|------------|--------------|-------------|
| 语法 | `import X from 'x'` | `await import('x')` | `require('x')` |
| 执行时机 | 模块初始化时 | 调用时（异步） | 调用时（同步） |
| 是否阻塞 | 是 | 否（返回 Promise） | 是（同步执行） |
| Tree-shaking | 支持 | 不支持 | 不支持 |
| 与 feature() 配合 | 不支持 | 支持 | 支持 |
| 类型安全 | 自动 | 需手动标注 | 需 `as typeof import()` |
| 循环依赖 | 可能出问题 | 可以解决 | 可以解决 |

### 2.2 选择加载方式决策树
- 是否需要编译时消除？
  - 是 → 是否需要异步加载？
    - 是 → `feature() + import()`
    - 否 → `feature() + require()`（Claude Code 最常用）
  - 否 → 是否需要按需加载？
    - 是 → 动态 `import()`
    - 否 → 静态 `import`

### 2.3 require() 的优势
1. **同步执行** - 立即可用，无需 await
2. **模块顶层可用** - 变量在模块加载时就有值
3. **配合 feature() 编译时消除** - 外部版本中整个三元表达式被替换为 null

### 2.4 双重守护模式
- `feature('X') && module` - 编译时+运行时双保险
- 既有编译时 feature 检查，又有运行时 null 检查

### 2.5 ESLint 标注规范
```typescript
/* eslint-disable @typescript-eslint/no-require-imports */
const mod = feature('X') ? require('./x.js') : null;
/* eslint-enable @typescript-eslint/no-require-imports */
```

---

## 3. 涉及的源码文件路径

### 3.1 核心源码文件
- `commands.ts` - feature flag + 条件 require 组合
- `query.ts` - 双重守护模式
- `services/compact/prompt.ts` - compact prompt 中的条件 require
- `main.tsx` - 延迟函数包装

---

## 4. 类名、函数名、接口名

### 4.1 函数
- `feature(flag: string): boolean` - Bun 特性标志函数
- `require(path: string)` - Node.js 同步加载
- `getTeammateUtils()` - 延迟加载 teammate 工具
- `getTeammatePromptAddendum()` - 延迟加载 teammate 提示附录
- `getTeammateModeSnapshot()` - 延迟加载 teammate 模式快照
- `applyCollapsesIfNeeded()` - 应用上下文折叠
- `COMMANDS()` - 获取命令列表

### 4.2 常量/变量
- `proactive` - PROACTIVE 功能模块
- `briefCommand` - KAIROS_BRIEF 功能模块
- `assistantCommand` - KAIROS 助手模块
- `bridge` - BRIDGE_MODE 桥接模块
- `voiceCommand` - VOICE_MODE 语音模块
- `agentsPlatform` - 代理平台模块
- `reactiveCompact` - 响应式压缩模块
- `contextCollapse` - 上下文折叠模块
- `proactiveModule` - proactive 模块引用
- `snipModule` - snip 压缩模块

---

## 5. 代码片段重点

### 5.1 feature() + require() 组合拳（commands.ts 第62-122行）
```typescript
/* eslint-disable @typescript-eslint/no-require-imports */
const proactive =
  feature('PROACTIVE') || feature('KAIROS')
    ? require('./commands/proactive.js').default
    : null;

const briefCommand =
  feature('KAIROS') || feature('KAIROS_BRIEF')
    ? require('./commands/brief.js').default
    : null;

const assistantCommand = feature('KAIROS')
  ? require('./commands/assistant/index.js').default
  : null;

const bridge = feature('BRIDGE_MODE')
  ? require('./commands/bridge/index.js').default
  : null;
/* eslint-enable @typescript-eslint/no-require-imports */
```

### 5.2 环境变量 + require()（commands.ts 第48-52行）
```typescript
/* eslint-disable @typescript-eslint/no-require-imports */
const agentsPlatform =
  process.env.USER_TYPE === 'ant'
    ? require('./commands/agents-platform/index.js').default
    : null;
/* eslint-enable @typescript-eslint/no-require-imports */
```

### 5.3 延迟函数包装（main.tsx 第69-73行）
```typescript
const getTeammateUtils = () =>
  require('./utils/teammate.js') as typeof import('./utils/teammate.js');
const getTeammatePromptAddendum = () =>
  require('./utils/swarm/teammatePromptAddendum.js')
    as typeof import('./utils/swarm/teammatePromptAddendum.js');
const getTeammateModeSnapshot = () =>
  require('./utils/swarm/backends/teammateModeSnapshot.js')
    as typeof import('./utils/swarm/backends/teammateModeSnapshot.js');
```

### 5.4 双重守护模式（query.ts 第14-21行、第440-447行）
```typescript
// 定义
const reactiveCompact = feature('REACTIVE_COMPACT')
  ? (require('./services/compact/reactiveCompact.js')
     as typeof import('./services/compact/reactiveCompact.js'))
  : null;

const contextCollapse = feature('CONTEXT_COLLAPSE')
  ? (require('./services/contextCollapse/index.js')
     as typeof import('./services/contextCollapse/index.js'))
  : null;

// 使用
if (feature('CONTEXT_COLLAPSE') && contextCollapse) {
  const collapseResult = await contextCollapse.applyCollapsesIfNeeded(
    messagesForQuery,
    toolUseContext,
    querySource,
  );
  messagesForQuery = collapseResult.messages;
}
```

### 5.5 compact prompt 中的条件 require（services/compact/prompt.ts 第4-10行）
```typescript
const proactiveModule =
  feature('PROACTIVE') || feature('KAIROS')
    ? (require('../../proactive/index.js')
       as typeof import('../../proactive/index.js'))
    : null;
```

### 5.6 命令列表展开
```typescript
const COMMANDS = memoize((): Command[] => [
  addDir,
  advisor,
  ...(proactive ? [proactive] : []),
  ...(briefCommand ? [briefCommand] : []),
  ...(bridge ? [bridge] : []),
]);
```
