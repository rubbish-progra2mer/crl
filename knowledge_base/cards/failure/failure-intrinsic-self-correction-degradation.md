<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-intrinsic-self-correction-degradation","card_kind":"failure","paper_id":"P013","evidence_ids":["ev-p013-intrinsic-self-correction-degrades","ev-p013-oracle-free-equal-budget-boundary"],"source_refs":[{"path":"papers/P013_intrinsic_self_correction_limits.pdf","sha256":"d172f0b3e933544f5165250338e3e989036e8d826fea34093e6aed4adb5b042a"}]} -->
# Intrinsic Self-Correction Can Degrade Reasoning

## Observed failure
[AUTHOR_FACT] 在没有 external feedback 的 intrinsic 设置中，模型有时在 self-correction 后退化。[[evidence:ev-p013-intrinsic-self-correction-degrades]]

## Conditions and scope
[AUTHOR_FACT] §3 的 intrinsic self-correction 去掉 oracle labels，但没有与等调用重采样对齐；§4 另行在相同 response 数下比较 debate 与 self-consistency。[[evidence:ev-p013-oracle-free-equal-budget-boundary]]

## Failed intervention
[CODEX_SYNTHESIS] 失败干预是让同一模型仅凭自身已有输出再判断并改写，没有引入新的可判别信息。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 结果不否定带环境反馈、tests、verifier 或外部记忆的 reflection；prompt 质量与预算仍是替代解释。

## Warning for future candidates
[CODEX_SYNTHESIS] 候选必须说明新信息来自哪里，并与等调用 self-consistency/重采样比较。

## Possible repair boundary
[CODEX_HYPOTHESIS] 可验证环境反馈可能提供真正的错误辨识信号，但不应被称作 intrinsic self-correction。

## Evidence ledger
[AUTHOR_FACT] 两条 Evidence 分别定位无反馈退化与无 oracle/等响应预算边界。[[evidence:ev-p013-intrinsic-self-correction-degrades]] [[evidence:ev-p013-oracle-free-equal-budget-boundary]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] intrinsic self-correction；no external feedback；oracle-label confound；equal inference budget；内在自纠退化。
