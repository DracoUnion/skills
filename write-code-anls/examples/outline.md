# Claude Code 完全指南 - 全书大纲

## 封面
- [封面](README.md)
- 关键知识点: 项目概览、12篇114节课程、51万行源码解析
- 源码对应: `src/main.tsx` (入口), `src/Tool.ts` (工具类型), `src/tools.ts` (工具注册)

---

## 前言

### 关于本书
- 关键知识点: 零基础友好的AI编程学习指南、哆啦A梦风格漫画、51万行TypeScript源码解析
- 源码对应: 无（概念介绍）
- 核心概念: AI Agent、Tool Use、QueryEngine、MCP

### 学习路线图
- 关键知识点: 四条学习路径（零基础/前端开发者/AI应用开发者/系统架构师）、核心知识图谱
- 源码对应: 无（概念介绍）
- 预计时间: 全书50-60小时

### 术语表
- 关键知识点: Agent、Agent Loop、MCP、Tool、Token、QueryEngine、AST、Bridge等50+术语
- 源码对应: `src/QueryEngine.ts`, `src/state/AppStateStore.ts`, `src/bridge/`

---

## 第一篇：基础入门

### 1.1 什么是 Claude Code？
- 关键知识点: AI编程助手等级（代码补全/对话式/自主代理）、四大核心能力（编辑/运行/搜索/协调）、技术栈概览
- 源码对应: `src/main.tsx`, `src/Tool.ts`, `src/tools.ts`
- 核心类/函数: `QueryEngine` 类, `getAllBaseTools()`, `buildTool()`

### 1.2 编程基础：终端与命令行
- 关键知识点: GUI vs CLI、基本终端命令（pwd/ls/cd/cat等）、环境变量、Git版本控制、IDE选择
- 源码对应: 无（概念介绍）

### 1.3 TypeScript 快速入门
- 关键知识点: 基本类型、接口与类型别名、函数与箭头函数、模块系统、async/await、泛型基础、条件导入
- 源码对应: `src/Tool.ts` (类型定义), `src/tools.ts` (import示例)
- 核心类型: `Tool<Input, Output, P>`, `ValidationResult`, `ToolInputJSONSchema`

### 1.4 React 与 Ink 终端 UI
- 关键知识点: 组件化思想、JSX语法、Props与State、React Hooks（useState/useEffect/useMemo）、Ink框架、Box/Text组件
- 源码对应: `src/components/` (144个组件), `src/ink/` (Ink定制实现)
- 核心组件: `Spinner.tsx`, `SearchBox.tsx`, `App.tsx`

---

## 第二篇：架构全景

### 2.1 软件架构概念
- 关键知识点: 分层架构模型（五层蛋糕）、关注点分离、可替换性/可测试性/可扩展性
- 源码对应: `src/state/store.ts`, `src/tools.ts`, `src/QueryEngine.ts`, `src/commands.ts`
- 核心类: `Store<T>`, `QueryEngine`, `createStore()`

### 2.2 技术栈全解析
- 关键知识点: TypeScript类型安全、Bun运行时、feature()编译时门控、React/Ink终端渲染、Dead Code Elimination
- 源码对应: `src/QueryEngine.ts`, `src/tools.ts`, `src/main.tsx`
- 核心技术: `feature('PROACTIVE')`, `feature('COORDINATOR_MODE')`

### 2.3 启动流程详解
- 关键知识点: main.tsx入口、并行预取启动、CLI参数解析、AppState初始化、命令系统加载、工具注册
- 源码对应: `src/main.tsx`, `src/state/AppStateStore.ts`, `src/commands.ts`, `src/tools.ts`
- 核心函数: `getDefaultAppState()`, `getCommands()`, `getTools()`

### 2.4 并行预取机制
- 关键知识点: MDM配置预取、Keychain预取、GrowthBook预取、Promise.all并行、Import间隙预取
- 源码对应: `src/main.tsx`, `src/utils/settings/mdm/rawRead.js`, `src/utils/secureStorage/keychainPrefetch.js`
- 核心函数: `startMdmRawRead()`, `startKeychainPrefetch()`, `profileCheckpoint()`

### 2.5 工具系统架构
- 关键知识点: 40+工具分类、工具注册中心、条件加载设计、工具过滤管道、assembleToolPool
- 源码对应: `src/tools.ts`, `src/constants/tools.ts`
- 核心函数: `getAllBaseTools()`, `filterToolsByDenyRules()`, `assembleToolPool()`
- 核心常量: `ALL_AGENT_DISALLOWED_TOOLS`, `ASYNC_AGENT_ALLOWED_TOOLS`, `COORDINATOR_MODE_ALLOWED_TOOLS`

### 2.6 QueryEngine 查询引擎
- 关键知识点: QueryEngine类结构、submitMessage流程、query.ts核心循环、流式工具执行、自动压缩
- 源码对应: `src/QueryEngine.ts`, `src/query.ts`
- 核心类/函数: `QueryEngine`类, `query()`函数, `StreamingToolExecutor`, `ask()`

### 2.7 权限系统设计
- 关键知识点: 权限模式（default/plan/auto/bypass）、权限决策流程、ToolPermissionContext、权限规则来源层次
- 源码对应: `src/utils/permissions/permissions.ts`, `src/state/AppStateStore.ts`
- 核心类型: `PermissionBehavior`, `PermissionRule`, `ToolPermissionContext`
- 核心函数: `hasPermissionsToUseTool()`, `filterToolsByDenyRules()`

### 2.8 Agent Swarm 协作
- 关键知识点: AgentTool子代理、代理生命周期、Worktree隔离、协调器模式、SendMessageTool通信、后台任务管理
- 源码对应: `src/tools/AgentTool/AgentTool.tsx`, `src/coordinator/coordinatorMode.ts`, `src/state/AppStateStore.ts`
- 核心函数: `runAgent()`, `registerAsyncAgent()`, `isCoordinatorMode()`
- 核心常量: `ALL_AGENT_DISALLOWED_TOOLS`, `COORDINATOR_MODE_ALLOWED_TOOLS`

### 2.9 MCP 扩展系统
- 关键知识点: MCP协议概念、MCP客户端实现、传输协议（stdio/SSE/HTTP/WebSocket）、MCPTool包装、安全模型
- 源码对应: `src/services/mcp/client.ts`, `src/services/mcp/types.ts`, `src/services/mcp/config.ts`, `src/tools/MCPTool/MCPTool.ts`
- 核心类型: `MCPServerConnection`, `McpServerConfigSchema`, `TransportSchema`
- 核心函数: `getClaudeCodeMcpConfigs()`, `buildMcpToolName()`

