# 第1课：为什么性能优化很重要？ - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第1课：为什么性能优化很重要？

### 1.2 二级标题
- 学习目标
- 生活类比：开一家早餐店
- 真实源码解析：Claude Code 的启动流程
- Claude Code 的六大优化策略
- 性能的两个维度：速度与成本
- 性能预算思维
- 动手练习
- 本课小结
- 下节预告

### 1.3 三级标题
- 启动时间是怎么被"吃掉"的？
- 性能检查点（Performance Checkpoint）
- 策略一览表
- 维度一：启动速度
- 维度二：API 成本

---

## 2. 关键知识点

### 2.1 性能优化的核心价值
- 性能影响用户体验：启动速度直接影响用户留存
- 性能影响成本：AI 应用中，token 使用量 = 真金白银
- 六大核心策略概览：并行、懒加载、死代码消除、压缩、缓存、流式

### 2.2 启动流程性能追踪
- `profileCheckpoint` - 性能检查点标记
- `startMdmRawRead` - MDM 子进程预取（~135ms）
- `startKeychainPrefetch` - macOS 钥匙串并行读取（~65ms）
- 模块 import 耗时（~135ms）

### 2.3 六大优化策略
| 策略 | 解决什么问题 | 对应课程 |
|------|-------------|----------|
| 并行预取 | 等待时间太长 | 第2课 |
| 懒加载 | 初始加载太重 | 第3课 |
| 死代码消除 | 包体积太大 | 第4课 |
| 上下文压缩 | 对话越来越长 | 第6课 |
| 缓存优化 | 重复计算太多 | 第7课 |
| 流式处理 | 要等全部完成 | 第9课 |

### 2.4 延迟预取（Deferred Prefetch）模式
- `startDeferredPrefetches()` 函数
- `void` 关键字表示 Fire-and-Forget
- 预取时机：UI 首次渲染后、用户开始打字前

### 2.5 性能预算思维
- Token 预算：`POST_COMPACT_TOKEN_BUDGET = 50_000`
- 时间预算：`AbortSignal.timeout(3000)` 文件计数限制
- 给每个环节设定时间/资源上限

---

## 3. 涉及的源码文件路径

### 3.1 核心源码文件
- `main.tsx` - 启动入口，性能检查点设置
- `utils/startupProfiler.js` - `profileCheckpoint`, `profileReport`
- `utils/settings/mdm/rawRead.js` - `startMdmRawRead`
- `utils/secureStorage/keychainPrefetch.js` - `startKeychainPrefetch`
- `services/compact/autoCompact.ts` - 自动压缩阈值计算

### 3.2 相关配置
- `process.env.CLAUDE_CODE_EXIT_AFTER_FIRST_RENDER` - 退出标志
- `isBareMode()` - 裸模式检测

---

## 4. 类名、函数名、接口名

### 4.1 函数
- `profileCheckpoint(name: string)` - 性能检查点
- `profileReport()` - 性能报告
- `startMdmRawRead()` - 启动 MDM 读取
- `startKeychainPrefetch()` - 启动钥匙串预取
- `startDeferredPrefetches()` - 延迟预取
- `isEnvTruthy(env: string | undefined)` - 环境变量检测
- `isBareMode()` - 裸模式检测
- `initUser()` - 用户初始化
- `getUserContext()` - 获取用户上下文
- `prefetchSystemContextIfSafe()` - 安全预取系统上下文
- `getRelevantTips()` - 获取相关提示
- `initializeAnalyticsGates()` - 初始化分析门控
- `prefetchOfficialMcpUrls()` - 预取 MCP URL
- `refreshModelCapabilities()` - 刷新模型能力
- `getAutoCompactThreshold(model: string)` - 获取自动压缩阈值

### 4.2 常量
- `MAX_OUTPUT_TOKENS_FOR_SUMMARY = 20_000` - 摘要输出最大 token
- `AUTOCOMPACT_BUFFER_TOKENS = 13_000` - 自动压缩缓冲 token
- `POST_COMPACT_TOKEN_BUDGET = 50_000` - 压缩后 token 预算
- `POST_COMPACT_MAX_TOKENS_PER_FILE = 5_000` - 每文件最大 token

---

## 5. 代码片段重点

### 5.1 启动时性能追踪（main.tsx 第1-20行）
```typescript
import { profileCheckpoint, profileReport } from './utils/startupProfiler.js';
profileCheckpoint('main_tsx_entry');
import { startMdmRawRead } from './utils/settings/mdm/rawRead.js';
startMdmRawRead();
import { startKeychainPrefetch } from './utils/secureStorage/keychainPrefetch.js';
startKeychainPrefetch();
```

### 5.2 延迟预取函数
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

### 5.3 自动压缩阈值计算
```typescript
export function getAutoCompactThreshold(model: string): number {
  const effectiveContextWindow = getEffectiveContextWindowSize(model);
  const autocompactThreshold = effectiveContextWindow - AUTOCOMPACT_BUFFER_TOKENS;
  return autocompactThreshold;
}
```
