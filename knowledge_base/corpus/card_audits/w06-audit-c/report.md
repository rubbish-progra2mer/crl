# W06 Card Source Audit C — Report

- Audit ID: `w06-audit-c`
- Auditor role: fresh independent source auditor (not a CRL Candidate Reviewer, not the main Codex)
- Scope: 12 Cards (P098–P101 × paper/failure/operator) vs. 4 official PDFs, `corpus/evidence.json`, `knowledge.w06_next.sqlite` passages, `corpus/manifest.json`
- Verdict scale per atomic claim: PASS / NARROW (smallest exact correction given) / REJECT (PDF-anchored refutation)

## 0. Mechanical verification layer (applies to all 12 cards)

- All 13 referenced evidence records exist in `evidence.json`: 13/13 found.
- For each evidence record, `source_content` == `passages.text[quote_start:quote_end]` in `knowledge.w06_next.sqlite`: 13/13 exact match.
- `passages.text_sha256` self-consistent with recomputed sha256(text) and equal to evidence `passage_text_sha256`: 13/13.
- PDF bytes sha256 vs. every card's `source_refs` and every evidence `fulltext_sha256`:
  - P098 `f73aaa44…43ab3` MATCH; P099 `4865494c…560d` MATCH; P100 `4db89bfa…164c` MATCH; P101 `50aa8da6…5d1a` MATCH.
- `manifest.json` P098–P101 records present; pdf_path/sha256 consistent with cards and files.
- Card META `evidence_ids` vs. inline `[[evidence:...]]` tokens: consistent for all 12 cards (no dangling or unlisted citations).

Mechanical result: 13/13 evidence–passage matches, 4/4 PDF hash matches, 12/12 META consistency. No asset was modified.

## 1. paper-p098 (`paper/paper-p098.md`) — PASS

1. [AUTHOR_FACT] SFT filtering and RL reward both stop at objective equivalence; bidirectionally blind to non-binding constraint errors [[ev-p098-nonbinding-blindness]] — PASS. Quote (PDF p.2): "objective equivalence is structurally blind to the constraint set… whenever the affected constraint is non-binding"; two modes named; "Both can pass executability and differential-testing filters, enter SFT data, and receive positive RL rewards."
2. [AUTHOR_FACT] INJ = constant objective + labeled-probe injection + solver feasibility verdict vs. label; same verifier as rejection-sampling filter and GRPO reward with 0.2/0.5/0.3 weights [[ev-p098-constraint-injection]] — PASS. INJ mechanics in quote; weights verified in PDF §5.1 "reward 0.2 rbuild + 0.5 rdiff + 0.3 rinj".
3. Ablation numbers SFT -2.86 / GRPO -4.00 with larger no-injection data — PASS. Table 3: 88.43−85.57=+2.86, 93.00−89.00=+4.00; no-injection arm has 7347 vs 6797 SFT samples and 855 vs 716 frontier prompts (App. E). Note: the −2.86/−4.00 values sit in Table 3, outside the cited quote span; the quote anchors the 550/7347 leak.
4. 550/7347 teacher samples pass DIFF but fail INJ — PASS (App. E quote, exact).
5. [AUTHOR_FACT] Pass@1 compresses constraint-level feedback; decoupled metrics "remain an open problem" [[ev-p098-open-problem]] — PASS (Limitations, exact quote).
6. [CODEX_SYNTHESIS] No capability conclusion on frontier wins; Gemini both teacher and strongest baseline; combined AVG trails 95.00 vs 93.00 — PASS. PDF: teachers = Gemini-3.1-Pro Preview + Claude Opus 4.6 (App. C); Table 2: Gemini AVG 95.00, VRPCoder-GRPO 93.00. Correctly refuses the invocation-named home-field/teacher-distillation confound.
7. εobj numeric value unreported — PASS. εobj appears only symbolically (Def. of DIFF, Table 1 rules, reward). Note: the separate evaluation Pass@1 tolerance 10^-3 is reported (§5.2/App. F) but is never identified with εobj.
8. Single training run, no variance — PASS (no multi-seed/σ reported anywhere for training).
9. Contract-mismatch samples discarded as a class, scale unreported — PASS (App. D: unmatched variables/indices "fails rejection sampling"; no count given).
10. TSPTW generalization gap -8.40 — PASS (§5.3: trails B4 by 8.40 points; 50 TSPTW instances absent from training).
11. Lineage: ORLM/OptMATH (SFT), SIRL/OR-R1 (RL) stop at execution/objective equivalence — PASS (§2.1: "acceptance signals mainly rely on executability or objective equivalence"; §2.2: "operate at the solution or answer level").

