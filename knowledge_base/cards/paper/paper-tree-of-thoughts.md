<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-tree-of-thoughts","card_kind":"paper","paper_id":"P002","evidence_ids":["ev-p002-branch-evaluate-search","ev-p002-search-resource-cost"],"source_refs":[{"path":"papers/P002_tree_of_thoughts.pdf","sha256":"6939cadebd84c8cdcc6ff3c2082b75851a86e2ef82008848d0af692f80521fa7"}]} -->
# Tree of Thoughts

## Role in the knowledge base
[CODEX_SYNTHESIS] Test-time reasoning search 的直接祖先与计算成本 baseline。

## Problem and setting
[CODEX_SYNTHESIS] 可分步构造且需要规划/回溯的 reasoning tasks；主要实验使用 GPT-4 生成与评估 thoughts。

## Changed computation
[AUTHOR_FACT] 将 thought generation/evaluation 与 BFS/DFS、lookahead 和 backtracking 组合。[[evidence:ev-p002-branch-evaluate-search]]

## Evidence-backed findings
[AUTHOR_FACT] 作者明确承认该搜索比 sampling methods 使用更多资源。[[evidence:ev-p002-search-resource-cost]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Evaluator 质量和搜索预算共同决定结果，不能把更多 GPT-4 calls 当作无成本结构改进。

## Lineage and baselines
[CODEX_SYNTHESIS] CoT 与 self-consistency 是直接生成基线；经典 search/MCTS 是先行谱系，后续 Agent tree-search 可复用或扩展 ToT-style 组件，不能把谱系邻近条目数量当独立机制证据。

## Evidence ledger
[AUTHOR_FACT] p.2 支持搜索机制；p.9 支持资源边界。[[evidence:ev-p002-branch-evaluate-search]] [[evidence:ev-p002-search-resource-cost]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] ToT；Tree of Thoughts；BFS DFS；thought evaluator；lookahead backtracking；思维树。
