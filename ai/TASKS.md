# Tasks Board — Bubble Stretch Tool

> 任务板。Hermes 负责维护，每个任务状态变更后立即更新。

---

## 状态枚举

| 状态 | 说明 |
|------|------|
| `TODO` | 待执行 |
| `IN_PROGRESS` | 执行中 |
| `REVIEW` | 审查中 |
| `CHANGES_REQUESTED` | 需修改 |
| `APPROVED` | 审查通过 |
| `MERGED` | 已合并 |
| `FAILED` | 失败 |
| `ESCALATED` | 已升级 |
| `EMERGENCY` | 应急模式 |

---

## Phase 1 任务清单

### T001 — A1：创建 AI 工作流文档

| 字段 | 值 |
|------|-----|
| **Task ID** | T001 |
| **Task Title** | 创建 docs/AI_WORKFLOW.md |
| **Status** | IN_PROGRESS |
| **Owner** | Hermes |
| **Reviewer** | Hermes 自检 |
| **Fallback Reviewer** | N/A |
| **Retry Count** | 0 |
| **Fallback Agent** | N/A |
| **Priority** | P0 |
| **Objective** | 建立 AI 自动开发协作规则文档 |
| **Scope** | 定义 Agent 角色、权限、任务生命周期、审查规则、失败重试规则、阶段禁止范围 |
| **Out of Scope** | 无 |
| **Files Allowed** | `docs/AI_WORKFLOW.md` |
| **Files Forbidden** | 所有代码文件 |
| **Acceptance Criteria** | 1. 文件存在 2. 结构清晰 3. 明确 Hermes 默认不得写代码 4. 明确 Gemini 超时 1 分钟由 Hermes 审查 5. 明确 Qwen Code 失败 3 次升级 Code Whale 6. 明确 Code Whale 失败 3 次才允许 Emergency Coding |
| **Review Criteria** | Hermes 自检：所有 AC 满足 |
| **Result** | Pending |

### T002 — A2：创建 AI 状态文件

| 字段 | 值 |
|------|-----|
| **Task ID** | T002 |
| **Task Title** | 创建 ai/STATE.md、TASKS.md、DECISIONS.md、REVIEW_LOG.md、FAILURE_LOG.md |
| **Status** | TODO |
| **Owner** | Hermes |
| **Reviewer** | Hermes 自检 |
| **Fallback Reviewer** | N/A |
| **Retry Count** | 0 |
| **Fallback Agent** | N/A |
| **Priority** | P0 |
| **Objective** | 初始化 AI 状态记录文件体系 |
| **Scope** | 创建 5 个状态文件 |
| **Out of Scope** | 无 |
| **Files Allowed** | `ai/STATE.md`, `ai/TASKS.md`, `ai/DECISIONS.md`, `ai/REVIEW_LOG.md`, `ai/FAILURE_LOG.md` |
| **Files Forbidden** | 所有代码文件 |
| **Acceptance Criteria** | 1. 五个文件均存在 2. 每个文件非空 3. 每个文件有明确用途 4. TASKS.md 包含状态枚举 5. FAILURE_LOG.md 包含失败记录模板 6. REVIEW_LOG.md 包含审查记录模板 |
| **Review Criteria** | Hermes 自检：所有 AC 满足 |
| **Result** | Pending |

### T003 — B1：初始化项目仓库结构

