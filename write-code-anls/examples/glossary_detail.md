# 术语表 - 细纲

## 文件信息
- **原文件**: part00-preface/glossary.md
- **类型**: 术语速查表
- **难度**: ★☆☆☆☆

---

## 一、术语组织结构

按字母顺序 A-Z 排列，涵盖 Claude Code 核心技术术语

---

## 二、A 类术语

### 2.1 Agent（代理）
- **定义**: 能够自主执行多步骤任务的 AI 系统
- **说明**: Claude Code 就是一个编程 Agent，能自己规划、执行、验证任务

### 2.2 Agent Loop（代理循环）
- **定义**: AI 反复 "思考 → 调用工具 → 获取结果 → 再思考" 的核心循环
- **说明**: 直到任务完成的循环机制

### 2.3 Agent Swarm（代理群）
- **定义**: 多个 Agent 协作完成复杂任务的机制
- **角色**: Coordinator（协调者）和 Worker（工作者）

### 2.4 API（应用程序接口）
- **定义**: 软件之间通信的约定接口
- **说明**: Claude Code 通过 API 与 Anthropic 的 Claude 模型通信

### 2.5 AppState（应用状态）
- **定义**: Claude Code 中管理 500+ 字段的全局状态对象
- **源码**: `src/state/AppStateStore.ts`

### 2.6 AST（抽象语法树）
- **定义**: 将代码解析为树形结构，便于分析
- **应用**: BashTool 用 AST 分析 Shell 命令的安全性

---

## 三、B 类术语

### 3.1 Bash
- **定义**: Unix/macOS 系统的命令行 Shell
- **工具**: BashTool 让 Claude Code 能执行 Shell 命令

### 3.2 Bridge（桥接）
- **定义**: Claude Code 中连接 CLI 和 IDE（VS Code、JetBrains）的通信系统
- **目录**: `src/bridge/`

### 3.3 Bun
- **定义**: 超快的 JavaScript/TypeScript 运行时
- **说明**: Claude Code 使用它替代 Node.js

---

## 四、C 类术语

### 4.1 CLI（命令行界面）
- **定义**: 通过文本命令与计算机交互的界面
- **示例**: 终端

### 4.2 Claude
- **定义**: Anthropic 公司开发的 AI 大语言模型
- **说明**: Claude Code 的核心智能来源

### 4.3 Commander.js
- **定义**: Node.js 的命令行参数解析库
- **应用**: Claude Code 用它处理命令行选项

### 4.4 Compact（压缩）
- **定义**: 当对话上下文太长时，自动将旧消息压缩为摘要的机制

### 4.5 Coordinator（协调者）
- **定义**: 多 Agent 系统中负责任务分配和调度的主 Agent

---

## 五、D 类术语

### 5.1 Dead Code Elimination（死代码消除）
- **定义**: 构建时移除不会执行的代码分支，减小包体积

### 5.2 Docsify
- **定义**: 基于 Markdown 的文档网站生成器
- **说明**: 本书就是用它构建的

---

## 六、F 类术语

### 6.1 Feature Flag（特性标志）
- **定义**: 通过配置开关控制功能是否启用，无需修改代码

### 6.2 Fork（分叉）
- **定义**: 创建子进程或子 Agent 来并行执行任务

---

## 七、G 类术语

### 7.1 GrowthBook
- **定义**: 特性标志管理平台
- **应用**: Claude Code 用它控制功能的灰度发布

---

## 八、H 类术语

### 8.1 Hook（钩子）
- **定义**: React 中管理组件状态和副作用的函数
- **示例**: useState、useEffect

---

## 九、I 类术语

### 9.1 Ink
- **定义**: React 的终端渲染器
- **说明**: 让你用 React 组件构建终端 UI

---

## 十、J 类术语

### 10.1 JSON Schema
- **定义**: 描述 JSON 数据格式的标准
- **应用**: 用于工具的输入参数验证

### 10.2 JWT（JSON Web Token）
- **定义**: 基于 JSON 的安全令牌
- **应用**: Bridge 系统用它做身份认证

### 10.3 JSONL
- **定义**: 每行一个 JSON 对象的文件格式
- **应用**: 用于存储会话历史

---

## 十一、L 类术语

### 11.1 Lazy Loading（懒加载）
- **定义**: 延迟加载模块，只在需要时才加载
- **目的**: 加快启动速度

