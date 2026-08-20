# W06 Card source audit C disposition

- Audit ID: `w06-audit-c`
- Report SHA-256: `ad007d008a08e3b1722021b97d2fb6c87bcbe7461e719af4be6c1cf22661f133`
- Decision: `ACCEPT_WITH_SINGLE_ROUND_NARROWING`
- Atomic totals: 95 PASS / 2 NARROW / 0 REJECT（97 原子项）

## Disposition

主 Codex 按审计意见完成一轮收窄（不循环审计），2 处 NARROW 均为同一根因（P101 的 1/200K WikiSQL 反例方向标签），逐条采纳审计给出的最小精确修正：

1. `paper-p101`："套件假阴有 1/200K 实证反例" → "套件误接受（假阳）方向在 WikiSQL 约 200K 预测中有 1 例实证反例"。
2. `failure-single-execution-denotation-false-positive`：误标子句 → "套件拒绝侧（广义假阴，'非自然库'类）无对称抽验；套件误接受（假阳）侧在 WikiSQL 约 200K 预测中有 1 例实证反例（多余 WHERE 未被覆盖）"。依据：论文自身约定（metric 判对/实际错 = false positive）、§8 证明严格 PL 意义假阴不可能、真正无对称审计的是拒绝侧。
3. 同根因外溢：`corpus/reads/P101/reconciliation.md` 的 "不是什么证据" 一行同步修正并落 2026-07-27 追记（审计范围外的自愿一致性修正，非审计要求）。

其余 10 张卡（P098–P100 全部 + P101 operator 卡）全 PASS：invocation 点名的四组过度声明风险（P098 主场/蒸馏混杂、P099 预算混杂与判官配置边界、P100 条件化偏差与 BoR [30] 归属、P101 单向审计与适配度量放松）均已在卡内正确对冲；全部点名数字过 PDF 核验；机械层 13/13 evidence 逐字节一致、4/4 PDF SHA 匹配。

修订后卡片重过 `manage_cards.py validate`；FTS 索引在三份审计全部处置后统一重建（见 v010 冻结快照）。一轮修订后不触发循环审计。
