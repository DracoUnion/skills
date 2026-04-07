# 第9课：MCP 扩展系统与外部集成 - 细纲

## 文件信息
- **原文件**: part02-architecture/09-mcp-extension.md
- **类型**: 架构全景
- **难度**: ★★★★☆

---

## 一、什么是 MCP

### 1.1 生活类比：USB 接口
MCP（Model Context Protocol）就是 AI 模型的"USB 接口"：
- **统一协议**：任何服务只要实现 MCP 协议，就能被 Claude Code 使用
- **即插即用**：配置好就能用，不需要修改 Claude Code 核心代码
- **双向通信**：Claude Code（客户端）和外部服务（服务器）可以互相通信

### 1.2 MCP 生态系统
```
Claude Code（MCP 客户端）
    ←→ MCP 协议 ←→ GitHub 服务器（创建 Issue、PR）
    ←→ MCP 协议 ←→ 数据库服务器（查询数据）
    ←→ MCP 协议 ←→ Jira 服务器（管理任务）
    ←→ MCP 协议 ←→ 自定义服务器（任何功能）
```

---

## 二、MCP 在 Claude Code 中的架构

### 2.1 架构层次
```
配置层（mcp.json / settings.json）
    ↓
客户端层（services/mcp/client.ts）
    ↓
传输层（stdio / SSE / WebSocket）
    ↓
工具层（MCPTool 包装）
    ↓
合并层（assembleToolPool()）
```

---

## 三、MCP 客户端实现

### 3.1 核心导入
**文件**: `src/services/mcp/client.ts`

```typescript
import { Client } from '@modelcontextprotocol/sdk/client/index.js'
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js'
import { SSEClientTransport } from '@modelcontextprotocol/sdk/client/sse.js'
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js'
import {
  CallToolResultSchema,
  ListToolsResultSchema,
  ListPromptsResultSchema,
  ListResourcesResultSchema,
} from '@modelcontextprotocol/sdk/types.js'
```

### 3.2 支持的传输协议
| 传输方式 | 适用场景 | 特点 |
|---------|---------|------|
| stdio | 本地 MCP 服务器 | 最简单，进程间管道 |
| SSE | 远程 HTTP 服务器 | 单向流，兼容性好 |
| Streamable HTTP | 远程 HTTP 服务器 | 双向流，更强大 |
| WebSocket | 实时双向通信 | 最灵活 |

---

## 四、MCP 服务器配置

### 4.1 配置文件结构
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxx"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://..."
      }
    }
  }
}
```

### 4.2 配置加载流程
```
配置来源
├── ~/.claude/settings.json（全局配置）
├── .claude/settings.json（项目配置）
├── --mcp-config 参数（命令行指定）
└── 企业 MDM 策略（管理员配置）
    ↓
parseMcpConfig()（解析配置）
    ↓
filterMcpServersByPolicy()（策略过滤）
    ↓
连接 MCP 服务器
```

---

## 五、MCPTool：将 MCP 工具包装为内置工具

### 5.1 MCPTool 包装器
**文件**: `src/services/mcp/client.ts`

```typescript
// MCPTool 将 MCP 工具包装为标准 Tool 接口
import { MCPTool } from '../../tools/MCPTool/MCPTool.js'
```

### 5.2 MCP 工具的命名约定
```
mcp__{服务器名}__{工具名}

例如：
mcp__github__create_issue
mcp__postgres__query
mcp__jira__create_ticket
```

### 5.3 工具合并流程
**文件**: `src/tools.ts`

```typescript
export function assembleToolPool(
  permissionContext: ToolPermissionContext,
  mcpTools: Tools,
): Tools {
  const builtInTools = getTools(permissionContext)
  const allowedMcpTools = filterToolsByDenyRules(mcpTools, permissionContext)

  // 排序保证 prompt cache 稳定性
  // 内置工具优先（名称冲突时）
  const byName = (a: Tool, b: Tool) => a.name.localeCompare(b.name)
  return uniqBy(
    [...builtInTools].sort(byName).concat(allowedMcpTools.sort(byName)),
    'name',
  )
}
```

### 5.4 工具合并流程图
```
内置工具（BashTool, FileReadTool...）
    ↓
排序 ──┐
       ├──→ 合并去重（uniqBy 'name'）→ 统一工具池
MCP 工具（mcp__github__*, mcp__postgres__*）
    ↓
排序
```

---

## 六、MCP 资源和提示

### 6.1 MCP 三大能力
| 能力 | 说明 | 示例 |
|------|------|------|
| 工具（Tools） | 可执行的操作 | create_issue |
| 资源（Resources） | 可读取的数据 | repo 文件列表 |
| 提示（Prompts） | 预定义的对话模板 | 代码审查模板 |

### 6.2 相关工具
**文件**: 
- `src/tools/ListMcpResourcesTool/ListMcpResourcesTool.ts` — 列出 MCP 服务器提供的资源
- `src/tools/ReadMcpResourceTool/ReadMcpResourceTool.ts` — 读取 MCP 服务器的资源内容

### 6.3 AppState 中的 MCP 状态
**文件**: `src/state/AppStateStore.ts`

```typescript
mcp: {
  clients: MCPServerConnection[],  // 连接的 MCP 服务器
  tools: Tool[],                    // MCP 提供的工具
  commands: Command[],              // MCP 提供的命令（斜杠命令）
  resources: Record<string, ServerResource[]>,  // MCP 资源
  pluginReconnectKey: number,       // 重新连接触发器
}
```

---

## 七、MCP 安全模型

### 7.1 权限控制层次
```
配置级别（哪些服务器被允许连接）
    ↓
