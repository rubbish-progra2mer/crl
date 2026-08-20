# RUN_LEDGER

- EVENT: RUN_CREATED
  AT: 2026-07-26T19:55:49+08:00
  MODE: RESEARCH
  VERSION: v001

- EVENT: PAID_API_PREAUTHORIZATION_RECORDED
  AT: 2026-07-26T19:58:00+08:00
  DETAIL: RUN_CHARTER.md updated with user grant of 2026-07-26; providers=deepseek; ceiling=USER_UNLIMITED (spend judiciously, report per experiment); purpose=subject rollouts, data generation, in-Run judging. Key never persisted.

- EVENT: PREFLIGHT_PASSED
  AT: 2026-07-26T19:54:00+08:00
  DETAIL: check_crl_health.py all_checks_pass=true; manage_cards.py validate 192 cards; pytest 111 passed. All exit 0. (Correction note: preflight ran before RUN_CREATED as required by CRL.md; recorded here after Run initialization.)

- EVENT: PROBLEM_V001_FROZEN
  AT: 2026-07-26T20:14:00+08:00
  ARTIFACT: problem_v001.md
  SHA256: cae9ef65de842f69c839365a58c8ef88ec78ac6dd5d509de0a919e7ba9c9400d
  DETAIL: Problem fixed after 11-query open-web occupancy scan (2026-07-26). Chosen open node: per-constraint enforcement audit and masking-rate quantification for NL-to-executable-constraint-model pipelines certified by solution-level checks; mechanism dimension (slack-luck structure) and complementarity dimension (error-triggered repair blindness to silent faults). Nine adjacent spaces found occupied and recorded in the Problem's occupancy scan section.

- EVENT: RESEARCH_MAP_V001_WRITTEN
  AT: 2026-07-26T20:40:00+08:00
  ARTIFACT: research_map_v001.md
  SHA256: dcb992df6a6c2ae58208c586e40bc500217f86cb844b4e355079ea6c966de7f9
  DETAIL: Three formal card queries (failure/operator/paper) + internal-lane query (0 hits, normal) executed 2026-07-26. Cross-cluster probe hit - P050 active counterexample verifier shares the compute property "acceptance evidence from passive output check to active counterexample search" with the planning-cluster certification failure. Kernels - K1 per-constraint enforcement probe and masking decomposition (keep, single unverified jump), K2 probe-triggered silent repair (kill this version - second jump plus occupied repair node). P055 Limitations page verified in original PDF (p.10 - "no feasible alternative", 20-sample zero-FP boundary). 14 evidence IDs bound. No experiment data downloaded or read at map time.

- EVENT: DATA_SPLIT_COMMITTED
  AT: 2026-07-26T20:52:00+08:00
  ARTIFACT: data_split_commitment_v001/MANIFEST.json
  SHA256: dfeaf9fe4688f9388576c6fbd36960eb095d1262bd8e2cf7e4c078551776dc7e
  DETAIL: Commit-reveal split of TravelPlanner validation split (osunlp/TravelPlanner, validation.csv + validation_ref_info.jsonl) executed BEFORE any instance content or outcome was read. Rule sha256("run03_tp_val_{i:03d}") % 5 -> {0,1}=W(67) {2,3}=D(80) {4}=C(33). Physically separate bucket files written; C bucket reserved untouched. Script frozen in same directory (self-SHA recorded in manifest).

- EVENT: Z3_EXCEPTION_ENV_CREATED
  AT: 2026-07-26T21:05:00+08:00
  DETAIL: Run-local exception environment D:\Desktop\crl\20260726_1955_run03\.venv_z3 (conda python 3.11.15 + pip z3-solver==4.15.4). Evidenced conflict - the shared env acceptance command compares pip freeze line-by-line against CRL_ENVIRONMENT_LOCK.txt; adding z3-solver would fail it, and lock refresh requires user approval. Env serves only this Run's solver-side execution; full spec to be recorded in experiment plan.

- EVENT: K1_WORKBENCH_FALSIFIER_COMPLETED
  AT: 2026-07-26T21:55:00+08:00
  ARTIFACT: workbench_v001/falsifier_report.md
  DETAIL: Decisive falsifier DID NOT fire. 22 W-bucket TP-SC3 instances, free-form deepseek-chat formalization (response model deepseek-v4-flash, temp 0): 16 ran, 14 certification-PASS, 4/14 (29 percent) with certificate-backed unenforced categories (cuisine x3, room_type x1) = masked silent under-constraint; plus caught case (house_rule) and 5 default-UNSAT over-constraint cases. K1 authorized into frozen implementation. Workbench artifacts frozen (cited by research_map_v001 rev 49fa5e04 and this ledger). API usage ~35.4k tokens.

- EVENT: RESEARCH_MAP_V001_REVISED_PREFREEZE
  AT: 2026-07-26T21:58:00+08:00
  ARTIFACT: research_map_v001.md
  SHA256: 49fa5e048b68dd2c1b09779e97996a92dac3568dfac59fe2b215fafa7f7b2071
  DETAIL: Pre-freeze revision adding actual falsifier results to K1 disposition. Supersedes rev dcb992df (pre-falsifier). Packet not yet frozen; version discipline intact.

