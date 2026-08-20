# P082 Reconciliation

- Disposition: `LIMITED_ADMISSION_SINGLE_CALL_TOOL_LEARNING`
- Read 1 SHA-256: `846662907b0f30a64c9c49ee943a1d2470cb67d768d9e8dfda4a4d51d24ff9d0`
- Accepted read-2: `read_2_attempts/r2-20260720-p082-a1/`
- Read-2 invocation SHA-256: `8ed98ab09b184fdc8894e623080c7932225ab7d0ebcaf5743dc3e0512e1a0b35`
- Read-2 report SHA-256: `a56dd788ab4f85851817bf365a4b5651dbb1b8fa892f5b31588cf2f562c697c3`
- Accepted read-3: `read_3_attempts/r3-20260720-p082-a1/`
- Read-3 invocation SHA-256: `8f3658f4dfe9f997383d0d1bc1e42a7f3ecb8dbc1690bc635a3f0c3ced580dd9`
- Read-3 report SHA-256: `d8cf95c949e54be0240609418d456351cd3b2eeb0277aa9ad5bdcd47252aec63`
- Other attempts: none.

## Source reconciliation

- `AGREE`: the model proposes inline API calls from a few demonstrations, executes them, filters by improvement in weighted future-token loss, inserts surviving calls/results into text and receives ordinary LM fine-tuning.
- `HINDSIGHT_BOUNDARY`: usefulness labels inspect already-existing future corpus tokens. This is offline hindsight supervision, not an online causal judgment of task success, truth or safety.
- `UTILITY_BOUNDARY`: lower future-token loss is not Agent utility; the source includes an irrelevant search result that still receives a positive score.
- `TRIGGER_BOUNDARY`: headline evaluation forces an API call whenever the API token enters top ten and reaches near-universal calling on several tasks. This is not natural top-1 greedy calibration.
- `INTERACTION_BOUNDARY`: evaluation allows at most one call per input; independently generated tool data cannot train chaining, browsing several results or query reformulation.
- `SYSTEM_BUDGET_BOUNDARY`: GPT-J-6.7B controls Atlas-xxl, BM25 Wikipedia, NLLB and calculator tools. External model/retrieval size, call cost and large-scale data-generation cost are not included in the 6.7B comparison.
- `MEASUREMENT_BOUNDARY`: LAMA/QA/math/MLQA use containment or first-number parsers that are looser than standard exact matching. Scores remain within-protocol facts, not strict cross-paper benchmark accuracy.
- `SCALE_AND_COST_BOUNDARY`: useful-call data can be extremely sparse, training uses eight A100-40GB GPUs, small controllers fail to benefit, and tool latency/monetary cost is absent from the decision objective.

## Frozen source role

Canonical single-call tool-learning ancestor for loss-utility-filtered self-supervision, paired with a Failure warning that predictability, forced calling and external oracle strength can masquerade as autonomous Agent tool competence.
