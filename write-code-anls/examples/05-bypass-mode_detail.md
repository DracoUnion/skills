# 05-bypass-mode.md 细纲

## 一、标题层级结构

### 1. Bypass 模式——最高权限也有底线
- 学习目标（5点）
- 生活类比：VIP 通道也有安检
- 源码直击：Bypass 模式的配置
  - symbol: '⏵⏵'
  - color: 'error'
- 三层安全底线
  - 第一层：Deny 规则不可绕过
  - 第二层：Ask 规则
  - 第三层：安全检查（Bypass-Immune）
- 源码中的三层底线
  - Step 1a: Deny 规则优先
  - Step 1f: 内容级 Ask 规则
  - Step 1g: 安全检查
- Bypass 不可绕过的路径
- 远程禁用（Killswitch）
  - checkAndDisableBypassPermissionsIfNeeded
- 危险权限清理
  - DANGEROUS_BASH_PATTERNS
- Bypass vs dontAsk 模式
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **Bypass 模式定位**
   - 跳过常规询问流程
   - 但保留核心安全检查
   - 红色显示警告用户处于高风险状态

2. **三层安全底线**
   - Deny 规则：用户明确禁止的操作
   - Ask 规则：用户要求必须询问的操作
   - 安全检查：.git/, .claude/ 等敏感路径

3. **Bypass-Immune 路径**
   - `.git/` → 修改 git 配置可能注入恶意 hooks
   - `.claude/` → Claude 的配置文件
   - `.vscode/` → VSCode 配置可能自动执行任务
   - `~/.bashrc`, `~/.zshrc`, `~/.profile` → Shell 配置可能植入后门

4. **远程禁用机制**
   - 组织管理员可远程禁用 Bypass
   - `shouldDisableBypassPermissions()` 检查
   - 禁用后降级到 Default 模式

5. **危险权限清理**
   - 切换到 Auto 模式时清理过于宽泛的 allow 规则
   - DANGEROUS_BASH_PATTERNS:
     - `python`, `python3`, `node`, `ruby`
     - `npx`, `npm run`, `yarn run`
     - `bash`, `sh`, `zsh`
     - `eval`, `exec`, `sudo`, `ssh`

6. **Bypass vs dontAsk**
   - Bypass: ask → allow（不确定的允许）
   - dontAsk: ask → deny（不确定的拒绝）

## 三、源码文件路径

- `src/utils/permissions/PermissionMode.ts` - 模式配置
- `src/utils/permissions/permissions.ts` - 权限检查中的 Bypass 处理
- `src/utils/permissions/bypassPermissionsKillswitch.ts` - 远程禁用
- `src/utils/permissions/dangerousPatterns.ts` - 危险模式

## 四、类名、函数名、接口名

### 常量
- `PERMISSION_MODE_CONFIG.bypassPermissions` - Bypass 模式配置
- `DANGEROUS_BASH_PATTERNS` - 危险 Bash 模式数组

### 核心函数
- `checkAndDisableBypassPermissionsIfNeeded()` - 检查并禁用 Bypass
- `shouldDisableBypassPermissions()` - 是否应该禁用 Bypass
- `createDisabledBypassPermissionsContext()` - 创建禁用上下文

### 消息
- `DONT_ASK_REJECT_MESSAGE` - dontAsk 模式拒绝消息

### 辅助函数
- `isDangerousBashPattern()` - 判断是否为危险模式
- `stripDangerousRules()` - 剥离危险规则
