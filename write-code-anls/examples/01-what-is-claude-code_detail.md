# 第 1 课：什么是 Claude Code？ - 细纲

## 文件信息
- **原文件**: part01-basics/01-what-is-claude-code.md
- **类型**: 基础入门
- **难度**: ★☆☆☆☆

---

## 一、什么是 AI 编程助手？

### 1.1 生活类比：工程师搭档
- **你的代码项目** = 正在装修的房子
- **代码文件** = 房子里的各个房间
- **AI 编程助手** = 工程师搭档
- **自然语言指令** = 对工程师说的话

### 1.2 AI 编程助手的三种等级
1. **代码补全工具**（像"自动填词"）
   - 例：GitHub Copilot 的行内补全
   
2. **对话式编程助手**（像"编程顾问"）
   - 例：ChatGPT
   
3. **自主编程代理**（像"编程搭档"）
   - **Claude Code 就是这个等级**
   - 能直接操作电脑：编辑文件、运行命令、搜索代码

---

## 二、Claude Code 的核心能力

### 2.1 四大核心能力
| 能力 | 说明 | 示例 |
|------|------|------|
| **编辑文件** | 直接读取和修改代码文件 | "帮我把 login 函数的错误提示改成中文" |
| **运行命令** | 在终端执行命令 | "运行一下测试看看有没有问题" |
| **搜索代码** | 快速搜索和定位代码 | "找一下项目里所有处理用户认证的代码" |
| **协调工作流** | 编排复杂多步骤任务 | "修复这个 bug，然后提交一个 PR" |

### 2.2 与其他工具的区别
| 特性 | ChatGPT | GitHub Copilot | Claude Code |
|------|---------|----------------|-------------|
| 交互方式 | 网页对话 | 编辑器内嵌 | 命令行终端 |
| 操作文件 | ❌ 不能 | ⚠️ 有限 | ✅ 直接读写 |
| 运行命令 | ❌ 不能 | ❌ 不能 | ✅ 执行终端命令 |
| 搜索代码 | ❌ 不能 | ⚠️ 有限 | ✅ 全项目搜索 |
| 工作模式 | 一问一答 | 行内补全 | 自主代理（Agent） |
| 上下文范围 | 对话窗口 | 当前文件 | 整个项目 |

---

## 三、为什么学习 Claude Code 源码？

### 3.1 四大学习价值
1. **理解 AI 编程代理的工作原理**
   - AI 如何与人类协作
   - Agent 系统设计
   - 工具调用机制
   - 权限控制实现

2. **学习工业级 TypeScript 项目**
   - 大型项目目录结构
   - TypeScript 类型系统高级用法
   - React 组件化设计模式
   - 异步编程最佳实践

3. **掌握前沿技术栈**
   - TypeScript + Bun + React/Ink
   - Commander.js + Zod + MCP
   - OpenTelemetry + GrowthBook

4. **培养读代码能力**
   - 阅读代码时间远多于编写代码

### 3.2 技术栈一览
| 技术 | 用途 |
|------|------|
| TypeScript | 主编程语言 |
| Bun | JavaScript/TypeScript 运行时 |
| React + Ink | 终端 UI 渲染 |
| Commander.js | 命令行参数解析 |
| Zod v4 | 运行时数据验证 |
| ripgrep | 代码搜索 |
| MCP SDK | 模型上下文协议 |
| Anthropic SDK | 与 Claude AI 通信 |
| OpenTelemetry | 可观测性 |
| GrowthBook | 特性开关管理 |
| OAuth/JWT | 认证和授权 |

---

## 四、项目规模统计

### 4.1 核心数据
```
📊 项目统计
├── 源码文件总数：    1,902 个
├── 代码总行数：      512,685+ 行
├── 主要语言：        TypeScript (.ts / .tsx)
├── 一级子目录：      36 个功能模块
├── 工具（Tools）：    43 个 AI 可调用的工具
├── 命令（Commands）：101 个斜杠命令
├── UI 组件：         144 个 React/Ink 组件
└── React Hooks：     85 个自定义 Hook
```

---

## 五、源码对应关系

### 5.1 核心文件
| 文件 | 作用 |
|------|------|
| `src/main.tsx` | 程序入口，CLI 解析 |
| `src/Tool.ts` | 工具类型定义 |
| `src/tools.ts` | 工具注册中心 |

### 5.2 关键类/函数
- `QueryEngine` 类 - 查询引擎核心
- `getAllBaseTools()` - 获取所有工具
- `buildTool()` - 工具工厂函数

---

## 六、动手练习

### 6.1 练习 1：感受项目规模
```bash
# 进入项目目录
cd /path/to/claude-code-main

# 查看 src 目录下有多少个子目录
ls src/

# 统计源码文件总数
find src -type f | wc -l

# 统计代码总行数
find src -type f -exec cat {} + | wc -l
```

### 6.2 练习 2：浏览核心文件
- `main.tsx` - 入口文件
- `Tool.ts` - 工具类型定义
- `tools.ts` - 工具注册

### 6.3 思考题
- `.tsx` 后缀意味着什么？
- `Tool.ts` 中有多少个 `type` 或 `interface`？
- `tools.ts` 中导入了多少个不同的工具？

---

## 七、关联文件

### 7.1 上一章
- [../part00-preface/README.md](../part00-preface/README.md) - 前言

### 7.2 下一章
- [02-programming-basics.md](02-programming-basics.md) - 编程基础

---

*此细纲由 Claude Code 自动生成*
