# 第九课：百宝袋 —— 插件与技能扩展机制 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第九课：百宝袋 —— 插件与技能扩展机制

### 1.2 二级标题
- 学习目标
- 一、生活类比：手机的 App 生态
- 二、Skills（技能）系统
- 三、技能发现机制
- 四、技能创建命令
- 五、Plugins（插件）系统
- 六、MCP 技能集成
- 七、SkillTool：技能调用工具
- 八、技能的高级特性
- 九、动手练习
- 十、本课小结
- 下节预告

### 1.3 三级标题
- 2.1 什么是技能？
- 2.2 SKILL.md 格式
- 2.3 Frontmatter 字段详解
- 3.1 五层发现源
- 3.2 去重机制
- 3.3 动态技能发现
- 3.4 条件技能激活
- 4.1 createSkillCommand
- 4.2 变量替换
- 5.1 内置插件
- 5.2 插件 vs 技能
- 5.3 内置插件管理
- 5.4 插件提供的技能
- 6.1 从 MCP 服务器发现技能
- 6.2 安全限制
- 7.1 SkillTool 是什么？
- 7.2 调用流程
- 8.1 条件路径激活
- 8.2 Fork 执行上下文
- 8.3 指定模型
- 8.4 关联钩子

---

## 2. 关键知识点

### 2.1 扩展三件套
- **Skills** - Markdown 定义的可复用任务模板
- **Plugins** - 多组件功能包（技能+钩子+MCP）
- **MCP** - 从远程 MCP 服务器发现的技能

### 2.2 SKILL.md Frontmatter 字段
| 字段 | 作用 | 示例 |
|------|------|------|
| `name` | 技能名称 | `deploy` |
| `description` | 描述 | `部署到生产环境` |
| `when_to_use` | AI 何时自动使用 | `当用户要求部署时` |
| `allowed-tools` | 允许的工具及参数 | `Bash(npm run *)` |
| `arguments` | 接受的参数 | `environment` |
| `user-invocable` | 用户能否用 `/skill` 调用 | `true` |
| `model` | 使用哪个模型 | `haiku` |
| `paths` | 条件激活路径 | `src/deploy/**` |
| `context` | 执行上下文 | `fork` |

### 2.3 五层技能发现源
1. 管理员技能（policySettings）
2. 用户技能（~/.claude/skills/）
3. 项目技能（.claude/skills/）
4. 额外目录（--add-dir）
5. 遗留命令（.claude/commands/）

### 2.4 技能 vs 插件
| 维度 | 技能（Skill） | 插件（Plugin） |
|------|---------------|----------------|
| 格式 | Markdown 文件 | 代码包 |
| 复杂度 | 简单流程 | 复杂功能 |
| 组成 | 单个 SKILL.md | 技能 + 钩子 + MCP |
| 管理 | 文件系统 | /plugin UI 开关 |
| ID 格式 | 名称 | `name@builtin` |

### 2.5 变量替换
| 变量 | 含义 | 示例 |
|------|------|------|
| `${1}` / `${environment}` | 用户传入的参数 | `production` |
| `${CLAUDE_SKILL_DIR}` | 技能所在目录 | `/path/to/skill/` |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID | `abc123` |

### 2.6 MCP 技能安全限制
- MCP 技能是远程和不受信任的
- 不执行内嵌 Shell 命令

---

## 3. 涉及的源码文件路径

### 3.1 技能系统
- `skills/loadSkillsDir.ts` - 技能加载
- `skills/mcpSkillBuilders.ts` - MCP 技能构建

### 3.2 插件系统
- `plugins/builtinPlugins.ts` - 内置插件

### 3.3 技能工具
- `tools/SkillTool/SkillTool.js` - 技能调用工具

---

## 4. 类名、函数名、接口名

### 4.1 函数
- `getSkillDirCommands(cwd: string)` - 获取技能目录命令
- `loadSkillsFromSkillsDir(dir, source)` - 从技能目录加载技能
- `discoverSkillDirsForPaths(filePaths, cwd)` - 动态发现技能目录
- `activateConditionalSkillsForPaths(filePaths, cwd)` - 激活条件技能
- `createSkillCommand(options)` - 创建技能命令
- `substituteArguments(content, args, ...)` - 替换参数
- `executeShellCommandsInPrompt(...)` - 执行提示中的 Shell 命令
- `registerBuiltinPlugin(definition)` - 注册内置插件
- `getBuiltinPlugins()` - 获取内置插件
- `getBuiltinPluginSkillCommands()` - 获取内置插件技能命令
- `registerMCPSkillBuilders(builders)` - 注册 MCP 技能构建器
- `skillDefinitionToCommand(skill)` - 技能定义转命令
- `parseSkillFrontmatterFields(frontmatter, markdownContent, resolvedName)` - 解析技能 frontmatter