- EVENT: CANDIDATE_V001_AND_EVIDENCE_PACKET_WRITTEN
  AT: 2026-07-26T22:40:00+08:00
  ARTIFACT: candidate_v001.md / evidence_packet_v001.md
  SHA256: 42e017c7f32e9d3fc2efda86080504456ab608f6523d07902993a8916455bb62 / 181646a9882a7daea2cc583addebd95a70419c27e57463ff5877fb7b7ef536b8
  DETAIL: K1 candidate (per-constraint enforcement probe + masking decomposition harness) with 14 evidence bindings; single unverified jump = masking phenomenon with slack structure on fresh data.

- EVENT: NEAREST_PRIOR_V001_PRECOMMIT_DRAFT
  AT: 2026-07-26T22:20:00+08:00
  ARTIFACT: nearest_prior_v001.md
  DETAIL: Private prior record drafted (4 views, exact searches, collisions incl. ReLoop 2602.15983 / Constraint Injection 2606.04816 / Zhong-Yu-Klein 2020 / vacuity-coverage classical thread). Final SHA to be committed at packet freeze; body excluded from common packet.

- EVENT: IMPLEMENTATION_AND_INPUTS_FROZEN
  AT: 2026-07-26T23:05:00+08:00
  ARTIFACT: experiment_v001/artifacts/ (11 files)
  DETAIL: tp_lib 74c21af7 / tp_prompt 6e89a8ac / tp_api 05388a7b / tp_solve_probe 1757291f / run_promotion fdfbbc53 / analysis 6ab2b874 / config 71657f07 / config_readiness a68fa89c / input_bucket_D.csv 3298b92a / input_bucket_D_ref_info 24eb1337 / input_split_manifest dfeaf9fe.

- EVENT: RESEARCH_MAP_V001_PRE_DEV_AUDIT_APPENDED
  AT: 2026-07-26T23:20:00+08:00
  ARTIFACT: research_map_v001.md
  SHA256: 0db0eddaaff5702296eaae90dca6bcbbfcebaa9661d475a19428b0ddb096a742
  DETAIL: Candidate Promotion Audit (pre-development questions) appended before any D-bucket read. Supersedes 49fa5e04.

- EVENT: EXPERIMENT_PLAN_V001_FROZEN_AND_READINESS_PASSED
  AT: 2026-07-26T23:30:00+08:00
  ARTIFACT: experiment_v001/plan.md
  SHA256: e53f64759163dd80c584e62c293fd08533865be7b07037903c2dcfa33d84d3de
  DETAIL: Plan frozen before results with preregistered SIG-1/SIG-2, C-bucket confirmation plan (C-GATE-1/2), z3 exception env record, and full exact-execution-readiness readback (selftest 0 mismatches; near-real W smoke incl. 3 real API calls; secret scan clean). dev_001 capture launched after freeze.

- EVENT: CORRECTION_TIMESTAMPS
  AT: 2026-07-26T21:12:00+08:00
  DETAIL: Correction to the AT fields of six earlier entries written with an over-advanced clock. Actual wall-clock (Asia/Shanghai): K1_WORKBENCH_FALSIFIER_COMPLETED ~20:58 (not 21:55); RESEARCH_MAP_V001_REVISED_PREFREEZE ~21:00 (not 21:58); Z3_EXCEPTION_ENV_CREATED ~20:40 (not 21:05); NEAREST_PRIOR_V001_PRECOMMIT_DRAFT ~20:52 (not 22:20); CANDIDATE_V001_AND_EVIDENCE_PACKET_WRITTEN ~20:55 (not 22:40); IMPLEMENTATION_AND_INPUTS_FROZEN ~21:00 (not 23:05); RESEARCH_MAP_V001_PRE_DEV_AUDIT_APPENDED ~21:02 (not 23:20); EXPERIMENT_PLAN_V001_FROZEN_AND_READINESS_PASSED ~21:03 (not 23:30). Event ORDER in this ledger is correct and matches artifact mtimes; only the clock readings were wrong. Original entries left unmodified per correction discipline.

- EVENT: DEV_001_COMPLETED_AND_RESULT_WRITTEN
  AT: 2026-07-26T21:35:00+08:00
  ARTIFACT: experiment_v001/result.md
  SHA256: 422f4d34a08491b0719a7f1a063d8ab7d653154b9385af17f23c2ca035b7d416
  DETAIL: dev_001 single-segment capture (28/28 D-bucket SC3 instances, exit 0, wall ~11.5 min) + metric_audit_001 (analysis recomputation capture). Headline: F1 23 ok / 21 certification-PASS; 3 certificate-backed faults (1 masked cuisine idx120 luck=1.0, 2 caught house_rule); M2 = 1/21 = 4.8% Wilson [0.85%, 22.7%] -> SIG-1 PASS; SIG-2 primary PASS (n_masked=1 disclosed); density-proxy direction failed (reported honestly). A3 self-check 0/3 covered (0/91 false alarms); A4 behavioral 3/3 (0/68); F2 checklist scaffold 0 faults in 26. API 84 calls, 124,766 tokens. All witnesses checker-confirmed. 10 result artifacts saved (captures + outputs + instance zip).

