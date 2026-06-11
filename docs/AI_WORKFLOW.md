# AI Workflow — Bubble Stretch Tool

> 本文档定义 Bubble Stretch Tool 项目的 AI 自动开发协作规则。
> 所有 AI Agent 必须严格遵守本文档规定的角色、权限、流程和边界。

---

## 1. Agent 角色定义

### 1.1 Hermes Agent（项目总指挥）

| 属性 | 值 |
|------|-----|
| **模型** | DeepSeek V4 Pro |
| **简称** | Hermes |

**职责**：
- 任务拆解与派发
- 状态记录与维护
- 审查调度与管理
- 失败重试与升级决策
- 阶段验收
- 维护文档、任务板、失败记录、审查记录

**默认权限（允许修改）**：
- `docs/*`
- `ai/*`
- `README.md`
- 任务说明、审查总结、阶段报告、架构决策记录

**默认禁止（禁止修改）**：
- `frontend/src/*`
- `backend/app/*`
- 任何生产代码
- 任何测试代码
- 任何构建配置中的业务实现部分

### 1.2 Qwen Code（第一代码生成代理）

| 属性 | 值 |
|------|-----|
| **模型** | 本地 qwen3.6 35B A3B Apex MTP |
| **上下文** | 64k |
| **KVCache** | FP16 |

**职责**：
- 生成前端代码
- 生成后端代码
- 生成测试代码
- 修复审查问题
- 执行小范围重构
- 补充技术说明

**限制**：
- 必须严格遵守 Hermes 派发任务的范围
- 不得主动实现未被任务要求的功能

### 1.3 Gemini Reviewer（第一审查方）

| 属性 | 值 |
|------|-----|
| **调用方式** | Hermes 通过 OpenTeam 调用 Gemini |

**职责**：
- 架构审查
- 代码正确性审查
- 边界条件审查
- 安全审查
- 测试审查
- 可维护性审查
- 范围控制审查

**限制**：
- 不允许直接修改代码
- 只能输出审查意见

### 1.4 Hermes Reviewer（替代审查方）

**激活条件**：OpenTeam 调用 Gemini 超过 1 分钟未返回结果。

**规则**：
- Hermes 替代审查时仍不得修改代码
- 使用与 Gemini 相同的审查标准和输出格式

### 1.5 Code Whale（代码兜底执行者）

| 属性 | 值 |
|------|-----|
| **模型** | DeepSeek V4 Flash |

**激活条件**：Qwen Code 在同一代码任务上连续 3 次未通过审查。

**职责**：
- 修复 Qwen Code 反复失败的代码任务
- 补齐测试
- 修复架构偏差
- 提交重新审查

**限制**：
- 与 Qwen Code 使用相同审查标准
- Code Whale 连续 3 次失败后，才允许 Hermes 考虑 Emergency Coding Mode

---

## 2. 权限边界

### 2.1 默认规则

| Agent | 可修改 | 禁止修改 |
|-------|--------|----------|
| Hermes | `docs/`, `ai/`, `README.md`, `scripts/` | `frontend/src/`, `backend/app/`, 任何生产/测试代码 |
| Qwen Code | 任务指定的文件范围 | 任务范围外的一切 |
| Gemini Reviewer | 无（只输出审查意见） | 所有文件 |
| Code Whale | 任务指定的文件范围 | 任务范围外的一切 |

### 2.2 Emergency Coding Mode 例外

**触发条件（必须同时满足全部 5 条）**：

1. Qwen Code 在同一代码任务上连续 3 次审查不通过
2. Code Whale 在同一代码任务上连续 3 次审查不通过
3. 审查方确认失败原因不是：需求不清、测试错误、任务拆解错误或架构错误
4. Hermes 已在 `ai/FAILURE_LOG.md` 中记录完整失败链路
5. Hermes 已创建 `emergency/hermes-fix-*` 分支

**Emergency Coding Mode 下的约束**：
- 必须写明失败原因
- 必须写明改动范围
- 必须补充或修正测试
- 必须重新提交审查
- **不得直接合并 main**

---

## 3. 任务生命周期

### 3.1 标准流程

```
Hermes 创建任务
  → Hermes 写入 ai/TASKS.md
  → Hermes 派发给 Qwen Code
  → Qwen Code 执行任务
  → Qwen Code 返回变更摘要
  → Hermes 请求 Gemini Reviewer 审查
  → Gemini 1 分钟内返回：采用 Gemini 审查结果
  → Gemini 超时 1 分钟：Hermes 执行替代审查
  → 审查通过（APPROVED）：Hermes 标记完成，进入下一任务
  → 审查不通过（CHANGES_REQUESTED）：Hermes 派发返工任务
  → 同一任务 Qwen Code 失败 3 次：升级 Code Whale
  → Code Whale 失败 3 次：进入 Emergency Coding 判断
```

### 3.2 任务状态枚举

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

