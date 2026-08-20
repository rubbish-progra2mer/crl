# Main Codex Implementation Audit v026

Disposition: `APPROVED_FOR_DEVELOPMENT_FREEZE`.

I read the complete v026 `program.py`, independent `audit.py`, `config.json`, `test_cmcd.py`, Candidate, Evidence Packet, Research Map, Selection Context and nearest-prior commitment before any Plan or Candidate score existed. The implementation changes the computation from v025 VIAF and v021–v022 single-reference residuals to a supervised cross-generator query/support pair model with a fixed four-control ladder.

## Leakage and support audit

- Task folds are `SHA256(task_id)[1] mod 3`. For each OOF bundle `(target_model, fold)`, training queries exclude the held-out fold and the complete target generator. Because supports share the query task, their task fold is also outside the held-out fold; `support_indexes` additionally excludes both the query generator and bundle-target generator.
- A training query therefore uses successful supports only from the third generator family. A held-out query uses successful supports from both other families. This distributional difference is explicit in the frozen setting rather than hidden: the Candidate asks whether the same pair learner can aggregate the two available cross-model supports at evaluation.
- Eligibility requires at least one successful baseline from every one of the three generator families. The read-only input preflight exited 0 and returned 4,256 source rows, 250 source tasks, 228 eligible tasks, 4,072 evaluated rows and 22 fixed excluded tasks.
- The three immutable input manifests preserve their original acquisition phases: bucket 1 Development, bucket 2 Development and bucket 3 v022 Confirmation. Bucket 3 is already exposed and is used only as v026 Development; neither its manifest nor its historical role is rewritten. Bucket 0 remains untouched.
- Each OOF row is assigned by exactly one `(target_model, fold)` bundle. The vectorizer fits only allowed training-query text. Full target-generator-excluded bundles are fit once and saved only for conditional frozen Confirmation.

## Comparator and loss audit

- `direct=[q]` is the ordinary transfer baseline; `triple_query=[q,q,q]` matches three sparse blocks; `consensus_no_abs=[q,r,r]` retains support and aggregation without the absolute-deviation block; `single_support` uses the same frozen Candidate pair model and lexicographically first allowed support. Candidate uses the mean of all allowed `[q,r,abs(q-r)]` pair probabilities.
- Pair construction gives every query's pairs raw weights summing to one. Pair-model class weights are computed from query-class counts, not duplicated pair counts, so support multiplicity neither changes a query's total loss weight nor inflates the global regularization scale. Direct and triple controls use the same query-level balanced-class convention through the shared base classifier.
- Candidate and no-absolute models use identical pair rows, weights, learner, vocabulary and regularization. Candidate and single-support use the identical fitted Candidate pair model. No threshold, support selector, hyperparameter, task removal or comparator may be changed after the Plan.

## Auditor and binding audit

The auditor independently reconstructs eligibility, supports, folds, pair matrices, aggregations, all five row scores, AUC, empirical TPR@5% FPR, task bootstrap, generator slices and every gate without importing `program.py` and without refitting. It verifies Candidate/Evidence/config/base/dataset/manifest/raw/source/model hashes, original acquisition phases, row/source/support identities, nine OOF bundle metadata records, three full-bundle metadata records, query-class weights, frozen strongest comparator and summary bytes.

`py_compile` exited 0. At the correct `implementation_v026` cwd, shared Python 3.11.15 ran `pytest -q test_cmcd.py` with exit 0: `6 passed in 2.03s`. Tests cover all-three-generator eligibility, simultaneous query/target-model support exclusion, exact absolute-deviation blocks, deterministic task folds, single-versus-mean aggregation and query-level pair/class weighting. Exact local `.pytest_cache` and `__pycache__` directories were then removed; `CACHE_LEFT=0`.

Current pre-freeze identities:

- program `d709235915e1406fa65c38b567773bc1fa43e3aad6be71e66bdd1b845053d2e1`;
- independent auditor `1676eecf7886b8a76047da8c50458b9855749bbede297fddebee90a9c9e83f3f`;
- config `9b784ed930a5514fe57a40c484519ca6d32c09ef45e9f0a091c35af2d84dd0c9`;
- tests `f7accf7ea298e99765e4d87c594bff479d71b1e6c07269184d2ad3efc4fae9fc`;
- Candidate `b43922594122236b08fcdd94836a5731a8d1cc91c49e7a0a918b51a225bc5f61`;
- Evidence Packet `0ad0e89d9dc7a690d4c4b586d10e37504df23c4a2e9d1a4541a1794dd9c1b3f8`, rebuilt through the workspace API and current for all three cited Evidence entries;
- Research Map `932c5a7e37565b2f060df4f141e2c4db4660342f275a34ee58b0456066378f23`.

This audit authorizes immutable artifact freezing and one publish-once Development Plan. It does not authorize bucket-0 acquisition, Confirmation, Review, Decision, Delivery or `READY_FOR_RESEARCH_USAGE`. Gate booleans cannot substitute for the post-Development main-Codex Promotion Audit.
