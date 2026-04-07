# 第3课：懒加载策略 —— 动态 import() 的艺术 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第3课：懒加载策略 —— 动态 import() 的艺术

### 1.2 二级标题
- 学习目标
- 生活类比：自助餐厅 vs 点餐厅
- 真实源码解析
- 静态导入 vs 动态导入对比
- 懒加载的四种封装模式
- 判断是否适合懒加载的决策树
- 懒加载的注意事项
- 动手练习
- 本课小结
- 下节预告

### 1.3 三级标题
- 案例一：113KB 的 insights 模块
- 案例二：循环依赖的懒加载
- 案例三：事件循环停顿检测器
- 案例四：微压缩模块的懒初始化
- 模式1：Shim 代理（Claude Code 最常用）
- 模式2：单例缓存
- 模式3：函数包装 require
- 模式4：Fire-and-Forget
- 陷阱1：首次调用的延迟
- 陷阱2：类型安全
- 陷阱3：错误处理

---

## 2. 关键知识点

### 2.1 静态导入 vs 动态导入
| 特性 | 静态 `import` | 动态 `import()` |
|------|--------------|----------------|
| 加载时机 | 应用启动 | 首次调用时 |
| 是否阻塞启动 | 是 | 否 |
| Tree-shaking | 支持 | 不支持 |
| 条件加载 | 不支持 | 支持 |
| 类型推断 | 自动 | 需手动标注 |
| 返回值 | 模块导出 | `Promise<模块>` |

### 2.2 四种懒加载封装模式
1. **Shim 代理模式** - 轻量壳 + 首次调用时加载真实实现
2. **单例缓存模式** - 第一次加载后缓存，避免重复加载
3. **函数包装 require** - 延迟加载解决循环依赖
4. **Fire-and-Forget** - 后台加载模块并启动

### 2.3 懒加载决策标准
- **体积大**：>50KB → 懒加载
- **使用率低**：<10% → 懒加载
- **有循环依赖** → 懒加载
- **仅特定构建** → 懒加载

### 2.4 懒加载注意事项
- 首次调用延迟：使用 `progressMessage` 给用户反馈
- 类型安全：使用 `as typeof import()` 保持类型推断
- 错误处理：动态导入可能失败，需要兜底处理

---

## 3. 涉及的源码文件路径

### 3.1 核心源码文件
- `commands.ts` - insights 模块懒加载
- `main.tsx` - 循环依赖懒加载、事件循环停顿检测器
- `services/compact/microCompact.ts` - 微压缩模块懒初始化

---

## 4. 类名、函数名、接口名

### 4.1 函数
- `getPromptForCommand(args, context)` - 获取命令提示
- `getTeammateUtils()` - 获取 teammate 工具（懒加载）
- `getTeammatePromptAddendum()` - 获取 teammate 提示附录（懒加载）
- `getTeammateModeSnapshot()` - 获取 teammate 模式快照（懒加载）
- `startEventLoopStallDetector()` - 启动事件循环停顿检测器
- `getCachedMCModule()` - 获取缓存的微压缩模块

### 4.2 类型/接口
- `Command` - 命令接口
- `RenderableMessage` - 可渲染消息类型
- `Tool` - 工具类型

### 4.3 变量
- `usageReport` - insights 命令（懒加载包装）
- `cachedMCModule` - 缓存的微压缩模块

---

## 5. 代码片段重点

### 5.1 Shim 代理模式 - insights 模块（commands.ts 第188-202行）
```typescript
const usageReport: Command = {
  type: 'prompt',
  name: 'insights',
  description: 'Generate a report analyzing your Claude Code sessions',
  contentLength: 0,
  progressMessage: 'analyzing your sessions',
  source: 'builtin',
  async getPromptForCommand(args, context) {
    const real = (await import('./commands/insights.js')).default;
    if (real.type !== 'prompt') throw new Error('unreachable');
    return real.getPromptForCommand(args, context);
  },
};
```

### 5.2 循环依赖懒加载（main.tsx 第69-73行）
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

### 5.3 Fire-and-Forget 懒加载（main.tsx 第428-430行）
```typescript
if ("external" === 'ant') {
  void import('./utils/eventLoopStallDetector.js')
    .then(m => m.startEventLoopStallDetector());
}
```

### 5.4 单例缓存模式（microCompact.ts 第62-69行）
```typescript
let cachedMCModule: typeof import('./cachedMicrocompact.js') | null = null;

async function getCachedMCModule(): Promise<
  typeof import('./cachedMicrocompact.js')
> {
  if (!cachedMCModule) {
    cachedMCModule = await import('./cachedMicrocompact.js');
  }
  return cachedMCModule;
}
```

### 5.5 类型安全标注
```typescript
const getModule = () =>
  require('./module.js') as typeof import('./module.js');
```
