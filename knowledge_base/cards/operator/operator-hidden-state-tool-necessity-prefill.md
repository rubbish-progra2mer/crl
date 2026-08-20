<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-hidden-state-tool-necessity-prefill","card_kind":"operator","paper_id":"P041","evidence_ids":["ev-p041-operator-core","ev-p041-probe-prefill-steering"],"source_refs":[{"path":"papers/P041_tool_call_necessity.pdf","sha256":"a05f71b904209ea49cbc9cd13434255aab4037f96640477810fb78a61b701ba0"}]} -->
# Hidden-State Tool-Necessity Probe with Prefill Steering

## Intervention target
[CODEX_SYNTHESIS] Whether generation is softly steered toward direct solving or tool use before the response begins.

## Before and after computation
[CODEX_SYNTHESIS] Prompted agents indiscriminately call or skip tools. The changed computation reads final-input-token hidden states with a linear probe, thresholds the necessity estimate, and prefills a short steering sentence before normal generation; it does not disable tool access.

## Inputs outputs information and timing
[CODEX_SYNTHESIS] Input: cross-layer hidden states for the final input token. Output: a probe probability/binary prediction and corresponding tool-needed or tool-unneeded prefill. Timing: immediately before generation; API and arguments are still selected by the model.

## Mechanism hypothesis
[CODEX_HYPOTHESIS] The model may encode necessity even when its generated policy fails to act on that information, and a short prefill can expose that latent distinction.

## Predicted observable signature
[CODEX_HYPOTHESIS] At a fixed accuracy target, unnecessary calls should fall without transferring work to longer reasoning; soft-prefill overrides should remain observable.

## Preconditions and transfer risks
[CODEX_SYNTHESIS] Labels rely on forced no-tool correctness oracles, internals must be accessible, thresholds are model-specific, and a prefill is steerable rather than an enforcement boundary.

## Source lineage
[CODEX_SYNTHESIS] Prompt-only tool restraint → latent necessity probe → inference-time prefill steering.

## Evidence ledger
[AUTHOR_FACT] The paper derives labels from forced no-tool success, decodes necessity from hidden states, and uses the prediction to prefill a steering sentence. [[evidence:ev-p041-operator-core]] [[evidence:ev-p041-probe-prefill-steering]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] WHEN2TOOL; hidden-state probe; PROBE&PREFILL; tool necessity; pre-generation steering; tool overcalling
