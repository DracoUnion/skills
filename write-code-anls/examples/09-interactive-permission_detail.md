# 09-interactive-permission.md 细纲

## 一、标题层级结构

### 1. 交互式权限——竞态赛跑与超时处理
- 学习目标（5点）
- 生活类比：多人抢答系统
- createResolveOnce：原子级竞争锁
  - claim() vs isResolved()
- handleInteractivePermission：四路赛跑架构
  - 赛道 1：用户对话框
  - 赛道 2：权限 Hooks
  - 赛道 3：AI 分类器
  - 赛道 4：远程桥/频道
- 投机执行与宽限期
  - 2 秒投机等待
  - 200ms 宽限期
- 中止信号的优雅处理
- UI 过渡动画的时序设计
- recheckPermission：配置变更时重新检查
- 完整的决策流程图
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **createResolveOnce 竞争锁**
   - `claim()`: 原子性检查并标记
   - `isResolved()`: 仅检查状态
   - `resolve()`: 交付结果
   - 防止竞态条件的关键设计

2. **四路赛跑架构**
   - 赛道 1: 用户对话框（永远在场）
   - 赛道 2: 权限 Hooks（异步后台）
   - 赛道 3: AI 分类器（异步后台）
   - 赛道 4: 远程桥/频道（Bridge/Channel）

3. **用户对话框处理**
   - `onUserInteraction()`: 用户开始交互
   - `onAllow()`: 用户允许
   - `onReject()`: 用户拒绝
   - `onAbort()`: 用户中止

4. **宽限期设计**
   - 200ms 宽限期防止误触
   - 前 200ms 的操作被忽略
   - 防止误按取消分类器

5. **投机执行**
   - 显示对话框前等待 2 秒
   - 分类器高置信度匹配 → 跳过对话框
   - Promise.race 实现

6. **UI 过渡动画**
   - 分类器自动批准后显示 ✓ 标记
   - 终端在前台：显示 3 秒
   - 终端不在前台：显示 1 秒
   - 用户可按 Esc 提前关闭

7. **中止处理**
   - AbortController 信号监听
   - 所有赛道响应中止
   - 统一清理资源

8. **recheckPermission**
   - 配置变更时重新检查
   - 使用 claim() 防止竞态
   - 用最新配置运行权限检查

## 三、源码文件路径

- `src/hooks/toolPermission/PermissionContext.ts` - createResolveOnce
- `src/hooks/toolPermission/handlers/interactiveHandler.ts` - 交互式处理器
- `src/hooks/useCanUseTool.tsx` - React Hook 入口

## 四、类名、函数名、接口名

### 核心类型
- `ResolveOnce<T>` - 一次性解析锁
  - `resolve(value: T): void`
  - `isResolved(): boolean`
  - `claim(): boolean`

### 核心函数
- `createResolveOnce<T>()` - 创建一次性解析锁
- `handleInteractivePermission()` - 处理交互式权限
- `executeAsyncClassifierCheck()` - 执行异步分类器检查
- `recheckPermission()` - 重新检查权限

### 辅助函数
- `setClassifierChecking()` / `clearClassifierChecking()` - 分类器状态
- `peekSpeculativeClassifierCheck()` - 查看投机分类结果
- `getTerminalFocused()` - 获取终端焦点状态

### 常量
- `GRACE_PERIOD_MS` = 200 - 宽限期
- `SPECULATIVE_TIMEOUT_MS` = 2000 - 投机等待超时
- `CHECKMARK_DISPLAY_MS` = 3000 - ✓ 标记显示时间
- `CHECKMARK_DISPLAY_MS_UNFOCUSED` = 1000 - 非焦点时显示时间

### 回调
- `bridgeCallbacks` - 远程桥回调
- `channelCallbacks` - 频道回调
