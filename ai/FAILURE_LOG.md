# Failure Log — Bubble Stretch Tool

> 所有失败、返工、升级记录。每次失败后立即追加。

---

## 失败记录模板

```
### Failure #F001

- **Date**: YYYY-MM-DD HH:MM
- **Task**: Txxx
- **Failed Agent**: Qwen Code / Code Whale
- **Reviewer**: Gemini / Hermes
- **Retry Count**: N
- **Failure Type**: 审查不通过 / 执行超时 / 测试失败 / 其他

**Failure Reason**:
详细说明失败原因。

**Required Changes**:
- 修改项 1
- 修改项 2

**Escalation**:
- 是否需要升级：Yes/No
- 升级目标：Code Whale / Emergency Coding
- 升级原因：

**Resolution**:
最终如何解决。
```

---

## 升级类型判定

| 条件 | 处理 |
|------|------|
| Qwen Code 同一任务 3 次未通过 | 升级为 ESCALATED，切换 Code Whale |
| Code Whale 同一任务 3 次未通过 | 暂停自动推进，判定是否 Emergency |
| 失败原因=需求不清/架构错误/测试错误等 | 不得进入 Emergency，先修正文档 |

---

## 失败记录

### Failure #F001

- **Date**: 2026-06-11 06:58
- **Task**: T003 (B1) — 初始化项目仓库结构
- **Failed Agent**: Qwen Code
- **Reviewer**: N/A（未进入审查）
- **Retry Count**: 3 (max)
- **Failure Type**: 执行超时（3 次）

**Failure Reason**:
Qwen Code 连续 3 次执行超时，无法产出文件：
- Retry #1 (180s): 只创建了 README.md（1/11），其余 10 个文件缺失
- Retry #2 (300s): 无任何文件产出
- Retry #3 (180s wall-time): 无任何文件产出

可能原因：本地模型 30tok/s 速度较慢，在复杂 prompt 下无法在超时前完成所有文件创建。

**Required Changes**:
- 创建 .gitignore
- 创建 docs/ARCHITECTURE.md, docs/PHASE_1_PLAN.md, docs/API_DRAFT.md
- 创建 frontend/README.md, backend/README.md
- 创建 scripts/dev_frontend.sh, scripts/dev_backend.sh, scripts/check_all.sh
- 创建 tests/README.md

**Escalation**:
- 是否需要升级：Yes
- 升级目标：Code Whale (DeepSeek V4 Flash)
- 升级原因：Qwen Code 连续 3 次超时失败，达到升级阈值

**Resolution**:
升级至 Code Whale 执行

---

### Failure #F002

- **Date**: 2026-06-11 07:18
- **Task**: T004 (C1) — 创建 Vue 3 + TypeScript + Vite 前端工程
- **Failed Agent**: Qwen Code
- **Reviewer**: N/A
- **Retry Count**: 2
- **Failure Type**: 执行超时

**Failure Reason**:
Qwen Code 两次尝试均超时：
- Retry #1 (300s wall-time): 创建了 10/15 文件（骨架 + 核心逻辑），缺失 4 组件 + CSS。超时前未能完成全部文件。
- Retry #2 (120s wall-time): 针对 5 个缺失文件的补充尝试，无产出。

与 B1 相同模式：本地模型 30tok/s 无法在规定时间内完成多文件创建任务。

**Escalation**:
- 是否需要升级：Yes
- 升级目标：Code Whale (DeepSeek V4 Flash)
- 升级原因：与 B1 相同超时模式，Qwen Code 不适合多文件代码生成任务

**Resolution**:
升级至 Code Whale 执行