### 4.2 常量
- `BUILTIN_PLUGINS` - 内置插件映射
- `managedSkillsDir` - 管理技能目录
- `userSkillsDir` - 用户技能目录
- `projectSkillsDirs` - 项目技能目录

### 4.3 类型/接口
- `SkillFrontmatter` - 技能 frontmatter
- `Command` - 命令类型
- `BuiltinPluginDefinition` - 内置插件定义
- `LoadedPlugin` - 已加载插件

---

## 5. 代码片段重点

### 5.1 SKILL.md 格式示例
```markdown
---
name: deploy
description: 部署应用到生产环境
when_to_use: 当用户要求部署或发布时
allowed-tools:
  - Bash(npm run build)
  - Bash(aws s3 sync *)
  - Bash(aws cloudfront create-invalidation *)
argument-hint: "[环境名称]"
arguments:
  - environment
---

# 部署流程

1. 运行构建: `npm run build`
2. 上传到 S3: `aws s3 sync dist/ s3://my-bucket/${environment}/`
3. 清除 CDN 缓存
4. 验证部署
```

### 5.2 技能并行加载（loadSkillsDir.ts）
```typescript
export const getSkillDirCommands = memoize(
  async (cwd: string): Promise<Command[]> => {
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
      // ...
    ]);

    return deduplicatedSkills;
  }
);
```

### 5.3 动态技能发现（loadSkillsDir.ts）
```typescript
export async function discoverSkillDirsForPaths(
  filePaths: string[],
  cwd: string,
): Promise<string[]> {
  for (const filePath of filePaths) {
    let currentDir = dirname(filePath);
    while (currentDir.startsWith(resolvedCwd + pathSep)) {
      const skillDir = join(currentDir, '.claude', 'skills');
      // 检查目录是否存在
      // 检查是否被 gitignore
      // 如果存在且未忽略，加入发现列表
    }
  }
}
```

### 5.4 条件技能激活（loadSkillsDir.ts）
```typescript
export function activateConditionalSkillsForPaths(
  filePaths: string[],
  cwd: string,
): string[] {
  for (const [name, skill] of conditionalSkills) {
    const skillIgnore = ignore().add(skill.paths);
    for (const filePath of filePaths) {
      if (skillIgnore.ignores(relativePath)) {
        dynamicSkills.set(name, skill);
        conditionalSkills.delete(name);
      }
    }
  }
}
```

### 5.5 创建技能命令（loadSkillsDir.ts）
```typescript
export function createSkillCommand({
  skillName,
  markdownContent,
  allowedTools,
  ...
}): Command {
  return {
    type: 'prompt',
    name: skillName,
    description,
    allowedTools,
    async getPromptForCommand(args, toolUseContext) {
      let finalContent = markdownContent;

      finalContent = substituteArguments(finalContent, args, ...);
      finalContent = finalContent.replace(
        /\${CLAUDE_SKILL_DIR}/g, skillDir
      );
      finalContent = finalContent.replace(
        /\${CLAUDE_SESSION_ID}/g, getSessionId()
      );

      if (loadedFrom !== 'mcp') {
        finalContent = await executeShellCommandsInPrompt(...);
      }

      return [{ type: 'text', text: finalContent }];
    }
  };
}
```

### 5.6 内置插件管理（builtinPlugins.ts）
```typescript
const BUILTIN_PLUGINS: Map<string, BuiltinPluginDefinition> = new Map();

export function registerBuiltinPlugin(
  definition: BuiltinPluginDefinition,
): void {
  BUILTIN_PLUGINS.set(definition.name, definition);
}

export function getBuiltinPlugins(): {
  enabled: LoadedPlugin[]
  disabled: LoadedPlugin[]
} {
  const settings = getSettings_DEPRECATED();
  for (const [name, definition] of BUILTIN_PLUGINS) {
    if (definition.isAvailable && !definition.isAvailable()) continue;

    const userSetting = settings?.enabledPlugins?.[pluginId];
    const isEnabled = userSetting !== undefined
      ? userSetting === true
      : (definition.defaultEnabled ?? true);

    // 分类到 enabled 或 disabled
  }
}
```

### 5.7 MCP 技能安全限制（loadSkillsDir.ts）
```typescript
// MCP 技能是远程和不受信任的
// 不执行内嵌 Shell 命令
if (loadedFrom !== 'mcp') {
  finalContent = await executeShellCommandsInPrompt(...);
}
```
