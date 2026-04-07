# 04-message-protocol.md 细纲

## 一、标题层级结构

### 1. 消息协议设计——SDKMessage / ControlRequest / ControlResponse
- 学习目标（4点）
- 消息协议的生活类比
  - 快递分拣中心
- 三种消息类型详解
  - SDKMessage：普通消息
  - ControlRequest：控制请求
  - ControlResponse：控制响应
- 消息路由：handleIngressMessage
  - 核心路由函数
  - 路由流程图
- 服务器控制请求的处理
  - handleServerControlRequest 函数
  - 控制请求处理流程
- 权限请求：从子进程到服务器
  - 子进程发起权限请求
  - 权限请求的流转
- 消息过滤：哪些消息该转发？
  - eligible 消息判断
  - 标题提取
- 结果消息
  - 构建归档消息
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **三种消息类型**
   - SDKMessage: type 字段区分（user/assistant/result/system）
   - ControlRequest: type='control_request'，必须回复
   - ControlResponse: type='control_response'，success/error

2. **ControlRequest 子类型**
   - initialize: 初始化会话
   - set_model: 切换模型
   - interrupt: 中断操作
   - set_max_thinking_tokens: 设置思考 Token 上限
   - set_permission_mode: 设置权限模式

3. **消息路由流程**
   - 检查 ControlResponse
   - 检查 ControlRequest
   - 检查 SDKMessage
   - UUID 去重（回音过滤）
   - 只转发 user 类型消息

4. **权限请求流转**
   - CLI stdout 发送 control_request
   - Bridge 转发到服务器
   - 服务器弹出确认框
   - 用户响应返回 Bridge
   - Bridge stdin 转发给 CLI

5. **消息过滤规则**
   - 虚拟消息（isVirtual）不转发
   - user/assistant/local_command 转发

## 三、源码文件路径

- `bridge/bridgeMessaging.ts` - 消息路由处理
- `bridge/sessionRunner.ts` - 权限请求类型
- `bridge/types.ts` - 消息类型定义

## 四、类名、函数名、接口名

### 类型守卫
- `isSDKMessage()` - 判断是否为 SDKMessage
- `isSDKControlRequest()` - 判断是否为 ControlRequest
- `isSDKControlResponse()` - 判断是否为 ControlResponse

### 核心函数
- `handleIngressMessage()` - 处理入站消息
- `handleServerControlRequest()` - 处理服务器控制请求
- `isEligibleBridgeMessage()` - 判断消息是否可转发
- `extractTitleText()` - 提取标题文本
- `makeResultMessage()` - 构建结果消息

### 类型
- `SDKMessage` - SDK 消息类型
- `SDKControlRequest` - 控制请求类型
- `SDKControlResponse` - 控制响应类型
- `PermissionRequest` - 权限请求类型
