# 第四课：极速启动 —— 性能优化黑科技全解 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第四课：极速启动 —— 性能优化黑科技全解

### 1.2 二级标题
- 学习目标
- 一、生活类比：快餐店 vs 大酒店
- 二、特性标志：编译时剪枝
- 三、lazySchema：延迟模式定义
- 四、memoize：缓存计算结果
- 五、提示缓存稳定性
- 六、并行加载
- 七、条件工具加载
- 八、嵌入式搜索工具
- 九、性能优化全景图
- 十、动手练习
- 十一、本课小结
- 下节预告

### 1.3 三级标题
- 2.1 bun:bundle 特性标志
- 2.2 Dead Code Elimination（死代码消除）
- 2.3 环境变量条件加载
- 3.1 问题：Schema 定义的开销
- 3.2 解决方案：lazySchema
- 4.1 技能加载的缓存
- 4.2 文件状态缓存
- 5.1 问题：缓存失效
- 5.2 解决方案：排序分区
- 6.1 技能并行发现
- 6.2 文件身份去重
- 7.1 简单模式
- 7.2 REPL 模式过滤

---

## 2. 关键知识点

### 2.1 Bun feature() 特性标志
- `import { feature } from 'bun:bundle'`
- 编译时决定代码包含与否
- 未启用的功能编译时移除

### 2.2 常见 Feature Flag
| 标志 | 控制的功能 |
|------|-----------|
| `COORDINATOR_MODE` | 协调者模式 |
| `PROACTIVE` | 主动行为 |
| `KAIROS` | 助手模式 |
| `AGENT_TRIGGERS` | 代理触发器 |
| `TERMINAL_PANEL` | 终端面板 |
| `HISTORY_SNIP` | 历史裁剪 |
| `CONTEXT_COLLAPSE` | 上下文折叠 |
| `WEB_BROWSER_TOOL` | 网页浏览器 |
| `OVERFLOW_TEST_TOOL` | 溢出测试 |
| `WORKFLOW_SCRIPTS` | 工作流脚本 |

### 2.3 lazySchema 原理
- 首次调用时才创建 Schema 对象
- 之后使用缓存
- 启动时零开销

### 2.4 memoize 缓存
- 加载技能文件涉及文件系统操作
- 用 `memoize` 缓存避免重复加载
- 需要清除缓存时：`getSkillDirCommands.cache?.clear?.()`

### 2.5 提示缓存稳定性
- 内置工具排在前面作为连续前缀
- MCP 工具排在后面
- 各自按名称排序
- `uniqBy` 保留插入顺序，内置工具同名优先

### 2.6 并行加载
- `Promise.all` 同时加载多个来源
- `realpath` 解析符号链接去重

---

## 3. 涉及的源码文件路径

### 3.1 核心源码文件
- `tools.ts` - feature flag、工具池组装、lazySchema
- `skills/loadSkillsDir.ts` - 技能并行加载、memoize
- `main.tsx` - 内容 hash 生成临时文件路径

---

## 4. 类名、函数名、接口名

### 4.1 函数
- `feature(flag: string)` - Bun 特性标志
- `lazySchema<T>(factory: () => T)` - 延迟 Schema 创建
- `memoize(fn)` - 函数结果缓存
- `getSkillDirCommands(cwd: string)` - 获取技能目录命令
- `clearSkillCaches()` - 清除技能缓存
- `assembleToolPool(permissionContext, mcpTools)` - 组装工具池
- `generateTempFilePath(prefix, ext, options)` - 生成临时文件路径
- `loadSkillsFromSkillsDir(dir, source)` - 从技能目录加载技能
- `getFileIdentity(filePath)` - 获取文件身份（realpath）
- `isEnvTruthy(env)` - 环境变量检测
- `hasEmbeddedSearchTools()` - 是否有嵌入式搜索工具
- `isReplModeEnabled()` - REPL 模式是否启用

### 4.2 常量
- `BUILTIN_PLUGINS` - 内置插件映射

### 4.3 类型/接口
- `Tools` - 工具数组类型
- `ToolPermissionContext` - 工具权限上下文

---

## 5. 代码片段重点

### 5.1 feature() 导入与使用（tools.ts）
```typescript
import { feature } from 'bun:bundle';

const SleepTool =
  feature('PROACTIVE') || feature('KAIROS')
    ? require('./tools/SleepTool/SleepTool.js').SleepTool
    : null;
```

### 5.2 lazySchema 使用（AgentTool.tsx）
```typescript
const baseInputSchema = lazySchema(() => z.object({
  description: z.string()
    .describe('A short (3-5 word) description of the task'),
  prompt: z.string()
    .describe('The task for the agent to perform'),
  subagent_type: z.string().optional()
    .describe('The type of specialized agent to use'),
  model: z.enum(['sonnet', 'opus', 'haiku']).optional(),
  run_in_background: z.boolean().optional()
}));
```

### 5.3 memoize 缓存技能加载（loadSkillsDir.ts）
```typescript
import memoize from 'lodash-es/memoize.js';

export const getSkillDirCommands = memoize(
  async (cwd: string): Promise<Command[]> => {
    const [managedSkills, userSkills, projectSkills, ...] =
      await Promise.all([...]);
    return deduplicatedSkills;
  }
);

export function clearSkillCaches() {
  getSkillDirCommands.cache?.clear?.();
}
```

### 5.4 提示缓存稳定性（tools.ts）
```typescript
export function assembleToolPool(
  permissionContext: ToolPermissionContext,
  mcpTools: Tools,
): Tools {
  const builtInTools = getTools(permissionContext);
  const allowedMcpTools = filterToolsByDenyRules(mcpTools, permissionContext);

  const byName = (a: Tool, b: Tool) => a.name.localeCompare(b.name);
  return uniqBy(
    [...builtInTools].sort(byName)
      .concat(allowedMcpTools.sort(byName)),
    'name',
  );
}
```

### 5.5 技能并行加载（loadSkillsDir.ts）
```typescript
const [
  managedSkills,
  userSkills,
  projectSkillsNested,
  additionalSkillsNested,
  legacyCommands,
] = await Promise.all([
  loadSkillsFromSkillsDir(managedSkillsDir, 'policySettings'),
  loadSkillsFromSkillsDir(userSkillsDir, 'userSettings'),
  Promise.all(
    projectSkillsDirs.map(dir =>
      loadSkillsFromSkillsDir(dir, 'projectSettings'))
  ),
  Promise.all(
    additionalDirs.map(dir =>
      loadSkillsFromSkillsDir(join(dir, '.claude', 'skills'), ...))
  ),
  loadSkillsFromCommandsDir(cwd),
]);
```

### 5.6 文件身份去重（loadSkillsDir.ts）
```typescript
async function getFileIdentity(filePath: string): Promise<string | null> {
  try {
    return await realpath(filePath);
  } catch {
    return null;
  }
}
```

### 5.7 简单模式（tools.ts）
```typescript
if (isEnvTruthy(process.env.CLAUDE_CODE_SIMPLE)) {
  const simpleTools: Tool[] = [BashTool, FileReadTool, FileEditTool];
  return filterToolsByDenyRules(simpleTools, permissionContext);
}
```

### 5.8 嵌入式搜索工具（tools.ts）
```typescript
...(hasEmbeddedSearchTools()
  ? []
  : [GlobTool, GrepTool]),
```
