# v016 Main-Codex Confirmation Evidence Audit

## Authority boundary

This document is the main Codex's scientific audit after the single frozen v016 Confirmation evaluator and independent audit. Mechanical gate booleans do not decide the claim. This audit may authorize only a complete immutable Review Packet; it does not authorize Delivery.

## Execution provenance

| Artifact | Exit / bytes | SHA-256 |
|---|---:|---|
| evaluator execution | exit `0`, 4.649595999999292 s | `8a4a8fee8f70564c5554ceed3f51553ec6124780d63e9d03acf50b58db9fba62` |
| evaluator stdout | 252 bytes | `3df81c1eb19a9272455a0a863612b7c2f3567c2fb82c0b7a45ba71d4707b7f16` |
| evaluator stderr | 0 bytes | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw rows | 12,717,378 bytes | `29802816b4c8766ff651eb527607b1a72a49a1b676605ad1ba8df5f2db2c0df9` |
| summary | 17,033 bytes | `8416581b1ce75e4aadeea67cbb2c7545d69e5887de44ebe76a1f48cbad495917` |
| bounded case samples | 80,692 bytes | `fb09335a89ab39938a55e9f353adcd404a576bdf0fb2a59c909da22e5059cb44` |
| independent execution | exit `0`, 0.4179906999997911 s | `def80f6c5818bc30a6085c307e46f7335f258d5cf860e4e96224d11698cdd2bf` |
| independent stdout | 91 bytes | `3aa705505b044fe3bcc130a73756f011aa209710111a398c32497feda7faf42b` |
| independent stderr | 0 bytes | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| independent report | 7,363 bytes | `fc2767b2d8c1a1448692c633921c7330b6c86d90bd3baf3a0058fef3fb4c2d7c` |

The evaluator capture hash-verified the frozen program, config, manifest, official detector, and all 36 Confirmation files before execution. All three outputs were absent before and present after. Both captures used the exact argv frozen in `confirmation_argv.json` SHA-256 `72d9066fc59a1d8d31bad97b3d42d7533d6f4fba9a2c17dd5e5fd62dcf384987`.

## Integrity findings

- 36/36 input files verified: 12 traces, 24 judges, zero ensembles, 342,075,457 bytes.
- Manifest SHA matched corrected config SHA; fixed dataset revision matched.
- 12,000 rows and 12,000 unique `(model_id, task_id)` keys.
- 10,792 two-judge-unanimous rows; 1,208 disagreements.
- 12 generator models and five domains.
- Join errors: 0.
- Official baseline identity errors: 0.
- Unexpected external labels: none; eight disclosed external rows passed through unchanged.
- Structural invariance violations: 0.
- Independent duplicate keys: 0; mislabeled-supported rows: 0.
- Independent maximum recorded metric error: 0.
- Independent raw-row SHA matched summary; every recorded metric gate matched recomputation.
- Independent `audit_ok=true`; every audit check true.

## Confirmation result

| Measure | Official | RGP | Delta / result |
|---|---:|---:|---:|
| unanimous-row accuracy | 0.9093773165307635 | 0.9273535952557450 | +0.01797627872498147 |
| correct rows / 10,792 | 9,814 | 10,008 | +194 |
| macro-F1 | 0.4930113216392318 | 0.4937678972140701 | +0.0007565755748383252 |

- Model-cluster bootstrap, 20,000 resamples, seed `20260723`: 95% `[0.011547301103986307, 0.024226015729936882]`; minimum `0.005406891495601173`.
- Corrections: 195.
- Regressions: 1.
- Changed rows: 271.
- Positive generator models: 10/12; `glm4-9b` and `mistral-7b` were exactly zero, none were negative.
- Positive domains: 5/5.
- Supported `official output_fabrication -> RGP correct -> unanimous correct` transitions: 195 across all five domains.
- Corrections by domain: cybersecurity 41, finance 16, legal 91, medical 38, real estate 9.
- All ten preregistered Confirmation gates passed.

The macro-F1 delta remains very small. This forbids a broad taxonomy-quality claim. The supported result is specifically reduced deterministic false fabrication labeling on the fixed released data.

