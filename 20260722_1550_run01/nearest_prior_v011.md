# Main Codex Nearest Prior Record

## Frozen before review

This record was written before v011 Development and will be bound by path and SHA before any Review Packet. It is excluded from the common Reviewer Packet body as required by `CRL.md`; its commitment SHA will be supplied separately if v011 reaches review.

## Search views

- **Changed computation:** learned post-encoder residual ranking from related hard negatives with a non-reversal constraint on prior correct margins.
- **Key components:** tool-specific hard-negative training, cross-encoder reranking, counterfactual negative generation, knowledge preservation, and safe/non-regressive learning to rank.
- **Full pipeline:** query and tool menu → frozen query/schema encoding → learned residual → margin cap → ranked function → top-1/MRR.
- **Composition and runnable baseline:** the identical unanchored residual head is locally runnable. ToolRet, ToolRerank, Re-Invoke, CausalNeg, and robust-ranker training are checked as stronger external neighbors.

## Exact searches

Executed 2026-07-23 through the open network:

- `tool retrieval hard negatives function calling contrastive`
- `function calling related tools hard negative training reranker`
- `tool selection contrastive learning hard negatives API`
- `BFCL expanded toolkit robustness mitigation retrieval training`
- `tool retrieval distillation preserve ranking fine tuning hard negatives`
- `function calling hard negative fine tuning preserve performance tool selection`
- `safe reranking no regression constraint learning to rank`
- `mistake driven residual reranker retrieval non regression`

Primary full-text or official landing pages read:

- P084, *On the Robustness of Agentic Function Calling*, local PDF SHA-256 `8276bcab484eef370bc63afca580ea19d8f6e2ccc6c2afcdaf684225d5e635c7`.
- P085/ToolRet, ACL 2025 Findings `2025.findings-acl.1258`, local PDF SHA-256 `26ce2766e8c4b72e88dfd2cf93bfe56ff758fea6fe0ec0bea34228f555311d2a`.
- ToolRerank, ACL Anthology `2024.lrec-main.1413`: `https://aclanthology.org/2024.lrec-main.1413/`.
- Re-Invoke, ACL Anthology `2024.findings-emnlp.270`: `https://aclanthology.org/2024.findings-emnlp.270/`.
- *Towards Robust Ranker for Text Retrieval*, ACL Anthology `2023.findings-acl.332`: `https://aclanthology.org/2023.findings-acl.332/`.
- *Hard Negatives, Hard Lessons*, ACL Anthology `2025.findings-emnlp.481`: `https://aclanthology.org/2025.findings-emnlp.481/`.
- CausalNeg, arXiv `2606.01304v2`: `https://arxiv.org/abs/2606.01304`.
- MemTR, ACL Anthology `2026.findings-acl.973`: `https://aclanthology.org/2026.findings-acl.973/`.

The local Card queries were also executed once:

- Failure: `semantically related toolkit expansion wrong function operation scope confusion`
- Operator: `learned retriever hard negative contrastive function selection menu`
- Paper: `tool retrieval learned classifier hard negative function calling`

## Component collisions

- ToolRet already builds more than 200k query/target/negative training instances and trains tool-specific retrieval models. Related-tool hard-negative learning is therefore a direct component collision.
- Robust-ranker work uses diverse hard-negative generators for contrastive ranker training. A generic hard-negative residual is not a defensible contribution.
- CausalNeg constructs controlled counterfactual negatives and adds a training objective to suppress source shortcuts. Counterfactual negative generation is not a v011 contribution.
- Hard Negatives, Hard Lessons shows that false negatives can damage retriever/reranker training and that relabeling can improve results. v011 does not solve label exhaustiveness.
- Generic safe/counterfactual learning-to-rank literature prevents claiming that non-regression constraints as a class are new.

## Composition collisions

- ToolRerank combines retrieval with adaptive truncation and hierarchy-aware reranking; it does not use a frozen cross-encoder residual capped by original thin-menu margins.
- Re-Invoke generates tool-side synthetic queries, extracts user intent, and applies multi-view similarity; it changes representations and requires generation, unlike v011.
- MemTR modifies decoding-time hidden computation inside a tool-calling LLM under uncertainty; it is not a post-encoder tool reranker.
- No checked primary source established the exact composition of P084-added related negatives, a frozen query/schema cross-encoder, a linear residual, and an analytic cap derived from correctly ranked original thin-menu margins. This is an incomplete search conclusion, not proof of novelty.

## Full-pipeline collisions

P084 diagnoses the failure but supplies no mitigation. ToolRet and ToolRerank address retrieval at larger scale, while v011 tests compact-menu top-1/MRR. The closest complete executable pipeline in the current workspace is therefore the same frozen cross-encoder plus the unanchored related-negative residual; it differs only by omission of the cap.

## Comparator roles and relative differences

- `cross_encoder`: frozen strong baseline; no learned v011 component.
- `unanchored_related_adapter`: closest-composition and unique-delta comparator; same CLS features, training pairs, optimizer, model, folds, and inference scoring, but scale is exactly 1.
- `thin_anchor_adapter`: proposed method; scale is capped only when the unanchored residual would reverse a positive thin-menu training margin.

No external implementation is substituted for the local closest-composition because the unique delta can be isolated exactly in local code. External systems differ in model size, training corpora, generated instructions, hierarchy, or inference information and would not be a same-budget delta ablation.

## Closest-composition conclusion

v011 is not novel as hard-negative training, residual reranking, or safe learning-to-rank. Its remaining testable difference is the thin-menu margin-derived cap inside a compact tool-ranking pipeline. Development must compare it to the unanchored residual and frozen cross-encoder. If the cap does not reduce regressions while retaining at least three quarters of unanchored corrections, the proposed delta fails even if the whole learned bundle improves.
