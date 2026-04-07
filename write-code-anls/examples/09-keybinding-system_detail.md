# 09-keybinding-system.md 细纲

## 一、标题层级结构

### 1. 键盘绑定系统——快捷键优先级与 Chord
- 学习目标（5点）
- 问题：一个按键，多种含义
  - 生活类比：办公大楼的门禁卡
- 绑定声明：defaultBindings
  - Global / Chat / Autocomplete / Settings / Confirmation
- 上下文优先级
- resolveKey：匹配算法
  - buildKeystroke
  - matchesBinding
- Chord：组合键序列
  - chord_started / chord_cancelled
  - chordPrefixMatches
- 平台适配
  - IMAGE_PASTE_KEY
  - MODE_CYCLE_KEY
- 修饰键的等价性
  - Alt ≡ Meta
- 完整的按键处理流程
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **多上下文绑定**
   - Global: 全局
   - Chat: 聊天界面
   - Autocomplete: 自动补全
   - Settings: 设置面板
   - Confirmation: 确认对话框

2. **上下文优先级**
   - 按上下文顺序查找
   - 最后一个匹配的胜出
   - 支持用户覆盖

3. **resolveKey 匹配**
   - 只查单键绑定（chord 由 resolveChord 处理）
   - 必须在活跃上下文中
   - 返回: match / none / unbound

4. **Chord 组合键**
   - 顺序按下的多个键
   - 如: Ctrl+X Ctrl+K
   - 状态: chord_started / chord_cancelled

5. **平台适配**
   - Windows: Ctrl+V 系统粘贴，用 Alt+V
   - Windows 老版本: Shift+Tab 不支持，用 Meta+M

6. **修饰键等价**
   - Alt ≡ Meta（终端无法区分）
   - Super(Cmd/Win) 独立

7. **按键处理流程**
   - stdin → parseMultipleKeypresses → Chord? → resolveChord/resolveKey → 执行

## 三、源码文件路径

- `keybindings/defaultBindings.ts` - 默认绑定
- `keybindings/resolver.ts` - 解析器
- `keybindings/reservedShortcuts.ts` - 保留快捷键

## 四、类名、函数名、接口名

### 核心函数
- `resolveKey()` - 解析按键
- `resolveChord()` - 解析 Chord
- `buildKeystroke()` - 构建按键描述
- `matchesBinding()` - 匹配绑定
- `chordPrefixMatches()` - Chord 前缀匹配
- `keystrokesEqual()` - 按键相等比较

### 类型
- `KeybindingBlock` - 绑定块
- `ParsedBinding` - 解析后的绑定
- `ParsedKeystroke` - 解析后的按键
- `ResolveResult` - 解析结果
- `ChordResolveResult` - Chord 解析结果

### 常量
- `DEFAULT_BINDINGS` - 默认绑定数组
- `IMAGE_PASTE_KEY` - 图片粘贴键
- `MODE_CYCLE_KEY` - 模式切换键
- `SUPPORTS_TERMINAL_VT_MODE` - 是否支持 VT 模式

### 辅助函数
- `getKeyName()` - 获取键名
- `getBindingDisplayText()` - 获取绑定显示文本
