# 第三课：三层安全锁 —— 权限安全体系深入 - 细纲

## 1. 标题层级结构

### 1.1 一级标题
- 第三课：三层安全锁 —— 权限安全体系深入

### 1.2 二级标题
- 学习目标
- 一、生活类比：银行保险柜
- 二、权限模式：三种安全等级
- 三、第一层：规则匹配
- 四、第二层：分类器（Classifier）
- 五、第三层：用户审批
- 六、工具级别的权限检查
- 七、文件系统保护
- 八、沙箱执行
- 九、权限流程总览
- 十、动手练习
- 十一、本课小结
- 下节预告

### 1.3 三级标题
- 2.1 模式概览
- 2.2 权限上下文
- 3.1 三种规则类型
- 3.2 规则来源与优先级
- 3.3 工具级 Deny 规则过滤
- 4.1 YOLO 分类器
- 4.2 Bash 命令的特殊分类
- 4.3 拒绝追踪
- 5.1 审批流程
- 5.2 权限更新的持久化
- 7.1 路径验证
- 7.2 工作目录限制

---

## 2. 关键知识点

### 2.1 权限模式
| 模式 | 安全等级 | 行为 | 适合场景 |
|------|----------|------|----------|
| `default` | 标准 | 敏感操作需要确认 | 日常开发 |
| `plan` | 严格 | 所有写操作需要确认 | 规划阶段 |
| `bypassPermissions` | 宽松 | 自动批准（有分类器兜底） | 信任场景 |

### 2.2 三层安全架构
1. **第一层：规则匹配** - Allow/Deny/Ask 规则
2. **第二层：分类器** - YOLO 安全分类器
3. **第三层：用户审批** - 交互式确认

### 2.3 规则来源与优先级
| 优先级 | 来源 | 文件位置 |
|--------|------|----------|
| 最高 | 企业策略 | 管理员配置 |
| 高 | 用户设置 | `~/.claude/settings.json` |
| 中 | 项目设置 | `.claude/settings.json` |
| 低 | 会话级 | 运行时 |

### 2.4 分类器风险评估
| 操作类型 | 风险评估 | 分类结果 |
|----------|----------|----------|
| 读取文件 | 低风险 | allow |
| 修改项目内文件 | 中风险 | allow |
| 执行 `rm -rf` | 高风险 | deny |
| 访问 `/etc/passwd` | 高风险 | deny |
| 安装未知包 | 中高风险 | ask |

### 2.5 PermissionResult 三种行为
- `{ behavior: 'allow', updatedInput: Input }` - 允许
- `{ behavior: 'deny', message: string }` - 拒绝
- `{ behavior: 'ask', message: string }` - 询问

---

## 3. 涉及的源码文件路径

### 3.1 核心源码文件
- `types/permissions.ts` - 权限类型定义
- `Tool.ts` - ToolPermissionContext、checkPermissions
- `utils/permissions/permissions.ts` - 权限规则处理
- `utils/permissions/yoloClassifier.ts` - YOLO 分类器
- `utils/permissions/bashClassifier.ts` - Bash 命令分类器
- `utils/permissions/denialTracking.ts` - 拒绝追踪
- `utils/permissions/PermissionUpdate.ts` - 权限更新
- `utils/permissions/pathValidation.ts` - 路径验证
- `utils/sandbox/sandbox-adapter.ts` - 沙箱执行

---

## 4. 类名、函数名、接口名

### 4.1 类型/接口
- `PermissionMode` - 权限模式（'default' | 'plan' | 'bypassPermissions'）
- `ToolPermissionContext` - 工具权限上下文
- `PermissionResult` - 权限结果
- `PermissionUpdate` - 权限更新
- `DenialTrackingState` - 拒绝追踪状态
- `ClassifierContext` - 分类器上下文

### 4.2 函数
- `isBypassPermissionsModeAvailable()` - 是否可跳过权限
- `getDenyRuleForTool(permissionContext, tool)` - 获取工具的 Deny 规则
- `filterToolsByDenyRules(tools, permissionContext)` - Deny 规则过滤
- `classifyYoloAction(toolName, input, context)` - YOLO 分类
- `shouldFallbackToPrompting(state)` - 是否应该回退到提示
- `applyPermissionUpdate(update, destination)` - 应用权限更新
- `checkPermissions(input, context)` - 工具级权限检查

### 4.3 常量
- `PERMISSION_RULE_SOURCES` - 权限规则来源
- `DENIAL_LIMITS` - 拒绝次数阈值
- `SETTING_SOURCES` - 设置来源

---

## 5. 代码片段重点

### 5.1 权限模式类型（types/permissions.ts）
```typescript
export type PermissionMode = 'default' | 'plan' | 'bypassPermissions';
```

### 5.2 权限上下文（Tool.ts）
```typescript
export type ToolPermissionContext = DeepImmutable<{
  mode: PermissionMode;
  additionalWorkingDirectories: Map<...>;
  alwaysAllowRules: ToolPermissionRulesBySource;
  alwaysDenyRules: ToolPermissionRulesBySource;
  alwaysAskRules: ToolPermissionRulesBySource;
  isBypassPermissionsModeAvailable: boolean;
  shouldAvoidPermissionPrompts?: boolean;
}>;
```

### 5.3 Deny 规则过滤（tools.ts）
```typescript
export function filterToolsByDenyRules<T extends { name: string }>(
  tools: readonly T[],
  permissionContext: ToolPermissionContext
): T[] {
  return tools.filter(
    tool => !getDenyRuleForTool(permissionContext, tool)
  );
}
```

### 5.4 YOLO 分类器（yoloClassifier.ts）
```typescript
export function classifyYoloAction(
  toolName: string,
  input: unknown,
  context: ClassifierContext
): 'allow' | 'deny' | 'ask' {
  // 分析操作的风险等级
  // 返回 allow / deny / ask
}
```

### 5.5 拒绝追踪（denialTracking.ts）
```typescript
export const DENIAL_LIMITS = { /* 拒绝次数阈值 */ };

export function shouldFallbackToPrompting(
  state: DenialTrackingState
): boolean {
  // 连续被拒绝太多次 → 回退到询问用户
}
```

### 5.6 权限更新持久化（PermissionUpdate.ts）
```typescript
export function applyPermissionUpdate(
  update: PermissionUpdate,
  destination: PermissionUpdateDestination
): void {
  // 将用户的允许/拒绝决策持久化到配置文件
}
```

### 5.7 工具级权限检查（Tool.ts）
```typescript
checkPermissions(
  input: z.infer<Input>,
  context: ToolUseContext,
): Promise<PermissionResult>;
```
