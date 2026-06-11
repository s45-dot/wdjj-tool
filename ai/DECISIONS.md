# Architecture Decisions — Bubble Stretch Tool

> 架构决策记录（ADR）。所有重要技术决策必须记录在此。

---

## ADR 索引

| ID | 标题 | 日期 | 状态 |
|----|------|------|------|
| ADR-0001 | 采用 Vue 3 + TypeScript + Vite 作为前端技术栈 | 2026-06-11 | Accepted |
| ADR-0002 | 采用 FastAPI + Python 作为后端技术栈 | 2026-06-11 | Accepted |
| ADR-0003 | 九宫格核心算法使用纯函数，与 Vue/Canvas/DOM 解耦 | 2026-06-11 | Accepted |
| ADR-0004 | OpenCode (Minimax 2.7) 为 Phase 4 主力 Coder，Qwen Code 禁用 | 2026-06-11 | Accepted |

---

## ADR-0004：OpenCode 为第四阶段主力 Coder

**日期**：2026-06-11
**状态**：Accepted

**Context**：Qwen Code 接入的本地模型暂时无法使用。OpenCode 已接入 Minimax 2.7 并验证可正常调用。

**Decision**：
- OpenCode 为 Phase 4 主力代码开发工具
- Qwen Code 禁用，不得调用
- Code Whale 继续作为 fallback
- 审查链路不变

**Consequences**：
- 任务粒度可从 MICRO-only 提升到 SMALL/MEDIUM
- Qwen Code 只能通过未来 ADR 恢复

---

## ADR-0001：采用 Vue 3 + TypeScript + Vite

**日期**：2026-06-11
**状态**：Accepted

**背景**：
Phase 1 需要快速搭建可交互的前端原型，支持 Canvas 渲染和组件化控制面板。

**决策**：
- Vue 3 Composition API
- TypeScript（类型安全）
- Vite（快速 HMR）
- 普通 CSS（Phase 1 不引入 Tailwind）
- 浏览器原生 fetch（不引入 Axios）
- 不引入 Router/Pinia（Phase 1 只需单页面）

**理由**：
- Vue 3 + Vite 生态成熟，社区支持好
- TypeScript 提供类型安全，减少运行时错误
- 保持依赖最小化，降低复杂度

**后果**：
- 后续引入 Router/Pinia 时需要重构 App.vue
- 普通 CSS 可能在组件增多时管理困难

---

## ADR-0002：采用 FastAPI + Python

**日期**：2026-06-11
**状态**：Accepted

**背景**：
Phase 1 需要提供图片上传和 health check API。

**决策**：
- FastAPI（自动 OpenAPI 文档、类型校验）
- Uvicorn（ASGI 服务器）
- Pillow（图片处理）
- python-multipart（文件上传）

**理由**：
- FastAPI 开箱即用，开发效率高
- Python 生态在图片处理方面成熟
- 依赖少，安装简单

**后果**：
- 后续扩展需注意 ASGI 兼容性
- Phase 1 不做数据库，文件系统存储临时上传

---

## ADR-0003：九宫格算法纯函数解耦

**日期**：2026-06-11
**状态**：Accepted

**背景**：
九宫格计算逻辑是核心算法，需要可测试、可复用。

**决策**：
- `computeNineSlicePatches()` 是纯函数，输入输出完全确定
- 不依赖 DOM、Canvas、Vue
- 校验逻辑独立于计算逻辑
- Canvas 渲染调用计算函数，不自己算坐标

**理由**：
- 纯函数易于单元测试
- 与 UI 框架解耦，方便复用
- 便于后续扩展到其他渲染后端

**后果**：
- Canvas 组件必须通过 props 传递参数
- 类型定义需要在前端共享
