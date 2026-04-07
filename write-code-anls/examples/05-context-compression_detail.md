# 第五课：记忆压缩术 —— 四层上下文管理详解 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第五课：记忆压缩术 —— 四层上下文管理详解

### 1.2 二级标题
- 学习目标
- 一、生活类比：图书馆的书架管理
- 二、Compact 系统核心：compact.ts
- 三、自动压缩触发器
- 四、Compact Boundary：压缩边界
- 五、分组策略
- 六、微压缩：apiMicrocompact
- 七、Session Memory Compact
- 八、Hooks 系统集成
- 九、Token 管理策略
- 十、动手练习
- 十一、本课小结
- 下节预告

### 1.3 三级标题
- 2.1 系统架构
- 2.2 核心依赖
- 2.3 Compact 提示词
- 3.1 autoCompact
- 3.2 压缩警告状态
- 4.1 什么是 Compact Boundary？
- 4.2 增量信息附加
- 5.1 消息分组
- 5.2 部分压缩
- 6.1 紧急场景
- 6.2 工具结果替换
- 7.1 会话记忆提取
- 7.2 压缩与记忆的协同
- 8.1 Pre-Compact Hooks
- 8.2 Post-Compact Hooks
- 9.1 Token 使用追踪
- 9.2 输出 Token 限制
- 9.3 上下文分析

---

## 2. 关键知识点

### 2.1 四层上下文管理
1. **Compact 摘要压缩** - 书架满了写摘要
2. **分组策略** - 关联消息一起处理
3. **工具结果替换** - 只保留目录和重点
4. **微压缩** - 直接查索引卡片

### 2.2 压缩警告状态
| 使用率 | 状态 | 行为 |
|--------|------|------|
| < 70% | 安全 | 正常工作 |
| 70-85% | 提醒 | UI 显示使用率 |
| 85-95% | 警告 | 建议压缩 |
| > 95% | 紧急 | 自动触发压缩 |

### 2.3 Compact Boundary
- 压缩边界标记
- `type: 'system', subtype: 'compact_boundary'`
- 分隔摘要和新消息

### 2.4 增量信息附加
| 增量类型 | 内容 | 作用 |
|----------|------|------|
| Agent Listing | 代理列表变化 | 知道有哪些子代理 |
| Deferred Tools | 延迟加载的工具 | 知道有哪些工具可用 |
| MCP Instructions | MCP 服务器指令 | 保持 MCP 连接上下文 |

### 2.5 微压缩（apiMicrocompact）
- API 调用级别的紧急裁剪
- 不走完整的压缩流程
- 直接截断或替换最大的工具结果

### 2.6 工具结果替换
- 大型工具输出替换为引用
- `ContentReplacementState` 追踪替换状态
- 需要时可以通过 FileRead 重新获取

---

## 3. 涉及的源码文件路径

### 3.1 核心源码文件
- `services/compact/compact.ts` - 完整压缩算法
- `services/compact/autoCompact.ts` - 自动压缩触发
- `services/compact/compactWarningState.ts` - 压缩警告状态
- `services/compact/apiMicrocompact.ts` - 微压缩
- `services/compact/sessionMemoryCompact.ts` - 会话记忆压缩
- `services/compact/prompt.ts` - 压缩提示词
- `services/compact/grouping.ts` - 消息分组
- `utils/tokens.js` - token 计算
- `utils/hooks.js` - 压缩前后钩子
- `utils/messages.js` - 消息处理
- `utils/attachments.js` - 附件处理
- `utils/contextAnalysis.js` - 上下文分析

---

## 4. 类名、函数名、接口名

### 4.1 函数
- `autoCompactIfNeeded()` - 自动压缩
- `microcompactMessages()` - 微压缩
- `createCompactBoundaryMessage()` - 创建压缩边界消息
- `getMessagesAfterCompactBoundary()` - 获取压缩边界后消息
- `isCompactBoundaryMessage()` - 检查是否为压缩边界消息
- `executePreCompactHooks()` - 执行压缩前钩子
- `executePostCompactHooks()` - 执行压缩后钩子
- `getAgentListingDeltaAttachment()` - 获取代理列表增量附件
- `getDeferredToolsDeltaAttachment()` - 获取延迟工具增量附件
- `getMcpInstructionsDeltaAttachment()` - 获取 MCP 指令增量附件
- `groupMessagesByApiRound()` - 按 API 轮次分组消息
- `getTokenUsage()` - 获取 token 使用
- `tokenCountFromLastAPIResponse()` - 从上次 API 响应计算 token
- `tokenCountWithEstimation()` - 带估算的 token 计数
- `analyzeContext()` - 分析上下文
- `tokenStatsToStatsigMetrics()` - token 统计转 Statsig 指标

### 4.2 常量
- `COMPACT_MAX_OUTPUT_TOKENS` - 压缩最大输出 token
- `PartialCompactDirection` - 部分压缩方向（'oldest' | 'newest'）

### 4.3 类型/接口
- `SystemCompactBoundaryMessage` - 系统压缩边界消息
- `CompactProgressEvent` - 压缩进度事件
- `ContentReplacementState` - 内容替换状态

---

## 5. 代码片段重点

### 5.1 Compact 系统架构（compact.ts）
```typescript
import {
  createCompactBoundaryMessage,
  getMessagesAfterCompactBoundary,
  isCompactBoundaryMessage,
  normalizeMessagesForAPI,
} from '../../utils/messages.js';

import {
  executePostCompactHooks,
  executePreCompactHooks,
} from '../../utils/hooks.js';

import {
  getTokenUsage,
  tokenCountFromLastAPIResponse,
  tokenCountWithEstimation,
} from '../../utils/tokens.js';
```

### 5.2 增量信息附加（compact.ts）
```typescript
import {
  getAgentListingDeltaAttachment,
  getDeferredToolsDeltaAttachment,
  getMcpInstructionsDeltaAttachment,
} from '../../utils/attachments.js';
```

### 5.3 Compact Boundary 消息类型
```typescript
type SystemCompactBoundaryMessage = {
  type: 'system';
  subtype: 'compact_boundary';
  summary: string;
  originalCount: number;
};
```

### 5.4 部分压缩方向
```typescript
type PartialCompactDirection = 'oldest' | 'newest';
// oldest: 只压缩最老的消息（默认）
// newest: 特殊场景
```

### 5.5 压缩进度事件
```typescript
export type CompactProgressEvent =
  | { type: 'hooks_start', hookType: 'pre_compact' | 'post_compact' }
  | { type: 'compact_start' }
  | { type: 'compact_end' };
```

### 5.6 Token 管理（compact.ts）
```typescript
import { COMPACT_MAX_OUTPUT_TOKENS } from '../../utils/context.js';
```

### 5.7 上下文分析
```typescript
import {
  analyzeContext,
  tokenStatsToStatsigMetrics,
} from '../../utils/contextAnalysis.js';
```