Atoms: 11 PASS.

## 2. failure-objective-equivalence-passes-nonbinding-errors — PASS

1. Two failure modes pass executability + differential testing, enter SFT, get positive RL reward [[ev-p098-nonbinding-blindness]] — PASS (verbatim-equivalent).
2. 550/7347 (≈7.5%) pass DIFF but fail INJ [[ev-p098-diff-leak-550]] — PASS (550/7347 = 7.49%).
3. Teacher distribution: Gemini-3.1-Pro + Claude Opus 4.6 — PASS (App. C; PDF says "Gemini-3.1-Pro Preview").
4. DIFF/answer-agreement as sole acceptance signal cannot constrain unactivated constraints — PASS (faithful mechanism restatement).
5. [AUTHOR_FACT] Pass@1 same-disease self-admission, open problem [[ev-p098-open-problem]] — PASS.
6. 550/7347 single-run statistic, no variance — PASS. Note: "单教师分布" is best read as "its (single) self-built teacher-generation distribution"; the same card names both teacher LLMs three lines earlier, so no factual error.
7. Fig.1 case is a constructed illustration, not a natural training-log sample — PASS (PDF: "Figure 1 illustrates this failure on a routing instance…").
8. [CODEX_HYPOTHESIS] soft-constraint/objective-penalty mechanisms left to DIFF, author-admitted — PASS (App. B.4: penalty-only mechanisms get no violating probe; "handled by DIFF or objective-equivalence signals").

Atoms: 8 PASS.

## 3. operator-labeled-probe-injection-dual-verifier — PASS

1. [AUTHOR_FACT] INJ operator implementation [[ev-p098-constraint-injection]] — PASS (exact quote; App. D restates identically).
2. Dual probe pairing: s+ must be accepted, s− must be rejected; same implementation for filter and reward — PASS (App. D "Verdict handling"; §5.1 GRPO reward reuse).
3. Inputs/outputs/timing: gold script as probe-label oracle; 0/1 signal; SFT filter + GRPO reward; evaluation does not use INJ — PASS (§4: "Cgold serves as the oracle throughout the pipeline"; §5.2: Pass@1 is the evaluation metric; constraint-level effect only isolated via ablation).
4. [AUTHOR_FACT] Mechanism: non-binding errors invisible in objective, visible in feasibility [[ev-p098-nonbinding-blindness]] — PASS.
5. [AUTHOR_FACT] Ablation isolation -2.86/-4.00; 550/7347 intercepted by the filter [[ev-p098-diff-leak-550]] — PASS. Quote covers the leak and its rejection by the main pipeline; −2.86/−4.00 verified in Table 3 (outside quote span; same note as paper card).
6. Preconditions: output-protocol contract (x variables, arc-first indices, node_id_map back-translation), contract-mismatch discard with unreported scale, vehicle-binding to prevent route-splitting masking, manual attacker catalog, instance sizes customers 4–12, VRP carrier — PASS. All verified: App. D (variable parsing; Eq. 8 vehicle binding "cannot be distributed across interchangeable vehicles"); Limitations ("manual design is still required"); Table 5 (n ranges 4–12 across all 15 profiles).

Atoms: 6 PASS.

## 4. paper-p099 (`paper/paper-p099.md`) — PASS

