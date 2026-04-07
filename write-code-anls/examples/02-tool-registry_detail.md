# 02-tool-registry.md 细纲

## 一、标题层级结构

### 1. 工具注册中心 —— getAllBaseTools 三级过滤
- 学习目标（5点）
- 生活类比：超市的货架管理
- 第一级：getAllBaseTools —— 仓库盘点
  - 永远加载的工具
  - 条件加载 - 环境检测
  - 条件加载 - Feature Flag
  - 条件加载 - 功能开关
- 第二级：filterToolsByDenyRules —— 权限黑名单
- 第三级：isEnabled —— 工具自检
- getTools vs assembleToolPool vs getMergedTools
- 简单模式（CLAUDE_CODE_SIMPLE）
- 特殊工具的处理
- REPL 模式的工具隐藏
- 工具预设（Tool Presets）
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **三种条件加载模式**
   - 环境检测：`hasEmbeddedSearchTools()`
   - Feature Flag：`feature('PROACTIVE')`
   - 运行时检测：`process.env.USER_TYPE`

2. **延迟加载打破循环依赖**
   - 使用 `require()` 延迟加载
   - 解决 `tools.ts -> TeamCreateTool -> ... -> tools.ts`

3. **工具池组装策略**
   - `getTools()`: 内置工具 + 三级过滤
   - `assembleToolPool()`: 内置工具 + MCP 工具，内置优先排序
   - `getMergedTools()`: Token 计数用

4. **Prompt Cache 保护**
   - 内置工具排在 MCP 工具前面
   - 缓存断点在最后一个内置工具之后

## 三、源码文件路径

- `src/tools.ts` - 工具注册中心核心逻辑
- `src/Tool.ts` - Tool 类型定义
- `src/tools/SleepTool/SleepTool.ts` - Feature Flag 示例
- `src/tools/TeamCreateTool/` - 延迟加载示例

## 四、类名、函数名、接口名

### 函数
- `getAllBaseTools()` - 获取所有基础工具（第 193-251 行）
- `getTools()` - 三级过滤获取工具（第 271-327 行）
- `assembleToolPool()` - 组装完整工具池（第 345-367 行）
- `filterToolsByDenyRules()` - deny 规则过滤（第 262-269 行）
- `getMergedTools()` - 获取合并工具（Token 计数用）

### 常量
- `TOOL_PRESETS` - 工具预设数组
- `specialTools` - 特殊工具集合
- `REPL_ONLY_TOOLS` - REPL 模式隐藏的工具

### 条件加载示例
```typescript
const SleepTool =
  feature('PROACTIVE') || feature('KAIROS')
    ? require('./tools/SleepTool/SleepTool.js').SleepTool
    : null
```

### 延迟加载示例
```typescript
const getTeamCreateTool = () =>
  require('./tools/TeamCreateTool/TeamCreateTool.js').TeamCreateTool
```
