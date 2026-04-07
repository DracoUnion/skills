# 第七课：永不遗忘 —— 自动记忆系统原理 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第七课：永不遗忘 —— 自动记忆系统原理

### 1.2 二级标题
- 学习目标
- 一、生活类比：你的个人笔记系统
- 二、记忆目录结构
- 三、四种记忆类型
- 四、记忆文件格式
- 五、记忆的保存流程
- 六、记忆的加载与注入
- 七、记忆搜索与召回
- 八、团队记忆
- 九、KAIROS 模式：日志式记忆
- 十、记忆系统的信任与安全
- 十一、动手练习
- 十二、本课小结
- 下节预告

### 1.3 三级标题
- 2.1 存储位置
- 2.2 MEMORY.md 索引文件
- 2.3 索引截断保护
- 3.1 类型分类法
- 3.2 各类型详解
- 3.3 什么不应该保存为记忆？
- 5.1 两步保存法
- 5.2 目录自动创建
- 6.1 加载时机
- 6.2 记忆提示注入
- 7.1 搜索过去的上下文
- 7.2 找到相关记忆
- 7.3 搜索策略
- 8.1 个人 vs 团队
- 8.2 团队记忆同步
- 9.1 长会话模式
- 9.2 日志 vs 索引
- 10.1 信任召回的内容
- 10.2 何时访问记忆

---

## 2. 关键知识点

### 2.1 记忆目录结构
```
~/.claude/projects/my-project/memory/
├── MEMORY.md              ← 索引文件（始终加载到上下文）
├── user_preferences.md    ← 用户偏好
├── project_structure.md   ← 项目架构
├── feedback_testing.md    ← 测试反馈
├── coding_standards.md    ← 编码标准
└── team/                  ← 团队共享记忆（可选）
    ├── MEMORY.md
    └── team_conventions.md
```

### 2.2 MEMORY.md 索引限制
- `MAX_ENTRYPOINT_LINES = 200` - 最大 200 行
- `MAX_ENTRYPOINT_BYTES = 25_000` - 最大 25KB

### 2.3 四种记忆类型
| 类型 | 适合保存 | 不适合保存 |
|------|----------|------------|
| `user` | "我是前端工程师"、"用 vim 键位" | 临时偏好 |
| `feedback` | "不要自动运行 npm install" | 一次性指示 |
| `project` | "数据库用 PostgreSQL" | 代码中可推断的信息 |
| `reference` | "设计文档在 Notion" | 完整文档内容 |

### 2.4 记忆文件格式
- YAML frontmatter + Markdown 内容
- frontmatter 字段：`name`, `type`, `description`

### 2.5 两步保存法
1. Step 1 - 写记忆到独立文件（如 user_role.md）
2. Step 2 - 在 MEMORY.md 中添加索引指针

### 2.6 搜索策略
1. 检查 MEMORY.md 索引
2. 搜索记忆目录（Grep）
3. 搜索会话日志（最后手段）

### 2.7 团队记忆
- 位置：`memory/team/`
- 范围：团队成员共享
- 同步：自动同步

### 2.8 KAIROS 模式
- 日志式追加而非索引式
- 夜间蒸馏自动整理到 MEMORY.md
- 适合长会话（可能持续数天）

---

## 3. 涉及的源码文件路径

### 3.1 核心源码文件
- `memdir/memdir.ts` - 记忆系统核心
- `memdir/paths.ts` - 记忆路径
- `memdir/memoryTypes.ts` - 记忆类型
- `memdir/findRelevantMemories.ts` - 记忆搜索
- `memdir/teamMemPaths.ts` - 团队记忆路径
- `services/teamMemorySync/` - 团队记忆同步

---

## 4. 类名、函数名、接口名

### 4.1 常量
- `ENTRYPOINT_NAME = 'MEMORY.md'` - 索引文件名
- `MAX_ENTRYPOINT_LINES = 200` - 最大索引行数
- `MAX_ENTRYPOINT_BYTES = 25_000` - 最大索引字节数
- `MEMORY_TYPE_VALUES` - 记忆类型值数组
- `DIR_EXISTS_GUIDANCE` - 目录存在指导
- `WHAT_NOT_TO_SAVE_SECTION` - 不应该保存的内容说明
- `TRUSTING_RECALL_SECTION` - 信任召回内容说明
- `WHEN_TO_ACCESS_SECTION` - 何时访问记忆说明

### 4.2 函数
- `loadMemoryPrompt()` - 加载记忆提示
- `buildMemoryLines(displayName, memoryDir)` - 构建记忆行
- `buildAssistantDailyLogPrompt()` - 构建助手日志提示
- `ensureMemoryDirExists(memoryDir)` - 确保记忆目录存在
- `truncateEntrypointContent(raw)` - 截断索引内容
- `buildSearchingPastContextSection(autoMemDir)` - 构建搜索过去上下文部分
- `findRelevantMemories()` - 找到相关记忆
- `isAutoMemoryEnabled()` - 自动记忆是否启用
- `getKairosActive()` - KAIROS 是否激活
- `isTeamMemoryEnabled()` - 团队记忆是否启用

