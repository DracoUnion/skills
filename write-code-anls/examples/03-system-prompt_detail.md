# 03-system-prompt.md 细纲

## 一、标题层级结构

### 1. 系统提示词构建：Git + CLAUDE.md + 工具
- 学习目标（5点）
- 生活类比：提示词就像演员的角色说明
- 三层上下文架构
  - System Prompt / User Context / System Context
- 源码解析：fetchSystemPromptParts
  - 并行获取三层上下文（第44-74行）
- 系统上下文：Git 状态信息
  - getSystemContext（第116-150行）
  - getGitStatus（第36-111行）
- 用户上下文：CLAUDE.md 和日期
  - getUserContext（第155-189行）
  - CLAUDE.md 的加载层次
- 系统提示词：角色定义 + 行为准则
  - 在 QueryEngine 中的组装
  - getSystemPrompt 构成
- 上下文如何注入 API 请求
  - prependUserContext（第660行）
  - appendSystemContext（第449-451行）
- 缓存优化：memoize 的妙用
- 特殊场景处理
  - 自定义系统提示词
  - Bare 模式
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **三层上下文架构**
   - System Prompt: AI 的角色定义 + 行为准则 + 工具说明
   - User Context: CLAUDE.md 项目规则 + 当前日期
   - System Context: Git 状态信息

2. **fetchSystemPromptParts 并行获取**
   - 使用 Promise.all 并行获取三层上下文
   - 加速启动过程

3. **Git 状态信息**
   - 当前分支（`git branch --show-current`）
   - 主分支（`git config init.defaultBranch`）
   - 文件状态（`git status --short`）
   - 最近提交（`git log --oneline -n 5`）
   - 用户名（`git config user.name`）

4. **CLAUDE.md 加载层次**
   - `~/.claude/CLAUDE.md`（全局规则）
   - 项目根目录/CLAUDE.md（项目规则）
   - 项目根目录/.claude/CLAUDE.md（项目规则）
   - 当前目录/CLAUDE.md（目录级规则）
   - `--add-dir` 额外目录（附加目录规则）

5. **缓存策略 memoize**
   - 系统上下文和用户上下文只构建一次
   - 后续使用缓存结果

6. **上下文注入位置**
   - User Context: 插入到第一条用户消息之前
   - System Context: 追加到系统提示词末尾

## 三、源码文件路径

- `src/utils/queryContext.ts` - fetchSystemPromptParts
- `src/context.ts` - getSystemContext / getUserContext / getGitStatus
- `src/constants/prompts.ts` - 系统提示词内容

## 四、类名、函数名、接口名

### 核心函数
- `fetchSystemPromptParts()` - 获取三层上下文（第44-74行）
- `getSystemContext()` - 获取系统上下文（第116-150行）
- `getUserContext()` - 获取用户上下文（第155-189行）
- `getGitStatus()` - 获取 Git 状态（第36-111行）
- `getSystemPrompt()` - 获取默认系统提示词

### 辅助函数
- `prependUserContext()` - 注入用户上下文
- `appendSystemContext()` - 注入系统上下文
- `asSystemPrompt()` - 拼接系统提示词
- `memoize()` - 缓存装饰器

### 常量
- `MAX_STATUS_CHARS` - Git 状态最大字符数

### 类型
- `SystemPromptParts` - 系统提示词部分
