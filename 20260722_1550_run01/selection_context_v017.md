# Neutral Selection Context

## Version scope

v017 started after the v016 RGP candidate was rejected by all three independent Reviews and by the Main Codex Decision. v017 was required to select a scientifically different failure and computation, use a fresh prospective Confirmation path, and avoid reopening G-only precedence, TPPA, P084 residual retuning, or the v016 measurement claim.

## Data exposure

- The P084 Development rows and their outcomes were already exposed in v008, v009, and v011. No v017 method was fit or screened on those rows.
- The knowledge-base PDF `P041_tool_call_necessity.pdf` was already part of the commissioned paper corpus. The Main Codex re-read its benchmark, method, label construction, and soft/hard-prefill ablations for selection.
- v017 downloaded five primary-paper PDFs into `sources_v017/` only to freeze nearest-prior evidence. It did not download When2Tool, Search-o1, BFCL, ToolRet, or any other Development/Confirmation dataset; it did not acquire model weights or execute model inference.
- The pinned BFCL live-multiple files retained from earlier prospective plans remain unacquired and unread.

## Routes checked

### Query-relative sibling-tool discrimination

The initial route was a direct pairwise or listwise comparison among semantically related candidate tools instead of independent query-tool scoring. Open primary-source search and frozen PDFs showed that this idea is already covered at the relevant level:

- `multi_field_tool_retrieval_2602.05366.pdf` models functionality, input constraints, and output formats as distinct retrieval fields and directly targets semantic and granularity mismatch.
- `scalecall_2511.00074.pdf` directly evaluates listwise ranking for disambiguating functionally overlapping tool inventories.
- `jtpro_2604.19821.pdf` uses rollout-driven reflection to co-optimize agent instructions and per-tool schema/argument descriptions for tool mis-selection and slot-filling errors.
- P087 TOOL-DE/REX and P086 Meta-Tool, already in the formal knowledge base, cover structured independent document expansion and desired-tool/required-parameter matching.

A new Candidate based only on pairwise presentation, sibling negatives, or `when not to use` text would therefore be an implementation variant without an adequately distinct changed computation.

### Counterfactual utility-gated tool steering

The second route started from a real limitation in P041 WHEN2TOOL: PROBE&PREFILL predicts binary model-adaptive necessity and applies a prefill to every item, while its own ablation shows that models differ sharply in whether they obey soft steering. The provisional computation was to collect paired default/tool-prefill/no-tool-prefill outcomes and learn an instance-level intervention-utility gate that defers to the default policy when neither intervention is predicted to help.

This route collided exactly with `to_call_or_not_2605.00737.pdf`. That paper defines true utility by comparing ALWAYS TOOL and NO TOOL outcomes, trains a hidden-state Latent Utility Estimator on positive-versus-neutral/negative utility, and uses its score to control or budget tool calls. `model_adaptive_necessity_2605.14038.pdf` additionally decomposes model-adaptive necessity into cognition and action representations and locates the knowing-doing mismatch at the cognition-to-action transition. The provisional v017 computation is therefore not novel enough to freeze as a Candidate.

## Optional-stopping disclosure

Both routes were stopped at nearest-prior selection. No v017 Candidate claim, implementation, Experiment Plan, Development capture, Promotion Audit, Confirmation, Review Packet, Reviewer, Decision, or Delivery was created. No empirical outcome was observed and no threshold, model, dataset subset, or claim was retuned.

