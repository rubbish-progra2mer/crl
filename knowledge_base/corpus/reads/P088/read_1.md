# P088 first read — joint non-negative retrieval directly precedes diversity reranking

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Non-negative Elastic Net Decoding for Information Retrieval
- Authors: Koki Okajima; Yasutoshi Ida; Tsukasa Yoshida; Yasuaki Nakamura
- Venue: arXiv:2606.17910 v1, technical report dated 2026-06-16
- Official landing page: `https://arxiv.org/abs/2606.17910`
- PDF: `knowledge_base/staging/plan06_prior_gap/P088_nnn_retrieval.pdf`
- PDF SHA-256: `adb67ce1c663402dc988cd9de4df891a1e6f540cf41011cd21e406da32ce636e`
- Parse check: 19 physical pages

## Canonical operator contribution

NNN decoding replaces independent query–document scores with a joint sparse non-negative reconstruction of the query embedding from the entire corpus. A selected item explains part of the query, changing the residual seen by correlated items and suppressing redundant near-neighbours. It is a direct changed-computation and nearest-composition prior for any tool-retrieval candidate that claims novelty from diversity, redundancy reduction or joint set selection.

## Evidence and closest lineage

- The decoder solves a non-negative elastic-net objective and returns the support ranked by coefficient magnitude. FISTA performs the inference.
- Theorem 1 states a per-query existence result: for fixed corpus embeddings and target set, every query recoverable by dense top-k is recoverable by NNN for some hyperparameters. A constructed correlated corpus gives strict separation.
- The practical frozen-embedding method uses one global `(lambda_1, lambda_2)` pair selected on validation data, rather than the theorem's per-query pair.
- Experiments compare dense retrieval, MMR, COLT, frozen NNN and trained NNN on three ToolBank datasets, ToolLens and MultiHop-RAG.
- Frozen NNN improves tool-retrieval completeness over dense retrieval in the reported ToolBank/ToolLens settings; trained NNN improves further. Gains grow with the number of relevant items, while single/few-item queries leave less room for the mechanism.

## Measurement and fairness boundaries

- The theorem does not guarantee that one global hyperparameter pair works across queries; the paper explicitly identifies this theory/deployment mismatch.
- Frozen NNN is hyperparameter-sensitive, and MultiHop-RAG contains conditions where an L1-only variant substantially hurts performance.
- Full-corpus FISTA costs `O(dNT)` per query. It does not inherit approximate-nearest-neighbour latency, and end-to-end unrolled training has `O(dNT)` memory per query.
- The experiments use one principal small embedding backbone with additional appendix checks; they do not establish arbitrary-corpus scalability.
- NNN optimizes complete set recovery under dataset labels. It does not determine whether retrieved tools are functionally executable or whether alternative unlabelled tools are valid.

## Draft knowledge objects

### Operator draft: `Joint Non-Negative Residual Decoding`

Select a tool set jointly by reconstructing the query embedding as a sparse non-negative combination of corpus embeddings. Each selected item subtracts explained semantic mass, so correlated redundant items are evaluated against the residual rather than the untouched query.

### Failure draft: `Independent Similarity Scores Return Redundant Tool Sets`

Independent top-k scoring ignores relationships among corpus items. In multi-tool queries, a high-scoring near-duplicate can displace a complementary required tool even when the fixed embeddings contain enough joint information to recover the set.

## Draft Evidence locators

- Physical pp.1–3: independent-scoring failure, joint reconstruction and closest retrieval lineage.
- Physical pp.4–6: objective, theorem/proposition, residual mechanism, practical inference and theory/deployment mismatch.
- Physical pp.7–9: fair baselines, main results, relevant-set-size signature and limitations.

All claims remain draft until independent read and reconciliation.
