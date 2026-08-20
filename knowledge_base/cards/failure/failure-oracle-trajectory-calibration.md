<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-oracle-trajectory-calibration","card_kind":"failure","paper_id":"P019","evidence_ids":["ev-p019-ground-truth-calibration-oracle"],"source_refs":[{"path":"papers/P019_steca.pdf","sha256":"f0957a2acf89227b77922ee4d5a9de10759cc6ad89778077f048c178a0184703"}]} -->
# Ground-Truth Trajectory Calibration Creates Oracle Advantage

## Observed failure
[AUTHOR_FACT] STeCa 的 calibration 把 deviated action 修订为 ground-truth counterpart，并接入 expert trajectory。[[evidence:ev-p019-ground-truth-calibration-oracle]]

## Conditions and scope
[CODEX_SYNTHESIS] 这是训练数据构造与归因边界，不否定其作为 supervised agent-learning 方法的结果。

## Failed intervention
[CODEX_SYNTHESIS] 若把该训练期 privileged information 描述成 agent 自主发现的 credit，会混淆 oracle teacher 与可部署 inference。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 增益可能来自更细粒度 credit、更多专家数据、强 reflection teacher 或轨迹分布变化。

## Warning for future candidates
[CODEX_SYNTHESIS] 必须区分训练期 expert action、环境可得 feedback 与测试期 Agent 实际可见信息。

## Possible repair boundary
[CODEX_HYPOTHESIS] 用可执行 verifier 或环境 reward 替代 ground-truth action，才能测试非 Oracle step calibration。

## Evidence ledger
[AUTHOR_FACT] `ev-p019-ground-truth-calibration-oracle` 定位到 PDF p.2 的 ground-truth 修订步骤。[[evidence:ev-p019-ground-truth-calibration-oracle]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] oracle trajectory；expert continuation；credit assignment confound；step calibration；专家轨迹优势。

