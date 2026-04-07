# 05-team-create-tool.md 细纲

## 一、标题层级结构

### 1. TeamCreateTool —— 团队组建机制
- 学习目标（5点）
- 通俗讲解：创业公司类比
- TeamCreateTool 源码全貌
  - 输入参数
  - 核心创建流程
  - 创建团队配置文件
  - 创建关联的任务列表
  - 更新应用状态
- 团队创建的完整流程
- 文件系统中的团队
- Team Lead vs Teammate
  - Team Lead（队长）
  - Teammate（队友）
  - 角色对比
- 团队工作流程
- TeamDeleteTool：优雅解散
- 设计要点解析
  - 为什么一个领导只能管一个团队？
  - 为什么需要 registerTeamForSessionCleanup？
  - 唯一名称生成
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **TeamCreateTool 输入参数**
   - team_name: 团队名称（必填）
   - description: 团队描述（选填）
   - agent_type: Team Lead 类型（选填）

2. **创建流程**
   - 检查是否已有团队
   - 生成唯一团队名
   - 生成 Team Lead ID
   - 创建 config.json
   - 创建任务目录
   - 更新 AppState

3. **TeamFile 结构**
   - name, description, createdAt
   - leadAgentId, leadSessionId
   - members[]（包含 agentId, name, agentType, model 等）

4. **Team Lead vs Teammate**
   - Team Lead: 创建团队的主 Agent，ID 确定性生成
   - Teammate: 通过 AgentTool 创建，ID 随机生成

5. **团队工作流程**
   - TeamCreate → TaskCreate → Agent Tool 添加队友
   - TaskUpdate 分配任务 → 队友工作 → TaskUpdate 标记完成
   - SendMessage shutdown_request → TeamDelete 清理资源

6. **TeamDelete 限制**
   - 必须关闭所有活跃队友才能解散
   - cleanupTeamDirectories 清理文件
   - clearTeammateColors 清除颜色分配

## 三、源码文件路径

- `tools/TeamCreateTool/TeamCreateTool.ts` - 团队创建工具
- `tools/TeamDeleteTool/TeamDeleteTool.ts` - 团队删除工具
- `tools/TeamCreateTool/prompt.ts` - 团队工作流提示词

## 四、类名、函数名、接口名

### 核心函数
- `generateUniqueTeamName()` - 生成唯一团队名
- `formatAgentId()` - 格式化 Agent ID
- `writeTeamFileAsync()` - 写入团队文件
- `readTeamFile()` - 读取团队文件
- `cleanupTeamDirectories()` - 清理团队目录
- `registerTeamForSessionCleanup()` - 注册会话清理

### 类型
- `TeamFile` - 团队文件结构
- `TeamMember` - 团队成员结构
- `TeamContext` - 团队上下文

### 常量
- `TEAM_LEAD_NAME = 'team-lead'` - Team Lead 名称
- `LEADER_TEAM_NAME_KEY` - 领导团队名键
