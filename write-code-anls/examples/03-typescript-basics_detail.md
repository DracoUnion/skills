# 第 3 课：TypeScript 快速入门 - 细纲

## 文件信息
- **原文件**: part01-basics/03-typescript-basics.md
- **类型**: 基础入门
- **难度**: ★★☆☆☆

---

## 一、JavaScript vs TypeScript

### 1.1 为什么需要类型
- **无类型问题**: 参数类型不明确，运行时才发现错误
- **类型好处**: 提前发现错误、代码提示、代码即文档、重构安全
- **Claude Code 实践**: 1,900 个源码文件全部使用 TypeScript

### 1.2 生活类比
- JavaScript = 没有标签的收纳箱
- TypeScript = 贴好标签的收纳箱

---

## 二、基本类型

### 2.1 原始类型
| 类型 | 示例 | 说明 |
|------|------|------|
| `string` | `"Claude Code"` | 字符串 |
| `number` | `1902`, `3.14` | 数字（整数和小数） |
| `boolean` | `true`, `false` | 布尔值 |
| `null` | `null` | 空值 |
| `undefined` | `undefined` | 未定义 |

### 2.2 数组类型
```typescript
let tools: string[] = ["BashTool", "FileReadTool", "GrepTool"]
let tools2: Array<string> = [...]  // 另一种写法
```

### 2.3 对象类型
```typescript
let user: { name: string; age: number } = { name: "张三", age: 25 }
let config: { debug: boolean; verbose?: boolean }  // ? 表示可选
```

### 2.4 联合类型
```typescript
type ValidationResult =
  | { result: true }
  | { result: false; message: string; errorCode: number }
```
- **源码来源**: `src/Tool.ts` 中的真实类型定义

---

## 三、接口（interface）和类型别名（type）

### 3.1 type（类型别名）
```typescript
type ToolInputJSONSchema = {
  [x: string]: unknown    // 索引签名：任意属性
  type: 'object'          // 必须包含 type 属性
  properties?: { ... }    // 可选属性
}
```
- **源码来源**: `src/Tool.ts` 第 15-21 行

### 3.2 interface（接口）
```typescript
interface Animal {
  name: string
  sound: string
  legs: number
}
```

### 3.3 type vs interface
| 特性 | type | interface |
|------|------|-----------|
| 描述对象 | ✅ | ✅ |
| 联合类型 | ✅ | ❌ |
| 继承/扩展 | `&` 运算符 | `extends` 关键字 |
| Claude Code 使用 | 大量使用 | 少量使用 |

---

## 四、函数和箭头函数

### 4.1 普通函数
```typescript
function add(a: number, b: number): number {
  return a + b
}
```

### 4.2 箭头函数
```typescript
const add = (a: number, b: number): number => a + b
```

### 4.3 Claude Code 中的真实示例
```typescript
export const getEmptyToolPermissionContext: () => ToolPermissionContext =
  () => ({
    mode: 'default',
    additionalWorkingDirectories: new Map(),
    // ...
  })
```
- **源码来源**: `src/Tool.ts`

---

## 五、模块系统（import / export）

### 5.1 export（导出）
```typescript
// 具名导出
export function add(a: number, b: number): number { ... }
export const PI = 3.14159

// 默认导出
export default function multiply(a: number, b: number): number { ... }
```

### 5.2 import（导入）
```typescript
import { add, PI } from './utils/math.js'        // 具名导入
import multiply from './utils/math.js'          // 默认导入
import type { User } from './types/user.js'     // 类型导入
```

### 5.3 Claude Code 中的真实 import
```typescript
import { toolMatchesName, type Tool, type Tools } from './Tool.js'
import { AgentTool } from './tools/AgentTool/AgentTool.js'
import chalk from 'chalk'  // 第三方包
```
- **源码来源**: `src/tools.ts` 文件开头

### 5.4 路径规则
| 路径形式 | 含义 | 示例 |
|----------|------|------|
| `'./file.js'` | 相对路径，项目内文件 | `'./Tool.js'` |
| `'chalk'` | 包名称，node_modules | `'chalk'` |
| `'bun:bundle'` | Bun 运行时内置模块 | `'bun:bundle'` |

