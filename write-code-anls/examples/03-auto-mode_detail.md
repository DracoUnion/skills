# 03-auto-mode.md 细纲

## 一、标题层级结构

### 1. Auto 模式——AI 分类器自动判断
- 学习目标（5点）
- 生活类比：雇了个保安队长
- Auto 模式的三层决策
  - 第一层：安全工具白名单
  - 第二层：acceptEdits 快速通道
  - 第三层：AI 分类器
- 安全工具白名单
  - SAFE_YOLO_ALLOWLISTED_TOOLS
  - isAutoModeAllowlistedTool
- acceptEdits 快速通道
- YOLO 分类器：两阶段 XML 决策
  - Stage 1 快速判断
  - Stage 2 深度思考
  - parseXmlBlock 解析
- 对话上下文压缩
  - buildTranscriptEntries
- 拒绝追踪：连续失败的熔断机制
  - DENIAL_LIMITS
  - shouldFallbackToPrompting
- 分类器不可用时的应对
  - Fail Closed 策略
  - 铁门关闭/打开策略
- 分类器开销追踪
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **Auto 模式三层决策**
   - 第一层：安全工具白名单（零延迟）
   - 第二层：acceptEdits 快速通道
   - 第三层：AI 分类器

2. **安全工具白名单**
   - FILE_READ_TOOL_NAME
   - GREP_TOOL_NAME, GLOB_TOOL_NAME, LSP_TOOL_NAME
   - TODO_WRITE_TOOL_NAME
   - ASK_USER_QUESTION_TOOL_NAME
   - ENTER_PLAN_MODE_TOOL_NAME, EXIT_PLAN_MODE_TOOL_NAME
   - SLEEP_TOOL_NAME

3. **YOLO 分类器两阶段设计**
   - Stage 1: max_tokens=64, 快速初筛
   - Stage 2: max_tokens=4096, 深度审核
   - Stage 1 允许 → 立即放行
   - Stage 1 阻止 → Stage 2 复核

4. **XML 解析**
   - 解析 `<block>yes/no</block>`
   - `yes` = 应该阻止
   - 使用 `stripThinking()` 去除 thinking 块

5. **对话上下文压缩**
   - 用户消息：保留文本
   - 助手消息：只保留 tool_use，排除文本内容
   - 防止提示注入攻击

6. **拒绝追踪机制**
   - `maxConsecutive`: 连续拒绝上限
   - `maxTotal`: 总拒绝上限
   - 超过阈值降级到人工确认

7. **Fail Closed 策略**
   - 分类器不可用 → 默认拒绝
   - 上下文太长 → 降级到手动确认

## 三、源码文件路径

- `src/utils/permissions/classifierDecision.ts` - 分类器决策
- `src/utils/permissions/yoloClassifier.ts` - YOLO 分类器
- `src/utils/permissions/denialTracking.ts` - 拒绝追踪

## 四、类名、函数名、接口名

### 核心函数
- `isAutoModeAllowlistedTool()` - 检查是否在白名单
- `executeAsyncClassifierCheck()` - 执行异步分类器检查
- `buildTranscriptEntries()` - 构建对话上下文
- `parseXmlBlock()` - 解析 XML 响应
- `recordDenial()` / `recordSuccess()` - 记录拒绝/成功
- `shouldFallbackToPrompting()` - 是否应该降级

### 常量
- `SAFE_YOLO_ALLOWLISTED_TOOLS` - 安全工具白名单集合
- `XML_S1_SUFFIX` - Stage 1 后缀
- `XML_S2_SUFFIX` - Stage 2 后缀
- `DENIAL_LIMITS` - 拒绝限制

### 类型
- `TranscriptEntry` - 对话条目类型
- `ClassifierDecision` - 分类器决策
- `DenialState` - 拒绝状态

### 辅助函数
- `stripThinking()` - 去除 thinking 块
- `calculateCostFromTokens()` - 计算 Token 成本
