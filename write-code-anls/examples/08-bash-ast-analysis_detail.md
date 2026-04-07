# 08-bash-ast-analysis.md 细纲

## 一、标题层级结构

### 1. BashTool 的 AST 级命令分析
- 学习目标（5点）
- 生活类比：X 光安检 vs 人眼检查
- AST 解析的三种结果
  - ParseForSecurityResult
- bashToolHasPermission：完整的权限检查流程
- 安全包装器剥离
  - stripSafeWrappers
  - SAFE_WRAPPER_PATTERNS
- 复合命令的安全处理
  - cd + git 组合攻击检查
  - 前缀规则不匹配复合命令
- 只读命令验证的深度防御
  - containsVulnerableUncPath
  - containsUnquotedExpansion
- 变量展开的陷阱
- 子命令数量上限
  - MAX_SUBCOMMANDS_FOR_SECURITY_CHECK
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **AST 解析三种结果**
   - `simple`: 解析成功，干净命令列表
   - `too-complex`: 包含危险结构（命令替换、循环等）
   - `parse-unavailable`: 解析器不可用，降级处理

2. **危险结构检测**
   - 命令替换: `$()` 或反引号
   - 进程替换: `<()` 或 `>()`
   - 花括号/子 Shell 分组
   - for/while/if 控制流

3. **安全包装器剥离**
   - `timeout`: 超时执行
   - `time`: 计时执行
   - `nice`: 调整优先级
   - `nohup`: 后台执行
   - 安全环境变量: NODE_ENV, RUST_BACKTRACE 等

4. **不安全环境变量**
   - `PATH`: 改变命令搜索路径
   - `LD_PRELOAD`: 注入共享库
   - `PYTHONPATH`: 改变 Python 模块加载
   - `NODE_OPTIONS`: 可包含代码执行标志

5. **复合命令安全检查**
   - `cd + git` 组合攻击检查
   - 前缀规则不匹配复合命令
   - 拆分子命令逐个检查

6. **深度防御措施**
   - UNC 路径检查（Windows WebDAV 攻击）
   - 未引用变量展开检查
   - `git -c` 参数检查
   - `$` 变量展开检查

7. **性能保护**
   - 子命令上限 50 个
   - 防止 CPU 饥饿攻击

## 三、源码文件路径

- `src/utils/bash/ast.ts` - AST 解析
- `src/tools/BashTool/bashPermissions.ts` - Bash 权限检查
- `src/tools/BashTool/readOnlyValidation.ts` - 只读命令验证
- `src/tools/BashTool/bashSecurity.ts` - AST 安全分析

## 四、类名、函数名、接口名

### 核心函数
- `parseCommandRaw()` - 原始命令解析
- `parseForSecurityFromAst()` - AST 安全解析
- `bashToolHasPermission()` - Bash 权限检查
- `stripSafeWrappers()` - 剥离安全包装器
- `isCommandReadOnly()` - 判断命令是否只读
- `checkSemantics()` - 检查语义安全性

### 类型
- `ParseForSecurityResult` - AST 解析结果
  - `kind: 'simple' | 'too-complex' | 'parse-unavailable'`
- `SimpleCommand` - 简单命令

### 常量
- `SAFE_WRAPPER_PATTERNS` - 安全包装器正则数组
- `SAFE_ENV_VARS` - 安全环境变量集合
- `READONLY_COMMANDS` - 只读命令数组
- `MAX_SUBCOMMANDS_FOR_SECURITY_CHECK` = 50

### 辅助函数
- `hasEnvVarPrefix()` / `stripEnvVar()` - 环境变量处理
- `hasWrapperPrefix()` / `stripWrapper()` - 包装器处理
- `containsVulnerableUncPath()` - UNC 路径检查
- `containsUnquotedExpansion()` - 未引用展开检查
- `isCommandSafeViaFlagParsing()` - Flag 解析验证