### 2.10 Bridge 与全架构总结
- 关键知识点: Bridge桥接系统、REPL Bridge、会话管理、退避和容错、全架构回顾
- 源码对应: `src/bridge/bridgeMain.ts`, `src/bridge/sessionRunner.ts`, `src/bridge/replBridge.ts`
- 核心常量: `DEFAULT_BACKOFF`, `BRIDGE_SAFE_COMMANDS`

---

## 第三篇：工具系统

### 3.1 工具系统概览
- 关键知识点: 工具系统四大支柱（注册中心/统一接口/权限系统/执行引擎）、三级过滤管道、工具分类
- 源码对应: `src/tools.ts`, `src/Tool.ts`, `src/tools/`, `src/utils/permissions/`
- 核心接口: `Tool<Input, Output, P>`, `ToolUseContext`
- 核心函数: `getAllBaseTools()`, `getTools()`, `buildTool()`

### 3.2 工具注册中心
- 关键知识点: getAllBaseTools三级过滤、三种条件加载模式、延迟加载打破循环依赖、工具池组装策略
- 源码对应: `src/tools.ts`, `src/tools/SleepTool/SleepTool.ts`, `src/tools/TeamCreateTool/`
- 核心函数: `getAllBaseTools()`, `getTools()`, `assembleToolPool()`, `getMergedTools()`
- 核心常量: `TOOL_PRESETS`, `specialTools`, `REPL_ONLY_TOOLS`

### 3.3 Tool 接口设计
- 关键知识点: Tool接口核心属性、工具生命周期、安全默认值（Fail-Closed）、Zod Schema设计、UI渲染方法
- 源码对应: `src/Tool.ts` (第362-695行), `src/utils/lazySchema.ts`
- 核心类型: `Tool<Input, Output, P>`, `ToolUseContext`, `ToolResult<Output>`, `ValidationResult`, `PermissionResult`
- 核心函数: `buildTool()`, `toolMatchesName()`
- 核心常量: `TOOL_DEFAULTS`

### 3.4 BashTool 深度解析
- 关键知识点: BashTool模块结构、命令分类（搜索/读取/列表/静默）、AST解析三种结果、安全包装器剥离、复合命令安全检查
- 源码对应: `src/tools/BashTool/BashTool.tsx`, `src/tools/BashTool/bashPermissions.ts`, `src/tools/BashTool/bashSecurity.ts`, `src/tools/BashTool/readOnlyValidation.ts`
- 核心函数: `bashToolHasPermission()`, `bashToolCheckPermission()`, `stripSafeWrappers()`, `parseCommandRaw()`, `isSearchOrReadBashCommand()`
- 核心常量: `BASH_SEARCH_COMMANDS`, `BASH_READ_COMMANDS`, `BASH_SILENT_COMMANDS`, `SAFE_ENV_VARS`, `BARE_SHELL_PREFIXES`, `MAX_SUBCOMMANDS_FOR_SECURITY_CHECK` = 50

### 3.5 文件操作工具
- 关键知识点: FileReadTool多格式支持、文件去重机制、FileEditTool安全模型、写入通知链
- 源码对应: `src/tools/FileReadTool/FileReadTool.ts`, `src/tools/FileEditTool/FileEditTool.ts`, `src/tools/FileWriteTool/FileWriteTool.ts`
- 核心函数: `readFileInRange()`, `readImageWithTokenBudget()`, `validateInput()`, `writeTextContent()`, `findActualString()`
- 核心常量: `BLOCKED_DEVICE_PATHS`, `CYBER_RISK_MITIGATION_REMINDER`, `maxResultSizeChars`

### 3.6 代码搜索工具
- 关键知识点: GrepTool输出模式（content/files_with_matches/count）、head_limit分页机制、GlobTool限制、条件加载
- 源码对应: `src/tools/GrepTool/GrepTool.ts`, `src/tools/GlobTool/GlobTool.ts`, `src/tools/GrepTool/prompt.ts`, `src/utils/ripgrep.ts`
- 核心函数: `call()`, `applyHeadLimit()`, `ripGrep()`, `toRelativePath()`
- 核心常量: `VCS_DIRECTORIES_TO_EXCLUDE`, `DEFAULT_HEAD_LIMIT` = 250, `maxResultSizeChars` = 20_000

### 3.7 权限守门人
- 关键知识点: 权限三种行为（allow/deny/ask）、七步检查流程、规则来源优先级、Safety Check不可绕过
- 源码对应: `src/utils/permissions/permissions.ts`, `src/types/permissions.ts`, `src/utils/permissions/PermissionResult.ts`
- 核心函数: `hasPermissionsToUseTool()`, `hasPermissionsToUseToolInner()`, `getDenyRuleForTool()`, `getAskRuleForTool()`, `toolAlwaysAllowedRule()`
- 核心类型: `PermissionBehavior`, `PermissionDecision`, `PermissionDecisionReason`, `ToolPermissionContext`, `PermissionRule`
- 核心常量: `PERMISSION_RULE_SOURCES`

### 3.8 AgentTool 子代理
- 关键知识点: 内置Agent类型、工具隔离、权限隔离、资源清理8步、Forked Agent模式
- 源码对应: `src/tools/AgentTool/AgentTool.ts`, `src/tools/AgentTool/runAgent.ts`, `src/tools/AgentTool/agentToolUtils.ts`, `src/tools/AgentTool/builtInAgents.ts`
- 核心函数: `runAgent()`, `filterToolsForAgent()`, `resolveAgentTools()`, `initializeAgentMcpServers()`
- 核心常量: `ONE_SHOT_BUILTIN_AGENT_TYPES`, `ALL_AGENT_DISALLOWED_TOOLS`, `CUSTOM_AGENT_DISALLOWED_TOOLS`, `ASYNC_AGENT_ALLOWED_TOOLS`

### 3.9 外部工具集成
- 关键知识点: MCP工具特点、LSP九种操作、WebFetch权限控制、assembleToolPool排序
- 源码对应: `src/tools/MCPTool/MCPTool.ts`, `src/tools/LSPTool/LSPTool.ts`, `src/tools/WebFetchTool/WebFetchTool.ts`, `src/tools/WebFetchTool/preapproved.ts`
- 核心常量: `MCP_TOOL_NAME_PREFIX`, `LSP_TOOL_NAME`, `WEB_FETCH_TOOL_NAME`, `MAX_LSP_FILE_SIZE_BYTES` = 10MB

