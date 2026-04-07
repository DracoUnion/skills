# 08-coordinator-flow.md 细纲

## 一、标题层级结构

### 1. Coordinator 编排全流程
- 学习目标（5点）
- 通俗讲解：电影导演类比
- Coordinator 的系统提示词
  - 角色定义
  - 可用工具
- 四阶段工作流
  - 阶段一：Research 研究
  - 阶段二：Synthesis 综合
  - 阶段三：Implementation 实施
  - 阶段四：Verification 验证
- Continue vs Spawn Fresh 决策
  - 决策流程图
  - 继续 Worker 的示例
  - 新建 Worker 的示例
- Worker 提示词的艺术
  - 好的提示词要素
  - 添加目的说明
  - 反模式
- 完整的示例会话
- 并发管理
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **Coordinator 角色**
   - 协调者，不是执行者
   - 所有消息都是对用户说的
   - 能直接回答就直接回答

2. **Coordinator 工具**
   - Agent: 创建 Worker
   - SendMessage: 继续 Worker
   - TaskStop: 停止 Worker

3. **四阶段工作流**
   - Research: 并行调查，不修改文件
   - Synthesis: Coordinator 综合理解，最关键
   - Implementation: 精确指令，包含路径和行号
   - Verification: 运行测试，独立验证

4. **核心原则：永远不要委托理解**
   - 错误："Based on your findings, fix it"
   - 正确："Fix the null pointer in src/auth/validate.ts:42..."

5. **Continue vs Spawn Fresh**
   - Continue: 上下文高度相关、修正错误
   - Spawn Fresh: 验证工作、完全不同的方法

6. **好的 Worker 提示词**
   - 包含文件路径、行号、错误消息
   - 说明"完成"的定义
   - 添加目的说明

7. **并发管理**
   - 只读任务可并行
   - 写入任务串行（同一文件集）
   - 验证可在不同文件集上并行

## 三、源码文件路径

- `coordinator/coordinatorMode.ts` - Coordinator 模式核心
- `coordinator/prompt.ts` - Coordinator 系统提示词

## 四、类名、函数名、接口名

### 核心函数
- `getCoordinatorSystemPrompt()` - 获取 Coordinator 系统提示词
- `isCoordinatorMode()` - 检查 Coordinator 模式

### 类型
- `CoordinatorConfig` - Coordinator 配置
- `WorkerTask` - Worker 任务

### 常量
- `RESEARCH_PHASE` - 研究阶段
- `SYNTHESIS_PHASE` - 综合阶段
- `IMPLEMENTATION_PHASE` - 实施阶段
- `VERIFICATION_PHASE` - 验证阶段
