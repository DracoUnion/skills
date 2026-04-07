# 05-text-input.md 细纲

## 一、标题层级结构

### 1. 输入框设计——TextInput 与多行编辑
- 学习目标（5点）
- 终端输入框 ≠ 浏览器输入框
  - 生活类比：手动排版 vs Word
- 架构总览
  - TextInput / BaseTextInput / useTextInput / Cursor
- useTextInput：输入处理的核心
  - Cursor 类管理文本和光标
  - 特殊按键处理
- Cursor 类：文本操作的瑞士军刀
  - 不可变模式
- 双击安全机制
  - useDoublePress
  - Ctrl+C / Escape 双击退出
- Kill Ring：Emacs 风格剪贴板
  - Ctrl+K / Ctrl+U / Ctrl+Y / Alt+Y
- 语音录制的波形光标
  - BARS 字符
  - EMA 指数移动平均
- 多行编辑
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **架构分层**
   - TextInput: 顶层组件
   - BaseTextInput: 渲染层
   - useTextInput: 逻辑层
   - Cursor: 文本+光标操作

2. **Cursor 类**
   - 不可变模式（每次返回新实例）
   - moveLeft/Right/Up/Down
   - moveToLineStart/End
   - moveWordForward/Backward
   - insert / del / backspace
   - deleteToLineEnd/Start
   - deleteWordBefore

3. **双击安全机制**
   - 第一次：显示提示
   - 第二次（时间窗口内）：执行退出
   - 超时：清空输入

4. **Kill Ring**
   - Ctrl+K: 删到行尾 → push
   - Ctrl+U: 删到行首 → push
   - Ctrl+W/Alt+Backspace: 删单词 → push
   - Ctrl+Y: 粘贴（pop 最近）
   - Alt+Y: 轮转（pop 更早）

5. **波形光标**
   - BARS = ' ▁▂▃▄▅▆▇█'
   - EMA 平滑: `smoothed * SMOOTH + target * (1 - SMOOTH)`
   - 静默时灰色，有声音时彩虹色

6. **多行编辑**
   - multiline=true: Enter 插入换行
   - 上下方向键在行间移动
   - 视口自动滚动

## 三、源码文件路径

- `hooks/useTextInput.ts` - 输入处理 Hook
- `components/TextInput.tsx` - 输入框组件
- `components/BaseTextInput.tsx` - 基础输入框
- `cursor/Cursor.ts` - Cursor 类
- `hooks/useDoublePress.ts` - 双击检测

## 四、类名、函数名、接口名

### 核心 Hook
- `useTextInput()` - 输入处理 Hook
- `useDoublePress()` - 双击检测 Hook

### Cursor 类
- `Cursor.fromText()` - 从文本创建
- `moveLeft()` / `moveRight()` - 左右移动
- `moveUp()` / `moveDown()` - 上下移动
- `moveToLineStart()` / `moveToLineEnd()` - 行首行尾
- `moveWordForward()` / `moveWordBackward()` - 单词移动
- `insert()` - 插入文本
- `del()` / `backspace()` - 删除
- `deleteToLineEnd()` / `deleteToLineStart()` - 删除到行尾/行首
- `deleteWordBefore()` - 删除前一个单词

### Kill Ring
- `pushToKillRing()` - 推入 Kill Ring
- `getLastKill()` - 获取最近删除
- `yank()` - 粘贴

### 常量
- `BARS` = ' ▁▂▃▄▅▆▇█'
- `SMOOTH` - EMA 平滑系数
- `SILENCE_THRESHOLD` = 0.15
- `LEVEL_BOOST` - 音量增强
