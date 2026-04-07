# 图解 Claude Code 完全指南 - 细纲

## 文件信息
- **原文件**: 10-architecture-overview.md
- **类型**: 第 10 课：状态管理架构全景与设计启示
- **难度**: ★★★☆☆

---

## 一、文档结构概览

### 1.1 学习目标
1. 建立 Claude Code 状态管理的完整心智模型
2. 理解各子系统之间的协作关系
3. 掌握 5 个可直接应用到自己项目的设计原则
4. 了解这套架构的局限性和可能的演进方向
5. 获得独立分析开源项目架构的能力

### 1.2 章节结构
| 章节 | 主题 | 核心内容 |
|------|------|---------|
| 一、架构全景图 | 全局视图 | 三层架构、数据流总览 |
| 二、各子系统关系矩阵 | 关系梳理 | 读取/写入/触发条件 |
| 三、核心组件源码文件清单 | 文件索引 | 12 个核心文件 |
| 四、5 个可复用设计原则 | 设计原则 | 最小 Store、副作用收口等 |
| 五、架构中的精妙细节 | 细节分析 | Object.is 短路、Set 管理等 |
| 六、架构的局限性 | 反向思考 | 单进程假设、无快照等 |
| 七、与主流方案对比 | 横向对比 | Redux/Zustand/MobX |
| 八、应用到你的项目 | 实践指导 | CLI/Web/桌面应用 |

---

## 二、关键知识点

### 2.1 三层架构
```mermaid
graph TB
    subgraph L1["第一层：运行时内存"]
        direction TB
        S["createStore(34行)<br>状态引擎"] --> AS["AppState<br>500+ 字段的巨型状态树"]
        AS --> OC["onChangeAppState<br>副作用收口"]
        AS --> SEL["selectors.ts<br>状态派生"]
        AS --> TVH["teammateViewHelpers.ts<br>视图辅助"]
    end

    subgraph L2["第二层：文件持久化"]
        direction TB
        GC["GlobalConfig<br>~/.claude/config.json<br>跨项目共享"]
        ST["Settings<br>settings.json (多层合并)<br>用户+项目+策略"]
        MD["Memdir<br>memory/ 目录<br>AI 长期记忆"]
        HI["History<br>history.jsonl<br>命令历史"]
    end

    subgraph L3["第三层：版本迁移"]
        direction LR
        M1["migrateFennec<br>ToOpus"]
        M2["migrateSonnet45<br>ToSonnet46"]
        M3["migrateEnable<br>AllProject..."]
        M4["... 共11个"]
    end

    OC --> |"verbose,<br>expandedView"| GC
    OC --> |"mainLoopModel,<br>settings"| ST
    S -.-> |"初始值来自"| GC
    S -.-> |"初始值来自"| ST

    L3 --> |"升级旧格式"| GC
    L3 --> |"升级旧格式"| ST

    MD -.-> |"findRelevantMemories"| AS
    HI -.-> |"getHistory"| AS
```

### 2.2 数据流总览
```mermaid
flowchart LR
    subgraph "启动阶段"
        BOOT1["读取 GlobalConfig"] --> BOOT2["读取 Settings"]
        BOOT2 --> BOOT3["运行 Migrations"]
        BOOT3 --> BOOT4["getDefaultAppState()"]
        BOOT4 --> BOOT5["createStore(state, onChange)"]
    end

    subgraph "运行阶段"
        RUN1["用户操作"] --> RUN2["setState(updater)"]
        RUN2 --> RUN3["Object.is 检查"]
        RUN3 --> |"变了"| RUN4["onChange 副作用"]
        RUN3 --> |"没变"| RUN5["跳过"]
        RUN4 --> RUN6["写 GlobalConfig"]
        RUN4 --> RUN7["写 Settings"]
        RUN4 --> RUN8["通知远端"]
        RUN2 --> RUN9["通知 listeners"]
        RUN9 --> RUN10["UI 重渲染"]
    end

    subgraph "关闭阶段"
        EXIT1["进程退出信号"] --> EXIT2["registerCleanup 回调"]
        EXIT2 --> EXIT3["刷盘缓冲区"]
        EXIT3 --> EXIT4["history.jsonl 写入"]
    end

    BOOT5 --> RUN1
    RUN1 --> EXIT1
```

### 2.3 各子系统关系矩阵
| 子系统 | 读取 | 写入 | 触发条件 |
|--------|------|------|---------|
| **createStore** | 被所有组件读取 | 只能通过 setState | 程序启动时创建 |
| **AppState** | 被 Store 管理 | 通过 Store.setState | 随 Store 创建 |
| **onChangeAppState** | 读 newState/oldState | 写 GlobalConfig/Settings | 每次 setState 后 |
| **Memdir** | 被 AI 按需读取 | 被 AI 按需写入 | 用户提问/AI 学到东西时 |
| **History** | 按 ↑ 或 Ctrl+R 读 | 用户每次输入时写 | 命令提交时 |
| **Migrations** | 读 Settings/Config | 写 Settings/Config | 每次启动时（版本检查） |

