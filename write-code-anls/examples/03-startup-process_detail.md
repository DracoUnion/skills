# 第3课：启动流程详解：从命令行到 REPL - 细纲

## 文件信息
- **原文件**: part02-architecture/03-startup-process.md
- **类型**: 架构全景
- **难度**: ★★★☆☆

---

## 一、启动流程全景

### 1.1 生活类比：开一家餐厅
1. 开门前检查（环境检查）
2. 打开灯和空调（初始化基础设施）
3. 准备食材（加载配置和数据）
4. 通知服务员就位（启动服务）
5. 翻开"营业中"牌子（显示 REPL 界面）

### 1.2 启动流程时间线
```
main.tsx 入口 → 并行预取启动 → CLI 参数解析 → 环境初始化 → 状态创建 → 服务连接 → REPL 渲染
```

---

## 二、入口文件的前几行

### 2.1 main.tsx 前20行
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

import { startKeychainPrefetch } from './utils/secureStorage/keychainPrefetch.js';
startKeychainPrefetch();
```

### 2.2 巧妙的设计
```
main.tsx
├── profileCheckpoint (记录时间)
├── startMdmRawRead() 🚀 (启动 MDM 子进程)
├── startKeychainPrefetch() 🚀 (启动钥匙串读取)
└── 继续加载 135ms 的其他模块

三者并行执行！
```

**类比**: 边等咖啡机加热（模块加载），边去信箱拿报纸（MDM 读取），边遛狗（钥匙串读取）。

---

## 三、CLI 参数解析

### 3.1 Commander.js 配置
**文件**: `src/main.tsx`

```typescript
import { Command as CommanderCommand } from '@commander-js/extra-typings'

const program = new CommanderCommand()

// 各种选项：
// --model / -m     指定模型
// --permission-mode 权限模式
// --resume / -r    恢复会话
// --verbose        详细输出
// --max-turns      最大轮数
// --mcp-config     MCP 配置文件
```

### 3.2 CLI 参数分类
| 分类 | 参数 |
|------|------|
| 模型相关 | `--model sonnet`, `--permission-mode plan` |
| 会话相关 | `--resume`, `--continue` |
| 高级选项 | `--mcp-config path`, `--max-turns 10`, `--verbose` |

---

## 四、AppState 初始化

### 4.1 getDefaultAppState
**文件**: `src/state/AppStateStore.ts`

```typescript
export function getDefaultAppState(): AppState {
  return {
    settings: getInitialSettings(),
    tasks: {},
    agentNameRegistry: new Map(),
    verbose: false,
    mainLoopModel: null,
    toolPermissionContext: {
      ...getEmptyToolPermissionContext(),
      mode: initialMode,
    },
    mcp: {
      clients: [],
      tools: [],
      commands: [],
      resources: {},
      pluginReconnectKey: 0,
    },
    plugins: {
      enabled: [],
      disabled: [],
      commands: [],
      errors: [],
    },
    todos: {},
    thinkingEnabled: shouldEnableThinkingByDefault(),
    // ...更多字段
  }
}
```

### 4.2 AppState 结构
```
AppState
├── settings（用户配置）
├── tasks（后台任务）
├── toolPermissionContext（权限上下文）
├── mcp（MCP 连接）
├── plugins（插件系统）
├── todos（待办列表）
├── mainLoopModel（当前模型）
└── replBridge*（桥接状态）
```

### 4.3 Store 包装
**文件**: `src/main.tsx`

```typescript
import { createStore } from './state/store.js'

const appStateStore = createStore<AppState>(
  getDefaultAppState(),
  onChangeAppState  // 状态变化时的回调
)
```

**类比**: 中央控制面板——灯光状态、空调温度、客人数量、点单列表……所有信息集中管理。

---

## 五、命令系统加载

### 5.1 命令加载流程
**文件**: `src/commands.ts`

```typescript
export async function getCommands(cwd: string): Promise<Command[]> {
  const allCommands = await loadAllCommands(cwd)
  const dynamicSkills = getDynamicSkills()

  const baseCommands = allCommands.filter(
    _ => meetsAvailabilityRequirement(_) && isCommandEnabled(_),
  )

  if (dynamicSkills.length === 0) {
    return baseCommands
  }

  const baseCommandNames = new Set(baseCommands.map(c => c.name))
  const uniqueDynamicSkills = dynamicSkills.filter(
    s => !baseCommandNames.has(s.name) &&
         meetsAvailabilityRequirement(s) &&
         isCommandEnabled(s),
  )

  return [...baseCommands, ...uniqueDynamicSkills]
}
```

### 5.2 命令加载层次
```
内置命令 (/help, /clear, /compact...)
插件命令（用户安装的插件）
技能命令（/skills 目录下的技能）
动态技能（运行时发现的技能）
工作流命令（workflow 脚本）
         ↓
    合并去重
         ↓
    最终命令列表
