# 06-vim-mode.md 细纲

## 一、标题层级结构

### 1. Vim 模式实现——状态机详解
- 学习目标（5点）
- Vim 编辑模式简介
  - 生活类比：遥控器的模式切换
- 状态机类型系统
  - VimState: INSERT | NORMAL
  - CommandState 11 种子状态
- 状态转换图
- 核心类型详解
  - Operator: delete/change/yank
  - Motion: h/l/w/b/e/0/^/$
  - Text Object: inner/around + w/"/(/[/{
- 转换函数：状态机的"引擎"
  - transition()
  - fromIdle / fromCount / fromOperator
- Dot Repeat（点重复）
  - RecordedChange
  - PersistentState
- 追踪完整操作：d2w
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **VimState 顶层状态**
   - INSERT: 记录 insertedText（用于 dot-repeat）
   - NORMAL: command 状态机

2. **CommandState 11 种子状态**
   - idle: 等待输入
   - count: 输入数字前缀
   - operator: 等待动作
   - operatorCount: 操作符+数字
   - operatorFind: 操作符+查找
   - operatorTextObj: 操作符+文本对象
   - find: f/F/t/T 查找
   - g: g 前缀
   - operatorG: 操作符+g
   - replace: r 替换
   - indent: >/< 缩进

3. **核心类型**
   - Operator: 'delete' | 'change' | 'yank'
   - Motion: h/l/j/k/w/b/e/W/B/E/0/^/$
   - TextObjScope: 'inner' | 'around'
   - TextObjType: w/W/"/'/`/(/)b/[/]/{/}/B/</>

4. **组合示例**
   - dw: delete + word
   - 3dw: 3 × delete word
   - ci": change + inner + "
   - yy: yank + line
   - d$: delete + $

5. **transition() 函数**
   - 纯函数状态转换
   - 返回 { next?, execute? }

6. **Dot Repeat**
   - RecordedChange 记录操作
   - . 键重放
   - PersistentState 跨命令保持

7. **持久化状态**
   - lastChange: 上次修改
   - lastFind: 上次查找
   - register: 寄存器内容
   - registerIsLinewise: 是否整行

## 三、源码文件路径

- `vim/types.ts` - Vim 类型定义
- `vim/transitions.ts` - 状态转换函数
- `vim/operators.ts` - 操作符实现
- `hooks/useVimInput.ts` - Vim 输入处理

## 四、类名、函数名、接口名

### 类型
- `VimState` - 顶层状态
- `CommandState` - 命令状态
- `Operator` - 操作符类型
- `RecordedChange` - 记录的改变
- `PersistentState` - 持久化状态
- `FindType` - 查找类型
- `TextObjScope` - 文本对象范围

### 核心函数
- `transition()` - 状态转换
- `fromIdle()` / `fromCount()` / `fromOperator()` - 各状态处理
- `executeOperatorMotion()` - 执行操作符+动作
- `resolveMotion()` - 解析动作

### 常量
- `OPERATORS` - 操作符映射
- `SIMPLE_MOTIONS` - 简单动作集合
- `TEXT_OBJ_SCOPES` - 文本对象范围
- `TEXT_OBJ_TYPES` - 文本对象类型
- `FIND_KEYS` - 查找键集合
- `MAX_VIM_COUNT` = 10000
