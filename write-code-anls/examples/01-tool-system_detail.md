# 第一课：超级工具箱 —— 40 种开发工具详解 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第一课：超级工具箱 —— 40 种开发工具详解

### 1.2 二级标题
- 学习目标
- 一、生活类比：你的瑞士军刀
- 二、工具的"身份证"：Tool 接口
- 三、工具注册中心：tools.ts
- 四、40+ 工具大全分类
- 五、工具池组装：三步合一
- 六、工具构建器：buildTool 工厂
- 七、工具搜索：ToolSearch 延迟加载
- 八、动手练习
- 九、本课小结
- 下节预告

### 1.3 三级标题
- 关键字段解读
- 工具的条件加载
- 4.1 文件操作类（"手术刀系列"）
- 4.2 命令执行类（"发动机系列"）
- 4.3 代理协作类（"通讯系列"）
- 4.4 信息获取类（"望远镜系列"）
- 4.5 计划与管理类（"指挥系列"）
- 4.6 扩展与集成类（"插件系列"）
- 为什么这么设计？
- 设计哲学：安全关闭原则（Fail-Closed）

---

## 2. 关键知识点

### 2.1 Tool 接口核心字段
| 字段 | 作用 | 生活类比 |
|------|------|----------|
| `name` | 工具唯一标识 | 工具上的品牌标签 |
| `isReadOnly` | 是否只是"看"不"改" | 卷尺只看不改 |
| `isDestructive` | 操作能否撤销 | 拆墙不可逆 |
| `isConcurrencySafe` | 能否多个同时用 | 两把卷尺可以同时量 |
| `checkPermissions` | 使用前安全检查 | 签安全协议 |
| `maxResultSizeChars` | 结果大小限制 | 报告太长存文件 |

### 2.2 工具分类（40+ 工具）
- **文件操作类**：FileReadTool、FileEditTool、FileWriteTool、GlobTool、GrepTool、NotebookEditTool
- **命令执行类**：BashTool、PowerShellTool、REPLTool
- **代理协作类**：AgentTool、TaskOutputTool、TaskStopTool、SendMessageTool、TeamCreateTool、TeamDeleteTool
- **信息获取类**：WebFetchTool、WebSearchTool、LSPTool、ToolSearchTool
- **计划与管理类**：EnterPlanModeTool、ExitPlanModeV2Tool、TodoWriteTool、TaskCreateTool、TaskGetTool、TaskUpdateTool、TaskListTool
- **扩展与集成类**：SkillTool、ListMcpResourcesTool、ReadMcpResourceTool、ConfigTool

### 2.3 工具池组装流程
1. `getAllBaseTools()` - 获取 40+ 内置工具
2. `getTools()` - 权限过滤
3. `filterToolsByDenyRules()` - Deny 规则过滤
4. `isEnabled` 过滤
5. `assembleToolPool()` - 合并内置 + MCP 工具，去重排序

### 2.4 安全关闭原则（Fail-Closed）
| 默认值 | 含义 | 安全策略 |
|--------|------|----------|
| `isConcurrencySafe = false` | 默认不并行 | 防止竞态条件 |
| `isReadOnly = false` | 默认假设写入 | 需要更严格的权限 |
| `isDestructive = false` | 默认非破坏性 | 特殊工具需主动声明 |

### 2.5 ToolSearch 延迟加载
- 当工具太多时，延迟加载工具描述
- `isToolSearchEnabledOptimistic()` 判断是否启用
- `searchHint` 字段帮助搜索匹配

---

## 3. 涉及的源码文件路径

### 3.1 核心源码文件
- `Tool.ts` - Tool 接口定义、buildTool 工厂
- `tools.ts` - 工具注册中心、工具池组装
- `tools/AgentTool/AgentTool.tsx` - AgentTool 定义
- `tools/BashTool/BashTool.ts` - BashTool 定义
- `tools/FileReadTool/FileReadTool.ts` - FileReadTool 定义
- `tools/FileEditTool/FileEditTool.ts` - FileEditTool 定义
- `tools/GlobTool/GlobTool.ts` - GlobTool 定义
- `tools/GrepTool/GrepTool.ts` - GrepTool 定义

### 3.2 相关工具
- `utils/permissions/permissions.ts` - 权限过滤

---

