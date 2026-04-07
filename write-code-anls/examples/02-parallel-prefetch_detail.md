# 第2课：并行预取详解 —— Promise.all 实战 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第2课：并行预取详解 —— Promise.all 实战

### 1.2 二级标题
- 学习目标
- 生活类比：网购取快递
- 真实源码解析
- 三种并行模式对比
- 模式四：Fire-and-Forget（发射后不管）
- 模式五：压缩后的并行恢复
- 并行预取的设计原则
- 动手练习
- 本课小结
- 下节预告

### 1.3 三级标题
- 模式一：启动时的并行预取
- 模式二：技能和插件的并行加载
- 模式三：带容错的并行加载
- 原则一：识别依赖关系
- 原则二：降级策略
- 原则三：预取时机

---

## 2. 关键知识点

### 2.1 串行 vs 并行执行
- 串行执行：总耗时 = 各操作耗时之和
- 并行执行：总耗时 = 最慢操作的耗时
- 节省比例示例：50+80+100=230ms → max(50,80,100)=100ms（节省56%）

### 2.2 Promise.all 三种模式
| 模式 | 一个任务失败的后果 | Claude Code 使用频率 |
|------|-------------------|---------------------|
| `Promise.all` | 整体失败 | 少用 |
| `Promise.allSettled` | 不影响，但需手动检查 | 偶尔用 |
| `Promise.all` + `.catch` | 不影响，自动降级为默认值 | **最常用** |

### 2.3 Fire-and-Forget 模式
- 使用 `void` 关键字启动后台任务
- 不等待结果，不阻塞主流程
- 黄金窗口：UI 首次渲染后、用户开始打字前

### 2.4 依赖关系分析
- 无依赖关系的操作 → 可以并行
- 有依赖关系的操作 → 必须串行
- 使用 `Promise.all` + `.catch()` 实现独立容错

---

## 3. 涉及的源码文件路径

### 3.1 核心源码文件
- `main.tsx` - 启动遥测并行预取
- `commands.ts` - 技能并行加载
- `services/compact/compact.ts` - 压缩后并行恢复

### 3.2 相关工具函数
- `utils/startupProfiler.js` - 性能追踪

---

## 4. 类名、函数名、接口名

### 4.1 函数
- `logStartupTelemetry()` - 启动遥测日志
- `getIsGit()` - 检查是否在 git 仓库
- `getWorktreeCount()` - 获取 worktree 数量
- `getGhAuthStatus()` - 获取 GitHub 认证状态
- `loadAllCommands(cwd: string)` - 加载所有命令
- `getSkills(cwd: string)` - 获取技能
- `getPluginCommands()` - 获取插件命令
- `getWorkflowCommands(cwd: string)` - 获取工作流命令
- `getSkillDirCommands(cwd: string)` - 获取技能目录命令
- `getPluginSkills()` - 获取插件技能
- `getBundledSkills()` - 获取捆绑技能
- `getBuiltinPluginSkillCommands()` - 获取内置插件技能命令
- `startDeferredPrefetches()` - 延迟预取
- `initUser()` - 用户初始化
- `getUserContext()` - 获取用户上下文
- `prefetchSystemContextIfSafe()` - 安全预取系统上下文
- `getRelevantTips()` - 获取相关提示
- `initializeAnalyticsGates()` - 初始化分析门控
- `prefetchOfficialMcpUrls()` - 预取 MCP URL
- `refreshModelCapabilities()` - 刷新模型能力
- `createPostCompactFileAttachments()` - 创建压缩后文件附件
- `createAsyncAgentAttachmentsIfNeeded()` - 创建异步 Agent 附件
- `logError(error: Error)` - 错误日志
- `logForDebugging(message: string)` - 调试日志
- `toError(err: unknown)` - 转换为 Error 对象

### 4.2 常量
- `POST_COMPACT_MAX_FILES_TO_RESTORE` - 压缩后最大恢复文件数

---

## 5. 代码片段重点

### 5.1 启动遥测并行预取（main.tsx）
```typescript
async function logStartupTelemetry(): Promise<void> {
  if (isAnalyticsDisabled()) return;

  const [isGit, worktreeCount, ghAuthStatus] = await Promise.all([
    getIsGit(),
    getWorktreeCount(),
    getGhAuthStatus()
  ]);

  logEvent('tengu_startup_telemetry', {
    is_git: isGit,
    worktree_count: worktreeCount,
    gh_auth_status: ghAuthStatus,
  });
}
```

### 5.2 技能并行加载（commands.ts）
```typescript
const loadAllCommands = memoize(async (cwd: string): Promise<Command[]> => {
  const [
    { skillDirCommands, pluginSkills, bundledSkills, builtinPluginSkills },
    pluginCommands,
    workflowCommands,
  ] = await Promise.all([
    getSkills(cwd),
    getPluginCommands(),
    getWorkflowCommands ? getWorkflowCommands(cwd) : Promise.resolve([]),
  ]);

  return [
    ...bundledSkills,
    ...builtinPluginSkills,
    ...skillDirCommands,
    ...workflowCommands,
    ...pluginCommands,
    ...pluginSkills,
    ...COMMANDS(),
  ];
});
```

### 5.3 带容错的并行加载（commands.ts）
```typescript
async function getSkills(cwd: string): Promise<{
  skillDirCommands: Command[]
  pluginSkills: Command[]
  bundledSkills: Command[]
  builtinPluginSkills: Command[]
}> {
  try {
    const [skillDirCommands, pluginSkills] = await Promise.all([
      getSkillDirCommands(cwd).catch(err => {
        logError(toError(err));
        logForDebugging('Skill directory commands failed to load');
        return [];
      }),
      getPluginSkills().catch(err => {
        logError(toError(err));
        logForDebugging('Plugin skills failed to load');
        return [];
      }),
    ]);

    const bundledSkills = getBundledSkills();
    const builtinPluginSkills = getBuiltinPluginSkillCommands();

    return { skillDirCommands, pluginSkills, bundledSkills, builtinPluginSkills };
  } catch (err) {
    logError(toError(err));
    return {
      skillDirCommands: [],
      pluginSkills: [],
      bundledSkills: [],
      builtinPluginSkills: [],
    };
  }
}
```

### 5.4 压缩后并行恢复（compact.ts）
```typescript
const [fileAttachments, asyncAgentAttachments] = await Promise.all([
  createPostCompactFileAttachments(
    preCompactReadFileState,
    context,
    POST_COMPACT_MAX_FILES_TO_RESTORE,
  ),
  createAsyncAgentAttachmentsIfNeeded(context),
]);
```

### 5.5 Fire-and-Forget 模式（main.tsx）
```typescript
export function startDeferredPrefetches(): void {
  void initUser();
  void getUserContext();
  prefetchSystemContextIfSafe();
  void getRelevantTips();
  void initializeAnalyticsGates();
  void prefetchOfficialMcpUrls();
  void refreshModelCapabilities();
  void settingsChangeDetector.initialize();
}
```
