# 05-file-tools.md 细纲

## 一、标题层级结构

### 1. FileReadTool 与 FileEditTool —— 文件操作双雄
- 学习目标（5点）
- 生活类比：图书馆的借阅与修改
- FileReadTool 架构
  - 输入参数
  - 文本文件读取
  - 图片处理：Token 预算压缩
- 文件去重（Dedup）机制
- 安全防护
  - 被阻止的设备文件
  - 恶意代码防护
- FileEditTool 的精确替换
  - 核心设计："搜索并替换"
  - "先读后改"强制约束
  - 并发修改检测
  - 引号智能匹配
- 写入文件后的通知链
- FileWriteTool vs FileEditTool 对比
- maxResultSizeChars 策略对比
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **FileReadTool 多格式支持**
   - 文本文件：行号 + 范围读取
   - 图片：压缩 + Token 预算
   - PDF：页面提取
   - Notebook：cells 数组

2. **文件去重机制**
   - 缓存 key: `file_path + offset + limit`
   - 检查 mtime 判断文件是否变化
   - 返回 `file_unchanged` 存根节省 token

3. **FileEditTool 安全模型**
   - 必须先读取才能编辑
   - `old_string` 必须唯一匹配
   - mtime 检测并发修改
   - 引号自动适配（直引号/弯引号）

4. **通知链**
   - 写入文件 → 通知 LSP → 通知 VSCode → 更新缓存

## 三、源码文件路径

- `src/tools/FileReadTool/FileReadTool.ts` - 文件读取工具
- `src/tools/FileEditTool/FileEditTool.ts` - 文件编辑工具
- `src/tools/FileWriteTool/FileWriteTool.ts` - 文件写入工具

## 四、类名、函数名、接口名

### FileReadTool
- `readFileInRange()` - 按行范围读取文件（第 1019-1028 行）
- `readImageWithTokenBudget()` - Token 预算图片读取（第 1097-1183 行）
- `readFileState` - 文件状态缓存 Map
- `BLOCKED_DEVICE_PATHS` - 被阻止的设备文件（第 98-115 行）
- `CYBER_RISK_MITIGATION_REMINDER` - 恶意代码防护提醒（第 729-730 行）

### FileEditTool
- `validateInput()` - 输入验证（第 137 行）
- `checkPermissions()` - 权限检查
- `call()` - 执行编辑
- `writeTextContent()` - 写入文本内容（第 491-517 行）
- `findActualString()` - 引号智能匹配（第 316-327 行）
- `preserveQuoteStyle()` - 保留引号风格

### 常量
- `maxResultSizeChars: Infinity` - FileReadTool 永不持久化
- `maxResultSizeChars: 100_000` - FileEditTool 100KB 限制

### 类型
- `FileStateCache` - 文件状态缓存类型
- `FileState` - 文件状态对象
- `ImageResult` - 图片读取结果
