# 03-agent-types.md 细纲

## 一、标题层级结构

### 1. Agent 类型详解 —— Explore / GeneralPurpose / Plan / Verification
- 学习目标（5点）
- 通俗讲解：医院科室类比
- Explore Agent：代码搜索专家
  - 设计定位
  - 源码分析
  - 系统提示词的关键设计
  - 使用场景
- GeneralPurpose Agent：全能工作者
  - 设计定位
  - 源码分析
  - 系统提示词
  - 与 Explore 的关键差异
- Plan Agent：架构规划师
  - 设计定位
  - 源码分析
  - 系统提示词的独特之处
  - 为什么 Plan 用 inherit 模型？
- Verification Agent：对抗性检验员
  - 设计定位
  - 源码分析
  - 令人震撼的系统提示词
  - 输出格式要求
- 四种 Agent 全面对比
  - 对比图
  - 什么是 ONE_SHOT？
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **Explore Agent**
   - 只读、快速代码搜索专家
   - 禁用 Write/Edit/Agent 工具
   - 使用 Haiku 模型（快且便宜）
   - omitClaudeMd: true 节省 token
   - ONE_SHOT: true

2. **GeneralPurpose Agent**
   - 默认万金油 Agent
   - tools: ['*'] 使用所有工具
   - 能写文件、编辑代码
   - 非 ONE_SHOT

3. **Plan Agent**
   - 只读架构设计师
   - 复用 Explore 的工具配置
   - model: 'inherit'（需要强推理能力）
   - 结构化输出要求（关键文件列表）
   - ONE_SHOT: true

4. **Verification Agent**
   - 对抗性质量检验员
   - color: 'red' 红色标识
   - background: true 后台运行
   - criticalSystemReminder 每轮注入
   - 输出格式：Check/Command/Output/Result/VERDICT

5. **四种 Agent 对比**
   - Explore: 只读、Haiku、最快
   - GeneralPurpose: 读写、默认模型
   - Plan: 只读、inherit、架构设计
   - Verification: 只读、inherit、对抗性检验

## 三、源码文件路径

- `tools/AgentTool/built-in/exploreAgent.ts` - Explore Agent
- `tools/AgentTool/built-in/generalPurposeAgent.ts` - GeneralPurpose Agent
- `tools/AgentTool/built-in/planAgent.ts` - Plan Agent
- `tools/AgentTool/built-in/verificationAgent.ts` - Verification Agent
- `tools/AgentTool/constants.ts` - ONE_SHOT 常量

## 四、类名、函数名、接口名

### Agent 定义
- `EXPLORE_AGENT` - Explore Agent 定义
- `GENERAL_PURPOSE_AGENT` - GeneralPurpose Agent 定义
- `PLAN_AGENT` - Plan Agent 定义
- `VERIFICATION_AGENT` - Verification Agent 定义

### 系统提示词函数
- `getExploreSystemPrompt()` - Explore 提示词
- `getGeneralPurposeSystemPrompt()` - GeneralPurpose 提示词
- `getPlanV2SystemPrompt()` - Plan 提示词
- `VERIFICATION_SYSTEM_PROMPT` - Verification 提示词

### 常量
- `ONE_SHOT_BUILTIN_AGENT_TYPES` - 一次性 Agent 类型集合
- `TOOL_VERBS` - 工具名称到动词映射
