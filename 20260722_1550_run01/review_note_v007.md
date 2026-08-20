# v007 Common Review Note

## Commitment bindings

- Common Protocol snapshot: `review_v007/supplemental/review_inputs_v007/CRL_REVIEWER_PROTOCOL.md`, 7,812 bytes, SHA-256 `d1dc1d603d562585fbe06a22597f8bd3d31182fdc000bdba45eb1f999c8026b8`.
- Prior role snapshot: `review_v007/roles/crl_prior_reviewer.md`, 1,413 bytes, SHA-256 `6261eeab830bb827371bb45442a92ee8a2908a41e55cea66417fea029508e048`.
- Scientific role snapshot: `review_v007/roles/crl_scientific_skeptic.md`, 1,474 bytes, SHA-256 `ff2877807562096f85306c257a8b6dcacc3f1dfd2a0173f4faf3b2156bb791ea`.
- Potential role snapshot: `review_v007/roles/crl_potential_reviewer.md`, 1,210 bytes, SHA-256 `42d0d78c4d3921f98c271cb271e4285cf0a7afda17a57d6f200985126ce16c6f`.
- Private Main Codex prior commitment: `nearest_prior_v007.md`, 949 bytes, SHA-256 `a35b853f126a29ff97722c0d51adbfb1fd312668a7febd886874978469a2b9c8`. Its text is excluded from this common Packet.

Peer role text is excluded from the common frozen-artifact manifest. Each Reviewer receives only its own committed role snapshot. All three exact requests must contain `REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN`.

## Neutral candidate and comparator identity

The frozen operation measures target-aware ToolRet training prompts against a deterministic distribution of three label-disjoint wrong-target prompts. Each 1,000-row phase forms one deduplicated corpus. Every query has six views: `query_only`, `aligned_full`, `mismatched_full_1`, `mismatched_full_2`, `mismatched_full_3`, and `generic_full`.

The primary controls are the three `mismatched_full_N` views. They use the same recipient query, retriever, corpus, top-k, and number of prompt tokens selected by minimum token-length difference with deterministic SHA tie breaking. `query_only` and `generic_full` are additional context controls. The aligned-minus-mean-mismatched NDCG@10 effect is aggregated first within ten fixed contiguous 100-row blocks and then equally across blocks.

The two retriever identities are:

- BM25 implemented in frozen `audit.py`, `k1=1.5`, `b=0.75`, deterministic complete top-10.
- `sentence-transformers/all-MiniLM-L6-v2` revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, normalized embeddings, CUDA, batch size 256, top-10.

No separate learned candidate retriever is compared. The tested delta is the input-control audit operator, not a deployable retrieval model. Attribution is therefore bundle-level to the aligned prompt versus the frozen three-donor control distribution.

## Frozen data and cost facts

- Dataset: `mangopy/ToolRet-Training-20w@fdf5a317455b1e60785de7ba587496aa6cc878e4`.
- Development rows: `[0,1000)`; 1,000 queries; 9,436 corpus documents; 12,000 raw cells.
- Confirmation rows: `[207826,208826)`; 1,000 queries; 9,309 corpus documents; 12,000 raw cells.
- Each phase evaluates 1,000 queries x 6 views x 2 retrievers. Bootstrap seed is `20260722` with 20,000 block-level replicates.
- Development source acquisition: 51.72985870001139 seconds. Development evaluation: 181.47894000000088 seconds.
- Confirmation acquisition: 56.819312200008426 seconds. Confirmation evaluation: 337.3789433000002 seconds. Main Codex independent audit: 3.128208500000028 seconds.
- Shared environment: Python 3.11.15, NVIDIA GeForce RTX 5060 Ti, PyTorch 2.12.0+cu130, CUDA runtime 13.0, sentence-transformers 5.6.0.
- No paid API was used. Dataset acquisition used the public Hugging Face rows endpoint with a fixed three-second delay.

## Same-Run attempt disclosure

- v001-v003 were execution-only acquisition failures caused by HTTP 429/SSL behavior and produced no scientific metric.
- v004 completed Development and Confirmation but failed its frozen Confirmation condition because one MiniLM source effect was exactly zero.
- v005 passed Development and failed untouched Confirmation donor coverage before producing Confirmation metrics.
- v006 acquired the Development range and failed before metrics because the embeddings output parent did not exist.
- v007 changed only that output-directory execution defect, reused the exact touched Development acquisition bytes, and left the Confirmation range untouched until the recorded promotion audit.

The common supplemental manifest includes the Run ledger and the prior versions' Selection Context, Candidate, Plan, Result, and attempts manifest so these failures and design changes are inspectable. No prior failure is presented as Delivery evidence.

## Neutral result facts

Development independently reconstructed 12,000 unique cells. BM25 equal-block mean/median/bootstrap were `0.17294899966329502`, `0.16745071801763145`, and `[0.1575434082996223, 0.19102766900522142]`. MiniLM values were `0.20330747026568474`, `0.20031678887676024`, and `[0.19424093392342617, 0.21287438671633252]`.

Confirmation independently reconstructed 12,000 unique cells, 12,000 complete unique corpus-bound top-10 rows, 3,000 deterministic donor pairs, zero target-overlap pairs, exact qrel metrics, and exact block/bootstrap summaries. BM25 equal-block mean/median/bootstrap were `0.15472698575926586`, `0.15881437019579883`, and `[0.13810078540627505, 0.17154230511897298]`. MiniLM values were `0.19767190048609523`, `0.1985772107226651`, and `[0.18139115743783601, 0.21385848024999743]`. Both retrievers were positive in all ten blocks. The lexical mechanism mean was `0.21566037397225948`.

The foreground shell returned timeout code 124 during Confirmation evaluation while the already-started single runner continued. Process inspection prevented a duplicate attempt; the runner later closed an exit-0 capture with all declared outputs.

## Claim boundary and disclosed defect

The maximum candidate claim is limited to positive-tool-linked retrieval information in target-aware generated training prompts beyond this deterministic three-wrong-prompt control distribution on the two frozen row ranges. It does not establish a deployable retriever improvement, causal effect, exhaustive labels, end-to-end task improvement, universal behavior, or all-row generalization.

The frozen Candidate's final procedural sentence says a failure freezes `v006`; for the current version the Run protocol would freeze `v007`. This stale version label does not change the frozen computation, data, gates, or success-path evidence. The executed Candidate bytes were not overwritten.