### 2.4 核心组件源码文件清单
| 文件 | 行数 | 核心职责 |
|------|------|---------|
| `state/store.ts` | 34 | 极简 Store 引擎 |
| `state/AppStateStore.ts` | 570 | 状态类型定义 + 工厂函数 |
| `state/onChangeAppState.ts` | 172 | 副作用收口 |
| `state/selectors.ts` | 77 | 派生状态计算 |
| `memdir/memdir.ts` | 508 | 记忆系统主模块 |
| `memdir/memoryTypes.ts` | 272 | 四种记忆类型定义 |
| `memdir/paths.ts` | 279 | 记忆路径计算 |
| `memdir/memoryScan.ts` | 95 | 记忆文件扫描 |
| `memdir/findRelevantMemories.ts` | 142 | AI 智能召回 |
| `memdir/memoryAge.ts` | 54 | 新鲜度计算 |
| `history.ts` | 465 | 命令历史系统 |
| `migrations/*.ts` | ~11 个文件 | 版本迁移函数 |

### 2.5 5 个可复用设计原则

#### 原则 1：最小必要 Store
```
🎯 状态管理的核心可以非常小——34 行足够。
```
```typescript
// Claude Code 的选择
createStore<T>(initialState, onChange)  // 就这么多

// 没有 middleware、没有 devtools、没有 selector、没有 action creator
// 需要什么就在 onChange 里加什么
```

#### 原则 2：副作用收口
```
🎯 所有副作用集中在一个地方处理，而不是分散在各个调用方。
```
```mermaid
graph LR
    subgraph "分散式（容易出 Bug）"
        A1["改权限"] --> B1["通知远端"]
        A2["改权限"] --> B2["❌ 忘记通知"]
        A3["改权限"] --> B3["❌ 忘记通知"]
    end

    subgraph "收口式（Claude Code 的选择）"
        C1["改权限"] --> D1["onChange"]
        C2["改权限"] --> D1
        C3["改权限"] --> D1
        D1 --> E1["自动通知远端"]
    end
```

#### 原则 3：文件系统即数据库
```
🎯 对于配置和记忆类数据，文件系统是零成本的数据库。
```
| Claude Code 的做法 | 等价的数据库操作 |
|-------------------|----------------|
| `readFileSync('MEMORY.md')` | `SELECT * FROM memories WHERE is_index = true` |
| `writeFile('user_role.md', content)` | `INSERT INTO memories (type, content) VALUES ('user', ...)` |
| `readdir(memoryDir, { recursive: true })` | `SELECT filename FROM memories` |
| `readLinesReverse('history.jsonl')` | `SELECT * FROM history ORDER BY id DESC` |

#### 原则 4：分层持久化
```
🎯 不同生命周期的数据用不同策略持久化。
```
```mermaid
graph TB
    subgraph "生命周期分层"
        T["瞬态<br>（毫秒~秒）"] --- |"不持久化"| T1["UI 焦点<br>弹出层状态<br>网络连接状态"]
        S["会话级<br>（分钟~小时）"] --- |"退出前写"| S1["命令历史缓冲<br>推测执行结果"]
        P["项目级<br>（天~月）"] --- |"立即写"| P1["模型选择<br>权限设置<br>项目记忆"]
        G["全局级<br>（月~年）"] --- |"立即写"| G1["用户偏好<br>主题设置<br>启动计数"]
    end
```

#### 原则 5：幂等迁移链
```
🎯 数据格式升级用幂等函数，而不是记录"是否已迁移"的标志位。
```
```typescript
// ✅ 幂等迁移：每次运行自行判断是否需要
function migrate(): void {
  const value = read()
  if (isOldFormat(value)) {
    write(convertToNewFormat(value))
  }
  // 如果已经是新格式，什么都不做
}

// ❌ 非幂等迁移：依赖外部标志
function migrate(): void {
  if (hasMigrated) return     // 标志位可能丢失
  write(convertToNewFormat(read()))
  hasMigrated = true
}
```

### 2.6 架构中的精妙细节

#### Object.is 短路 —— 零成本跳过
```typescript
// store.ts 中的短路
if (Object.is(next, prev)) return
```
这一行避免了：
- 不必要的 onChange 调用
- 不必要的磁盘写入
- 不必要的 UI 重渲染
- 不必要的网络请求

#### Set 管理监听者 —— O(1) 操作
```typescript
const listeners = new Set<Listener>()
// 添加：O(1)，不重复
// 删除：O(1)，不需要遍历
// 遍历：有序，按添加顺序
```

#### 异步生成器读取 —— 内存友好
```typescript
async function* makeLogEntryReader(): AsyncGenerator<LogEntry> {
  // 惰性读取：需要多少读多少，不把整个文件加载到内存
  for await (const line of readLinesReverse(historyPath)) {
    yield deserializeLogEntry(line)
  }
}
```