```

---

## 六、工具注册

### 6.1 getTools 函数
**文件**: `src/tools.ts`

```typescript
export const getTools = (permissionContext: ToolPermissionContext): Tools => {
  // 简单模式：只有 Bash、Read 和 Edit
  if (isEnvTruthy(process.env.CLAUDE_CODE_SIMPLE)) {
    const simpleTools: Tool[] = [BashTool, FileReadTool, FileEditTool]
    return filterToolsByDenyRules(simpleTools, permissionContext)
  }

  // 完整模式：获取所有工具并过滤
  const tools = getAllBaseTools().filter(tool => !specialTools.has(tool.name))
  let allowedTools = filterToolsByDenyRules(tools, permissionContext)
  const isEnabled = allowedTools.map(_ => _.isEnabled())
  return allowedTools.filter((_, i) => isEnabled[i])
}
```

### 6.2 两种模式对比
| 模式 | 工具数量 | 适用场景 |
|------|---------|---------|
| 简单模式 (`--bare`) | 3个 | 脚本化调用 |
| 完整模式 | 40+个 | 交互式使用 |

---

## 七、启动到 REPL 的完整流水线

### 7.1 启动序列
```
用户输入 $ claude "你好"
    ↓
CLI 解析参数 (Commander.js)
    ↓
环境初始化
├── 加载配置文件
├── 检查认证状态
└── 加载 GrowthBook 配置
    ↓
创建 AppState + Store
    ↓
连接 MCP 服务器
    ↓
启动 React/Ink UI
    ↓
渲染终端界面
    ↓
显示 REPL 或执行单次查询
```

---

## 八、两种运行模式

### 8.1 交互模式（REPL）
```bash
$ claude          # 进入交互式 REPL
$ claude          # 在 REPL 中持续对话
```

### 8.2 非交互模式（Print/Headless）
```bash
$ claude -p "解释这段代码"    # 单次查询，输出后退出
$ echo "你好" | claude        # 管道输入
```

### 8.3 模式选择逻辑
```
用户输入
    ↓
有 -p 参数 或 管道输入 → Print 模式（非交互）
无参数，直接运行 → REPL 模式（交互式）
    ↓                    ↓
QueryEngine            React/Ink UI
单次查询               持续交互
输出结果并退出         查询循环等待用户输入
```

---

## 九、动手练习

### 练习1：追踪启动日志
运行 Claude Code 时加上 `--verbose` 参数，观察启动过程中的日志输出。

### 练习2：理解 AppState
打开 `state/AppStateStore.ts`，列出 `AppState` 中前 10 个字段并解释用途。

### 练习3：命令探索
阅读 `commands.ts` 中的 `COMMANDS` 数组：
- [ ] 总共有多少个内置命令？
- [ ] 哪些命令只对内部用户可用？（`INTERNAL_ONLY_COMMANDS`）
- [ ] `REMOTE_SAFE_COMMANDS` 包含哪些命令？为什么？

### 思考题
1. 为什么要在模块加载之前就启动 MDM 读取和钥匙串预取？
2. AppState 为什么要用 `DeepImmutable` 类型包装？
3. 如果启动时 MCP 服务器连接失败，系统会怎么处理？

---

## 十、小结

| 启动阶段 | 关键操作 | 文件 |
|---------|---------|------|
| 入口 | profileCheckpoint + 并行预取 | `main.tsx` 前20行 |
| 解析 | CLI 参数解析 | `main.tsx` Commander |
| 初始化 | 配置加载，环境设置 | `entrypoints/init.js` |
| 状态 | AppState + Store 创建 | `state/AppStateStore.ts` |
| 命令 | 加载所有命令和技能 | `commands.ts` |
| 工具 | 注册工具集 | `tools.ts` |
| 渲染 | REPL 或 Print 模式 | `ink/` + REPL |

### 关键设计模式
- **并行预取**: 利用 import 时间并行执行 I/O 操作
- **延迟加载**: `feature()` 门控 + 条件 require
- **两种模式**: 交互式 REPL vs 非交互式 Print

---

## 十一、关联文件

### 11.1 上一章
- [02-tech-stack.md](02-tech-stack.md) - 技术栈全解析

### 11.2 下一章
- [04-parallel-prefetch.md](04-parallel-prefetch.md) - 并行预取机制

---

*此细纲由 Claude Code 自动生成*