### 3.10 实战：构建新工具
- 关键知识点: Tool接口三层方法、buildTool安全默认值、开发流程、权限模式选择
- 源码对应: `src/Tool.ts`, `src/tools.ts`, `src/utils/lazySchema.ts`, `src/utils/permissions/filesystem.ts`
- 核心函数: `buildTool()`, `lazySchema()`, `checkReadPermissionForTool()`, `getRuleByContentsForTool()`
- 核心常量: `TOOL_DEFAULTS`, `DEFAULT_HEAD_LIMIT` = 250

---

## 第四篇：查询引擎

### 4.1 QueryEngine 是什么
- 关键知识点: QueryEngine核心地位、QueryEngineConfig配置项、核心属性、submitMessage方法、ask()函数
- 源码对应: `src/QueryEngine.ts`, `src/query.ts`
- 核心类: `QueryEngine`, `QueryEngineConfig`
- 核心方法: `submitMessage()`, `ask()`, `interrupt()`
- 核心类型: `Message`, `NonNullableUsage`, `SDKPermissionDenial`

### 4.2 Agent Loop 核心循环
- 关键知识点: Agent Loop核心流程、State对象结构、六个阶段循环、终止条件类型
- 源码对应: `src/query.ts`
- 核心函数: `query()`, `queryLoop()`
- 核心类型: `QueryParams`, `State`, `Terminal`, `Continue`
- 核心常量: `DEFAULT_MAX_TURNS`

### 4.3 系统提示词构建
- 关键知识点: 三层上下文架构（System Prompt/User Context/System Context）、fetchSystemPromptParts并行获取、Git状态信息、CLAUDE.md加载层次
- 源码对应: `src/utils/queryContext.ts`, `src/context.ts`, `src/constants/prompts.ts`
- 核心函数: `fetchSystemPromptParts()`, `getSystemContext()`, `getUserContext()`, `getGitStatus()`
- 核心常量: `MAX_STATUS_CHARS`

### 4.4 流式响应
- 关键知识点: 流式事件六种类型、AsyncGenerator链条、暂扣机制、Usage追踪流程、流式工具执行
- 源码对应: `src/query.ts`, `src/QueryEngine.ts`, `src/services/api/claude.ts`
- 核心类型: `StreamEvent`, `RequestStartEvent`, `TombstoneMessage`
- 核心函数: `callModel()`, `isWithheldMaxOutputTokens()`, `isWithheldPromptTooLong()`

### 4.5 并行工具执行器
- 关键知识点: TrackedTool状态机、并发安全判断、调度规则、错误级联机制、结果产出顺序
- 源码对应: `src/services/tools/StreamingToolExecutor.ts`
- 核心类: `StreamingToolExecutor`
- 核心类型: `TrackedTool`, `ToolStatus`
- 核心方法: `addTool()`, `processQueue()`, `executeTool()`, `getCompletedResults()`, `discard()`

### 4.6 工具执行策略
- 关键知识点: 两种执行器对比（toolOrchestration vs StreamingToolExecutor）、partitionToolCalls分批逻辑、串行vs并发执行
- 源码对应: `src/services/tools/toolOrchestration.ts`, `src/services/tools/StreamingToolExecutor.ts`
- 核心函数: `runTools()`, `partitionToolCalls()`, `runToolsSerially()`, `runToolsConcurrently()`
- 核心常量: `MAX_TOOL_USE_CONCURRENCY` = 10

### 4.7 重试与错误处理
- 关键知识点: 指数退避算法、随机抖动、429 vs 529处理、模型回退机制、持久重试模式
- 源码对应: `src/services/api/withRetry.ts`
- 核心函数: `withRetry()`, `getRetryDelay()`, `shouldRetry()`
- 错误类型: `FallbackTriggeredError`, `CannotRetryError`, `APIUserAbortError`
- 核心常量: `BASE_DELAY_MS` = 500, `MAX_529_RETRIES` = 3, `PERSISTENT_MAX_BACKOFF_MS` = 5分钟

### 4.8 Token 计数与成本
- 关键知识点: 三种计数方式（粗估/精确/Haiku回退）、粗估算法、Usage组成、预算控制、Token告警状态
- 源码对应: `src/services/tokenEstimation.ts`, `src/QueryEngine.ts`
- 核心函数: `roughTokenCountEstimation()`, `countMessagesTokensWithAPI()`, `countTokensViaHaikuFallback()`, `checkTokenBudget()`
- 核心常量: `BYTES_PER_TOKEN` = 4, `BYTES_PER_TOKEN_JSON` = 2, `FLOOR_OUTPUT_TOKENS` = 3000

### 4.9 Thinking 模式
- 关键知识点: 三种Thinking模式（disabled/enabled/adaptive）、ThinkingConfig类型、模型支持矩阵、Ultrathink彩蛋
- 源码对应: `src/utils/thinking.ts`, `src/services/tokenEstimation.ts`
- 核心类型: `ThinkingConfig`
- 核心函数: `shouldEnableThinkingByDefault()`, `modelSupportsThinking()`, `modelSupportsAdaptiveThinking()`, `isUltrathinkEnabled()`
- 核心常量: `RAINBOW_COLORS`, `TOKEN_COUNT_THINKING_BUDGET`

### 4.10 协作全景
- 关键知识点: 系统全景架构、三种使用方式（REPL/SDK/CLI）、工具注册流程、Agent子系统、会话持久化、五大设计原则
- 源码对应: `src/QueryEngine.ts`, `src/query.ts`, `src/tools.ts`, `src/context.ts`
- 核心函数: `getAllBaseTools()`, `assembleToolPool()`, `recordTranscript()`, `ask()`

---

## 第五篇：权限系统

### 5.1 为什么需要权限控制
- 关键知识点: 三种权限行为、五种权限模式、十种决策原因类型、AI Agent三类风险
- 源码对应: `src/types/permissions.ts`, `src/utils/permissions/permissions.ts`
- 核心类型: `PermissionBehavior`, `ExternalPermissionMode`, `InternalPermissionMode`, `PermissionDecisionReason`
- 核心常量: `EXTERNAL_PERMISSION_MODES`

### 5.2 Default 模式
- 关键知识点: Default模式核心理念、hasPermissionsToUseTool执行流程、只读命令白名单、Accept Edits模式
- 源码对应: `src/utils/permissions/PermissionMode.ts`, `src/utils/permissions/permissions.ts`, `src/tools/BashTool/readOnlyValidation.ts`
- 核心常量: `PERMISSION_MODE_CONFIG`, `READONLY_COMMANDS`, `COMMAND_ALLOWLIST`, `ACCEPT_EDITS_ALLOWED_COMMANDS`