### 4.3 类型/接口
- `EntrypointTruncation` - 索引截断结果
- `MemoryType` - 记忆类型（'user' | 'feedback' | 'project' | 'reference'）

---

## 5. 代码片段重点

### 5.1 记忆目录结构（memdir/paths.ts）
```typescript
// 记忆文件存储在：~/.claude/projects/<project-slug>/memory/
// 每个项目有自己的记忆目录
```

### 5.2 MEMORY.md 索引（memdir/memdir.ts）
```typescript
export const ENTRYPOINT_NAME = 'MEMORY.md';
export const MAX_ENTRYPOINT_LINES = 200;
export const MAX_ENTRYPOINT_BYTES = 25_000;
```

### 5.3 记忆类型（memoryTypes.ts）
```typescript
export const MEMORY_TYPE_VALUES = [
  'user',       // 用户相关
  'feedback',   // 反馈相关
  'project',    // 项目相关
  'reference',  // 参考资料
] as const;
```

### 5.4 索引截断保护（memdir/memdir.ts）
```typescript
export function truncateEntrypointContent(raw: string): EntrypointTruncation {
  const contentLines = trimmed.split('\n');
  const wasLineTruncated = lineCount > MAX_ENTRYPOINT_LINES;
  const wasByteTruncated = byteCount > MAX_ENTRYPOINT_BYTES;

  if (truncated.length > MAX_ENTRYPOINT_BYTES) {
    const cutAt = truncated.lastIndexOf('\n', MAX_ENTRYPOINT_BYTES);
    truncated = truncated.slice(0, cutAt > 0 ? cutAt : MAX_ENTRYPOINT_BYTES);
  }

  return {
    content: truncated +
      `\n\n> WARNING: ${ENTRYPOINT_NAME} is ${reason}.
      Only part of it was loaded.
      Keep index entries to one line under ~200 chars;
      move detail into topic files.`,
    // ...
  };
}
```

### 5.5 两步保存法说明（memdir/memdir.ts）
```typescript
// 保存记忆是两步过程：
// Step 1 — 写记忆到独立文件（如 user_role.md）
// Step 2 — 在 MEMORY.md 中添加索引指针
```

### 5.6 目录自动创建（memdir/memdir.ts）
```typescript
export async function ensureMemoryDirExists(memoryDir: string): Promise<void> {
  const fs = getFsImplementation();
  try {
    await fs.mkdir(memoryDir);
  } catch (e) {
    // fs.mkdir 已经处理 EEXIST
    // 只记录真正的权限错误
  }
}

export const DIR_EXISTS_GUIDANCE =
  'This directory already exists — write to it directly with the Write tool
  (do not run mkdir or check for its existence).';
```

### 5.7 记忆加载时机（memdir/memdir.ts）
```typescript
export async function loadMemoryPrompt(): Promise<string | null> {
  const autoEnabled = isAutoMemoryEnabled();

  // KAIROS 模式：使用日志式记忆
  if (feature('KAIROS') && autoEnabled && getKairosActive()) {
    return buildAssistantDailyLogPrompt(skipIndex);
  }

  // 团队记忆模式
  if (feature('TEAMMEM') && teamMemPaths.isTeamMemoryEnabled()) {
    return teamMemPrompts.buildCombinedMemoryPrompt(...);
  }

  // 标准模式
  if (autoEnabled) {
    await ensureMemoryDirExists(autoDir);
    return buildMemoryLines('auto memory', autoDir, ...).join('\n');
  }

  return null;
}
```

### 5.8 搜索策略（memdir/memdir.ts）
```typescript
export function buildSearchingPastContextSection(autoMemDir: string): string[] {
  return [
    '## Searching past context',
    '',
    'When looking for past context:',
    '1. Search topic files in your memory directory:',
    '```',
    `Grep with pattern="<search term>" path="${autoMemDir}" glob="*.md"`,
    '```',
    '2. Session transcript logs (last resort — large files, slow):',
    '```',
    `Grep with pattern="<search term>" path="${projectDir}/" glob="*.jsonl"`,
    '```',
    'Use narrow search terms rather than broad keywords.',
  ];
}
```

### 5.9 KAIROS 日志式记忆（memdir/memdir.ts）
```typescript
function buildAssistantDailyLogPrompt(): string {
  const logPathPattern = join(
    memoryDir, 'logs', 'YYYY', 'MM', 'YYYY-MM-DD.md'
  );

  return [
    '# auto memory',
    '',
    'This session is long-lived. Record anything worth remembering',
    'by **appending** to today\'s daily log file:',
    '',
    `\`${logPathPattern}\``,
    '',
    'Write each entry as a short timestamped bullet.',
    'A separate nightly process distills these logs into MEMORY.md.',
  ].join('\n');
}
```
