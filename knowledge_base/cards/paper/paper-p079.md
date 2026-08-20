<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p079","card_kind":"paper","paper_id":"P079","evidence_ids":["ev-p079-action-conditioned-contextualization","ev-p079-ground-truth-action-retry","ev-p079-unseen-ui-boundary"],"source_refs":[{"path":"papers/P079_lcow.pdf","sha256":"2695ec5c912241fbdb56fc5f9ee3a4f60d1aaa23b511f35cff3d32908e97dead"}]} -->
# Learning Contextualized World Models for Web Agents

## Role in the knowledge base
[CODEX_SYNTHESIS] 将冗长 AXTree 压缩为 action-relevant observation 的输入重写机制；Web 是机制实验载体。

## Problem and setting
[CODEX_SYNTHESIS] Web Agent 必须从长 AXTree 中找到完成下一动作所需的少量 UI 信息。

## Changed computation
[AUTHOR_FACT] 训练从成功轨迹采样多个 contextualized observations，以多个 Agent 能否预测 demonstrated next action 选目标，再监督微调 contextualizer。[[evidence:ev-p079-action-conditioned-contextualization]]

## Evidence-backed findings
[CODEX_SYNTHESIS] 论文以动作可恢复性而非文本重构作为 contextualization 的监督信号。

## Limitations and failure signals
[AUTHOR_FACT] 候选全为零分时，训练会把 ground-truth next action 作为额外上下文重试。[[evidence:ev-p079-ground-truth-action-retry]]
[AUTHOR_FACT] 在未见的 Filter-List UI 类别上方法没有提升，因为训练未包含所需 filter affordance。[[evidence:ev-p079-unseen-ui-boundary]]

## Lineage and baselines
[CODEX_SYNTHESIS] contextualizer 同时产出 reasoning 与 observation subset，因此不能当作纯无决策压缩器；评测需区分信息保留、隐含规划与训练 oracle。

## Evidence ledger
[CODEX_SYNTHESIS] action-conditioned 训练、ground-truth retry 与 unseen-UI 失败分别绑定独立 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] AXTree contextualization; action-preserving observation compression; web agent context overload; ground-truth action retry; unseen UI affordance
