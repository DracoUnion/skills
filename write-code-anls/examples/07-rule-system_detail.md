# 07-rule-system.md 细纲

## 一、标题层级结构

### 1. 规则系统——Allow/Deny/Ask 的优先级
- 学习目标（5点）
- 生活类比：公司制度体系
- 规则的三个维度
  - source / ruleBehavior / ruleValue
- 七种规则来源
  - PermissionRuleSource
- 行为优先级：Deny > Ask > Allow
- 四种规则匹配模式
  - 工具级匹配
  - 精确匹配
  - 前缀匹配
  - 通配符匹配
- Deny 规则的增强保护
  - stripAllEnvVars
- 规则的存储位置
- 规则同步机制
  - syncPermissionRulesFromDisk
- 权限上下文的完整结构
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **规则三维度**
   - source: 规则来源（谁制定）
   - ruleBehavior: allow/deny/ask
   - ruleValue: toolName + ruleContent

2. **七种规则来源优先级**
   - policySettings（组织策略，最高）
   - flagSettings（Feature Flag）
   - userSettings（用户全局）
   - projectSettings（项目级）
   - localSettings（本地，不提交 Git）
   - cliArg / command（命令行参数）
   - session（会话临时，最低）

3. **行为优先级**
   - Deny > Ask > Allow
   - 拒绝永远胜过允许

4. **四种匹配模式**
   - 工具级: `Bash` → 匹配整个工具
   - 精确: `Bash(npm install)` → 完全匹配
   - 前缀: `Bash(npm:*)` → 前缀+空格匹配
   - 通配符: `Bash(npm * --save)` → 模式匹配

5. **Deny 规则增强保护**
   - 剥离所有环境变量
   - 防止 `FOO=bar dangerous_cmd` 绕过

6. **规则存储位置**
   - `~/.claude/settings.json` - 全局设置
   - `.claude/settings.json` - 项目设置
   - `.claude/settings.local.json` - 本地设置

7. **规则同步机制**
   - 先清空磁盘来源规则
   - 再重新加载所有规则
   - 确保删除操作生效

## 三、源码文件路径

- `src/types/permissions.ts` - PermissionRule 类型
- `src/utils/permissions/PermissionRule.ts` - 规则结构
- `src/utils/permissions/permissions.ts` - 规则匹配
- `src/tools/BashTool/bashPermissions.ts` - Bash 规则匹配

## 四、类名、函数名、接口名

### 类型
- `PermissionRule` - 权限规则
- `PermissionRuleSource` - 规则来源类型
- `PermissionRuleValue` - 规则值
- `ToolPermissionRulesBySource` - 按来源组织的规则
- `ToolPermissionContext` - 权限上下文

### 核心函数
- `matchingRulesForInput()` - 匹配输入的规则
- `filterRulesByContentsMatchingInput()` - 按内容过滤规则
- `syncPermissionRulesFromDisk()` - 从磁盘同步规则
- `applyPermissionUpdate()` / `applyPermissionUpdates()` - 应用规则更新
- `convertRulesToUpdates()` - 转换规则为更新

### 常量
- `PERMISSION_RULE_SOURCES` - 规则来源数组
- `RULE_SOURCES_IN_ORDER` - 有序规则来源

### 匹配模式
- `toolMatchesRule()` - 工具级匹配
- `matchWildcardPattern()` - 通配符匹配
- `stripSafeWrappers()` - 剥离安全包装器
- `stripAllEnvVars` - 剥离所有环境变量（Deny 规则）
