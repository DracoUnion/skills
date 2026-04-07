# 06-search-tools.md 细纲

## 一、标题层级结构

### 1. GrepTool 与 GlobTool —— 代码搜索利器
- 学习目标（5点）
- 生活类比：图书馆的两种找书方式
- GrepTool 架构全景
- GrepTool 源码深度解析
  - 输入参数设计
  - VCS 目录排除
  - 三种输出模式详解
  - head_limit 分页机制
- GlobTool 源码深度解析
  - 简洁的输入设计
  - 结果限制与截断
- 两者的共同基因
- 搜索工具对比表
- 条件加载机制
- GrepTool 的 Prompt 设计
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **GrepTool 输出模式**
   - `content`: 显示匹配行内容（带行号、上下文）
   - `files_with_matches`: 只显示文件路径（按修改时间排序）
   - `count`: 显示每个文件的匹配数

2. **head_limit 机制**
   - 默认值：250
   - `head_limit=0` 表示不限制（逃生口）
   - 只在真正截断时才报告 appliedLimit

3. **GlobTool 限制**
   - 默认限制 100 个文件
   - 超出时标记 truncated

4. **条件加载**
   - `hasEmbeddedSearchTools()` 为 true 时跳过 GlobTool/GrepTool
   - 内嵌搜索工具更快时使用 Shell 别名

## 三、源码文件路径

- `src/tools/GrepTool/GrepTool.ts` - Grep 工具
- `src/tools/GlobTool/GlobTool.ts` - Glob 工具
- `src/tools/GrepTool/prompt.ts` - GrepTool 提示词
- `src/utils/ripgrep.ts` - ripgrep 封装

## 四、类名、函数名、接口名

### GrepTool
- `call()` - 执行搜索（第 233-240 行）
- `checkPermissions()` - 权限检查
- `applyHeadLimit()` - 应用 head_limit（第 106-128 行）
- `VCS_DIRECTORIES_TO_EXCLUDE` - VCS 排除目录（第 94-102 行）
- `DEFAULT_HEAD_LIMIT` - 默认限制 250（第 106 行）

### GlobTool
- `call()` - 执行 glob 搜索（第 154-176 行）
- `mapToolResultToToolResultBlockParam()` - 结果映射（第 177-197 行）
- `glob()` - glob 库调用

### 常量
- `VCS_DIRECTORIES_TO_EXCLUDE` - ['.git', '.svn', '.hg', '.bzr', '.jj', '.sl']
- `DEFAULT_HEAD_LIMIT` = 250
- `maxResultSizeChars` = 20_000

### 类型
- `Output` - 输出类型定义
- `GrepInput` - Grep 输入参数
- `GlobInput` - Glob 输入参数

### 函数
- `ripGrep()` - ripgrep 调用（utils/ripgrep.ts）
- `toRelativePath()` - 路径相对化
- `checkReadPermissionForTool()` - 读取权限检查