### 3.3 每个任务必须记录的信息

- **Task ID** — 任务编号（如 T001）
- **Task Title** — 任务标题
- **Status** — 当前状态
- **Owner** — 执行 Agent
- **Reviewer** — 审查方
- **Fallback Reviewer** — 替代审查方
- **Retry Count** — 重试次数
- **Fallback Agent** — 兜底 Agent
- **Priority** — 优先级
- **Objective** — 目标
- **Scope** — 允许范围
- **Out of Scope** — 禁止范围
- **Files Allowed** — 允许修改的文件
- **Files Forbidden** — 禁止修改的文件
- **Acceptance Criteria** — 验收标准
- **Review Criteria** — 审查标准
- **Result** — 最终结果

---

## 4. 审查规则

### 4.1 审查请求格式

Hermes 向 Gemini Reviewer 发起审查时，必须提供：

- 任务编号
- 任务目标
- 允许修改文件
- 禁止修改文件
- 变更摘要
- 核心代码片段
- 验收标准
- 需要重点审查的问题

### 4.2 审查输出格式

```
# Review Result

Task: Txxx
Reviewer: Gemini / Hermes
Status: APPROVED / CHANGES_REQUESTED / REJECTED

## Summary
一句话总结。

## Blocking Issues
- 问题 1
- 问题 2

## Non-blocking Suggestions
- 建议 1
- 建议 2

## Required Changes
- 必须修改 1
- 必须修改 2

## Scope Check
- 是否存在越界实现：Yes / No
- 说明：

## Risk Level
Low / Medium / High

## Final Decision
APPROVED / CHANGES_REQUESTED / REJECTED
```

### 4.3 判定规则

**APPROVED**（通过）：
- 功能达成
- 无阻塞问题
- 无越界实现
- 无明显安全问题
- 无明显架构污染
- → Hermes 更新 `ai/TASKS.md` 和 `ai/REVIEW_LOG.md`，进入下一任务

**CHANGES_REQUESTED**（需修改）：
- 功能基本正确
- 存在可修复问题
- 不应直接合并
- → Hermes 复制 Required Changes，派回原执行 Agent，Retry Count +1，更新 `ai/FAILURE_LOG.md`

**REJECTED**（拒绝）：
- 方向错误
- 范围严重越界
- 核心实现错误
- 存在严重安全风险
- → Hermes 记录失败，Retry Count +1，要求重新实现；达到 3 次升级 Code Whale

---

## 5. 失败重试与升级规则

### 5.1 Qwen Code 失败

同一任务下，Qwen Code 每次未通过审查，Hermes 必须：

1. Retry Count +1
2. 记录失败原因
3. 记录审查方
4. 记录 Required Changes
5. 重新派发修复任务

当 Retry Count 达到 3：
- 标记 `ESCALATED`
- 切换 Owner 为 Code Whale
- 记录升级原因

### 5.2 Code Whale 失败

Code Whale 使用相同规则。同一任务失败 3 次后：
- Hermes 暂停自动推进
- 分析失败类型
- 判断是否允许 Emergency Coding Mode

### 5.3 不允许升级为 Emergency Coding 的情况

如果失败原因是以下之一，Hermes **不得**进入 Emergency Coding Mode：

- 需求不清
- 验收标准冲突
- 前置任务未完成
- 测试用例错误
- 架构方案错误
- 文件结构不一致
- 任务粒度过大

→ 这种情况下，Hermes 必须先修正任务说明或架构文档。

---

## 6. 超时降级规则

| 场景 | 超时时间 | 降级方案 |
|------|----------|----------|
| OpenTeam 调用 Gemini 审查 | 1 分钟 | Hermes 执行替代审查 |
| Qwen Code 执行任务 | 5 分钟 | 检查文件是否已写入，运行测试判定 |

---

## 7. 分支规则

| 分支类型 | 命名规则 | 用途 |
|----------|----------|------|
| 主分支 | `main` | 稳定版本 |
| 功能分支 | `feat/sX-<desc>` | Qwen Code 开发 |
| 修复分支 | `fix/sX-<desc>` | 审查后修复 |
| 应急分支 | `emergency/hermes-fix-*` | Emergency Coding Mode |

---

## 8. 日志记录规则

### 8.1 文件用途

| 文件 | 用途 |
|------|------|
| `ai/STATE.md` | 当前阶段、当前任务、阻塞项、下一步 |
| `ai/TASKS.md` | 任务板（含状态枚举） |
| `ai/DECISIONS.md` | 架构决策记录（ADR） |
| `ai/REVIEW_LOG.md` | 所有审查结果 |
| `ai/FAILURE_LOG.md` | 所有失败、返工、升级记录 |

### 8.2 记录时机

- 任务状态变更 → 立即更新 `ai/TASKS.md` 和 `ai/STATE.md`
- 审查完成 → 立即写入 `ai/REVIEW_LOG.md`
- 审查不通过/失败/升级 → 立即写入 `ai/FAILURE_LOG.md`
- 架构决策 → 立即追加 `ai/DECISIONS.md`

