# 第6课：上下文压缩算法深入解析 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第6课：上下文压缩算法深入解析

### 1.2 二级标题
- 学习目标
- 生活类比：笔记本写满了
- 真实源码解析
- 微压缩（MicroCompact）
- 压缩的容错机制
- 完整的压缩流程
- 动手练习
- 本课小结
- 下节预告

### 1.3 三级标题
- 1. 自动压缩的触发机制
- 2. 压缩 Prompt 的设计
- 3. 分析-摘要两阶段生成
- 4. 压缩后的上下文恢复
- 5. 图片剥离优化
- 压缩后恢复的内容
- Prompt-too-long 重试
- 断路器机制

---

## 2. 关键知识点

### 2.1 自动压缩触发机制
| 阈值 | 计算方式 | 触发行为 |
|------|---------|---------|
| 自动压缩阈值 | 上下文窗口 - 13,000 | 自动触发压缩 |
| 警告阈值 | 上下文窗口 - 20,000 | 显示黄色警告 |
| 错误阈值 | 上下文窗口 - 20,000 | 显示红色警告 |

### 2.2 压缩 Prompt 的 9 个关键部分
1. 主要请求和意图
2. 关键技术概念
3. 文件和代码段
4. 错误和修复
5. 问题解决过程
6. 所有用户消息
7. 待办任务
8. 当前工作（最重要）
9. 可选的下一步

### 2.3 分析-摘要两阶段生成
- `<analysis>` 标签：草稿阶段，组织思路
- `<summary>` 标签：最终结构化输出
- 格式化函数剥离 `<analysis>` 内容

### 2.4 压缩后恢复的内容
- 最近读取的文件（最多5个）
- 计划文件（如果存在）
- 已调用的技能（token 预算内）
- 异步 Agent 状态
- 延迟工具 schema
- MCP 指令

### 2.5 微压缩（MicroCompact）
- 只压缩特定工具的输出
- 可压缩工具：FileRead、Shell、Grep、Glob、WebSearch、WebFetch、FileEdit、FileWrite
- 把旧工具结果替换为简短标记

### 2.6 容错机制
- **PTL 重试**：从头部截断消息组重试
- **断路器**：连续失败超过 3 次停止自动压缩

---

## 3. 涉及的源码文件路径

### 3.1 核心源码文件
- `services/compact/autoCompact.ts` - 自动压缩触发逻辑
- `services/compact/compact.ts` - 完整压缩算法
- `services/compact/prompt.ts` - 压缩 prompt 设计
- `services/compact/microCompact.ts` - 微压缩实现
- `utils/tokens.js` - token 计算工具
- `utils/hooks.js` - 压缩前后钩子
- `utils/messages.js` - 消息处理工具
- `utils/attachments.js` - 附件处理

---

## 4. 类名、函数名、接口名

### 4.1 函数
- `getEffectiveContextWindowSize(model: string)` - 获取有效上下文窗口大小
- `getAutoCompactThreshold(model: string)` - 获取自动压缩阈值
- `getMaxOutputTokensForModel(model: string)` - 获取模型最大输出 token
- `getContextWindowForModel(model: string, betas: string[])` - 获取模型上下文窗口
- `stripImagesFromMessages(messages: Message[])` - 剥离消息中的图片
- `createPostCompactFileAttachments()` - 创建压缩后文件附件
- `createAsyncAgentAttachmentsIfNeeded()` - 创建异步 Agent 附件
- `truncateHeadForPTLRetry()` - PTL 重试截断
- `groupMessagesByApiRound()` - 按 API 轮次分组消息
- `getPromptTooLongTokenGap()` - 获取 PTL token 差距
- `roughTokenCountEstimationForMessages()` - 粗略 token 估算
- `executePreCompactHooks()` - 执行压缩前钩子
- `executePostCompactHooks()` - 执行压缩后钩子
- `createCompactBoundaryMessage()` - 创建压缩边界消息
- `getMessagesAfterCompactBoundary()` - 获取压缩边界后消息
- `isCompactBoundaryMessage()` - 检查是否为压缩边界消息
- `normalizeMessagesForAPI()` - 标准化消息用于 API
- `microcompactMessages()` - 微压缩消息

