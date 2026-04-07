# 第 2 课：编程基础——终端、命令行与开发环境 - 细纲

## 文件信息
- **原文件**: part01-basics/02-programming-basics.md
- **类型**: 基础入门
- **难度**: ★☆☆☆☆

---

## 一、什么是终端（Terminal）？

### 1.1 GUI vs CLI
- **GUI（图形用户界面）**: 桌面、图标、窗口
- **CLI（命令行界面）**: 文本命令操作

### 1.2 为什么程序员用终端？
| 原因 | 解释 |
|------|------|
| 更快 | 熟练后打字比点鼠标快 |
| 更强大 | 很多操作只能在终端完成 |
| 可自动化 | 命令可以写成脚本 |
| 远程操作 | 连接远程服务器 |
| Claude Code 运行于此 | 命令行工具 |

### 1.3 打开终端
- **macOS**: `Cmd + 空格`，输入 "Terminal"
- **Windows**: `Win + R`，输入 "cmd" 或 "powershell"
- **Linux**: `Ctrl + Alt + T`

---

## 二、基本终端命令

### 2.1 核心命令速查表
| 命令 | 作用 | 示例 |
|------|------|------|
| `pwd` | 显示当前目录 | `pwd` |
| `ls` | 列出文件 | `ls -la` |
| `cd` | 切换目录 | `cd src/` |
| `mkdir` | 创建目录 | `mkdir new-folder` |
| `cat` | 查看文件 | `cat README.md` |
| `touch` | 创建空文件 | `touch index.ts` |
| `rm` | 删除文件 | `rm temp.txt` |
| `cp` | 复制 | `cp a.txt b.txt` |
| `mv` | 移动/重命名 | `mv old.txt new.txt` |
| `clear` | 清屏 | `clear` |
| `echo` | 输出文本 | `echo "hello"` |

---

## 三、文件系统和路径

### 3.1 绝对路径 vs 相对路径
- **绝对路径**: 从根目录 `/` 开始
  - 例: `/Users/zhangsan/projects/claude-code-main/src/main.tsx`
- **相对路径**: 从当前位置开始
  - 例: `src/main.tsx`

### 3.2 特殊路径符号
| 符号 | 含义 | 示例 |
|------|------|------|
| `.` | 当前目录 | `./src/main.tsx` |
| `..` | 上一级目录 | `cd ..` |
| `~` | 用户主目录 | `cd ~/Desktop` |
| `/` | 根目录 | `cd /` |

---

## 四、环境变量

### 4.1 概念
环境变量 = 全局配置信息，所有程序都能读取

### 4.2 常用操作
```bash
# 查看 HOME 变量
echo $HOME

# 查看 PATH 变量
echo $PATH

# 设置环境变量
export MY_NAME="zhangsan"
echo $MY_NAME
```

### 4.3 Claude Code 中的应用
```typescript
// 当 USER_TYPE 环境变量是 'ant' 时，才加载 REPL 工具
const REPLTool =
  process.env.USER_TYPE === 'ant'
    ? require('./tools/REPLTool/REPLTool.js').REPLTool
    : null
```

---

## 五、包管理器

### 5.1 概念
- **代码包** = 乐高积木套装
- **包管理器** = 乐高商店
- **package.json** = 购物清单

### 5.2 常见包管理器
| 包管理器 | 用于 | 安装命令示例 |
|----------|------|-------------|
| npm | JavaScript/TypeScript | `npm install react` |
| pnpm | JavaScript/TypeScript | `pnpm install react` |
| yarn | JavaScript/TypeScript | `yarn add react` |
| pip | Python | `pip install numpy` |

### 5.3 Claude Code 使用的关键包
```typescript
import chalk from 'chalk'                    // 终端文字颜色
import React from 'react'                    // UI 框架
import { Command } from '@commander-js/extra-typings'  // 命令行解析
```

---

## 六、Git 版本控制

### 6.1 核心概念
| 概念 | 解释 | 类比 |
|------|------|------|
| 仓库 (Repository) | 被 Git 管理的项目文件夹 | 带修订记录的笔记本 |
| 提交 (Commit) | 一次代码修改的"快照" | 笔记本中的一页记录 |
| 分支 (Branch) | 代码的独立发展线 | 故事的平行时间线 |
| 合并 (Merge) | 把两条分支合在一起 | 时间线汇合 |
| 远程仓库 (Remote) | 代码在云端备份 | 云端备份 |

### 6.2 常用 Git 命令
```bash
git status          # 查看当前状态
git diff            # 查看修改内容
git add .           # 添加到暂存区
git commit -m "修复bug"  # 提交修改
git log --oneline   # 查看提交历史
git checkout -b feature/new-login  # 创建新分支
git checkout main   # 切换到已有分支
```

---

## 七、IDE（集成开发环境）

### 7.1 IDE vs 普通文本编辑器
| 功能 | 普通编辑器 | IDE |
|------|---------------|-----|
| 写文字 | ✅ | ✅ |
| 语法高亮 | ❌ | ✅ |
| 自动补全 | ❌ | ✅ |
| 错误检测 | ❌ | ✅ |
| 内置终端 | ❌ | ✅ |
| Git 集成 | ❌ | ✅ |
| 调试工具 | ❌ | ✅ |

### 7.2 推荐的 IDE
| IDE | 特点 | 适合 |
|-----|------|------|
| VS Code | 微软出品，免费，插件丰富 | 通用开发 |
| Cursor | 基于 VS Code，深度集成 AI | AI 辅助开发 |
| WebStorm | JetBrains 出品，功能强大 | 专业前端/Node.js |

---

## 八、关联文件

### 8.1 上一章
- [01-what-is-claude-code.md](01-what-is-claude-code.md)

### 8.2 下一章
- [03-typescript-basics.md](03-typescript-basics.md) - TypeScript 基础

---

*此细纲由 Claude Code 自动生成*