---

## 9. 第一阶段禁止范围

第一阶段（Phase 1）**禁止**实现以下任何内容：

- ❌ Android .9.png 导出
- ❌ iOS JSON 导出
- ❌ ZIP 打包
- ❌ 二维码访问
- ❌ 桌面端封装
- ❌ 数据库
- ❌ 账号系统
- ❌ 项目历史记录
- ❌ 批量处理
- ❌ 完整聊天 UI
- ❌ contentInsets 调参
- ❌ 复杂 UI 框架
- ❌ Router
- ❌ 状态管理库（Pinia 等）

第一阶段只验证核心技术闭环，不追求完整产品化。

---

## 10. 版本

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1.0.0 | 2026-06-11 | Hermes Agent | 初始版本，基于 Phase 1 开发指南 |
| 2.0.0 | 2026-06-11 | Hermes Agent | Phase 2/3：慢速 Qwen 调度 + 四级审查链路 + OpenTeam 降级规则 |

---

## 11. Qwen Code 慢速模式调度规则（Phase 2+）

### 11.1 背景

本地 Qwen Code 模型：qwen3.6 35B A3B Apex MTP，实际速度 20-30 tokens/s。

### 11.2 任务切片标准

| 任务级别 | 文件数 | 行数 | 建议等待 |
|----------|--------|------|----------|
| MICRO | 1 | <150 | 8-12 分钟 |
| SMALL | 1-3 | <300 | 15-25 分钟 |
| MEDIUM | 3-5 | <500 | 30-45 分钟 |
| LARGE | 禁止 | — | 必须拆分为 MICRO/SMALL |

每个任务必须：目标单一、文件范围固定、接口签名预定义、禁止事项显式化。

### 11.3 超时分级

| 超时类型 | 含义 | 是否计入失败 |
|----------|------|-------------|
| SOFT_TIMEOUT | 生成慢或输出未完成 | ❌ 不计入 |
| FAILED_REVIEW | 审查 REJECTED 或核心实现错误 | ✅ 计入 |

SOFT_TIMEOUT 不计入 3 次失败规则。只有 FAILED_REVIEW 才计入。

### 11.4 Qwen Code 优先原则

Qwen Code 仍是默认代码生成主力（节省 API 费用）。不得因慢而跳过。同一任务 3 次 FAILED_REVIEW 后才升级 Code Whale。

---

## 12. 四级审查降级链路（Phase 2+）

### 12.1 审查顺序

```
任务完成
  → 1. Gemini Reviewer via OpenTeam (70s timeout)
    → 返回有效结果 → 采用，结束
    → 超时 → 进入 2
  → 2. ChatGPT Reviewer via OpenTeam (70s timeout)
    → 返回有效结果 → 采用，结束
    → 超时 → 进入 3
  → 3. DeepSeek Web Reviewer via CDP Browser (70s timeout)
    → 返回有效结果 → 采用，结束
    → 超时 → 进入 4
  → 4. Hermes Reviewer（替代审查）
```

任一审查方返回有效结果即采用，不继续后续。

### 12.2 审查输出格式

```
# Review Result
Task: Px-Txxx
Reviewer: Gemini / ChatGPT / DeepSeek Web / Hermes
Status: APPROVED / CHANGES_REQUESTED / REJECTED

## Summary
## Blocking Issues
## Required Changes
## Scope Check
## Correctness Check
## Security Check
## Test Check
## Risk Level
## Final Decision
```

### 12.3 审查记录格式

必须记录：审查方尝试顺序、各超时秒数、采用哪个结果、未采用原因。

---

## 13. OpenTeam 双审查降级规则

### 13.1 触发条件

当 Gemini + ChatGPT 两个 OpenTeam 审查方 **连续 3 次** 都超时（70s 内无有效返回），触发降级。

### 13.2 降级操作

- 停用 OpenTeam 审查链路
- 切换为 **Hermes + DeepSeek Web 交替审查**
- 记录降级决策到 `ai/DECISIONS.md`
- 后续任务不再尝试 Gemini/ChatGPT，直接使用 Hermes/DeepSeek

### 13.3 恢复条件

用户手动指令恢复。

---

## 14. 第二阶段禁止范围

- ❌ 二维码访问
- ❌ 桌面端封装
- ❌ 数据库
- ❌ 账号系统
- ❌ 项目历史记录
- ❌ 批量处理
- ❌ 复杂聊天 UI
- ❌ 完整设备预设系统
- ❌ 在线云同步

---

## 15. 第三阶段禁止范围

- ❌ 桌面端封装
- ❌ 账号系统
- ❌ 云同步
- ❌ 多人协作
- ❌ 数据库历史记录
- ❌ 批量处理
- ❌ 公网部署
