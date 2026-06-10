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

*暂无失败记录 — Phase 1 开始于 2026-06-11*