## Bounded original-byte audit

The main Codex selected the lexicographically first correction in each observed domain and every regression. For all six samples, the trace SHA, both judge-file SHAs, canonical task SHA, and answer SHA matched the frozen raw-row bindings.

### Corrections

1. `RI-SEC-012`, `claude-haiku-4-5`, cybersecurity. The expected `lookup_mitre_attack(T1078)` was called; the answer reproduced `T1078.004 Cloud Accounts`, detection guidance, mitigations, and tactics from the mock return. Both judges independently labeled it correct. Official labeled fabrication; RGP labeled correct.
2. `OF-FIN-004`, `claude-haiku-4-5`, finance. The answer reported the three META Form 4 sales and transparently derived approximate proceeds from returned share counts and prices. Both judges accepted the harmless `limit=10` versus expected `limit=3` variation and labeled the grounded answer correct.
3. `OF-LEG-036`, `claude-haiku-4-5`, legal. The answer reported the returned ERISA loyalty/prudence duties, plan-document duty, diversification/monitoring, and the returned 2024 regulatory history. Both judges labeled it correct.
4. `OF-MED-042`, `claude-haiku-4-5`, medical. The answer reproduced the returned JUPITER population, rosuvastatin dose, 44% effect, HR 0.56, mortality result, and early stop. Both judges accepted the broader retrieval limit because the target record was correctly reported.
5. `RI-RE-038`, `llama3.1-70b`, real estate. The answer accurately reported `withdrawn`, the April 28 withdrawal, April 29 relisting, and $799K price from the returned status note. Both judges labeled it correct.

These examples support the predicted mechanism: the benchmark's coarse full-return coverage proxy fired even though the exact required evidence was present and the independent judges found the answer grounded.

### Sole regression

`RI-MED-014`, `qwen3.5-9b`, medical is a real RGP failure. The answer contains the required `contraindicated` and `fetal warfarin` values, but adds structured counseling not fully supported by the tool return: a specific weeks 6–12 risk window, near-term intracranial hemorrhage, low-molecular-weight/unfractionated heparin recommendations, contraception, ultrasound, INR-management, and multidisciplinary-management guidance. Both judges labeled `output_fabrication`; official retained that label; RGP changed it to `correct` solely because required grounding was satisfied.

This proves that required-field satisfaction does not exclude additional unsupported claims. RGP must not be represented as a complete fabrication detector. The 195:1 correction/regression balance supports only an aggregate precedence correction under the fixed reference.

## Development-to-Confirmation consistency

Development showed delta `+0.016693418940609953`, bootstrap lower `+0.010464272171620851`, 157 corrections / 1 regression, 9/10 positive models, and 5/5 positive domains. Untouched Confirmation independently showed delta `+0.01797627872498147`, bootstrap lower `+0.011547301103986307`, 195 corrections / 1 regression, 10/12 positive models, and 5/5 positive domains.

The effect size, uncertainty, mechanism transition, and rare-regression pattern are consistent across disjoint generator-model partitions. No Confirmation threshold was changed after exposure.

## Scientific judgment

The narrow claim survives Confirmation:

> On the fixed released ToolFailBench traces, checking the benchmark's unchanged required-answer contract before its coarse fabrication heuristic reduces deterministic false fabrication labels relative to two unanimous independent judges across multiple generator models and domains.

The evidence does not establish human-gold correctness, semantic equivalence, complete fabrication detection, broad macro-taxonomy improvement, leaderboard invalidity, or generalization beyond the fixed dataset, partition, and judge pair.

The two judges share a benchmark rubric and may have correlated errors. Their unanimity is a released reference, not ground truth. The result is a narrow benchmark measurement correction with a real disclosed failure mode.

## Disposition

`AUTHORIZED_TO_FREEZE_COMPLETE_REVIEW_PACKET`

Review remains mandatory. Three fresh direct leaf Reviewers may be started only after the Packet has frozen every listed byte and passed readback integrity. No Reviewer or automated gate may authorize Delivery; the main Codex must make the final evidence decision after rereading the Packet, frozen bytes, and three raw reports.