## 4. 类名、函数名、接口名

### 4.1 类型/接口
- `Tool<Input, Output, P>` - 工具接口
- `ToolPermissionContext` - 工具权限上下文
- `PermissionResult` - 权限结果
- `Tools` - 工具数组类型
- `Command` - 命令类型

### 4.2 函数
- `buildTool<D extends AnyToolDef>(def: D)` - 工具构建工厂
- `getAllBaseTools()` - 获取所有基础工具
- `getTools(permissionContext: ToolPermissionContext)` - 获取工具（带权限过滤）
- `assembleToolPool(permissionContext, mcpTools)` - 组装工具池
- `filterToolsByDenyRules(tools, permissionContext)` - Deny 规则过滤
- `isToolSearchEnabledOptimistic()` - 工具搜索是否启用
- `isWorktreeModeEnabled()` - Worktree 模式是否启用
- `isAgentSwarmsEnabled()` - Agent Swarm 模式是否启用

### 4.3 常量
- `TOOL_DEFAULTS` - 工具默认值
- `BUILTIN_TOOLS` - 内置工具集合
- `SLEEP_TOOL_NAME` - Sleep 工具名称
- `AGENT_TOOL_NAME` - Agent 工具名称
- `BASH_TOOL_NAME` - Bash 工具名称
- `FILE_READ_TOOL_NAME` - 文件读取工具名称
- `FILE_EDIT_TOOL_NAME` - 文件编辑工具名称

---

## 5. 代码片段重点

### 5.1 Tool 接口定义（Tool.ts）
```typescript
export type Tool<Input, Output, P> = {
  name: string;
  description(input): string;
  inputSchema: Input;
  call(args, context): Result;
  isEnabled(): boolean;
  isReadOnly(input): boolean;
  isDestructive?(input): boolean;
  isConcurrencySafe(input): boolean;
  checkPermissions(input, ctx): PermissionResult;
  maxResultSizeChars: number;
};
```

### 5.2 工具注册（tools.ts）
```typescript
export function getAllBaseTools(): Tools {
  return [
    AgentTool,
    TaskOutputTool,
    BashTool,
    GlobTool,
    GrepTool,
    FileReadTool,
    FileEditTool,
    FileWriteTool,
    NotebookEditTool,
    WebFetchTool,
    TodoWriteTool,
    WebSearchTool,
    TaskStopTool,
    AskUserQuestionTool,
    SkillTool,
    EnterPlanModeTool,
    // ... 更多条件加载的工具
  ];
}
```

### 5.3 工具条件加载（tools.ts）
```typescript
const SleepTool =
  feature('PROACTIVE') || feature('KAIROS')
    ? require('./tools/SleepTool/SleepTool.js').SleepTool
    : null;

...(isWorktreeModeEnabled()
  ? [EnterWorktreeTool, ExitWorktreeTool] : []),

...(isAgentSwarmsEnabled()
  ? [getTeamCreateTool(), getTeamDeleteTool()] : []),
```

### 5.4 工具池组装（tools.ts）
```typescript
export function assembleToolPool(
  permissionContext: ToolPermissionContext,
  mcpTools: Tools,
): Tools {
  const builtInTools = getTools(permissionContext);
  const allowedMcpTools = filterToolsByDenyRules(mcpTools, permissionContext);

  const byName = (a: Tool, b: Tool) => a.name.localeCompare(b.name);
  return uniqBy(
    [...builtInTools].sort(byName).concat(allowedMcpTools.sort(byName)),
    'name',
  );
}
```

### 5.5 buildTool 工厂（Tool.ts）
```typescript
const TOOL_DEFAULTS = {
  isEnabled: () => true,
  isConcurrencySafe: () => false,
  isReadOnly: () => false,
  isDestructive: () => false,
  checkPermissions: (input) =>
    Promise.resolve({ behavior: 'allow', updatedInput: input }),
  toAutoClassifierInput: () => '',
};

export function buildTool<D extends AnyToolDef>(def: D): BuiltTool<D> {
  return {
    ...TOOL_DEFAULTS,
    userFacingName: () => def.name,
    ...def,
  };
}
```

### 5.6 工具搜索条件加载（tools.ts）
```typescript
...(isToolSearchEnabledOptimistic()
  ? [ToolSearchTool] : []),
```
