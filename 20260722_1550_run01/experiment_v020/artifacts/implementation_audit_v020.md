# Main-Codex Implementation Audit v020

Status: `IMPLEMENTATION_READY_FOR_ONE_SHOT_DEVELOPMENT`

This is a pre-execution code/protocol audit. No v020 model has been fitted and no v020 Development metric exists.

## Candidate and evidence bindings

- Candidate SHA-256: `7C1326B3309CD0E21F52C749B38724C965821E81CF6880F20DDE07678462F690`.
- Rebuilt Evidence Packet SHA-256: `514F61891E70AF5BE51A23DF0E891DD3CABB0C2DE18BC3112C79BD7BDF6F1154`.
- Packet rebuild reported the Candidate current and all three cited Evidence PDF/passage bytes current.

## Fixed data carrier

- Exposed Development dataset: 38,050,057 bytes, SHA-256 `BD766EB62CF98E8FB1B8DD17C20D5EDFC759EEB737BD3C232F73E656F9E713A3`.
- Frozen v012 base evaluator: 39,154 bytes, SHA-256 `A29B8AACE75BF5505620FAB71C982E296E045CB1590A20A5A9C19A63C233D78D`.
- Frozen prospective acquisition program: 12,438 bytes, SHA-256 `CF87EC4994081B4516695806B471DAF75E923FE511D0B67D05B4AB126D34E836`.
- Repository commit: `d8a29613235a0ef56a8b70b3142626a533da28c2`.
- Development bucket: 2. Prospective Confirmation bucket: 3, still unacquired and unread.

The main-Codex structural preflight opened only exposed Development bytes and exited `0`. It reconstructed 1,729 source rows, 94 references, 1,613 evaluated examples, and two ineligible tasks. Deterministic splits were 54/20/20 tasks and 943/318/352 rows for train/validation/Development-test. Development-test contained 131 negatives and 221 positives. Reference/evaluated row overlap was zero.

## Primary-source readback

- Terminal Wrench PDF SHA `140DF68E...19E8A`, five pages: stripped monitoring AUC `0.9168`, TPR@5%FPR `0.44` on its reported judge population.
- Cheap Reward Hacking Detection PDF SHA `C5FD9451...75CE0`, 20 pages: separately stripped-trained encoder AUC `0.7631`, TPR@5%FPR `0.2275`; full reasoning-visible result is not a same-information comparator.
- TRACE PDF SHA `98A3121D...3A5649`, 22 pages: contrastive clusters improve its reported LLM Detection Rate from 45% to 63%, preventing a first-contrastive claim.
- Praetor PDF SHA `842D593F...15AA98`: verified-benign pDFA/parameter envelopes target runtime structured workflows, not the fixed v020 post-hoc classification setting.

## Program audit

`implementation_v020/program.py`, SHA-256 `67AC151B6817D6619F915AAD581DA6C70F9ECDAFEB780D87E31816C36009DE92`:

- reconstructs exactly one excluded successful reference per eligible task using the frozen v012 rule;
- fits the TF-IDF vocabulary only on evaluated training trajectories, never on validation/test labels or Confirmation;
- uses identical vocabulary, labels, class weights, logistic learner, C, seed, and validation threshold selection for all five methods;
- computes `novel=max(x-r,0)` and `missing=max(r-x,0)` without dense expansion;
- includes raw text, reference concatenation, unsigned absolute delta, and v012 RCED as mandatory comparators;
- selects the strongest comparator conservatively from Development-test AUC and freezes that identity before Confirmation;
- saves the vectorizer, scaler, all five models, thresholds, feature dimensions, Development task IDs, raw predictions, reference records, source hashes, and environment;
- Confirmation code loads the frozen bundle, rejects task overlap, and performs no fit or threshold selection.

The maximum scientific delta is the signed sparse residual representation. There is no LLM call, trajectory generation, repository write, or environment mutation in Development.

## Independent audit audit

`implementation_v020/audit.py`, SHA-256 `2F42878764989288EE44A68D287AF2CCCFB2E25F72F7EB2FDE40E9D81A898607`:

- independently reconstructs reference selection and deterministic task splits from raw input;
- verifies config, dataset, base module, raw rows, reference records, summary, and model bundle hashes;
- loads all five frozen models and independently rebuilds all feature matrices and scores;
- checks raw row IDs, targets, reference IDs, reference exclusion, and Confirmation task disjointness;
- independently recomputes five AUC/low-FPR/frozen-threshold metric records, strongest comparator, 2,000 task-cluster bootstrap samples, and every gate;
- returns exit `1` on any binding, score replay, metric, split, or reference error.

## Tests and config

- Config SHA-256: `FB437F9B70D57E7CA0C4D13BAA13A41B0F28BE0441870574F7B909C2208CD43B`.
- Objective test SHA-256: `4FC711296923E32FA0E0AC72B538CD01CEA5CE8A8B0C22E6574447CE15395500`.
- Final `py_compile` over program, audit, and test: exit `0`.
- Final `pytest -q implementation_v020/test_residual.py`: exit `0`, `2 passed in 1.99s`.
- Tests prove residual direction/reconstruction and zero residual for identical vectors.

## Main-Codex conclusion

No bounded pre-execution defect was found that invalidates one frozen Development. Implementation, config, dataset, base/acquisition modules, Candidate, Packet, tests, prior commitment, and four primary PDFs must now be frozen through `ResearchWorkspace.save_experiment_artifact()`. The publish-once Plan must bind their hashes and exact runner argv before fitting. No Reviewer is authorized.
