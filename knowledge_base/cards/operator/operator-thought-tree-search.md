<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-thought-tree-search","card_kind":"operator","paper_id":"P002","evidence_ids":["ev-p002-branch-evaluate-search"],"source_refs":[{"path":"papers/P002_tree_of_thoughts.pdf","sha256":"6939cadebd84c8cdcc6ff3c2082b75851a86e2ef82008848d0af692f80521fa7"}]} -->
# Thought Branch–Evaluate–Backtrack Search

## Intervention target
[AUTHOR_FACT] 把单路径生成改为对 thought states 的生成、评估和 BFS/DFS 搜索。[[evidence:ev-p002-branch-evaluate-search]]

## Before and after computation
[CODEX_SYNTHESIS] Baseline 是一次向前的 chain；changed computation 是 branch → value/evaluate → prune/select → lookahead/backtrack。

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为当前 thought state，输出为候选子状态与保留集合；评估发生在提交下一步前并增加采样、评估调用和搜索状态。

## Mechanism hypothesis
[CODEX_SYNTHESIS] 显式维护多个候选允许早期错误路径被剪枝，并让局部不确定性通过回溯恢复。

## Predicted observable signature
[CODEX_HYPOTHESIS] 在相同生成预算下，收益应伴随更高的正确分支保留率，而不只是候选总数增加。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 依赖可分解 thought、有效 evaluator 和可承受搜索预算；错误 evaluator 会系统性剪掉可行路径。

## Source lineage
[CODEX_SYNTHESIS] Tree of Thoughts 是该语言化 branch–evaluate search 的直接来源，并借鉴经典 heuristic/tree search；后续 verifier-guided 或 Agent tree-search 只有组件相同时才是谱系邻近项，不自动构成独立机制证据。

## Evidence ledger
[AUTHOR_FACT] `ev-p002-branch-evaluate-search` 定位到 PDF p.2 对 BFS/DFS、lookahead 与 backtracking 的定义。[[evidence:ev-p002-branch-evaluate-search]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] Tree of Thoughts；branch evaluate prune；lookahead；backtracking；test-time search；思维树搜索。
