# Neutral Selection Context

## Version scope and optional stopping

v011 follows ten candidate versions in the same Run. v001-v006 contained acquisition, execution, or Confirmation-coverage failures. v007 completed Development, Confirmation, a frozen Packet, three independent Reviewer reports, and a Main Codex `NO-GO_FOR_DELIVERY` decision. v008 failed before scientific output. v009 produced a real negative Development result. v010 closed before Candidate freeze after its checked routes lacked trustworthy outcome labels, were not executable in the authoritative environment, or reduced out-of-fold top-1.

The full P084 200-row Development set, gold functions, v009 rankings, and fourteen frozen cross-encoder errors have already been read. v011 is therefore not an independent estimate on P084. It prospectively fixes a scientifically different training computation and uses grouped out-of-fold predictions to reduce direct row reuse. The pinned BFCL v4 live-multiple Confirmation files remain unacquired and unread.

## v011 routes checked

1. Ordinary related-tool hard-negative fine-tuning was rejected as the proposed delta because ToolRet already trains tool-specific retrievers from query, target tools, and mined negatives; general contrastive hard-negative training is not a new computation.
2. Generated counterfactual-query training was rejected as the proposed delta because CausalNeg and DocReRank already construct controlled negative queries or counterfactual requirements for retriever/reranker training, and the local P084 file does not preserve a trustworthy one-to-one label from every generated request variant to every added tool.
3. Inference-time use of P084 `perturbed_question` was rejected because the fixed untouched BFCL v4 Confirmation does not supply the same lineage field.
4. A frozen cross-encoder plus a learned related-negative residual is retained only as the executable closest-composition comparator.
5. The v011 Candidate adds one proposed delta: cap that residual so every correctly ordered thin-menu training margin remains strictly positive. Development measures whether this preservation constraint reduces regressions without erasing corrections.

## Data and byte boundaries

- Development: the already-touched 200 P084 expanded menus and BFCL v3 gold.
- Confirmation: fixed BFCL v4 live-multiple query and answer files at repository commit `6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`; not acquired before Promotion Audit.
- Model: local `cross-encoder/ms-marco-MiniLM-L6-v2@c5ee24cb16019beea0893ab7796b1df96625c6b8`.
- No v011 scientific result existed when the computation, folds, optimizer, anchor rule, metrics, gates, code, and config were fixed.