### 5.3 Auto 模式
- 关键知识点: Auto模式三层决策、安全工具白名单、YOLO分类器两阶段设计、XML解析、拒绝追踪机制
- 源码对应: `src/utils/permissions/classifierDecision.ts`, `src/utils/permissions/yoloClassifier.ts`, `src/utils/permissions/denialTracking.ts`
- 核心函数: `isAutoModeAllowlistedTool()`, `executeAsyncClassifierCheck()`, `buildTranscriptEntries()`, `parseXmlBlock()`
- 核心常量: `SAFE_YOLO_ALLOWLISTED_TOOLS`, `XML_S1_SUFFIX`, `XML_S2_SUFFIX`, `DENIAL_LIMITS`

### 5.4 Plan 模式
- 关键知识点: Plan模式核心理念、Plan + Bypass特殊组合、prePlanMode状态保存
- 源码对应: `src/utils/permissions/PermissionMode.ts`, `src/types/permissions.ts`
- 核心常量: `PAUSE_ICON`, `ENTER_PLAN_MODE_TOOL_NAME`, `EXIT_PLAN_MODE_TOOL_NAME`
- 核心工具: `EnterPlanModeTool`, `ExitPlanModeTool`

### 5.5 Bypass 模式
- 关键知识点: Bypass模式定位、三层安全底线、Bypass-Immune路径、远程禁用机制、危险权限清理
- 源码对应: `src/utils/permissions/PermissionMode.ts`, `src/utils/permissions/permissions.ts`, `src/utils/permissions/bypassPermissionsKillswitch.ts`, `src/utils/permissions/dangerousPatterns.ts`
- 核心常量: `DANGEROUS_BASH_PATTERNS`
- 核心函数: `checkAndDisableBypassPermissionsIfNeeded()`, `shouldDisableBypassPermissions()`

### 5.6 权限检查流水线
- 关键知识点: 权限检查流水线10步、短路机制、passthrough行为、权限建议系统
- 源码对应: `src/utils/permissions/permissions.ts`
- 核心函数: `hasPermissionsToUseTool()`, `hasPermissionsToUseToolInner()`, `createPermissionRequestMessage()`

### 5.7 规则系统
- 关键知识点: 规则三维度、七种规则来源优先级、行为优先级（Deny > Ask > Allow）、四种匹配模式
- 源码对应: `src/types/permissions.ts`, `src/utils/permissions/PermissionRule.ts`, `src/utils/permissions/permissions.ts`, `src/tools/BashTool/bashPermissions.ts`
- 核心类型: `PermissionRule`, `PermissionRuleSource`, `PermissionRuleValue`
- 核心函数: `matchingRulesForInput()`, `filterRulesByContentsMatchingInput()`, `syncPermissionRulesFromDisk()`
- 核心常量: `PERMISSION_RULE_SOURCES`, `RULE_SOURCES_IN_ORDER`

### 5.8 BashTool AST 分析
- 关键知识点: AST解析三种结果、危险结构检测、安全包装器剥离、复合命令安全检查、深度防御措施
- 源码对应: `src/utils/bash/ast.ts`, `src/tools/BashTool/bashPermissions.ts`, `src/tools/BashTool/readOnlyValidation.ts`, `src/tools/BashTool/bashSecurity.ts`
- 核心函数: `parseCommandRaw()`, `parseForSecurityFromAst()`, `bashToolHasPermission()`, `stripSafeWrappers()`, `checkSemantics()`
- 核心类型: `ParseForSecurityResult`, `SimpleCommand`
- 核心常量: `SAFE_WRAPPER_PATTERNS`, `SAFE_ENV_VARS`, `READONLY_COMMANDS`, `MAX_SUBCOMMANDS_FOR_SECURITY_CHECK` = 50

### 5.9 交互式权限
- 关键知识点: createResolveOnce竞争锁、四路赛跑架构、用户对话框处理、宽限期设计、投机执行
- 源码对应: `src/hooks/toolPermission/PermissionContext.ts`, `src/hooks/toolPermission/handlers/interactiveHandler.ts`, `src/hooks/useCanUseTool.tsx`
- 核心类型: `ResolveOnce<T>`
- 核心函数: `createResolveOnce()`, `handleInteractivePermission()`, `recheckPermission()`
- 核心常量: `GRACE_PERIOD_MS` = 200, `SPECULATIVE_TIMEOUT_MS` = 2000, `CHECKMARK_DISPLAY_MS` = 3000

### 5.10 安全设计原则
- 关键知识点: Fail-Closed原则、Defense-in-Depth纵深防御、Least Privilege最小权限、Separation of Concerns关注点分离、Auditability可审计性
- 源码对应: `src/types/permissions.ts`, `src/utils/permissions/permissions.ts`, `src/utils/permissions/PermissionMode.ts`, `src/utils/permissions/PermissionRule.ts`, `src/utils/permissions/yoloClassifier.ts`
- 核心概念: `Fail-Closed`, `Defense-in-Depth`, `Least Privilege`, `Separation of Concerns`, `Auditability`

---

## 第六篇：终端 UI

### 6.1 终端 UI 基础
- 关键知识点: 终端本质（字符网格）、ANSI转义码、声明式vs命令式、Ink渲染管线、双缓冲策略
- 源码对应: `ink/termio/dec.ts`, `ink/termio/csi.ts`, `ink/termio/sgr.ts`, `ink/renderer.ts`, `ink/components/App.tsx`
- 核心函数: `createRenderer()`, `renderNodeToOutput()`
- 核心常量: `HIDE_CURSOR`, `SHOW_CURSOR`

### 6.2 Ink 框架入门
- 关键知识点: Ink定位、Box组件、Text组件、自定义Reconciler、Yoga布局引擎、Ink DOM、事件系统
- 源码对应: `ink/reconciler.ts`, `ink/components/Box.tsx`, `ink/components/Text.tsx`, `ink/dom.ts`, `ink/components/App.tsx`
- 核心函数: `createReconciler()`, `createNode()`, `createTextNode()`, `applyProp()`, `setStyle()`
- 核心组件: `Box`, `Text`

### 6.3 双层 App 架构
- 关键知识点: 双层架构（业务层+基础设施层）、Provider洋葱模型、Context数据流、React Compiler优化
- 源码对应: `components/App.tsx`, `ink/components/App.tsx`, `components/design-system/ThemedText.tsx`, `components/design-system/ThemeProvider.tsx`
- 核心组件: `App`, `FpsMetricsProvider`, `StatsProvider`, `AppStateProvider`, `InkApp`
- 核心函数: `resolveColor()`, `getTheme()`

