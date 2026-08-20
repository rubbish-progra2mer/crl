<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-likelihood-utility-does-not-guarantee-agent-utility","card_kind":"failure","paper_id":"P082","evidence_ids":["ev-p082-future-token-loss-filtered-calls","ev-p082-top-k-single-call-boundary","ev-p082-chaining-cost-sparsity-boundary"],"source_refs":[{"path":"papers/P082_toolformer.pdf","sha256":"6d7483d94653008e40c2058a1c22441c92e3713dae278b6361e8efc447c99522"}]} -->
# Likelihood Utility Does Not Guarantee Agent Utility

## Observed failure
[CODEX_SYNTHESIS] 能降低后续 token loss 的 tool call 未必提升多步任务成功、鲁棒性或净成本；这是训练 proxy 与 Agent objective 的结构性错位。

## Conditions and scope
[CODEX_SYNTHESIS] 当 training selector 只看局部 language-model likelihood，而部署目标是多步 success、成本或安全时最明显。

## Failed intervention
[CODEX_SYNTHESIS] 单以 future-token loss 作为调用 utility，未直接优化完整 Agent objective。

## Evidence and alternative explanations
[AUTHOR_FACT] Toolformer 以 future-token loss 过滤并学习 API calls。[[evidence:ev-p082-future-token-loss-filtered-calls]]
[AUTHOR_FACT] 推理提高 top-10 API 触发倾向但最多一次调用。[[evidence:ev-p082-top-k-single-call-boundary]] [AUTHOR_FACT] 方法不支持 chaining/interactive calls，数据可稀疏且不计调用成本。[[evidence:ev-p082-chaining-cost-sparsity-boundary]]

## Warning for future candidates
[CODEX_SYNTHESIS] 自监督 tool-learning Candidate 必须直接测 task success、wrong-call harm、call count/latency 与 chained use；不能以 language-model loss 单独支撑 Agent claim。

## Possible repair boundary
[CODEX_HYPOTHESIS] 用可观察的 task utility 与 call cost 校准或二次筛选 likelihood-selected calls；P082 未验证该修复。

## Evidence ledger
[CODEX_SYNTHESIS] proxy、inference trigger 与 limitation 均绑定 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] tool utility proxy mismatch; future token loss; downstream task success; API call cost; single-call limitation