策略级别（企业策略过滤服务器）
    ↓
工具级别（filterToolsByDenyRules，按工具名禁止）
    ↓
执行级别（canUseTool 运行时检查）
    ↓
Channel 级别（通道权限控制）
```

### 7.2 MCP 通道权限
**文件**: 
- `src/services/mcp/channelPermissions.ts` — 控制 MCP 服务器的通道访问权限
- `src/services/mcp/channelAllowlist.ts` — MCP 服务器的白名单管理

### 7.3 OAuth 认证
**文件**: 
- `src/services/mcp/auth.ts` — MCP 服务器的 OAuth 认证流程
- `src/tools/McpAuthTool/McpAuthTool.ts` — 处理 MCP 认证的工具

### 7.4 OAuth 认证流程
```
Claude Code → 连接请求 → MCP 服务器
                ← 需要认证 (401)
Claude Code → 发起 OAuth 流程 → OAuth 提供者
                ← 认证令牌
Claude Code → 带令牌重新连接 → MCP 服务器
                ← 连接成功 ✅
```

---

## 八、MCP 与插件系统

### 8.1 插件 + MCP 集成
```
插件（Plugin）
├── 插件的 MCP 服务器（自动连接）
├── 插件命令（斜杠命令）
└── 插件技能（可调用技能）

原生 MCP 服务器
├── MCP 工具
└── MCP 资源

统一管理 ← 合并
```

### 8.2 AppState 中的插件状态
**文件**: `src/state/AppStateStore.ts`

```typescript
plugins: {
  enabled: LoadedPlugin[],   // 已启用的插件
  disabled: LoadedPlugin[],  // 已禁用的插件
  commands: Command[],       // 插件提供的命令
  errors: PluginError[],     // 加载错误
  installationStatus: {      // 安装状态
    marketplaces: [...],
    plugins: [...]
  },
  needsRefresh: boolean,     // 是否需要刷新
}
```

---

## 九、IDE 集成：VSCode SDK MCP

### 9.1 VS Code SDK MCP 服务器
**文件**: `src/services/mcp/vscodeSdkMcp.ts`

让 Claude Code 能够与 VS Code 编辑器交互：
- 获取诊断信息
- 在编辑器中打开文件
- 终端操作

---

## 十、动手练习

### 练习1：配置一个 MCP 服务器
在 `~/.claude/settings.json` 中添加：
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
    }
  }
}
```

### 练习2：探索 MCP 文件结构
浏览 `services/mcp/` 目录：
- [ ] `client.ts` — MCP 客户端主逻辑
- [ ] `config.ts` — 配置解析
- [ ] `types.ts` — 类型定义
- [ ] `auth.ts` — 认证处理
- [ ] `channelPermissions.ts` — 通道权限

### 练习3：追踪 MCP 工具流
从配置到最终被模型使用，MCP 工具经历了哪些步骤？
- [ ] 配置文件 → 解析
- [ ] 连接服务器 → 获取工具列表
- [ ] MCPTool 包装 → 注册
- [ ] assembleToolPool → 合并
- [ ] 模型调用 → 执行

### 思考题
1. MCP 的 stdio 传输方式有什么优缺点？
2. 为什么 MCP 工具名要加 `mcp__` 前缀？
3. 如果 MCP 服务器在查询过程中断开连接，会怎样？

---

## 十一、小结

| 概念 | 说明 | 文件 |
|------|------|------|
| MCP 协议 | AI 工具的标准接口 | `@modelcontextprotocol/sdk` |
| MCP Client | 客户端实现 | `services/mcp/client.ts` |
| MCPTool | 工具包装器 | `tools/MCPTool/MCPTool.ts` |
| 传输层 | stdio/SSE/HTTP/WS | `services/mcp/client.ts` |
| 配置管理 | 多来源配置 | `services/mcp/config.ts` |
| 安全模型 | 多层权限检查 | `services/mcp/channelPermissions.ts` |
| 资源/提示 | 数据和模板 | `ListMcpResourcesTool` |

### 核心价值
MCP 让 Claude Code 从一个封闭系统变成了一个**开放平台**——任何人都可以开发 MCP 服务器来扩展 Claude Code 的能力。

---

## 十二、关联文件

### 12.1 上一章
- [08-agent-swarm.md](08-agent-swarm.md) - Agent Swarm 多代理

### 12.2 下一章
- [10-bridge-and-summary.md](10-bridge-and-summary.md) - Bridge 桥接系统与总结

---

*此细纲由 Claude Code 自动生成*
