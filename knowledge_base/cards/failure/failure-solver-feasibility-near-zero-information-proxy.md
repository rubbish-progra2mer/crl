<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-solver-feasibility-near-zero-information-proxy","card_kind":"failure","paper_id":"P097","evidence_ids":["ev-p097-feasibility-gap","ev-p097-behavioral-perturbation"],"source_refs":[{"path":"papers/P097_reloop.pdf","sha256":"8563653b872e78822f024b4d2f11532f75354e98c729ed26ac5bbf9675724c66"}]} -->
# Solver Feasibility Is a Near-Zero-Information Proxy for Formulation Correctness

## Observed failure
[AUTHOR_FACT] 组合问题上 SOTA 模型 solver-feasibility 高达 91.1% 而 formulation correctness 仅 0.5%——90 点 feasibility-correctness gap；成因："solver feedback catches syntax errors, not missing constraints"，LLM self-critique 继承产生错误的推理缺口，execution-based reranking 需要不可得的 ground truth。[[evidence:ev-p097-feasibility-gap]]

## Conditions and scope
[CODEX_SYNTHESIS] NL→Gurobi 代码生成；RetailOpt-190（38 archetype×5 变体组合基准）与 MAMO/IndustryOR；preprint（NeurIPS 投稿格式）。本文的 gap 是可行性与正确性的总量级测量。

## Failed intervention
[CODEX_SYNTHESIS] 以"代码执行成功 + solver 返回 optimal/feasible"为正确性信号；经全套 ReLoop 干预后 Claude 仍 2/3 silent failure——执行层修复救不了语义层。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] gap 数字的证据边界（reconciliation）：ReLoop 增益含重试预算混杂（~3× token、≤3 次再生成 vs Base 单次，无等预算盲重试对照）；跨基准 Base 4/5 为引用自 SIRL 非复跑；single-run pass@1 无误差条——gap 本身是同管线内测量、稳健，方法增益点值不引用。
[AUTHOR_FACT] 扰动检测的适用边界：仅局部可扰动缺陷有效，结构性静默失败（内部自洽的错误分解）扰动测不到。[[evidence:ev-p097-behavioral-perturbation]]（边界出自 §5.4/Limitations，PDF 直核；所绑引文为机制定义）

## Warning for future candidates
[CODEX_SYNTHESIS] 任何以执行或可行性通过率为主要 observable 的认证类候选方法都必须面对该测量；本文支持 gap 量化与失败分类。

## Possible repair boundary
[CODEX_HYPOTHESIS] 行为扰动测试适合局部缺陷域，独立参考检查器可能覆盖结构性缺陷域；系数量级错误与形式化等价错误仍无解（作者自认 beyond scope）。

## Evidence ledger
[CODEX_SYNTHESIS] gap 与成因、扰动边界绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] feasibility-correctness gap; silent failure; solver feedback syntax errors; missing constraints; execution proxy; 91.1 vs 0.5; RetailOpt; formulation correctness; feasible but wrong formulation; executing and returning optimal yet incorrect; solver reports optimal to the wrong problem; missing constraints go undetected; silent formulation failures