### 6.4 虚拟滚动优化
- 关键知识点: 虚拟滚动原理、三段式策略（估算/测量/缓存）、滚动量化、宽度变化处理、滑动步进
- 源码对应: `hooks/useVirtualScroll.ts`, `components/VirtualMessageList.tsx`
- 核心Hook: `useVirtualScroll()`
- 核心常量: `DEFAULT_ESTIMATE` = 3, `OVERSCAN_ROWS` = 80, `COLD_START_COUNT` = 30, `MAX_MOUNTED_ITEMS` = 300, `SLIDE_STEP` = 25, `SCROLL_QUANTUM`

### 6.5 输入框设计
- 关键知识点: 架构分层、Cursor类、双击安全机制、Kill Ring、波形光标、多行编辑
- 源码对应: `hooks/useTextInput.ts`, `components/TextInput.tsx`, `components/BaseTextInput.tsx`, `cursor/Cursor.ts`, `hooks/useDoublePress.ts`
- 核心Hook: `useTextInput()`, `useDoublePress()`
- 核心类: `Cursor`
- 核心常量: `BARS` = ' ▁▂▃▄▅▆▇█'

### 6.6 Vim 模式
- 关键知识点: VimState顶层状态、CommandState 11种子状态、核心类型（Operator/Motion/Text Object）、transition函数、Dot Repeat
- 源码对应: `vim/types.ts`, `vim/transitions.ts`, `vim/operators.ts`, `hooks/useVimInput.ts`
- 核心类型: `VimState`, `CommandState`, `Operator`, `RecordedChange`, `PersistentState`
- 核心函数: `transition()`, `fromIdle()`, `fromCount()`, `fromOperator()`, `executeOperatorMotion()`
- 核心常量: `OPERATORS`, `SIMPLE_MOTIONS`, `TEXT_OBJ_SCOPES`, `TEXT_OBJ_TYPES`, `MAX_VIM_COUNT` = 10000

### 6.7 Spinner 动画
- 关键知识点: 终端动画挑战、Spinner帧动画、共享时钟ClockContext、卡顿检测、减弱动效
- 源码对应: `components/Spinner/SpinnerGlyph.tsx`, `ink/hooks/use-animation-frame.ts`, `components/Spinner/utils.ts`
- 核心Hook: `useAnimationFrame()`
- 核心组件: `SpinnerGlyph`
- 核心常量: `DEFAULT_CHARACTERS`, `SPINNER_FRAMES`, `ERROR_RED`, `REDUCED_MOTION_DOT`, `REDUCED_MOTION_CYCLE_MS` = 2000

### 6.8 Diff 展示
- 关键知识点: Rust NAPI优势、StructuredDiff组件、WeakMap缓存、Gutter宽度计算、双列分割渲染
- 源码对应: `components/StructuredDiff.tsx`, `components/StructuredDiffFallback.tsx`, `napi-rs/`
- 核心组件: `StructuredDiff`, `StructuredDiffFallback`, `RawAnsi`, `NoSelect`
- 核心常量: `RENDER_CACHE`, `MAX_CACHE_VARIANTS` = 4

### 6.9 键盘绑定系统
- 关键知识点: 多上下文绑定、上下文优先级、resolveKey匹配、Chord组合键、平台适配
- 源码对应: `keybindings/defaultBindings.ts`, `keybindings/resolver.ts`, `keybindings/reservedShortcuts.ts`
- 核心函数: `resolveKey()`, `resolveChord()`, `buildKeystroke()`, `matchesBinding()`, `chordPrefixMatches()`
- 核心类型: `KeybindingBlock`, `ParsedBinding`, `ParsedKeystroke`, `ResolveResult`, `ChordResolveResult`
- 核心常量: `DEFAULT_BINDINGS`, `IMAGE_PASTE_KEY`, `MODE_CYCLE_KEY`

### 6.10 设计系统与主题
- 关键知识点: Theme类型结构、可用主题、颜色解析链、ThemedText优先级、自动主题检测
- 源码对应: `utils/theme.ts`, `components/design-system/ThemedText.tsx`, `components/design-system/ThemedBox.tsx`, `components/design-system/ThemeProvider.tsx`, `components/design-system/color.ts`
- 核心类型: `Theme`, `ThemeName`, `ThemeSetting`
- 核心函数: `getTheme()`, `resolveColor()`, `color()`, `useTheme()`
- 核心组件: `ThemeProvider`, `ThemedText`, `ThemedBox`, `Divider`, `StatusIcon`, `ProgressBar`, `LoadingState`, `ListItem`, `Tabs`, `Dialog`, `FuzzyPicker`, `Pane`

---

## 第七篇：状态管理

### 7.1 状态管理概念
- 关键知识点: 状态（State）概念、状态管理解决的三大问题（可追踪/可控制/可通知）、Claude Code三层状态架构、AppState核心类型
- 源码对应: `state/store.ts`, `state/AppStateStore.ts`, `state/onChangeAppState.ts`
- 核心类型: `Store<T>`, `createStore`, `AppState`, `DeepImmutable`, `Listener`, `OnChange<T>`
- 核心函数: `getState()`, `setState()`, `subscribe()`, `getDefaultAppState()`

### 7.2 createStore 极简 Store
- 关键知识点: 类型定义详解、闭包私有状态、setState核心逻辑、Object.is短路优化、subscribe模式
- 源码对应: `state/store.ts` (34行)
- 核心类型: `Store<T>`, `Listener`, `OnChange<T>`
- 核心函数: `createStore<T>()`, `getState()`, `setState(updater)`, `subscribe(listener)`

### 7.3 AppState 组织之道
- 关键知识点: AppState规模、DeepImmutable不可变类型、状态分域（核心/UI/权限/插件/协作/Bridge）、getDefaultAppState工厂函数
- 源码对应: `state/AppStateStore.ts` (570行)
- 核心类型: `AppState`, `DeepImmutable<T>`, `CompletionBoundary`, `SpeculationState`, `ModelSetting`, `SettingsJson`
- 核心函数: `getDefaultAppState()`, `getInitialSettings()`, `getEmptyToolPermissionContext()`, `shouldEnableThinkingByDefault()`

### 7.4 副作用同步
- 关键知识点: 副作用定义、收口设计vs分散式设计、onChangeAppState函数签名、副作用清单、双重检查、逆向同步
- 源码对应: `state/onChangeAppState.ts` (172行)
- 核心函数: `onChangeAppState()`, `externalMetadataToAppState()`, `toExternalPermissionMode()`, `notifySessionMetadataChanged()`