### 4.2 常量
- `MAX_OUTPUT_TOKENS_FOR_SUMMARY = 20_000` - 摘要输出最大 token
- `AUTOCOMPACT_BUFFER_TOKENS = 13_000` - 自动压缩缓冲 token
- `WARNING_THRESHOLD_BUFFER_TOKENS = 20_000` - 警告阈值缓冲 token
- `ERROR_THRESHOLD_BUFFER_TOKENS = 20_000` - 错误阈值缓冲 token
- `MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3` - 最大连续自动压缩失败次数
- `POST_COMPACT_MAX_FILES_TO_RESTORE = 5` - 压缩后最大恢复文件数
- `POST_COMPACT_TOKEN_BUDGET = 50_000` - 压缩后 token 预算
- `POST_COMPACT_MAX_TOKENS_PER_FILE = 5_000` - 每文件最大 token
- `POST_COMPACT_MAX_TOKENS_PER_SKILL = 5_000` - 每技能最大 token
- `POST_COMPACT_SKILLS_TOKEN_BUDGET = 25_000` - 技能 token 预算

### 4.3 可压缩工具集合
- `COMPACTABLE_TOOLS` - 包含 FILE_READ_TOOL_NAME、SHELL_TOOL_NAMES、GREP_TOOL_NAME、GLOB_TOOL_NAME、WEB_SEARCH_TOOL_NAME、WEB_FETCH_TOOL_NAME、FILE_EDIT_TOOL_NAME、FILE_WRITE_TOOL_NAME

---

## 5. 代码片段重点

### 5.1 自动压缩阈值计算（autoCompact.ts）
```typescript
const MAX_OUTPUT_TOKENS_FOR_SUMMARY = 20_000;
export const AUTOCOMPACT_BUFFER_TOKENS = 13_000;
export const WARNING_THRESHOLD_BUFFER_TOKENS = 20_000;
export const ERROR_THRESHOLD_BUFFER_TOKENS = 20_000;
const MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3;

export function getEffectiveContextWindowSize(model: string): number {
  const reservedTokensForSummary = Math.min(
    getMaxOutputTokensForModel(model),
    MAX_OUTPUT_TOKENS_FOR_SUMMARY,
  );
  let contextWindow = getContextWindowForModel(model, getSdkBetas());
  return contextWindow - reservedTokensForSummary;
}

export function getAutoCompactThreshold(model: string): number {
  const effectiveContextWindow = getEffectiveContextWindowSize(model);
  return effectiveContextWindow - AUTOCOMPACT_BUFFER_TOKENS;
}
```

### 5.2 压缩后并行恢复（compact.ts 第532-539行）
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

### 5.3 图片剥离优化（compact.ts 第145-200行）
```typescript
export function stripImagesFromMessages(messages: Message[]): Message[] {
  return messages.map(message => {
    if (message.type !== 'user') return message;

    const content = message.message.content;
    if (!Array.isArray(content)) return message;

    let hasMediaBlock = false;
    const newContent = content.flatMap(block => {
      if (block.type === 'image') {
        hasMediaBlock = true;
        return [{ type: 'text' as const, text: '[image]' }];
      }
      if (block.type === 'document') {
        hasMediaBlock = true;
        return [{ type: 'text' as const, text: '[document]' }];
      }
      return [block];
    });

    if (!hasMediaBlock) return message;

    return {
      ...message,
      message: { ...message.message, content: newContent },
    } as typeof message;
  });
}
```

### 5.4 PTL 重试截断（compact.ts 第243-291行）
```typescript
export function truncateHeadForPTLRetry(
  messages: Message[],
  ptlResponse: AssistantMessage,
): Message[] | null {
  const groups = groupMessagesByApiRound(input);
  if (groups.length < 2) return null;

  const tokenGap = getPromptTooLongTokenGap(ptlResponse);
  let dropCount: number;
  if (tokenGap !== undefined) {
    let acc = 0;
    dropCount = 0;
    for (const g of groups) {
      acc += roughTokenCountEstimationForMessages(g);
      dropCount++;
      if (acc >= tokenGap) break;
    }
  } else {
    dropCount = Math.max(1, Math.floor(groups.length * 0.2));
  }

  dropCount = Math.min(dropCount, groups.length - 1);
  return groups.slice(dropCount).flat();
}
```

### 5.5 微压缩可压缩工具集合（microCompact.ts）
```typescript
const COMPACTABLE_TOOLS = new Set<string>([
  FILE_READ_TOOL_NAME,
  ...SHELL_TOOL_NAMES,
  GREP_TOOL_NAME,
  GLOB_TOOL_NAME,
  WEB_SEARCH_TOOL_NAME,
  WEB_FETCH_TOOL_NAME,
  FILE_EDIT_TOOL_NAME,
  FILE_WRITE_TOOL_NAME,
]);
```
