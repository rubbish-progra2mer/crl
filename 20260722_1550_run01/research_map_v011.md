<!-- crl-v3-evidence-ids
["ev-p084-expanded-toolkit-controlled-setting","ev-p084-related-toolkit-error-types","ev-p084-generated-tool-single-dataset-boundary","ev-p085-large-corpus-scale","ev-p085-retrieval-completeness-failure","ev-p085-non-exhaustive-label"]
-->
# Research Map

## Observed Failure and boundary

- [AUTHOR_FACT] P084 keeps 200 original requests fixed while increasing the average visible menu from 2.7 to 5.6 with semantically related but intended-function-different tools. [[evidence:ev-p084-expanded-toolkit-controlled-setting]]
- [AUTHOR_FACT] The expanded menus produce wrong-function, wrong-count, wrong-parameter, and hallucinated-parameter errors. [[evidence:ev-p084-related-toolkit-error-types]]
- [AUTHOR_FACT] The P084 construction uses one source dataset and LLM-generated related requests/tools. [[evidence:ev-p084-generated-tool-single-dataset-boundary]]
- [AUTHOR_FACT] ToolRet evaluates 7,615 tasks against 43,215 merged tools and reports low complete target-set recovery for query-only retrievers. [[evidence:ev-p085-large-corpus-scale]] [[evidence:ev-p085-retrieval-completeness-failure]]
- [CODEX_SYNTHESIS] The v011 measurable target is function ranking inside a compact related menu. It is not open-corpus completeness, argument correctness, execution, or task success. ToolRet's non-exhaustive labels also warn that semantically plausible alternatives can be false negatives in merged corpora. [[evidence:ev-p085-non-exhaustive-label]]

## Intervention stage

The frozen cross-encoder reads one user query and one serialized tool schema, emits one scalar score and a final-layer CLS vector, then ranks the visible menu. v011 intervenes after frozen encoding and before ranking. It never changes the tool schema, query, gold set, model weights, or visible menu.

## Operator shortlist and source recheck

- **Frozen cross-encoder:** query/schema relevance score; retained as the primary strong baseline.
- **Ordinary related-negative residual:** fit one linear residual vector from gold-minus-added-related CLS differences with logistic pairwise loss and L2. This is a runnable learned-reranker comparator, not the proposed contribution.
- **Thin-menu preservation cap:** compute the largest scalar in `[0,1]` that keeps every positive frozen margin on correctly ranked original thin menus strictly positive. This is the only proposed delta.
- **Generated or mined hard negatives:** ToolRet, CausalNeg, DocReRank, and robust-ranker work establish this as a crowded component family. It cannot itself support v011 novelty.
- **Document/query expansion and hierarchy-aware reranking:** Re-Invoke and ToolRerank are relevant full-pipeline comparators but change tool/query representations or hierarchy/truncation rather than applying the v011 margin-preservation cap.

## Competing method kernels

1. **Generic hard-negative adaptation.** Target: related-tool confusion. Computation: train on gold versus added related tools. Direct denial: it is already a standard learned retrieval/reranking pattern and has no protected delta.
2. **Counterfactual request training.** Target: distinguish near intents. Computation: create or use negative queries. Direct denial: direct recent priors exist, and the local P084 lineage is incomplete for one-to-one supervision.
3. **Thin-anchored residual adaptation.** Target: correct expanded-menu errors while retaining original thin-menu competence. Computation: learn the same residual as kernel 1, then analytically cap its scale using frozen positive thin-menu margins. Direct denial: no OOF final-result gain, no regression reduction versus the unanchored comparator, or a direct prior with the same tool-ranking composition.

## Natural-language disposition

Kernel 1 is retained only as the closest-composition comparator. Kernel 2 is killed before implementation. Kernel 3 is promoted to Candidate because it has one isolatable computation, uses the same model/data/tool budget as its comparator, and can fail directly on final ranking metrics.

## Candidate Promotion Audit

Before Development:

- Target Failure appears as a ground-truth function losing top-1 or rank under a related expanded menu.
- The Candidate changes only the post-encoder residual score scale.
- A positive effect must appear in top-1 and MRR; preservation of a training margin alone is not a result.
- The nearest composition is the identical unanchored related-negative residual head. ToolRet and robust-ranker training are broader component priors.
- P084 Development is already outcome-exposed. Grouped five-fold OOF prevents each held-out query and duplicate query hash from training its own adapter, but does not restore an untouched Development estimate.

## Unique narrow Gap

The only proposed gap is whether a closed-form thin-menu non-reversal cap can retain most corrections from related-negative adaptation while reducing its expanded-menu regressions. No claim is made that hard-negative training, linear residual reranking, or frozen cross-encoder features are new.

## Post-Development Promotion Audit

- The frozen cross-encoder again exhibits the target ranking failure: top-1 `0.930`, MRR `0.9591666667`, with fourteen missed top-1 rows.
- Both the unanchored and thin-anchored OOF residuals have exactly the same top-1 and MRR as the baseline, with zero corrections and zero regressions.
- The learned scores change every row and change the complete order on 22 rows, but all changes remain below the first relevant tool.
- All five fold anchor scales and the full-Development anchor scale equal `1.0`; the proposed cap never binds, so the Candidate is identical to its closest-composition comparator.
- Independent raw audit SHA-256 `52c8ed78f4f0b4db9c6b466c066b34702fe7a840cc6c2926221772c6dc8e2ecf` recomputes all recorded metrics and bootstrap intervals.
- Development fails final-result and mechanism conditions. Confirmation is not authorized. v011 disposition is `DEVELOPMENT_NOT_PROMOTED`.