### 7.5 Memdir 记忆魔法
- 关键知识点: 为什么用文件系统、路径计算、Git仓库共享记忆、安全验证、MEMORY.md截断保护、scanMemoryFiles、记忆文件格式、findRelevantMemories智能召回
- 源码对应: `memdir/memdir.ts`, `memdir/paths.ts`, `memdir/memoryScan.ts`, `memdir/findRelevantMemories.ts`, `memdir/memoryAge.ts`
- 核心函数: `getAutoMemPath()`, `scanMemoryFiles()`, `findRelevantMemories()`, `truncateEntrypointContent()`, `memoryAgeDays()`
- 核心常量: `MAX_ENTRYPOINT_LINES` = 200, `MAX_ENTRYPOINT_BYTES` = 25_000, `MAX_MEMORY_FILES` = 200, `FRONTMATTER_MAX_LINES` = 30

### 7.6 四种记忆分类法
- 关键知识点: 四种记忆类型（user/feedback/project/reference）、何时存/如何用、什么不该存、Frontmatter格式、个人vs团队模式
- 源码对应: `memdir/memoryTypes.ts` (272行)
- 核心类型: `MEMORY_TYPES`, `MemoryType`
- 核心常量: `TYPES_SECTION_INDIVIDUAL`, `WHAT_NOT_TO_SAVE_SECTION`, `TRUSTING_RECALL_SECTION`, `MEMORY_FRONTMATTER_EXAMPLE`

### 7.7 History 会话历史
- 关键知识点: 存储位置（JSONL）、LogEntry数据结构、StoredPastedContent两种存储方式、写入流程（缓冲+延迟刷盘）、读取流程（反向读取）、撤销机制
- 源码对应: `history.ts` (465行)
- 核心类型: `LogEntry`, `StoredPastedContent`, `HistoryEntry`, `PastedContent`
- 核心函数: `addToHistory()`, `flushPromptHistory()`, `immediateFlushHistory()`, `makeLogEntryReader()`, `getHistory()`, `removeLastFromHistory()`
- 核心常量: `MAX_PASTED_CONTENT_LENGTH` = 1024, `MAX_HISTORY_ITEMS` = 100

### 7.8 Migrations 版本迁移
- 关键知识点: 为什么需要迁移、幂等的定义、迁移案例（模型别名/设置位置）、迁移版本号机制、迁移函数通用模板、容错设计
- 源码对应: `migrations/migrateFennecToOpus.ts`, `migrations/migrateSonnet45ToSonnet46.ts`, `migrations/migrateEnableAllProjectMcpServersToSettings.ts`, `utils/config.ts`
- 核心函数: `migrateFennecToOpus()`, `migrateSonnet45ToSonnet46()`, `migrateEnableAllProjectMcpServersToSettings()`, `getSettingsForSource()`, `updateSettingsForSource()`
- 核心常量: `CURRENT_MIGRATION_VERSION`, `migrationVersion`

### 7.9 持久化策略
- 关键知识点: 瞬态vs持久态、持久化决策树、三种写入时机（立即/延迟/退出前）、四种存储位置（GlobalConfig/Settings/Memdir/History）、不持久化的设计智慧
- 源码对应: `state/onChangeAppState.ts`, `utils/config.ts`, `history.ts`, `memdir/paths.ts`
- 核心函数: `saveGlobalConfig()`, `getGlobalConfig()`, `updateSettingsForSource()`, `registerCleanup()`

### 7.10 架构全景
- 关键知识点: 三层架构、数据流总览、各子系统关系矩阵、核心组件源码文件清单、5个可复用设计原则、架构中的精妙细节、架构局限性
- 源码对应: `state/store.ts`, `state/AppStateStore.ts`, `state/onChangeAppState.ts`, `memdir/`, `history.ts`, `migrations/`
- 核心概念: 最小必要Store、副作用收口、文件系统即数据库、分层持久化、幂等迁移链

---

## 第八篇：服务与集成

### 8.1 服务层概览
- 关键知识点: 服务层定位、六大核心模块职责、源码目录结构、API客户端核心代码、模块协作关系
- 源码对应: `services/api/client.ts`, `services/mcp/types.ts`, `services/lsp/LSPClient.ts`, `services/oauth/crypto.ts`, `services/analytics/index.ts`, `services/compact/`
- 核心函数: `getAnthropicClient()`, `generateCodeVerifier()`, `generateCodeChallenge()`, `logEvent()`

### 8.2 API 客户端封装
- 关键知识点: 工厂函数签名、四条分支路径（Direct/Bedrock/Foundry/Vertex）、通用配置、请求追踪、智能重试核心参数、指数退避+抖动算法、降级策略、持久重试模式
- 源码对应: `services/api/client.ts`, `services/api/withRetry.ts`
- 核心函数: `getAnthropicClient()`, `buildFetch()`, `withRetry()`, `getRetryDelay()`
- 核心常量: `DEFAULT_MAX_RETRIES` = 10, `BASE_DELAY_MS` = 500, `MAX_529_RETRIES` = 3, `PERSISTENT_MAX_BACKOFF_MS` = 5分钟
- 错误类: `FallbackTriggeredError`

### 8.3 错误分类与降级
- 关键知识点: 错误分诊函数、20+种错误分类表、用户友好的错误提示、场景感知的提示、SSL/TLS错误链遍历算法、Prompt-Too-Long Token解析
- 源码对应: `services/api/errors.ts`, `services/api/errorUtils.ts`
- 核心函数: `classifyAPIError()`, `getAssistantMessageFromError()`, `extractConnectionErrorDetails()`, `parsePromptTooLongTokenCounts()`, `getPromptTooLongTokenGap()`
- 核心常量: `SSL_ERROR_CODES`, `maxDepth` = 5

### 8.4 MCP 协议深入
- 关键知识点: MCP四大组件（Client/Server/Tool/Resource）、连接状态、八种服务器类型、七种配置作用域、配置优先级、安全策略（Allowlist/Denylist）、插件去重机制
- 源码对应: `services/mcp/types.ts`, `services/mcp/config.ts`
- 核心类型: `MCPServerConnection`, `McpServerConfigSchema`, `ConfigScopeSchema`
- 核心函数: `getClaudeCodeMcpConfigs()`, `getMcpServerSignature()`, `doesEnterpriseMcpConfigExist()`, `urlPatternToRegex()`