#### 双重检查避免无意义写入
```typescript
// 先检查 AppState 变没变
if (newState.verbose !== oldState.verbose) {
  // 再检查磁盘上的值是否已经正确
  if (getGlobalConfig().verbose !== newState.verbose) {
    saveGlobalConfig(...)  // 真正需要写才写
  }
}
```

#### Sonnet 作为"记忆选择器"
```typescript
// 不是关键字匹配，不是向量搜索，而是直接用 LLM 判断相关性
const result = await sideQuery({
  model: getDefaultSonnetModel(),
  system: SELECT_MEMORIES_SYSTEM_PROMPT,
  messages: [{ role: 'user', content: `Query: ${query}\n\nAvailable memories:\n${manifest}` }],
})
```

### 2.7 架构的局限性

#### 单进程假设
Store 是进程内的闭包状态。如果 Claude Code 需要多进程共享状态（比如多个终端窗口），当前架构需要通过文件系统（GlobalConfig）间接同步，延迟较高。

#### 无状态快照/回滚
当前的 Store 没有历史快照功能——不能回到"5 分钟前的状态"。

#### 记忆的线性扫描
`scanMemoryFiles` 对所有 .md 文件做线性扫描。当记忆文件增长到几百个以上时，这可能成为性能瓶颈。

#### JSONL 文件的增长
`history.jsonl` 只追加不清理。长期使用后文件可能变得很大，反向读取变慢。

### 2.8 与主流方案对比
| 维度 | Claude Code | Redux | Zustand | MobX |
|------|------------|-------|---------|------|
| 核心代码量 | 34 行 | ~1500 行 | ~300 行 | ~5000 行 |
| 依赖 | 0 | 0 | 0 | 0 |
| 学习曲线 | 极低 | 中 | 低 | 中 |
| 中间件 | onChange 收口 | middleware chain | middleware | reactions |
| 持久化 | 内置（文件系统） | 需要插件 | 需要插件 | 需要插件 |
| DevTools | 无 | 有 | 有 | 有 |
| 适合场景 | CLI 工具 | 大型 SPA | 中型 React 应用 | 响应式需求 |

---

## 三、关联文件索引

### 3.1 前置阅读
- [09-persistence-strategy.md](09-persistence-strategy.md) - 持久化策略

### 3.2 全系列回顾
| 课程 | 一句话总结 |
|------|----------|
| 第 1 课 | 状态管理 = 统一管理数据的读取、修改和通知 |
| 第 2 课 | 34 行代码实现完整的 Store：闭包 + 发布订阅 + Object.is |
| 第 3 课 | 500+ 字段按功能分域，DeepImmutable 保护不可变性 |
| 第 4 课 | 一个 onChange 函数收口所有副作用，消灭分散式 Bug |
| 第 5 课 | 文件系统即数据库，MEMORY.md 做索引，Sonnet 做智能召回 |
| 第 6 课 | user/feedback/project/reference 四种类型，不存能从代码推导的 |
| 第 7 课 | JSONL 追加写入，缓冲区优先读取，文件锁防并发 |
| 第 8 课 | 幂等迁移函数，前置守卫保证安全，失败不阻塞启动 |
| 第 9 课 | 瞬态/会话/项目/全局四级，立即写/延迟写/退出写三种时机 |
| 第 10 课 | 三层架构全景，5 个可复用原则，架构的局限与演进 |

---

## 四、源码对应关系

### 4.1 核心类型
| 名称 | 类型 | 位置 | 说明 |
|------|------|------|------|
| `Store<T>` | interface | `state/store.ts` | Store 接口定义 |
| `AppState` | type | `state/AppStateStore.ts` | 应用状态类型 |
| `DeepImmutable<T>` | type | `state/AppStateStore.ts` | 深度不可变类型 |
| `LogEntry` | type | `history.ts` | 历史记录条目 |
| `MemoryType` | type | `memdir/memoryTypes.ts` | 记忆类型 |

### 4.2 核心函数
| 函数名 | 位置 | 功能 |
|--------|------|------|
| `createStore()` | `state/store.ts` | 创建 Store 实例 |
| `getDefaultAppState()` | `state/AppStateStore.ts` | 获取默认状态 |
| `onChangeAppState()` | `state/onChangeAppState.ts` | 副作用收口 |
| `addToHistory()` | `history.ts` | 添加到历史 |
| `scanMemoryFiles()` | `memdir/memoryScan.ts` | 扫描记忆文件 |
| `findRelevantMemories()` | `memdir/findRelevantMemories.ts` | 智能召回 |

---

## 五、本课小结

| 概念 | 解释 |
|------|------|
| 三层架构 | 运行时内存 → 文件持久化 → 版本迁移 |
| 5 个设计原则 | 最小 Store、副作用收口、文件系统即数据库、分层持久化、幂等迁移 |
| Object.is 短路 | 状态未变化时零成本跳过 |
| Set 管理监听者 | O(1) 添加删除 |
| 异步生成器 | 惰性读取，内存友好 |
| 架构局限 | 单进程假设、无快照、线性扫描 |

---

*此细纲由 Claude Code 自动生成，用于快速导航和内容概览*
