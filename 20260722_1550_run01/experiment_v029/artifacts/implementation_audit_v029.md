# Main Codex Implementation Audit v029

Disposition: `APPROVED_FOR_DEVELOPMENT_FREEZE`.

I read the complete v029 program, independent auditor, acquisition script, config, tests, Candidate, Evidence Packet, Research Map, Selection Context and nearest-prior commitment before any v029 cross-encoder score existed.

## Computation and isolation

- Four texts are deterministic from source tool bytes: full, name-plus-arguments, name-plus-operation-description, and name only.
- `operation_drop` and `argument_drop` are literal score differences from the same full score. Candidate is exactly `full + min(operation_drop, argument_drop)`.
- Controls are full, each single deletion view, the mean of both drops and the maximum of both drops. There is no fitted value, menu normalization, generated text, original-menu marker, gold count or adaptive rule.
- Query folds are deterministic evaluation slices only; no data is fit. Development and Confirmation use identical computation.
- Confirmation acquisition is conditional and pinned to two exact raw GitHub paths at commit `6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`.

## Independent audit

The auditor does not import the program. It independently rebuilds all texts, reruns all 4,484 cross-encoder pairs, reconstructs six scores for 1,121 tools, replays SHA tie-breaking, rankings, top-1, MRR, corrections, five fold slices, 20,000 bootstrap samples and gates, and checks every config/data/model/raw/query/environment binding.

Support requires view-score repeat error `<=1e-6`, formula and metric error `<=1e-12`, no identity/ranking error and `AUDIT_OK`.

## Actual pre-freeze checks

Shared Python 3.11.15 ran `py_compile` with exit `0` and `pytest -q test_dcn.py` with exit `0`: `6 passed in 4.56s`. Tests cover recursive schema views, all Candidate/control formulas, deterministic folds/ties, missing-gold rejection, frozen method order and independent auditor equivalence. Generated caches were removed; `CACHE_LEFT=0`.

A structural preflight verified Candidate/Packet/data/model hashes and parsed 200 queries, 1,121 tools, 4,484 planned query/view pairs, fold counts `34,38,39,47,42`, and six model files totaling 91,815,758 bytes. It did not load the model or compute a v029 score.

Current bytes:

- program `2a77cfc2cd4f3b5f0d65ba6a9a4c08541dd7318edafabd39b72c92abdcfe74d5`;
- independent auditor `be43956b4099bbc8d37b6a775e40ee3f8419566e4dfbc91077c0715dca1f7308`;
- config `48fc9344c937edf5007f2aabb71619bfcf070eba3274a19bbf5c19d1ab5e4431`;
- acquisition `11405eb06a2683537a0788dde535cc9efa7a3d2dcc1e1a8adb6248784f86bd5c`;
- tests `1425f3e239f12cefb6dd899b5afeff12389d3bc03888cfa79c8b596a278d8d89`;
- Candidate `2ea2c1ef080a1edc1b81c94161e8f215931cb4fe4fb3449580baf8ef9814c244`;
- Evidence Packet `1317d24f9a2e63826b47f330fb0510f6567ab82c3df9fea899399c5c748dea6d`, with all four formal Evidence entries current.

This audit authorizes immutable artifact freezing and one publish-once v029 Development Plan. It does not authorize Confirmation, Review, Decision, Delivery or `READY_FOR_RESEARCH_USAGE`.