1. [AUTHOR_FACT] exec_spec extension + symbolic-first/runtime-fallback + {pre,post}×{completeness,soundness} buckets (official tests + human hacks) [[ev-p099-two-stage-check]] — PASS (§2.2 quote; extension and buckets verified §2.2/§3.1).
2. Judge contrast 49/191 (25.7%) false acceptance — PASS (§4.3 exact; Table 4 confusion matrix).
3. Soundness ablation 77→58 / 82→78 / 59→51 — PASS (§4.3 exact).
4. gemini-3.1pro 0.778 strongest; open-source 0.215–0.255 — PASS (§4.2).
5. pass@3=0.756 but pass3 only 34.8% — PASS (App. F.4). Note: these are gpt5.3-codex three-run numbers; the card does not name the model.
6. Over-specification an independent failure mode — PASS (App. F: "over-specification is itself a failure mode distinct from under-specification").
7. "Code easy, spec hard" comparison task-inequivalence, author wording self-limited — PASS (App. F.6 restricts to unique-output subset; 153/187 = 81.8%; hedged phrasing "often are not").
8. Budget-type evaluation confound ($2.5 + 75 min + latency/cache); model ranking not a capability conclusion — PASS (§4.1 + App. F: API latency and prompt-cache pricing named by authors). Correctly bounds the invocation-named ranking confound.
9. 400-step cap stated inconsistently in two places — PASS (Table 1 header: "Open-source models; max 400 steps"; App. F: "For SWE-AGENT, we additionally impose a limit of 400 API calls per problem", while §4.1 runs all six models inside SWE-AGENT — the scopes conflict).
10. Judge only tested as no-tool self-evaluation — PASS (App. F.7: same model, one-shot prompt, no execution tools). Correctly bounds the invocation-named "26% beyond self-judge no-tool config" risk.
11. Internal inconsistencies: mean 21 vs 20; completeness bucket Max:100 unexplained — PASS. Text (§3.1): "problems have 21 pre-sound… test cases" on average; Figure 5 image label reads "Mean: 20" for pre_sound. Figure 5 shows Max: 100 for the completeness buckets (soundness buckets Max: 200) with no explanation.
12. Four-bucket labels are platform-artifact approximations; single-file competitive-programming domain — PASS (Figure 4 routing by Codeforces adjudication; solve.rs skeleton tasks).

Atoms: 12 PASS.

## 5. failure-llm-judge-misses-executable-spec-errors — PASS