### 8.5 MCP 传输与工具发现
- 关键知识点: 五种传输方式（Stdio/SSE/HTTP/WebSocket/In-Process）、In-Process Transport双向消息传递、工具发现、工具名称规范化、环境变量展开
- 源码对应: `services/mcp/InProcessTransport.ts`, `services/mcp/mcpStringUtils.ts`, `services/mcp/config.ts`
- 核心类: `InProcessTransport`
- 核心函数: `createLinkedTransportPair()`, `buildMcpToolName()`, `expandEnvVars()`

### 8.6 LSP 集成
- 关键知识点: LSP角色定位、createLSPClient闭包模式、LSPServerManager多服务器路由、文件生命周期通知（didOpen/didChange/didSave/didClose）、优雅关闭
- 源码对应: `services/lsp/LSPClient.ts`, `services/lsp/LSPServerManager.ts`, `services/lsp/config.ts`
- 核心类型: `LSPClient`, `LSPServerManager`
- 核心函数: `createLSPClient()`, `createLSPServerManager()`, `getAllLspServers()`, `ensureServerStarted()`, `openFile()`, `changeFile()`, `closeFile()`

### 8.7 OAuth 2.0 + PKCE
- 关键知识点: OAuth流程、PKCE三个安全随机值（Verifier/Challenge/State）、Base64URL编码、令牌过期检查
- 源码对应: `services/oauth/crypto.ts`, `services/oauth/client.ts`, `services/oauth/auth-code-listener.ts`
- 核心函数: `generateCodeVerifier()`, `generateCodeChallenge()`, `generateState()`, `buildAuthUrl()`, `exchangeCodeForTokens()`, `refreshOAuthToken()`, `isOAuthTokenExpired()`
- 核心类: `AuthCodeListener`
- 核心常量: `bufferTime` = 5分钟

### 8.8 上下文压缩
- 关键知识点: 三层压缩体系（微压缩/自动压缩/完整压缩）、有效上下文窗口、自动压缩触发点、微压缩、自动压缩、完整压缩、Prompt-Too-Long自动恢复
- 源码对应: `services/compact/autoCompact.ts`, `services/compact/microCompact.ts`, `services/compact/prompt.ts`
- 核心函数: `getEffectiveContextWindowSize()`, `getAutoCompactThreshold()`, `shouldAutoCompact()`, `calculateTokenWarningState()`, `truncateHeadForPTLRetry()`
- 核心常量: `AUTOCOMPACT_BUFFER_TOKENS` = 13_000, `MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES` = 3, `POST_COMPACT_MAX_FILES_TO_RESTORE` = 5, `POST_COMPACT_TOKEN_BUDGET` = 50_000

### 8.9 特性标志与遥测
- 关键知识点: 事件日志设计理念（零依赖）、核心API、安全类型约束、GrowthBook三种读取模式、覆盖优先级、周期性刷新、Datadog日志上报、实验曝光记录
- 源码对应: `services/analytics/index.ts`, `services/analytics/datadog.ts`, `services/analytics/growthbook.ts`
- 核心函数: `logEvent()`, `logEventAsync()`, `stripProtoFields()`, `getFeatureValue_CACHED_MAY_BE_STALE()`, `setupPeriodicGrowthBookRefresh()`, `logExposureForFeature()`, `refreshGrowthBookAfterAuthChange()`
- 核心常量: `GROWTHBOOK_REFRESH_INTERVAL_MS` (6h/20min), `DEFAULT_FLUSH_INTERVAL_MS` = 15000, `MAX_BATCH_SIZE` = 100, `NETWORK_TIMEOUT_MS` = 5000

### 8.10 自动记忆提取
- 关键知识点: 自动记忆提取架构、初始化与闭包状态、工具权限控制、与主代理的互斥、提取提示词结构、Forked Agent模式、写入结果追踪
- 源码对应: `services/extractMemories/extractMemories.ts`, `services/extractMemories/prompts.ts`
- 核心函数: `initExtractMemories()`, `createAutoMemCanUseTool()`, `buildExtractAutoOnlyPrompt()`, `runForkedAgent()`, `extractWrittenPaths()`, `hasMemoryWritesSince()`
- 核心常量: `maxTurns` = 5, `timeoutMs` = 60_000

---

## 第九篇：Bridge 桥接

### 9.1 什么是 Bridge
- 关键知识点: Bridge功能、Bridge架构
- 源码对应: `src/bridge/bridgeMain.ts`, `src/bridge/bridgeApi.ts`, `src/bridge/sessionRunner.ts`

### 9.2 跨进程通信基础
- 关键知识点: 进程间通信概念、消息传递机制
- 源码对应: `src/bridge/bridgeMessaging.ts`, `src/bridge/replBridgeTransport.ts`

### 9.3 bridgeMain 主循环
- 关键知识点: bridgeMain.ts核心、退避配置
- 源码对应: `src/bridge/bridgeMain.ts`
- 核心常量: `DEFAULT_BACKOFF`, `STATUS_UPDATE_INTERVAL_MS` = 1000, `SPAWN_SESSIONS_DEFAULT` = 32

### 9.4 消息协议设计
- 关键知识点: 消息格式、序列化与反序列化
- 源码对应: `src/bridge/types.ts`, `src/bridge/bridgeMessaging.ts`

### 9.5 BoundedUUIDSet
- 关键知识点: 有限UUID集合、去重机制
- 源码对应: `src/bridge/boundedUUIDSet.ts`

### 9.6 JWT 认证
- 关键知识点: JWT令牌、认证流程
- 源码对应: `src/bridge/jwtUtils.ts`, `src/bridge/trustedDevice.ts`

### 9.7 sessionRunner 会话管理
- 关键知识点: 会话生命周期、会话创建与销毁
- 源码对应: `src/bridge/sessionRunner.ts`, `src/bridge/createSession.ts`

### 9.8 传输层抽象
- 关键知识点: 传输层接口、多种传输实现
- 源码对应: `src/bridge/replBridgeTransport.ts`, `src/bridge/pollConfig.ts`

### 9.9 IDE 集成实践
- 关键知识点: VS Code集成、JetBrains集成
- 源码对应: `src/bridge/replBridge.ts`, `src/services/mcp/vscodeSdkMcp.ts`

### 9.10 Bridge 架构总结
- 关键知识点: Bridge完整架构、性能优化、安全考虑
- 源码对应: `src/bridge/` 目录全部文件

---

## 第十篇：多 Agent 协作

