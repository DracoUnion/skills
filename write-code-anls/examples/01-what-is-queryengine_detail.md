# 01-what-is-queryengine.md 细纲

## 一、标题层级结构

### 1. QueryEngine 是什么？Claude Code 的大脑
- 学习目标（5点）
- 生活类比：QueryEngine 就像一位超级管家
- QueryEngine 在 Claude Code 中的位置
  - 系统架构图
- 源码解析：QueryEngine 类的核心结构
  - 配置类型 QueryEngineConfig（第130-173行）
  - QueryEngine 类定义（第184-207行）
  - 核心方法 submitMessage（第209-212行）
- QueryEngine 的五大职责
  - 职责1：系统提示词构建
  - 职责2：用户输入处理
  - 职责3：启动查询循环
  - 职责4：用量追踪与预算控制
  - 职责5：会话持久化
- QueryEngine 与 ask() 的关系
- 消息流转的数据结构
- QueryEngine 的生命周期
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **QueryEngine 核心地位**
   - 处于系统"心脏"位置，对接用户界面，协调 AI 模型和工具系统
   - 管理整个对话的生命周期

2. **QueryEngineConfig 配置项**
   - `cwd`: 当前工作目录
   - `tools`: 可用工具列表
   - `mcpClients`: MCP 服务器连接
   - `canUseTool`: 工具权限检查函数
   - `maxTurns`: 最大轮次限制
   - `maxBudgetUsd`: 最大预算（美元）

3. **核心属性**
   - `mutableMessages`: 对话消息列表（可变）
   - `abortController`: 中止控制器
   - `totalUsage`: 总使用量统计

4. **submitMessage 方法**
   - 使用 `async *` 异步生成器语法
   - 实现流式响应（Streaming）

5. **ask() 函数**
   - QueryEngine 的一次性便捷包装
   - 适用于一次性查询场景

6. **消息类型**
   - `user`: 用户输入
   - `assistant`: AI 回复
   - `system`: 系统消息
   - `progress`: 进度更新
   - `attachment`: 附件
   - `stream_event`: 流式事件

## 三、源码文件路径

- `src/QueryEngine.ts` - QueryEngine 主类
- `src/query.ts` - 查询循环（queryLoop）

## 四、类名、函数名、接口名

### 核心类
- `QueryEngine` - 查询引擎主类（第184-207行）
- `QueryEngineConfig` - 引擎配置类型（第130-173行）

### 核心方法
- `submitMessage()` - 提交消息入口（第209-212行）
- `ask()` - 便捷包装函数（第1186-1295行）
- `interrupt()` - 中断方法

### 类型
- `Message` - 消息数据结构
- `NonNullableUsage` - 用量统计类型
- `SDKPermissionDenial` - 权限拒绝记录

### 常量
- `EMPTY_USAGE` - 空用量初始值