---

## 六、async/await 异步编程

### 6.1 同步 vs 异步
- **同步**: 阻塞等待，完成后才继续
- **异步**: 非阻塞，等待期间可做其他事

### 6.2 async/await 语法
```typescript
async function readFile(path: string): Promise<string> {
  const content = await fs.readFile(path, 'utf-8')
  return content
}
```

### 6.3 Promise
```typescript
async function getGreeting(): Promise<string> {
  return "你好，世界！"
}
```

### 6.4 Claude Code 中的异步方法
```typescript
// Tool.ts 中的异步方法签名
call(args: z.infer<Input>, ...): Promise<ToolResult<Output>>
description(input: z.infer<Input>, ...): Promise<string>
checkPermissions(...): Promise<PermissionResult>
```
- **源码来源**: `src/Tool.ts`

---

## 七、泛型基础

### 7.1 什么是泛型
泛型 = 类型的"占位符"，使用时再指定具体类型

```typescript
function box<T>(item: T): { content: T } {
  return { content: item }
}

box<string>("hello")   // T = string
box<number>(42)        // T = number
```

### 7.2 Claude Code 中的泛型示例
```typescript
export type Tool<
  Input extends AnyObject = AnyObject,    // 输入类型
  Output = unknown,                        // 输出类型
  P extends ToolProgressData = ToolProgressData,  // 进度数据类型
> = {
  name: string
  call(args: z.infer<Input>, ...): Promise<ToolResult<Output>>
  // ...
}
```
- **源码来源**: `src/Tool.ts` 核心类型定义

---

## 八、条件导入和动态导入

### 8.1 条件导入示例
```typescript
import { feature } from 'bun:bundle'

const SleepTool =
  feature('PROACTIVE') || feature('KAIROS')
    ? require('./tools/SleepTool/SleepTool.js').SleepTool
    : null

const REPLTool =
  process.env.USER_TYPE === 'ant'
    ? require('./tools/REPLTool/REPLTool.js').REPLTool
    : null
```
- **源码来源**: `src/tools.ts`

### 8.2 为什么要条件导入
- **死代码消除**（Dead Code Elimination）
- 普通用户不需要的功能不加载
- 不同部署环境需要不同功能组合
- 减小产物体积，加快启动速度

---

## 九、小结

| 概念 | 要点 |
|------|------|
| TypeScript | JavaScript + 类型系统，提前发现错误 |
| 基本类型 | `string`、`number`、`boolean`、`array`、`object` |
| type / interface | 给复杂类型"起名字" |
| 箭头函数 | `(x: number) => x * 2` |
| import / export | 文件间代码引用 |
| async / await | 异步编程，非阻塞 |
| 泛型 | 类型占位符 `<T>` |
| 条件导入 | 根据条件加载模块，优化体积 |

---

## 十、动手练习

### 练习 1：基本类型练习
创建 `practice.ts`，练习变量声明和类型定义。

### 练习 2：阅读 Tool.ts
打开 `src/Tool.ts`，理解：
- `ToolInputJSONSchema`（第 15-21 行）
- `ValidationResult`（第 95-101 行）
- `Tool<Input, Output, P>`（第 362 行开始）

### 练习 3：分析 import 语句
阅读 `src/tools.ts` 前 15 行，回答：
1. `'./Tool.js'` 中的 `./` 表示什么？
2. `type Tool` 前为什么有 `type` 关键字？
3. `toolMatchesName` 没有 `type` 意味着什么？

### 练习 4：理解条件导入
分析 `src/tools.ts` 中的条件导入代码，理解 `feature()` 和 `require()` 的用法。

---

## 十一、关联文件

### 11.1 上一章
- [02-programming-basics.md](02-programming-basics.md) - 编程基础

### 11.2 下一章
- [04-react-and-ink.md](04-react-and-ink.md) - React 与 Ink

---

*此细纲由 Claude Code 自动生成*