### 11.2 LSP（Language Server Protocol）
- **定义**: 语言服务器协议
- **功能**: 提供代码智能感知（自动补全、跳转定义等）

---

## 十二、M 类术语

### 12.1 MCP（Model Context Protocol）
- **定义**: 模型上下文协议
- **说明**: AI 调用外部工具的行业标准协议

### 12.2 Memdir（记忆目录）
- **定义**: Claude Code 基于文件系统的长期记忆存储机制

### 12.3 Mermaid
- **定义**: 用文本描述生成图表的工具
- **说明**: 本书大量使用

### 12.4 Migration（迁移）
- **定义**: 配置文件版本升级的机制
- **目的**: 确保旧配置自动适配新版本

---

## 十三、O 类术语

### 13.1 OAuth 2.0
- **定义**: 开放授权标准
- **应用**: Claude Code 用它实现安全登录

### 13.2 OpenTelemetry（OTel）
- **定义**: 可观测性标准框架
- **用途**: 收集应用的指标、日志和追踪数据

---

## 十四、P 类术语

### 14.1 PKCE（Proof Key for Code Exchange）
- **定义**: OAuth 2.0 的安全扩展
- **目的**: 防止授权码被截获

### 14.2 Prefetch（预取）
- **定义**: 提前加载可能需要的数据
- **应用**: Claude Code 启动时并行预取配置

### 14.3 Prompt（提示词）
- **定义**: 发送给 AI 模型的文本指令
- **说明**: 系统提示词决定了 AI 的行为方式

### 14.4 Pub/Sub（发布/订阅）
- **定义**: 一种消息传递模式
- **说明**: 发布者发送消息，订阅者接收通知

---

## 十五、Q 类术语

### 15.1 QueryEngine（查询引擎）
- **定义**: Claude Code 的核心引擎
- **功能**: 管理对话生命周期和工具调用循环
- **源码**: `src/QueryEngine.ts`

---

## 十六、R 类术语

### 16.1 React
- **定义**: Facebook 开发的 UI 库
- **说明**: 用于声明式构建用户界面
- **应用**: Claude Code 用它（通过 Ink）渲染终端 UI

### 16.2 REPL（Read-Eval-Print Loop）
- **定义**: 读取-执行-打印循环
- **说明**: 交互式命令行环境

### 16.3 ripgrep（rg）
- **定义**: 超快的代码搜索工具
- **应用**: GrepTool 基于它实现

---

## 十七、S 类术语

### 17.1 SSE（Server-Sent Events）
- **定义**: 服务器向客户端推送事件的 Web 技术

### 17.2 Stream（流）
- **定义**: 数据分块传输的方式
- **应用**: Claude Code 用流式响应实现打字机效果

### 17.3 Store
- **定义**: 状态容器
- **说明**: Claude Code 的 createStore 只有 34 行代码
- **源码**: `src/state/store.ts`

---

## 十八、T 类术语

### 18.1 Token
- **定义**: AI 模型处理文本的基本单位
- **换算**: 约 4 个字符 = 1 个 token

### 18.2 Tool（工具）
- **定义**: Claude Code 中执行特定操作的模块
- **示例**: BashTool、FileReadTool

### 18.3 Tool Use（工具调用）
- **定义**: AI 模型通过结构化请求调用外部工具的机制

### 18.4 TypeScript
- **定义**: JavaScript 的超集，添加了类型系统
- **说明**: Claude Code 的主编程语言

---

## 十九、V 类术语

### 19.1 Virtual Scroll（虚拟滚动）
- **定义**: 只渲染视口内的元素
- **目的**: 优化长列表性能

---

## 二十、W 类术语

### 20.1 WebSocket
- **定义**: 全双工通信协议
- **应用**: Bridge 系统的 v1 传输层使用

### 20.2 Worker
- **定义**: 多 Agent 系统中执行具体任务的子 Agent

---

## 二十一、Y 类术语

### 21.1 Yoga
- **定义**: Facebook 的 Flexbox 布局引擎
- **应用**: Ink 用它计算终端中的组件布局

---

## 二十二、Z 类术语

### 22.1 Zod
- **定义**: TypeScript 的运行时数据验证库
- **应用**: Claude Code 用它定义工具的输入 Schema

---

## 二十三、关联文件

- [roadmap.md](roadmap.md) - 学习路线图
- [../part01-basics/01-what-is-claude-code.md](../part01-basics/01-what-is-claude-code.md) - 开始学习

---

*此细纲由 Claude Code 自动生成*
