# P041 Reconciliation

- Disposition：`ACCEPTED_WITH_NARROWING`
- Read 1 SHA-256：`12095077a71c1037ec6eea655caa20b7cc70dab420024ccc98ab3ec075d71527`
- Accepted read-2 attempt：`read_2_attempts/r2-20260719-p041-a1/`
- Invocation SHA-256：`0a00c8cf5bf9a112480739a1485a137d04b66db86e27bf75f4288f4f67534a50`
- Report SHA-256：`5b407d148e06d3857cbc50b7ac5be9d97c301c873d57463740c0bb87d622daa1`

## Source reconciliation

- `AGREE`：changed computation 是用最后输入 token 的跨层 hidden-state probe 得到 necessity prediction，再预填一条 steering sentence 后正常生成；它不硬性门控工具访问，也不负责 API/参数选择。
- `AGREE`：训练标签来自强制无工具反事实与正确性 oracle；方法需要模型隐藏状态、模型专属监督与阈值校准，不能外推到闭源 API。
- `AGREE`：soft prefill 可被模型忽略，hard prefill 会伤害准确率；多跳/OOD 结果并非单调省调用。

## Admission boundary

作为“可访问隐藏状态下的监督式工具必要性 probe + prefill steering” Operator 与其权限/迁移 Failure 准入。标题中的“already know”不作为无监督、通用或零成本结论。

## PLAN_05 Card source-audit disposition

- Audit: `plan05-audit-b/report.md`；SHA-256 `723dc035b239ff70866e18e301bbaba4c25bc4085656971611939c2798560742`；task `/root/plan05_card_source_audit_b`
- Card SHA-256: pre `478e67c4440270f138f679d6cfd7fa9dfdbb7f31b67907b0841cc2e36535de03` (`operator-hidden-state-tool-necessity-gate`) → post `bff7760cc0fcc8b60d997027eb223f422308caa690336c6a289bee57dcc27ff8` (`operator-hidden-state-tool-necessity-prefill`)
- Disposition: `REPLACED_WITH_SOURCE-FAITHFUL_OPERATOR`

旧 Card 将 soft prefill 误写为 tool-access gate，已删除并以 probe + threshold + prefill 的真实计算取代；明确 steering 可被覆盖。
