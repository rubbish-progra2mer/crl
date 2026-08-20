# Main Codex Implementation Audit v027

Disposition: `APPROVED_FOR_DEVELOPMENT_FREEZE`.

I read the complete v027 `program.py`, independent `audit.py`, conditional acquisition script, config, tests, Candidate, Evidence Packet, Research Map, Selection Context and nearest-prior commitment before any v027 model inference or ranking existed.

## Isolation and computation

- Development query fold is `SHA256(query_id)[1] mod 5`. Each fold's scaler, pointwise control and both pairwise models fit only other query IDs; the held-out query and its entire expanded menu are absent from all fitting.
- The three schema views are deterministic functions of the existing tool bytes. `full` concatenates operation and recursively serialized arguments; `operation` uses split function identity and source description; `arguments` recursively retains paths, names, types, descriptions, enums, required/optional/default and embedded layouts. No perturbed question, original-menu membership, gold count, query-value span, generated text or Confirmation byte enters inference.
- Every training menu creates both orientations of all gold/non-gold tool pairs. Each orientation receives `0.5 / pair_count`, so a query's total pair weight is exactly one and positive/negative pair classes each receive one half. The zero-intercept pair objective is therefore symmetric and menu size does not change a query's total loss contribution.
- The pointwise field control uses the same training rows, field vector, standardizer, learner and C; its per-tool weights total one per query, and explicit class weights are computed from those query-normalized weighted class totals. `pairwise_full` uses the identical pair construction with only the full score. `equal_fields` has no learned coefficients. The primary baseline is the exact full-view cross-encoder score consumed by Candidate.
- OOF top-1/MRR determines the strongest control before Confirmation. One full Development bundle is fit once only for conditional Confirmation and is bound to config, Candidate and Evidence Packet hashes.

## Auditor and conditional acquisition

The auditor does not import `program.py` and never refits. It independently reconstructs query text, gold-name sets, recursive schema views, folds and tool identities; verifies the six-file cross-encoder snapshot; reruns all frozen cross-encoder field pairs; checks frozen scaler means/scales and query-normalized model metadata; replays every method score/ranking; and recomputes top-1, MRR, corrections, fold slices, 20,000 query-row bootstrap samples and all gates. It also verifies config/Candidate/Evidence/input/raw/query-hash/environment/model/report bindings. Tolerances are `1e-6` for repeated GPU cross-encoder logits, `1e-9` for frozen linear scores and `1e-12` for metrics.

The separate acquisition script is conditional only. It has no retry or alternate source: after a positive Promotion Audit it downloads exactly the two configured raw GitHub files at commit `6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`, verifies UTF-8 JSONL and identical unique query-ID sets, and records byte counts, SHAs, URLs, commit, config and Python in one manifest. It has not been executed.

## Actual pre-freeze checks

Shared Python 3.11.15 ran `py_compile` with exit 0 and `pytest -q test_mfcr.py` with exit 0: `5 passed in 6.92s`. The tests cover deterministic recursive fields including embedded `properties.required`, input/gold identity, deterministic query folds and tie-breaking, symmetric pair orientation/weight totals, pointwise weighting and all five score-vector shapes. Exact `.pytest_cache` and `__pycache__` directories were removed; `CACHE_LEFT=0`.

A read-only structural preflight verified the frozen model manifest and parsed all Development inputs without loading the model for inference: 6 model files, 91,815,758 bytes, 200 queries, 1,121 tool candidates, 200 gold names, 3,363 field pairs, and fold counts `34,38,39,47,42`. No v027 field score, coefficient, ranking, metric or Candidate output was computed.

Current bytes:

- program `58e2493aaf5a9bd1f7063d28ed7153ebbc7885b53e6c205deda9d21132e91da6`;
- independent auditor `37d93688c96618d2423a77fc3377e21023a023f9a8ac71dd510092a018530674`;
- config `cd18ad8b645a2c82d98aa9009596303d10097426da2fa7649e84964500bb30c9`;
- conditional acquisition `11405eb06a2683537a0788dde535cc9efa7a3d2dcc1e1a8adb6248784f86bd5c`;
- tests `b5e6c8733588346043d0f9b991ca9b575951d232002f09fdf0530a794b5c4429`;
- Candidate `249a050c1539e579bb120a9f13399f9ddcc49a8e73728d2c733a33415d0dddb3`;
- Evidence Packet `ba3e98ff68703cb062ef3ad01bd1321cf30c031ea84e8ff9027e47c56b854972`, current for all four Evidence entries;
- Research Map `e1cb8a5cf8f540fd7251d0a3d0053d8ae17c67c81b23c98b17c849615019e10d`;
- ToolRerank PDF `dc1d0cf7537401d602aef27160b5f854b688bf607e51d3c0e33febccc66237d4`.

This audit authorizes immutable artifact freezing and one publish-once v027 Development Plan. It does not authorize Confirmation acquisition, Review, Decision, Delivery or `READY_FOR_RESEARCH_USAGE`.
