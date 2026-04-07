# 图解 Claude Code 完全指南 - 细纲

## 文件信息
- **原文件**: 07-oauth-authentication.md
- **类型**: 第 7 课：OAuth 2.0 + PKCE 安全认证
- **难度**: ★★★☆☆

---

## 一、文档结构概览

### 1.1 学习目标
1. 理解 OAuth 2.0 授权码流程的基本原理
2. 掌握 PKCE（Proof Key for Code Exchange）防劫持机制
3. 学会从源码中识别认证流程的每个步骤
4. 了解令牌刷新、多组织支持和 CCR 模式的特殊处理

### 1.2 章节结构
| 章节 | 主题 | 核心内容 |
|------|------|---------|
| 一、"代领快递"的比喻 | 概念入门 | OAuth 流程类比 |
| 二、PKCE 密码学基础 | 安全机制 | Verifier/Challenge/State |
| 三、完整认证流程 | 流程图 | 7 步认证流程 |
| 四、授权 URL 构建 | 实现细节 | buildAuthUrl |
| 五、本地回调服务器 | 实现细节 | AuthCodeListener |
| 六、令牌交换与刷新 | 核心功能 | exchangeCodeForTokens |
| 七、PKCE 安全性图解 | 安全分析 | 防劫持原理 |

---

## 二、关键知识点

### 2.1 OAuth 流程类比
```
你（用户）告诉快递站：允许小李（Claude Code）代领
快递站（Anthropic 服务器）给小李一张取件码（授权码）
小李用取件码换了一张快递卡（Access Token）
以后小李凭卡就能直接领快递
```

**PKCE 的作用**：防止有人偷听到取件码后冒充小李 —— 你和小李事先约定了一个暗号（Code Verifier），取件码必须配合暗号才能使用。

### 2.2 PKCE 三个安全随机值
```typescript
// services/oauth/crypto.ts

// 1. Code Verifier：43-128 字符的随机字符串
export function generateCodeVerifier(): string {
  return base64URLEncode(randomBytes(32))
}

// 2. Code Challenge：Verifier 的 SHA-256 哈希
export function generateCodeChallenge(verifier: string): string {
  const hash = createHash('sha256')
  hash.update(verifier)
  return base64URLEncode(hash.digest())
}

// 3. State：防 CSRF 的随机状态参数
export function generateState(): string {
  return base64URLEncode(randomBytes(32))
}
```

### 2.3 Base64URL 编码
```typescript
function base64URLEncode(buffer: Buffer): string {
  return buffer
    .toString('base64')
    .replace(/\+/g, '-')    // + → -
    .replace(/\//g, '_')    // / → _
    .replace(/=/g, '')      // 去掉填充
}
```

为什么不用普通 Base64？因为 `+`、`/`、`=` 在 URL 中有特殊含义，会导致参数解析错误。

### 2.4 令牌过期检查
```typescript
export function isOAuthTokenExpired(expiresAt: number | null): boolean {
  if (expiresAt === null) return false

  const bufferTime = 5 * 60 * 1000  // 提前 5 分钟刷新
  return Date.now() + bufferTime >= expiresAt
}
```

---

## 三、关联文件索引

### 3.1 前置阅读
- [06-lsp-integration.md](06-lsp-integration.md) - LSP 集成

### 3.2 后续课程
- [08-context-compression.md](08-context-compression.md) - 上下文压缩

### 3.3 核心源码文件
| 文件路径 | 职责 | 行数 |
|---------|------|------|
| `services/oauth/crypto.ts` | PKCE 加密函数 | ~50 行 |
| `services/oauth/client.ts` | OAuth 客户端 | ~200 行 |
| `services/oauth/auth-code-listener.ts` | 本地回调服务器 | ~150 行 |

---

## 四、源码对应关系

### 4.1 核心函数
| 函数名 | 位置 | 功能 |
|--------|------|------|
| `generateCodeVerifier()` | `services/oauth/crypto.ts` | 生成 Code Verifier |
| `generateCodeChallenge()` | `services/oauth/crypto.ts` | 生成 Code Challenge |
| `generateState()` | `services/oauth/crypto.ts` | 生成 State 参数 |
| `buildAuthUrl()` | `services/oauth/client.ts` | 构建授权 URL |
| `exchangeCodeForTokens()` | `services/oauth/client.ts` | 授权码换令牌 |
| `refreshOAuthToken()` | `services/oauth/client.ts` | 刷新令牌 |
| `isOAuthTokenExpired()` | `services/oauth/client.ts` | 检查令牌过期 |

### 4.2 核心类
| 类名 | 位置 | 说明 |
|------|------|------|
| `AuthCodeListener` | `services/oauth/auth-code-listener.ts` | 本地回调服务器 |

### 4.3 核心常量
| 常量名 | 值 | 说明 |
|--------|-----|------|
| `bufferTime` | 5 * 60 * 1000 | 提前 5 分钟刷新令牌 |

---

## 五、本课小结

| 概念 | 解释 |
|------|------|
| OAuth 2.0 | 安全的第三方授权协议，不需要共享密码 |
| PKCE | Proof Key for Code Exchange，防止授权码被劫持 |
| Code Verifier | 随机生成的 43-128 字符字符串 |
| Code Challenge | Verifier 的 SHA-256 哈希 |
| State | 防 CSRF 的随机状态参数 |
| 认证流程 | 生成参数 → 启动服务器 → 浏览器授权 → 交换令牌 |
| 令牌刷新 | 提前 5 分钟刷新，避免请求中途过期 |

---

*此细纲由 Claude Code 自动生成，用于快速导航和内容概览*
