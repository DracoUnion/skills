# 05-bounded-uuid-set.md 细纲

## 一、标题层级结构

### 1. BoundedUUIDSet——环形缓冲区去重
- 学习目标（4点）
- 为什么需要去重？
  - 生活类比：微信群消息
  - Bridge 中的去重场景
- 为什么不用普通 Set？
  - 普通 Set 的问题（内存泄漏）
  - 解决方案：环形缓冲区
- 源码逐行解析
  - 完整源码
  - 逐行解读
  - 执行过程动画
- 设计分析
  - 时间复杂度
  - 空间复杂度
  - 为什么同时用 Array 和 Set？
  - 淘汰的合理性
- 在 Bridge 中的使用场景
  - 回音过滤
  - 重复投递过滤
  - 两个 Set 的协作
- 环形缓冲区的通用知识
  - 常见应用场景
  - 取模运算的魔力
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **去重目的**
   - 过滤回音（自己发出的消息被转发回来）
   - 防止重复处理（网络抖动导致重复投递）

2. **BoundedUUIDSet 数据结构**
   - ring: 环形数组（维护插入顺序）
   - set: Set（O(1) 查找）
   - writeIdx: 下一个写入位置

3. **时间复杂度**
   - add(): O(1)
   - has(): O(1)
   - clear(): O(n)

4. **空间复杂度**
   - 始终 O(capacity)，不会随消息数量增长

5. **淘汰策略**
   - FIFO（先进先出）
   - 超过容量时淘汰最老的元素

6. **两个 Set 协作**
   - recentPostedUUIDs: 记录自己发出的消息
   - recentInboundUUIDs: 记录已处理的消息

## 三、源码文件路径

- `bridge/bridgeMessaging.ts` - BoundedUUIDSet 实现

## 四、类名、函数名、接口名

### 类
- `BoundedUUIDSet` - 有界 UUID 集合
  - `add(uuid)` - 添加 UUID
  - `has(uuid)` - 检查是否存在
  - `clear()` - 清空集合

### 属性
- `capacity` - 最大容量
- `ring` - 环形数组
- `set` - 快速查找集合
- `writeIdx` - 写入位置索引

### 使用场景
- `recentPostedUUIDs` - 最近发出的消息 UUID
- `recentInboundUUIDs` - 最近收到的消息 UUID