- EVENT: AUDITS_APPENDED_AND_SUPPORT_DOCS_FINAL
  AT: 2026-07-26T21:45:00+08:00
  ARTIFACT: research_map_v001.md / selection_context_v001.md / nearest_prior_v001.md
  SHA256: 5ba2f32e3a090393e6356cc6c30ccfa351c5be231dea8d45d203ef7f348b3940 / (in packet manifest) / bf323e29b576e3ed3f75697cae8eab647912579a9dcaf9f6814acb389b165394
  DETAIL: Post-development Promotion Audit + Seed Readiness Audit appended (C-GATE-1 severity ~8 percent computed and disclosed). nearest_prior_v001.md finalized and precommitted; body excluded from packet.

- EVENT: REVIEW_PACKET_V001_FROZEN
  AT: 2026-07-26T21:52:00+08:00
  ARTIFACT: review_v001/packet.md
  SHA256: 741ea35369def8513d7e6a3622c3498313012ff43f17d921f4eba7c26726362c
  DETAIL: Frozen with experiment v001 artifacts (21 files incl. captures and outputs) + 17 supplemental files (research map, selection context, split commitment, workbench falsifier chain incl. per-instance zip, readiness evidence, charter). Commitment section binds protocol snapshot ba46b084 / role snapshots 6261eeab, c9a401432, 90dc36c2 / private prior bf323e29. Three formal report slots verified empty before any reviewer launch. Snapshot copies restored into review_v001 after mechanical freeze (freeze tool requires creating the directory itself; packet manifest unaffected).

- EVENT: THREE_FRESH_LEAF_REVIEWERS_COMPLETED
  AT: 2026-07-26T22:20:00+08:00
  ARTIFACT: review_v001/reviewer_1.md / reviewer_2.md / reviewer_3.md
  SHA256: ef5297f359b84da5eca397ca3c78ea45c332059976fda33200e5e62d1aa2a21b / 6cafe0c2ed266671ca6e4f9db8c027ea468a47030d9be7341b3635530bff8552 / 86f16f7f106ceb3de7453d908739b2068925d52bfd6cf50467802748d1487814
  DETAIL: Launched simultaneously as fresh leaf subagents 21:57; staged reports written by each reviewer (MD-12 channel), returned texts verified identical, saved via manage_review save-report only after all three returned. All three: full per-artifact hash readback (30 items each), no fatal objections, deliver-after-fixes recommendations. R1 ran 13 open-web queries + 6 full-text retrievals and surfaced VeriSimpl (2607.20474); R2 independently recomputed all metrics, re-executed idx120 with self-written probe code, re-probed the discarded workbench first-launch response; R3 re-ran analysis (JSON-equal), selftest, and idx120 certificate offline.

- EVENT: PRE_DECISION_VERIFICATIONS
  AT: 2026-07-26T22:25:00+08:00
  ARTIFACT: decision_support_v001/
  DETAIL: Extended probe-checker selftest on W idx064/122/135 covering all four local-constraint categories (0 mismatches, closing R2 objection 5-2); both neighbor self-admission quotes verified verbatim with locators (ReLoop section 1; Constraint Injection Limitations + Introduction); C-GATE-1 power recomputed (6.5-7.9 percent at D point estimate).

- EVENT: DECISION_V001_DELIVER_IMPLEMENT
  AT: 2026-07-26T22:35:00+08:00
  ARTIFACT: decision_v001.md
  SHA256: 8aa4267b29f781f1435d2c532c975193633603a1c969cefbbe429bbd3c28a51e
  DETAIL: Objection-by-objection disposition of all 17 deduplicated objections (0 unresolved fatal; 2 conditional-fatal resolved via binding errata E1 VeriSimpl disclosure and E15 Claim-2 lambda adjudication). DELIVER_IMPLEMENT with binding errata E1-E17. Machine-improvement note recorded: future packet manifests must include implementation bytes; plan template must not use truncated hashes.

- EVENT: DELIVERY_WRITTEN_RUN_CLOSED
  AT: 2026-07-26T22:40:00+08:00
  ARTIFACT: DELIVERY.md
  SHA256: fa8648aa62dabc472d4f98cb92e778c549d87cf81309e1e1c8d71decf1db82d0
  DETAIL: Root DELIVERY.md written via write_delivery_record bound to decision 8aa4267b (all errata E1-E17 executed in text). Seed: certificate-level enforcement-masking decomposition for solver-backed LLM formalization certification, with reserved untouched C bucket + preregistered gates + power warning handed to receiver. STATUS -> DELIVERED. Total run03 API usage: ~163k tokens (~0.05-0.1 USD). Internal-lane reflow candidate noted for next KB cycle: density-proxy direction failure (fresh-D-validated negative result) eligible for INTERNAL_RUN_EVIDENCE Failure card.
