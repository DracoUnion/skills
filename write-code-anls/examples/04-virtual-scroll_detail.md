# 04-virtual-scroll.md 细纲

## 一、标题层级结构

### 1. 消息列表与虚拟滚动优化
- 学习目标（5点）
- 问题：1000 条消息的噩梦
  - 每个 MessageRow ≈ 250 KB
  - 1000 条 = ~250 MB
- 虚拟滚动的核心思路
  - topSpacer + visible items + bottomSpacer
- 高度估算的三段式策略
  - 估算: DEFAULT_ESTIMATE = 3
  - 测量: measureRef
  - 缓存: heightCache
- 滚动量化：减少 React 提交
  - SCROLL_QUANTUM = 40
- 终端宽度变化：缩放而非清除
  - heightCache 按比例缩放
- 滑动步进：限制单次挂载
  - SLIDE_STEP = 25
- VirtualMessageList 组件
- 动手练习
- 本课小结
- 下节预告

## 二、关键知识点

1. **虚拟滚动原理**
   - 只渲染视口内 + overscan 的项目
   - 其余用 spacer 占位
   - 大幅减少内存和渲染开销

2. **关键常量**
   - DEFAULT_ESTIMATE = 3（未测量项估算高度）
   - OVERSCAN_ROWS = 80（视口上下多渲染）
   - COLD_START_COUNT = 30（冷启动渲染项）
   - MAX_MOUNTED_ITEMS = 300（挂载项上限）
   - SLIDE_STEP = 25（每次最多新挂载）
   - SCROLL_QUANTUM = 40（滚动量子）

3. **三段式策略**
   - 估算: 故意偏低（3行），避免空白
   - 测量: measureRef 获取真实高度
   - 缓存: Map 存储，下次直接使用

4. **滚动量化**
   - scrollTop 按 40 行取整
   - 跨越量子边界时才触发 React 重渲染
   - 视觉滚动始终流畅

5. **宽度变化处理**
   - 缩放 heightCache: h * ratio
   - 避免清除导致的 600ms 卡顿

6. **滑动步进**
   - 快速滚动时分多次 commit
   - 每次最多挂载 25 项
   - scrollClampMin/Max 钳制视口

## 三、源码文件路径

- `hooks/useVirtualScroll.ts` - 虚拟滚动 Hook
- `components/VirtualMessageList.tsx` - 虚拟消息列表

## 四、类名、函数名、接口名

### 核心 Hook
- `useVirtualScroll()` - 虚拟滚动 Hook
- `useSyncExternalStore()` - 同步外部存储

### 返回值
- `range: [number, number]` - 渲染范围
- `topSpacer: number` - 顶部占位高度
- `bottomSpacer: number` - 底部占位高度
- `measureRef` - 测量回调工厂
- `spacerRef` - 顶部 spacer ref
- `offsets` - 累计偏移量
- `scrollToIndex` - 滚动到指定项

### 常量
- `DEFAULT_ESTIMATE` = 3
- `OVERSCAN_ROWS` = 80
- `COLD_START_COUNT` = 30
- `PESSIMISTIC_HEIGHT` = 1
- `MAX_MOUNTED_ITEMS` = 300
- `SLIDE_STEP` = 25
- `SCROLL_QUANTUM` = OVERSCAN_ROWS >> 1

### 辅助函数
- `getScrollTop()` - 获取滚动位置
- `setScrollTop()` - 设置滚动位置