| 字段 | 值 |
|------|-----|
| **Task ID** | T003 |
| **Task Title** | 初始化项目仓库结构 |
| **Status** | TODO |
| **Owner** | Qwen Code |
| **Reviewer** | Gemini via OpenTeam |
| **Fallback Reviewer** | Hermes |
| **Retry Count** | 0 |
| **Fallback Agent** | Code Whale |
| **Priority** | P0 |
| **Objective** | 创建所有必需的空文件/占位文件，建立项目目录骨架 |
| **Scope** | 创建 README.md、.gitignore、docs/*、ai/*、frontend/README.md、backend/README.md、scripts/*.sh、tests/README.md |
| **Out of Scope** | Vue/FastAPI/任何依赖安装、任何业务代码 |
| **Files Allowed** | `README.md`, `.gitignore`, `docs/`, `ai/`, `frontend/README.md`, `backend/README.md`, `scripts/`, `tests/README.md` |
| **Files Forbidden** | `frontend/src/`, `backend/app/` |
| **Acceptance Criteria** | 1. 所有必需文件存在 2. 没有业务代码 3. 没有引入依赖 4. 文档非空 5. 脚本清晰可读 6. AI 文档和产品文档没有混淆 |
| **Review Criteria** | 所有必需文件存在、没有业务代码、没有引入依赖、文档非空、脚本清晰可读、AI 与产品文档分离 |
| **Result** | Pending |

### T004 — C1：创建前端最小工程

| 字段 | 值 |
|------|-----|
| **Task ID** | T004 |
| **Task Title** | 创建 Vue 3 + TypeScript + Vite 前端工程 |
| **Status** | TODO |
| **Owner** | Qwen Code |
| **Reviewer** | Gemini via OpenTeam |
| **Fallback Reviewer** | Hermes |
| **Retry Count** | 0 |
| **Fallback Agent** | Code Whale |
| **Priority** | P0 |
| **Objective** | 创建可运行的前端骨架 |
| **Scope** | 创建 package.json、index.html、vite.config.ts、tsconfig.json、src/main.ts、App.vue、core/types.ts、core/rect.ts、core/validators.ts、core/nineSlice.ts、components/*.vue、styles/main.css |
| **Out of Scope** | Router、Pinia、Tailwind、Axios、导出、后端上传、复杂 UI |
| **Files Allowed** | `frontend/*` |
| **Files Forbidden** | 后端代码 |
| **Acceptance Criteria** | 1. npm install 可执行 2. npm run dev 可执行 3. Vue 组件结构清晰 4. TypeScript 类型无明显错误 5. 无越界实现 6. 无未授权依赖 |
| **Review Criteria** | npm install/dev 可执行、无类型错误、无越界功能、无未授权依赖 |
| **Result** | Pending |

### T005 — D1：创建后端最小工程

| 字段 | 值 |
|------|-----|
| **Task ID** | T005 |
| **Task Title** | 创建 FastAPI 后端骨架 |
| **Status** | TODO |
| **Owner** | Qwen Code |
| **Reviewer** | Gemini via OpenTeam |
| **Fallback Reviewer** | Hermes |
| **Retry Count** | 0 |
| **Fallback Agent** | Code Whale |
| **Priority** | P0 |
| **Objective** | 创建可启动的本地 API 服务 |
| **Scope** | 创建 requirements.txt、app/main.py、config.py、schemas.py、routers/health.py、routers/upload.py、services/image_loader.py |
| **Out of Scope** | 导出、.9.png、数据库、用户系统 |
| **Files Allowed** | `backend/*` |
| **Files Forbidden** | 前端代码 |
| **Acceptance Criteria** | 1. uvicorn 可启动 2. GET /api/health 正常 3. POST /api/upload 可上传 PNG 4. 非 PNG 返回 400 5. 超 5MB 返回 400 |
| **Review Criteria** | 后端可启动、health 正常、upload 有类型/大小限制、Pillow 验证、文件名随机化、无阶段外功能 |
| **Result** | Pending |

### T006 — E1：实现九宫格核心矩形计算

| 字段 | 值 |
|------|-----|
| **Task ID** | T006 |
| **Task Title** | 实现九宫格核心矩形计算 |
| **Status** | TODO |
| **Owner** | Qwen Code |
| **Reviewer** | Gemini via OpenTeam |
| **Fallback Reviewer** | Hermes |
| **Retry Count** | 0 |
| **Fallback Agent** | Code Whale |
| **Priority** | P0 |
| **Objective** | 实现与 DOM/Canvas/Vue 完全无关的纯函数九宫格计算 |
| **Scope** | nineSlice.ts、types.ts、rect.ts |
| **Out of Scope** | Vue 组件、Canvas 渲染、后端 |
| **Files Allowed** | `frontend/src/core/nineSlice.ts`, `frontend/src/core/types.ts`, `frontend/src/core/rect.ts` |
| **Files Forbidden** | Vue 组件、后端代码、样式文件 |
| **Acceptance Criteria** | 1. 纯函数 2. 不依赖 DOM/Canvas/Vue 3. 完整校验 4. 总是返回 9 个 patch 5. patch 顺序稳定 6. 坐标正确 7. 异常信息明确 |
| **Review Criteria** | 纯函数性、无外部依赖、完整校验、9 patch、顺序稳定、坐标正确、异常明确 |
| **Result** | Pending |

### T007 — F1：实现 Canvas 九宫格绘制

| 字段 | 值 |
|------|-----|
| **Task ID** | T007 |
| **Task Title** | 实现 Canvas 九宫格绘制 |
| **Status** | TODO |
| **Owner** | Qwen Code |
| **Reviewer** | Gemini via OpenTeam |
| **Fallback Reviewer** | Hermes |
| **Retry Count** | 0 |
| **Fallback Agent** | Code Whale |
| **Priority** | P0 |
| **Objective** | 实现 Canvas 上的九宫格拉伸渲染 |
| **Scope** | nineSlice.ts（新增 drawNineSlice）、BubbleCanvas.vue |
| **Out of Scope** | 拖拽辅助线、文本绘制、后端上传、复杂动画 |
| **Files Allowed** | `frontend/src/core/nineSlice.ts`, `frontend/src/components/BubbleCanvas.vue` |
| **Files Forbidden** | 其他组件、后端 |
| **Acceptance Criteria** | 1. 页面显示 Canvas 2. 修改 targetWidth 横向拉伸 3. 修改 targetHeight 纵向拉伸 4. 四角不变形 |
| **Review Criteria** | drawNineSlice 复用 computeNineSlicePatches、支持 dpr、props 变化重绘、Canvas 清晰、无超范围功能 |
| **Result** | Pending |

### T008 — G1：实现前端本地 PNG 加载

| 字段 | 值 |
|------|-----|
| **Task ID** | T008 |
| **Task Title** | 实现前端本地 PNG 加载 |
| **Status** | TODO |
| **Owner** | Qwen Code |
| **Reviewer** | Gemini via OpenTeam |
| **Fallback Reviewer** | Hermes |
| **Retry Count** | 0 |
| **Fallback Agent** | Code Whale |
| **Priority** | P0 |
| **Objective** | 用户可在浏览器中选择本地 PNG 文件 |
| **Scope** | ImageUploader.vue、App.vue |
| **Out of Scope** | 后端上传、导出、拖拽上传、第三方组件 |
| **Files Allowed** | `frontend/src/components/ImageUploader.vue`, `frontend/src/App.vue` |
| **Files Forbidden** | 后端代码 |
| **Acceptance Criteria** | 1. 选 PNG 后显示原图尺寸 2. Canvas 显示拉伸后图 3. 非 PNG 不接受或提示 |
| **Review Criteria** | 只接受 PNG、释放旧 URL、正确读取尺寸、未调用后端、无越界 |
| **Result** | Pending |

### T009 — H1：实现 Insets 控制面板

| 字段 | 值 |
|------|-----|
| **Task ID** | T009 |
| **Task Title** | 实现 Insets 控制面板 |
| **Status** | TODO |
| **Owner** | Qwen Code |
| **Reviewer** | Gemini via OpenTeam |
| **Fallback Reviewer** | Hermes |
| **Retry Count** | 0 |
| **Fallback Agent** | Code Whale |
| **Priority** | P0 |
| **Objective** | 用户可通过 slider/number 调整四边 insets |
| **Scope** | InsetsPanel.vue、App.vue、validators.ts |
| **Out of Scope** | contentInsets、导出、拖拽辅助线、复杂 toast |
| **Files Allowed** | `frontend/src/components/InsetsPanel.vue`, `frontend/src/App.vue`, `frontend/src/core/validators.ts` |
| **Files Forbidden** | 后端代码 |
| **Acceptance Criteria** | 1. 调 slider 后 Canvas 实时变化 2. 输入非法值时显示错误 3. 非法值不导致页面崩溃 |
| **Review Criteria** | range/number 同步、边界控制正确、非法参数不崩溃、错误和警告显示、无 contentInsets |
| **Result** | Pending |

### T010 — I1：实现 DebugPanel

| 字段 | 值 |
|------|-----|
| **Task ID** | T010 |
| **Task Title** | 实现 DebugPanel |
| **Status** | TODO |
| **Owner** | Qwen Code |
| **Reviewer** | Gemini via OpenTeam |
| **Fallback Reviewer** | Hermes |
| **Retry Count** | 0 |
| **Fallback Agent** | Code Whale |
| **Priority** | P0 |
| **Objective** | 显示九宫格渲染的所有关键参数 |
| **Scope** | DebugPanel.vue、App.vue |
| **Out of Scope** | 图表、复杂 UI、后端调用 |
| **Files Allowed** | `frontend/src/components/DebugPanel.vue`, `frontend/src/App.vue` |
| **Files Forbidden** | 后端代码 |
| **Acceptance Criteria** | 1. 上传图片后完整信息 2. 调整 insets 后实时变化 3. 非法参数时显示错误 |
| **Review Criteria** | 显示所有必要字段、随 insets 实时更新、随图片变化更新、无后端调用、无复杂 UI |
| **Result** | Pending |

### T011 — J1：接入后端 /api/health

| 字段 | 值 |
|------|-----|
| **Task ID** | T011 |
| **Task Title** | 接入后端 /api/health |
| **Status** | TODO |
| **Owner** | Qwen Code |
| **Reviewer** | Gemini via OpenTeam |
| **Fallback Reviewer** | Hermes |
| **Retry Count** | 0 |
| **Fallback Agent** | Code Whale |
| **Priority** | P1 |
| **Objective** | 前端可检测后端连接状态 |
| **Scope** | api/client.ts、api/healthApi.ts、App.vue、DebugPanel.vue |
| **Out of Scope** | 后端上传接入、导出、自动重试、Axios |
| **Files Allowed** | `frontend/src/api/client.ts`, `frontend/src/api/healthApi.ts`, `frontend/src/App.vue`, `frontend/src/components/DebugPanel.vue` |
| **Files Forbidden** | 后端代码 |
| **Acceptance Criteria** | 1. 后端启动显示 connected 2. 后端关闭显示 disconnected 3. 不影响 Canvas |
| **Review Criteria** | 使用 fetch、无 Axios、优雅处理后端关闭、不影响本地 Canvas、无后端上传 |
| **Result** | Pending |

### T012 — K1：第一阶段综合验收

| 字段 | 值 |
|------|-----|
| **Task ID** | T012 |
| **Task Title** | 执行第一阶段综合验收 |
| **Status** | TODO |
| **Owner** | Hermes |
| **Reviewer** | Hermes 自检 |
| **Fallback Reviewer** | N/A |
| **Retry Count** | 0 |
| **Fallback Agent** | N/A |
| **Priority** | P0 |
| **Objective** | 验证所有 Phase 1 功能 |
| **Scope** | 整个项目 |
| **Out of Scope** | N/A |
| **Files Allowed** | `docs/PHASE_1_REPORT.md` |
| **Files Forbidden** | N/A |
| **Acceptance Criteria** | 见开发指南第 9 节（13 条硬标准） |
| **Review Criteria** | 13 条硬标准全部通过 |
| **Result** | Pending |

### T013 — L1：输出阶段报告

| 字段 | 值 |
|------|-----|
| **Task ID** | T013 |
| **Task Title** | 输出 docs/PHASE_1_REPORT.md |
| **Status** | TODO |
| **Owner** | Hermes |
| **Reviewer** | Hermes 自检 |
| **Fallback Reviewer** | N/A |
| **Retry Count** | 0 |
| **Fallback Agent** | N/A |
| **Priority** | P1 |
| **Objective** | 生成 Phase 1 完成报告 |
| **Scope** | 报告文档 |
| **Out of Scope** | N/A |
| **Files Allowed** | `docs/PHASE_1_REPORT.md` |
| **Files Forbidden** | 所有代码文件 |
| **Acceptance Criteria** | 报告包含：任务完成列表、Agent 执行摘要、审查摘要、失败摘要、关键决策、可用功能、验证结果、已知问题、Phase 2 风险评估 |
| **Review Criteria** | Hermes 自检：模板字段完整 |
| **Result** | Pending |
