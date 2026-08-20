# Nearest Prior Commitment v027

## Directly read neighbors

- P084, *On the Robustness of Agentic Function Calling*, is the exact failure/data source. It fixes 200 requests, expands compact menus with related tools and evaluates AST construction, not a trained retrieval repair.
- ToolRerank, ACL Anthology PDF SHA-256 `dc1d0cf7537401d602aef27160b5f854b688bf607e51d3c0e33febccc66237d4`, trains a BERT retriever, cross-encoder reranker and single/multi-tool classifier. Its added computation is adaptive seen/unseen truncation plus tool-hierarchy concentration/diversification. It already establishes hard-negative cross-encoder training and specialized tool reranking; v027 cannot claim either.
- P087 TOOL-DE performs offline, query-independent generation of function description, tags, when-to-use and limitations, merges the generated profile with source documentation and applies semantic judgment. Its field ablation shows full expansion is not uniformly best. v027 generates no documentation and evaluates deterministic schema fields online.
- P086 Meta-Tool generates a hypothetical tool and required-parameter descriptions, then matches them to a large library. v027 has no query generator or parameter assignment.
- DTDR conditions retrieval on evolving tool plans and demonstration-derived dependencies. The present benchmark is one fixed request/menu with no evolving plan.

## Local lineage

v009 TPPA used deterministic query-value spans, dense span/required-parameter similarity, type/enum edges, partial assignment and fusion with the same cross-encoder. Its unique capacity/null component was not identified and it corrected only one Development row. v027 discards spans, dense embeddings, assignment and fusion grids; it learns menu-relative differences among three cross-encoder schema views under held-out query folds.

Pairwise logistic ranking, standardization, schema serialization and field scoring are standard components. The bounded open contrast is whether their exact operation/argument/full composition transfers from exposed BFCL v3 related menus to untouched v4 live-multiple menus. Open web searches did not surface the exact composition, but that is not proof of first-ever novelty.