1. [AUTHOR_FACT] Judge on own specs: 49 of 191 (25.7%) marked correct [[ev-p099-judge-miss]] — PASS.
2. [AUTHOR_FACT] Completeness-only overestimates; 77→58/82→78/59→51 [[ev-p099-soundness-necessity]] — PASS.
3. Conditions: 581 tasks; judge static one-shot self-eval without execution tools; cross-model/tooled/voting judges untested (explicitly not excluded) — PASS (App. F.7; the hedge matches the paper's actual coverage).
4. Failed intervention framing (LLM judgment replacing executable tests; sparse completeness-only suites) — PASS.
5. "More testcases" not the axis — F.8 shows near-saturation at small budgets; the overestimation axis is missing direction (soundness); denominator of 26% is compile-clean incorrect specs (54 non-compiling excluded) — PASS (App. F.8 "curves flatten"; Table 4 caption: "The 54 benchmark-incorrect specifications that did not compile were excluded").
6. [CODEX_HYPOTHESIS] repair boundary (executable compilation + human adversarial hacks occupied) — PASS.

Atoms: 6 PASS.

## 6. operator-four-bucket-executable-spec-testing — PASS

1. [AUTHOR_FACT] Per-testcase symbolic check (assert(spec) for completeness, negated assertion for soundness), fallback to runtime exec_spec on failure or timeout, all four buckets must pass [[ev-p099-two-stage-check]] — PASS (§2.2: "If verification fails or times out, the evaluator uses the runtime check"; assertion polarity verified verbatim).
2. Inputs/outputs/timing: hacks routed by platform adjudication; byte-level round-trip P(R(t))==t acceptance; six resolution categories mapped by bucket polarity; visible samples for iteration, hidden suite final — PASS (§3.1 Figure 4; Figure 3 caption "lossless only if Treproduced == t byte-for-byte"; Figure 6 six categories).
3. [CODEX_HYPOTHESIS] mechanism incl. exec_spec_unverified cutting the correspondence proof to remove evaluator false failures — PASS (§2.2: "unnecessary failure mode… we therefore introduce exec_spec_unverified").
4. [AUTHOR_FACT] Signature: soundness bucket drop (77→58 etc.); 26% judge miss gap [[ev-p099-soundness-necessity]] [[ev-p099-judge-miss]] — PASS.
5. Preconditions/risks: finite-testcase upper-bound nature (all-pass ≠ faithful); budget/latency/cache confound, no ranking conclusion (author-admitted) — PASS.

Atoms: 5 PASS.

## 7. paper-p100 (`paper/paper-p100.md`) — PASS

1. [AUTHOR_FACT] Evaluation-layer BoR + control-layer RL stopping policy with metric-endogenous depth pressure [[ev-p100-bor-self-pruning]] — PASS (§3.3 exact quote).
2. [AUTHOR_FACT] Difficulty-bucket separation (hard bucket: all other methods 0%) and aggregate masking; weak-scorer negative result K=80.7 [[ev-p100-fixed-depth-buckets]] [[ev-p100-weak-scorer-collapse]] — PASS (§4.1: FK=5/F1/FK=1 all 0% on gold rank 6–20, BoR 16.7±4.3%, FK=5 aggregate 64.7 vs 61.9; §4.2 K=80.7).
3. BFCL 90.3%@K=7.4 ≈ FK=50 — PASS (90.3±2.4% at K=7.4±2.5 vs FK=50 90.8%).
4. Downstream over-presentation harmful direction robust; point values carry conditioning bias — PASS (Table 1 Choice Acc conditioned on presented-gold; effect replicated with embedding scorer, "consistent across scorer types"). Correctly bounds the invocation-named 93.1-vs-87.1 conditional-selection risk.
5. BoR attribution to [30] (this paper RL-izes it) — PASS (§3.1: "BoR was introduced as a chance-corrected selectivity metric in Repantis et al. [30]"). Correctly handles the invocation-named attribution risk.
6. step_cost sensitivity ≈3× — PASS (K=7.4 at step_cost 0.005 → K=2.2 at 0.01; ratio 3.4).
7. F1 ablation one condition uses simplified variant — PASS (footnote 1: BFCL+BM25 row uses constant terminal reward 1.0).
8. MetaTool single seed — PASS (§5.3: "MetaTool results are reported from single-seed runs, although they cover six conditions").
9. Constructed candidate sets do not represent original benchmark retrieval — PASS (§5.2: "None of the benchmarks we use were designed to evaluate search depth").
10. found@1 inconsistent in two places (flagged OPEN) — PASS. BFCL BM25 found@1 is 60.0% in §4.1 but 65% in §4.3 ("higher found@1 on this split (77% vs 65%)"; FK=1 Presented%=65.0 in Table 1), both on 120-query test splits; no reconciliation in the paper. Flagging as OPEN rather than asserting an error is the correct strength.
11. Single downstream LLM; execution correctness out of scope; Rq=1 throughout — PASS (§5.3; all tool experiments single-tool).
12. DynamicRAG closest prior (author-admitted), Less-is-More/ToolRerank filter line — PASS (§2.1: "DynamicRAG [34] is closely related"; §2.2).

Atoms: 12 PASS.

## 8. failure-fixed-shortlist-depth-masks-hard-query-zero — PASS

1. [AUTHOR_FACT] ToolBench buckets: gold rank 6–20 → FK=5/FK=1/F1 all 0% (BoR 16.7±4.3%); FK=5 aggregate higher 64.7 vs 61.9; uniform depth saturates easy/medium, hard and above zeroed; aggregate masks distributional failure [[ev-p100-fixed-depth-buckets]] — PASS (all six numbers exact; "catches all easy and medium queries… finds nothing on hard and very hard"; very hard: BoR 0.2%, others 0%).
2. Conditions: truncation step (post-scorer, pre-prompt); Rq=1 constructed candidate sets; preprint (Meta Platforms); F1-type fixed penalty trains K≈1.5 flat across buckets — PASS (title page affiliation; §4.1/Figure 1).
3. Failed intervention framing — PASS.
4. [AUTHOR_FACT] Boundary: BM25 found@1=33% → K=80.7 (1.04 bits), nothing to stop on with weak scorer [[ev-p100-weak-scorer-collapse]] — PASS (§4.2: "only 1.04 bits of selectivity"; "no reliable signal for where to stop"; paper itself: "nearly showing all tools").
5. Downstream 93.1 vs 87.1 point values carry conditional-selection bias (presented sets differ); direction survives (FK=5 medium: 100% presented, only 60.9% chosen); point values not to be cited — PASS. This is exactly the bound the invocation requires.
6. [CODEX_HYPOTHESIS] Residual open faces (author-admitted): execution-layer correctness and Rq>1 — PASS (§5.3: argument correctness "outside the scope"; all experiments single-tool).

Atoms: 6 PASS.

## 9. operator-chance-corrected-depth-reward — PASS

1. [AUTHOR_FACT] BoR reward decreases as list grows; ~7 bits at K=3/500, ~2 bits at K=100; not an engineered penalty [[ev-p100-bor-self-pruning]] — PASS (exact quote; arithmetic checks: −log2(3/500)=7.38, −log2(100/500)=2.32).
2. Stopping policy: per-item scan, binary STOP/CONTINUE MDP, reward −log2(Prand(kstop)) on hit, score-shape state — PASS (§3.2). Note: the paper's state also includes "the BoR ceiling at the current depth", which is a deterministic function of the listed depth/N features; the card's "只看分数形状特征" omission is not information-bearing.
3. Inputs/outputs/timing incl. oracle relevance labels in training, none at inference — PASS (§3.2: "trained with oracle Rq and assumes Rq=1 at inference").
4. [CODEX_HYPOTHESIS] mechanism — PASS (consistent with §3.1/3.3).
5. [AUTHOR_FACT] Depth rises monotonically with difficulty 2.5→6.9; F1 flat K≈1.5; hard-bucket coverage recovered [[ev-p100-fixed-depth-buckets]] — PASS (2.5→4.8→5.7→6.9 monotone; Figure 1).
6. Attribution note: BoR from [30] (author overlap, ICLR Blogposts 2026); contribution = rewardization + buckets + downstream; risks: step_cost 0.005→0.01 gives K 7.4→2.2, bits not comparable across corpora (Prand denominator), MetaTool single seed — PASS ([30] = Repantis et al., authors overlap with the paper; §4.1 N-sweep shows same task, larger N → more bits, grounding the incomparability note).
7. Lineage: cheminformatics chance-correction (BEDROC/enrichment factor) → BoR [30] → this paper — PASS (§2.3 verbatim).

Atoms: 7 PASS.

## 10. paper-p101 (`paper/paper-p101.md`) — REVISE (one NARROW)

1. Setting: semantic equivalence undecidable in general (Chu 2017); string match false-negative, single-db execution false-positive; formal methods cannot express sort/float — PASS (§1/§2 verbatim).
2. [AUTHOR_FACT] Scoring switched to per-database denotation comparison on distilled suites; entailment chain exact match ⇒ semantic ⇒ test suite ⇒ single denotation [[ev-p101-neighbor-distillation]] — PASS. Note: the chain is verified at §2 ("exact match ⇒ semantic accuracy ⇒ test suite accuracy ⇒ single denotation accuracy"), outside the cited quote span; the quote anchors the distillation objective.
3. [AUTHOR_FACT] ESM FN 2.6% mean / 8.1% worst, growing with complexity; leaderboard actually distorted (61% submission undervalued by 8%) [[ev-p101-esm-fn-rate]] [[ev-p101-metric-distortion]] — PASS (Table 1 all-data FN mean 2.6, max 8.1; §1 the 61%/8%/five-submissions claim verbatim; §6.3 five-dots evidence).
4. 1000 random dbs distinguish >99% of neighbors; single high-coverage random db reproduces full-suite outcomes on 21 submissions — PASS (§6.1; §6.4: "produces the exact same outcomes as running the full test suite on the 21 submissions").
5. Human audit one-sided (only disagreement-side false-positive direction verified) — PASS (§6.1: 100 samples all from ESM-incorrect/suite-correct; purpose "make sure that our method does not create any false positive").
6. "套件假阴有 1/200K 实证反例" — NARROW. The 1-in-~200K WikiSQL counterexample (App. A.3) is a query the suite judged CORRECT that is semantically wrong (over-generated "WHERE col2 > 10" not covered) — i.e., a suite false ACCEPTANCE, which both the paper's convention (metric-says-correct/actually-wrong = false positive, cf. Table 2 usage) and this card's own first clause ("假阳") call a false positive. The paper additionally states the suite "provably never creates false negatives in a strict programming language sense" (§8). Smallest exact correction: replace "套件假阴有 1/200K 实证反例" with "套件误接受（假阳）方向在 WikiSQL 约 200K 预测中有 1 例实证反例".
7. FP/FN are adapted-metric relative quantities; constant-substitution enumeration loosens the judgment — PASS (§5.3 (1): adapted suite "enumerates all possible ways to replace the constants… correct if one of the replacements passes"; §7 row-6 LIKE example: "might also unexpectedly loosen the semantic accuracy metric"). Correctly bounds the invocation-named adapted-metric risk.
8. Dataset-level reliability boundary Advising 63.2% / ATIS 76.3%; WikiSQL not recommended by the authors — PASS (Table 4; App. A.3: "we do NOT recommend researchers to use test suite accuracy for WikiSQL").
9. Abstract 2.5% vs body 2.6% inconsistency (cite 2.6%) — PASS (abstract "2.5%"; Table 1/§6.2 "2.6%"). Note: the Introduction also repeats 2.5%, so the discrepancy is abstract+intro vs Table 1/§6.2; the card's statement remains true.

Atoms: 8 PASS, 1 NARROW.

## 11. failure-single-execution-denotation-false-positive — REVISE (one NARROW)

1. [AUTHOR_FACT] Bidirectional metric distortion, actually distorted leaderboard: 61%-semantic-accuracy submission undervalued 8%, five weaker submissions favored; worse on complex queries [[ev-p101-metric-distortion]] — PASS.
2. [AUTHOR_FACT] ESM FN 2.6%/8.1% (hard fraction 4%/12.1%); single-db false positive is the Fig.1 textbook case (missing-WHERE query with coincidentally equal denotation) [[ev-p101-esm-fn-rate]] — PASS (§6.2 exact incl. "4% on average and 12.1%"; Figure 1 verified: Prediction 1 "(missing WHERE)" accepted on database 1).
3. Conditions: Spider 21 leaderboard submissions + 11 datasets; EMNLP 2020 limited admission; abstract 2.5% vs Table 1/body 2.6%, cite 2.6% — PASS (footnote 1 lists eleven datasets; venue verified via manifest).
4. Failed intervention framing (single-db execution or string/clause match as semantic correctness) — PASS.
5. Audit one-sidedness: 100 manual checks all drawn from the ESM–suite disagreement side, verifying only the no-suite-false-positive direction — PASS (§6.1 exact).
6. "套件自身假阴方向无对称抽验且有 1/200K 实证反例（WikiSQL 多余 WHERE 未被覆盖）" — NARROW. Direction mislabel: the WikiSQL 1/200K case (App. A.3) is the suite wrongly ACCEPTING a semantically wrong query — the same accept-side (false-positive) direction the 100-sample audit covered, found under exhaustive disagreement screening on WikiSQL, not an instance of an unaudited "假阴" direction. What genuinely lacks symmetric audit is the suite-rejection side (broader-sense false negatives via unnatural databases, the paper's "A wins" discussion in §8; strict-sense FN is provably impossible per §8). Smallest exact correction: replace the clause with "套件拒绝侧（广义假阴，'非自然库'类）无对称抽验；套件误接受（假阳）侧在 WikiSQL 约 200K 预测中有 1 例实证反例（多余 WHERE 未被覆盖）".
7. FP/FN numbers are "adapted ESM vs suite" relative quantities (constant-substitution enumeration loosened the judgment) — PASS (§5.3 (1)).
8. Multi-WHERE stacking and exact-cardinality predicates are random-fuzzing blind spots (Advising reliable fraction only 63.2%) — PASS (App. A.2 names exactly these two categories: ≤24 stacked WHEREs in ATIS; "WHERE COUNT(*) > 5000" requiring exact table size; Table 4 Advising 63.2%).
9. [CODEX_HYPOTHESIS] repair boundary (three premises; solver carrier partial) — PASS as hypothesis; premises consistent with §8's two stated framework requirements.

Atoms: 8 PASS, 1 NARROW.

## 12. operator-neighbor-distilled-test-suites — PASS

1. [AUTHOR_FACT] Neighbor generation by single-point modification (constants/strings/comparison operators/column names, span drop); distinguishing all neighbors forces execution to exercise every modified part — computable coverage proxy; greedy retention of databases that distinguish still-undistinguished neighbors [[ev-p101-neighbor-distillation]] — PASS (§3.1 modification list verbatim; quote anchors the coverage rationale; greedy procedure verified §4.2, outside quote span).
2. Inputs/outputs/timing: random instance generator with gold constants and close variants mixed in; Spider 1000 random dbs distilled, >99% neighbors distinguished; one-off offline; oracle produced before obtaining model predictions — PASS (§4.1 "constant values used in g… and their close variants"; §6.1; §5.2: "The first author obtained these model-predicted queries from the second author after producing the test suites").
3. [CODEX_HYPOTHESIS] mechanism — PASS (matches quote's stated rationale).
4. [AUTHOR_FACT] Suite exposes systematic scoring error vs single-db/string match (ESM FN 2.6%/8.1%, grows with complexity) [[ev-p101-esm-fn-rate]] — PASS.
5. Preconditions/risks: three premises; known blind spots floating-point-precision neighbors, multi-WHERE stacking, exact-cardinality predicates; suite is tight upper bound, not equivalence decision; Goodhart risk author-admitted — PASS (§6.1 float precision admission; App. A.2 two categories; abstract/§2 "tight upper bound"; §8: "due to Goodhardt's law, since researchers will optimize over our metric").
6. Lineage fuzzing/coverage tradition (Miller 1963) — PASS (quote cites Miller and Maloney, 1963).

Atoms: 6 PASS.

## Summary table

| card_id | verdict |
|---|---|
| paper-p098 | PASS |
| failure-objective-equivalence-passes-nonbinding-errors | PASS |
| operator-labeled-probe-injection-dual-verifier | PASS |
| paper-p099 | PASS |
| failure-llm-judge-misses-executable-spec-errors | PASS |
| operator-four-bucket-executable-spec-testing | PASS |
| paper-p100 | PASS |
| failure-fixed-shortlist-depth-masks-hard-query-zero | PASS |
| operator-chance-corrected-depth-reward | PASS |
| paper-p101 | REVISE (1 NARROW: relabel the 1/200K WikiSQL counterexample as suite false-acceptance/假阳, not 套件假阴) |
| failure-single-execution-denotation-false-positive | REVISE (1 NARROW: same direction mislabel; the genuinely unaudited side is the suite-rejection/broad-FN side) |
| operator-neighbor-distilled-test-suites | PASS |

Atomic totals: 95 PASS, 2 NARROW, 0 REJECT (97 atoms).

Invocation-named overstatement risks, disposition: P098 frontier-win confound — properly refused by the cards (PASS); P099 ranking/budget confound and judge-config bound — properly bounded (PASS); P100 93.1-vs-87.1 conditioning and BoR [30] attribution — properly bounded/attributed (PASS); P101 one-sided-audit boundary and adapted-metric loosening — present in the cards, but the counterexample's error direction is mislabeled (the two NARROWs above).

## Provenance

- What I read (complete list):
  - `knowledge_base/corpus/card_audits/w06-audit-c/invocation.md`
  - The twelve named cards under `knowledge_base/cards/` (paper/paper-p098.md, failure/failure-objective-equivalence-passes-nonbinding-errors.md, operator/operator-labeled-probe-injection-dual-verifier.md, paper/paper-p099.md, failure/failure-llm-judge-misses-executable-spec-errors.md, operator/operator-four-bucket-executable-spec-testing.md, paper/paper-p100.md, failure/failure-fixed-shortlist-depth-masks-hard-query-zero.md, operator/operator-chance-corrected-depth-reward.md, paper/paper-p101.md, failure/failure-single-execution-denotation-false-positive.md, operator/operator-neighbor-distilled-test-suites.md)
  - `knowledge_base/corpus/evidence.json` (parsed programmatically; used only the 13 P098–P101 records)
  - `knowledge_base/corpus/manifest.json` (parsed programmatically; used only the P098–P101 paper records)
  - `knowledge_base/knowledge.w06_next.sqlite` (read-only SELECTs on `passages` for the 8 referenced passage_ids; schema listing)
  - The four PDFs `knowledge_base/papers/P098_constraint_injection.pdf`, `P099_verus_specgym.pdf`, `P100_tool_shortlist_size.pdf`, `P101_distilled_test_suites.pdf` — full text extracted independently with pymupdf; P099 Figure 5 additionally rendered to an image to read in-figure labels (Mean/Max annotations).
- What I did not read: no reconciliation.md, no read_1.md, no read-2 reports (no genuine source ambiguity remained that required one), no earlier Card audits or dispositions (including the other W06 audits), no calibration/blind queries, judgments, results, reports, or revealed regressions, no Candidate/Commissioning/Reviewer assets, no other cards. The session scratchpad contained leftover files from other sessions (including audit_*.md and p09x text extracts); none were opened — all PDF text used was re-extracted fresh into auditc_-prefixed files.
- Modifications: none. No card, evidence, manifest, PDF, or database was modified. All sqlite access was read-only SELECT/PRAGMA.
- Start context: invocation start time 2026-07-27T02:35:00+08:00; audit executed in a single fresh session. End context: report written and hashed immediately after the last PDF verification, 2026-07-27 (local).
- Model/version: Claude (Fable 5), model id claude-fable-5, running as a Claude Agent SDK subagent.
- Procedural blinding: audit performed from PDFs + evidence.json + manifest.json + sqlite passages only; forbidden-read lists honored as above; verdicts formed without access to any other audit output.
- Thread/task ID: not exposed by the harness; audit identity = w06-audit-c.
- Tool limits: PDF figure annotations not present in the extracted text layer (P099 Figure 5; P100 Figures 1–2) were verified by rendering the page region to an image where load-bearing (P099 Figure 5); P100 figure-adjacent claims were verified against the surrounding body text. No web access used.
- Report SHA-256: recorded in the audit ledger alongside this file (computed over these exact bytes after writing; embedding it inside the file would self-invalidate the hash).
- Mechanical result: 13/13 evidence-passage exact matches; 13/13 passage sha256 matches; 4/4 PDF sha256 matches; 12/12 card META/citation consistency; 95 PASS / 2 NARROW / 0 REJECT atomic findings; 10 cards PASS, 2 cards REVISE.
