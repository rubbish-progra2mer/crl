<!-- crl-v3-evidence-ids
["ev-p084-expanded-toolkit-controlled-setting","ev-p084-related-toolkit-error-types","ev-p087-structured-query-independent-expansion","ev-p087-fields-not-universally-beneficial"]
-->
# Candidate v027 — Menu-Relative Field Contrast Ranking (MFCR)

## Changed computation

MFCR scores each existing tool schema through three deterministic views using one frozen cross-encoder: full schema, operation identity/description, and recursively serialized arguments. On other query folds, it learns a zero-intercept linear rank score from within-menu gold-minus-distractor and distractor-minus-gold field-score differences. Each query contributes total pair weight one, independent of menu size or number of gold/non-gold pairs. The held-out query and all tools in its menu are absent from its fitted scaler and ranker.

At inference, every tool is scored independently by the frozen learned field weights, then the menu is ordered by score with tool-name SHA-256 tie-breaking. No gold count, original-menu membership, perturbed question, query-value alignment, LLM generation, tool hierarchy, per-query threshold or Confirmation label is available.

## Mandatory controls

- identical frozen full-schema cross-encoder;
- equal mean of the three standardized field scores;
- pointwise field classifier with identical fields, folds, standardizer, learner and menu weighting;
- pairwise full-score-only ranker with the identical pair construction and learner.

MFCR must strictly beat every control in OOF top-1. This isolates its unique supported delta to using operation/argument field contrasts in a menu-pair objective, not extra cross-encoder calls, supervised labels, capacity, schema length or generic pairwise fitting.

## Data and claim boundary

Development is the fully exposed 200-query BFCL v3 P084 expanded-toolkit set. Its fixed files are SHA-256 `aef168155ebd74b7ac2401198b201343bc7d16d7a3d7e0d4e6d8ee82c6969b2a` (questions/original menus), `1be15f014a2d04af06fec2797e4e53f7a335ce46e6bbdc2ec0ef3cabd6074a7b` (expanded menus) and `244e00ce9395df948bcafc7bee64e8f9c87ef70887587d83cae45b13699f3047` (gold). Untouched Confirmation is BFCL v4 live-multiple at commit `6ea57973c7a6097fd7c5915698c54c17c5b1b6c8` and may be acquired only after a positive written Promotion Audit.

Only if Development, untouched Confirmation, independent audits, three fresh leaf Reviews and the main-Codex Decision all pass:

> On the two pinned BFCL compact related-tool menu datasets, a query-fold-trained linear ranker over frozen full/operation/argument cross-encoder views improves top-1 gold-function membership and first-gold MRR over the identical monolithic cross-encoder and field/pairwise controls.

No argument correctness, complete multi-call recall, execution, Agent task success, large-registry retrieval, unseen-tool universality, causal, generic reranking or first-ever claim is allowed.
