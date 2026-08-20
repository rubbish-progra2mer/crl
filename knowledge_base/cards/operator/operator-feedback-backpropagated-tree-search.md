<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-feedback-backpropagated-tree-search","card_kind":"operator","paper_id":"P003","evidence_ids":["ev-p003-search-control-loop"],"source_refs":[{"path":"papers/P003_lats.pdf","sha256":"a6b84613eeeaa3beb979ac3e34cbb3575bceb7ccf6050a2c2fc677d5e3a3ab19"}]} -->
# Feedback-Backpropagated Agent Tree Search

## Intervention target
[AUTHOR_FACT] LATS 以 selection、expansion、evaluation、simulation、backpropagation 和 reflection 的有界循环替代单轨 Agent rollout。[[evidence:ev-p003-search-control-loop]]

## Before and after computation
[CODEX_SYNTHESIS] Before 是按当前轨迹直接继续或重试；after 是维护可回溯状态树，对多个动作分支先扩展和估值，再选择执行路径并把终局反馈回传到祖先状态。

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入包括当前树状态、候选动作、环境 observation、LM value 与失败 reflection；输出是被扩展/保留的后继状态及更新后的路径价值。evaluation 与 selection 发生在继续执行分支之前。

## Mechanism hypothesis
[CODEX_SYNTHESIS] 环境反馈和 value 不只产生文字批评，而是改变树中状态价值与下一轮分支选择，从而改变实际执行的 action trajectory。

## Predicted observable signature
[CODEX_HYPOTHESIS] 若机制成立，收益应伴随正确分支保留率或失败分支剪除率提高；只增加 rollout 数而不改变分支选择不能单独证明该 Operator。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 需要可回溯状态、可解释的 action boundary、足够可靠的 value/feedback 和明确预算；错误 heuristic、稀疏 reward 或通用 reflection 都可能误导搜索。

## Source lineage
[CODEX_SYNTHESIS] 该 Operator 是 ReAct、MCTS、LM value 与 verbal reflection 的显式组合机制；其价值在于信息如何回传并改变 action selection，不把各组件重新组合本身冒充 primitive novelty。

## Evidence ledger
[AUTHOR_FACT] `ev-p003-search-control-loop` 定位 PDF p.5 对六阶段操作顺序及计算预算终止条件的定义。[[evidence:ev-p003-search-control-loop]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] verifier-guided search；value-guided action selection；feedback backpropagation；MCTS agent planning；branch execution；环境反馈树搜索。