### 10.1 什么是多 Agent 系统
- 关键知识点: 单Agent vs 多Agent、多Agent系统优势
- 源码对应: `src/tools/AgentTool/AgentTool.tsx`, `src/coordinator/coordinatorMode.ts`

### 10.2 AgentTool 源码解析
- 关键知识点: AgentTool定义、关键特性、输入Schema
- 源码对应: `src/tools/AgentTool/AgentTool.tsx`
- 核心常量: `baseInputSchema`, `fullInputSchema`

### 10.3 Agent 类型详解
- 关键知识点: 内置Agent类型、一次性Agent优化
- 源码对应: `src/tools/AgentTool/builtInAgents.ts`
- 核心常量: `ONE_SHOT_BUILTIN_AGENT_TYPES`

### 10.4 沙箱隔离
- 关键知识点: Worktree隔离、工具权限隔离
- 源码对应: `src/utils/worktree.ts`, `src/constants/tools.ts`

### 10.5 TeamCreateTool
- 关键知识点: 团队架构、TeamContext
- 源码对应: `src/tools/TeamCreateTool/TeamCreateTool.ts`, `src/state/AppStateStore.ts`
- 核心类型: `teamContext`

### 10.6 SendMessageTool
- 关键知识点: 代理间通信、消息路由
- 源码对应: `src/tools/SendMessageTool/SendMessageTool.ts`

### 10.7 消息路由模式
- 关键知识点: 消息路由机制、代理名称注册
- 源码对应: `src/state/AppStateStore.ts`
- 核心类型: `agentNameRegistry`

### 10.8 Coordinator 编排
- 关键知识点: 协调器模式、Coordinator允许的工具
- 源码对应: `src/coordinator/coordinatorMode.ts`, `src/constants/tools.ts`
- 核心函数: `isCoordinatorMode()`, `getCoordinatorUserContext()`
- 核心常量: `COORDINATOR_MODE_ALLOWED_TOOLS`

### 10.9 Swarm vs Coordinator
- 关键知识点: Swarm模式、Coordinator模式、对比分析
- 源码对应: `src/tools/AgentTool/AgentTool.tsx`, `src/coordinator/coordinatorMode.ts`

### 10.10 实战设计
- 关键知识点: 设计自己的多Agent系统、最佳实践
- 源码对应: 综合参考 `src/tools/AgentTool/`, `src/coordinator/`

---

## 第十一篇：性能优化

### 11.1 为什么性能重要
- 关键知识点: 性能对用户体验的影响、Claude Code性能目标
- 源码对应: `src/main.tsx` (启动优化), `src/query.ts` (运行时优化)

### 11.2 并行预取
- 关键知识点: 启动时并行预取、查询级预取
- 源码对应: `src/main.tsx`, `src/query.ts`, `src/commands.ts`
- 核心函数: `startMdmRawRead()`, `startKeychainPrefetch()`, `startRelevantMemoryPrefetch()`

### 11.3 懒加载策略
- 关键知识点: 动态导入、条件加载、feature()门控
- 源码对应: `src/tools.ts`, `src/commands.ts`, `src/main.tsx`
- 核心技术: `await import()`, `feature('XXX')`

### 11.4 死代码消除
- 关键知识点: Bun打包优化、条件require、编译时代码消除
- 源码对应: `src/tools.ts`, `src/commands.ts`
- 核心模式: `feature('X') ? require('./X.js') : null`

### 11.5 条件 Require
- 关键知识点: 运行时条件加载、环境变量控制
- 源码对应: `src/tools.ts`
- 核心模式: `process.env.X ? require('./X.js') : null`

### 11.6 上下文压缩算法
- 关键知识点: 三层压缩体系、Token阈值计算
- 源码对应: `services/compact/autoCompact.ts`, `services/compact/microCompact.ts`
- 核心函数: `shouldAutoCompact()`, `microcompact()`

### 11.7 Prompt 缓存优化
- 关键知识点: Prompt Cache稳定性、工具排序
- 源码对应: `src/tools.ts`
- 核心函数: `assembleToolPool()`

### 11.8 React 渲染优化
- 关键知识点: 虚拟滚动、滚动量化、React Compiler优化
- 源码对应: `hooks/useVirtualScroll.ts`, `components/VirtualMessageList.tsx`
- 核心Hook: `useVirtualScroll()`

### 11.9 流式处理
- 关键知识点: 流式响应、流式工具执行
- 源码对应: `src/query.ts`, `src/services/tools/StreamingToolExecutor.ts`
- 核心类: `StreamingToolExecutor`

### 11.10 优化检查清单
- 关键知识点: 启动优化、运行时优化、内存优化、渲染优化
- 源码对应: 综合所有优化相关文件

---

## 第十二篇：亮点总结

### 12.1 超级工具箱
- 关键知识点: 40+工具分类、工具系统设计亮点
- 源码对应: `src/tools.ts`, `src/Tool.ts`, `src/tools/`

### 12.2 多代理军团
- 关键知识点: Agent Swarm架构、Coordinator模式
- 源码对应: `src/tools/AgentTool/`, `src/coordinator/`

### 12.3 三层安全锁
- 关键知识点: 权限系统分层、Fail-Closed设计
- 源码对应: `src/utils/permissions/`

### 12.4 极速启动
- 关键知识点: 并行预取、懒加载、死代码消除
- 源码对应: `src/main.tsx`, `src/tools.ts`, `src/commands.ts`

### 12.5 记忆压缩术
- 关键知识点: 三层压缩体系、上下文管理
- 源码对应: `services/compact/`

### 12.6 终端魔法屏
- 关键知识点: React/Ink、虚拟滚动、设计系统
- 源码对应: `src/components/`, `src/ink/`

### 12.7 永不遗忘
- 关键知识点: Memdir记忆系统、四种记忆类型
- 源码对应: `memdir/`

### 12.8 双向传送门
- 关键知识点: Bridge桥接系统、IDE集成
- 源码对应: `src/bridge/`

### 12.9 百宝袋
- 关键知识点: MCP协议、插件系统、外部工具集成
- 源码对应: `services/mcp/`, `services/plugins/`

### 12.10 王者对决
- 关键知识点: Claude Code vs 其他AI编程工具
- 源码对应: 综合对比

---

## 附录

### 源码文件索引
- 关键知识点: 完整源码文件索引、按功能分类
- 源码对应: 全书所有涉及的源码文件

### 推荐阅读
- 关键知识点: 延伸阅读资源、相关技术文档
- 源码对应: 无

---

*本大纲由 Claude Code 根据所有 *_detail.md 细纲文件汇总生成*
*生成时间: 2026/04/07*
