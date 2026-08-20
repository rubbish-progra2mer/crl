# W06 Card Source Audit B — Report (`w06-audit-b`)

- Audit ID: `w06-audit-b`
- Role: fresh independent source auditor (not a CRL Candidate Reviewer, not the main Codex)
- Scope: 12 Cards (P094–P097 × paper/failure/operator) vs the four official PDFs, `corpus/evidence.json`, and `knowledge.w06_next.sqlite` passages
- Start: 2026-07-27T02:35:00+08:00 (per invocation) — End: 2026-07-27T02:58+08:00
- No card, evidence, manifest, PDF, or database file was modified.

Verdict key (atomic claims): PASS = verified against source; NARROW = needs the stated smallest correction; REJECT = refuted against the PDF; N/A = internal knowledge-base cross-reference not checkable within this audit's allowed reads (excluded from counts).

## 0. Mechanical verification (all 12 cards)

1. CRL_CARD_META parsed cleanly on all 12 cards; `card_id`/`card_kind`/`paper_id`/`evidence_ids`/`source_refs` all well-formed.
2. All 9 referenced evidence objects exist in `evidence.json` (`ev-p094-sf-length-collapse`, `ev-p094-sf-guardrails`, `ev-p094-incremental-protocol`, `ev-p095-prior-override-drift`, `ev-p095-matched-comparison`, `ev-p096-shared-misinterpretation`, `ev-p096-simplification-inversion`, `ev-p097-feasibility-gap`, `ev-p097-behavioral-perturbation`).
3. For every evidence object: `source_content` == `passages.text[quote_start:quote_end]` byte-exact in `knowledge.w06_next.sqlite`; `passages.text_sha256` == sha256(text) recomputed; evidence `passage_text_sha256` == DB value. 9/9 exact.
4. PDF sha256 recomputed from bytes:
   - P094 `022d3771…9508`, P095 `60f55421…b4a1`, P096 `81b34a70…95b3`, P097 `8563653b…4c66` — each matches all card `source_refs`, the manifest record, and every evidence `fulltext_sha256`. 4/4.
5. Full text of all four PDFs re-extracted independently with pymupdf; all checks below are against this fresh extraction.

## 1. P094 — MemoryAgentBench

### 1.1 `paper-p094`

| # | Atomic claim | Verdict | Anchor / correction |
|---|---|---|---|
| 1 | FactConsolidation = update-annotated, multi-length, SH/MH selective-forgetting benchmark | PASS | §3.1 (MQUAKE counterfactual edit pairs, p.6); FC lengths 6K/32K (Table 5) and 32K/64K/262K (main) |
| 2 | Four-competency framework AR/TTL/LRU/SF | PASS | Abstract, §5 Conclusion |
| 3 | ICLR 2026 published | PASS | Page headers "Published as a conference paper at ICLR 2026" |
| 5 | Problem framing (one-shot long-context vs incremental absorption gap) | PASS | §1 |
| 6 | Two-phase incremental protocol (chunk-wise absorb + incremental update + post-hoc questions) `[[ev-p094-incremental-protocol]]` | PASS | Quote supports sentence fully (§3.3, p.7) |
| 7 | SF collapses with length under explicit serial-number guardrails, o4-mini 80.0→14.0 | PASS | Table 5 (FactCon-MH, 6K=80.0, 32K=14.0) + §3.3 guardrail text; both quotes support |
| 8 | "护栏与覆写提示消融排除指令缺失解释" — the overwrite-prompt-ablation half | NARROW | Claim is true (Appendix K.2, Table 19: Policy A FC-MH 4.0, Policy B 4.0; authors conclude SF is not solvable by prompt engineering alone) but neither bound evidence quote covers the ablation. Smallest correction: bind an Appendix K.2/Table 19 passage to this clause or retag the clause CODEX_SYNTHESIS with locator "App. K.2/Table 19". |
| 9 | Commercial memory agents Overall below bare 4o-mini reference | PASS | Table 3: Mem0 21.1, Cognee 20.6, Zep 24.0, MIRIX 26.2 vs GPT-4o-mini 42.2/42.3 |
| 10 | FC-MH ≤28% across all systems | PASS | §4.2 "(with achieving at most 28% accuracy)"; table max = GPT-5-mini 28.0 |
| 11 | Backbone confound (LC agents use own models; RAG/commercial fixed 4o-mini) | PASS | Table 3 caption |
| 12 | Chunk confound (commercial 4096 uniform vs RAG 512 on AR-synthetic/SF) | PASS | §4.1 (p.8), Table 15 |
| 13 | Fair comparison = Appendix J strict compute-matched three budget tiers | PASS | App. J, Table 18 (Low/Medium/High) |
| 14 | GPT-4o doubles as judge and evaluated system (mild self-affinity risk) | PASS | GPT-4o judge on LME(S*)/∞Bench-Sum (App. B/D, App. L.1); GPT-4o also evaluated (Table 3) |
| 15 | FC serial guardrail conflicts with P091 marker-free regime | N/A | Cross-corpus claim; P091 outside allowed reads |
| 16 | Lineage section | N/A→consistent | Internal positioning |
| 17 | Evidence ledger "三条绑定 exact Passage" | PASS | Mechanically verified (§0) |
| 18 | Retrieval vocabulary | PASS | All terms grounded |

Card verdict: REVISE (binding-only; content fully source-true). Smallest correction as in row 8.

### 1.2 `failure-selective-forgetting-collapses-with-context-length`

| # | Atomic claim | Verdict | Anchor / correction |
|---|---|---|---|
| 1 | FactCon-MH o4-mini 80.0@6K → 14.0@32K; task solvable, failure appears with history length | PASS | Table 5 + §4.3.4 prose ("solvable under short-context settings"); quote supports |
| 2 | Guardrail wording: serial-indexed facts, "newer facts have larger serial numbers", mandated newest-fact conflict resolution | PASS | §3.3 (p.7); quote verbatim |
| 3 | ICLR 2026; two-phase protocol | PASS | See 1.1 rows 3, 6 |
| 4 | SF is a synthetic conflict stream, author-acknowledged and defended | PASS | App. G item 3 ("controlled synthetic setting", deliberate) |
| 5 | Prompt-engineering ablations (aggressive/conservative overwrite) do not rescue (Table 19) | PASS | App. K.2: FC-MH 4.0 both policies; authors' own conclusion |
| 6 | Main-table cross-row confounds do not affect this failure: 6K/32K contrast is same-model same-task | PASS | Table 5 is o4-mini/GPT-4o vs themselves across lengths |
| 7 | "TTL 零样本地板 <4% 排除预训练先验解释" | NARROW | The <4% zero-shot floor is measured only on the TTL tasks (MCC/Recom., App. H.2, Table 16) and validates the TTL premise; it does not speak to FactConsolidation priors. Smallest correction: replace with "FactCon 由 MQUAKE 反事实编辑对构造（§3.1），先验答案即为被更新掉的旧值，先验解释不成立" (or explicitly scope the <4% claim to TTL and drop it from this failure's alternative-explanation list). |
| 8 | Guardrailed regime not directly comparable to marker-free (P091); collapse-with-guardrails is lower-bound evidence | PASS (P091 part N/A) | Guardrails confirmed in-protocol; lower-bound reading is sound synthesis |
| 10 | Repair-boundary hypothesis: chunk=512 + strong backbone + deeper retrieval joint cell untested; two placed alternative routes | PASS | Verified by absence: backbone ablation (§4.3.3) and chunk ablation (§4.3.1/App. E.2) are separate sweeps, no joint cell; P095 assembly route confirmed in P095 |
| 11 | Evidence ledger | PASS | Mechanical |
| 12 | Retrieval vocabulary | PASS | Grounded |

Card verdict: REVISE (one scope correction, row 7).

### 1.3 `operator-incremental-injection-benchmark-reconstruction`

| # | Atomic claim | Verdict | Anchor |
|---|---|---|---|
| 1 | Intervention target framing | PASS | §1/§3 |
| 2 | After-state: chunk-by-chunk absorb/update, questions after all chunks; memorization instruction per chunk; per-dataset task instructions `[[ev-p094-incremental-protocol]]` | PASS | Quote covers first half; the instruction clauses are inside the same bound passage (P094:p0007:s0002, §3.3 "Prompt Formulation and Interaction Protocol") — support is passage-exact. Note: quote span is narrower than the sentence; harmless. |
| 3 | Two-phase flow + one-context-many-questions amortization | PASS | §3.1 dataset formulation (p.7): multiple questions per single injected context; LME(S*) 5 contexts / 300 questions |
| 4 | Competency guardrails declared as protocol part `[[ev-p094-sf-guardrails]]` | PASS | Quote supports directly |
| 5 | Mechanism hypothesis (incremental injection exposes build/update/integration) | PASS | Tagged hypothesis; consistent with §1/App. L.2 |
| 6 | Predicted signature incl. compute-matched three tiers (App. J) | PASS | App. J, Table 18 |
| 7 | Discrete chunks are not true streaming (author-acknowledged) | PASS | App. L.2 |
| 8 | Chunk size is a strong confound; 512 vs 4096 notable on AR | PASS | §4.3.1, Fig. 2, Table 8 |
| 9 | Source lineage (static long-context benchmarks → incremental reconstruction) | PASS | §5 ("we restructure existing datasets") |
| 10 | Evidence ledger line | PASS | Mechanical |
| 11 | Retrieval vocabulary | PASS | Grounded |

Card verdict: PASS.

## 2. P095 — Deterministic Freshness

### 2.1 `paper-p095`

| # | Atomic claim | Verdict | Anchor / correction |
|---|---|---|---|
| 2 | Problem framing (explicit total-order markers present, LLM still unreliable at "newer wins") | PASS | Abstract, §1 |
| 3 | "extract-then-max 三步管线：…确定性择新 → 生成" | NARROW | §3.1 defines three steps as retrieval → candidate extraction → freshness picking; the answer is the extracted entity of the max-serial candidate returned directly — there is no LLM generation step. Smallest correction: "…Python max(serial) 确定性择新 → 直接返回该候选的抽取实体（无生成步）". |
| 4 | Multi-hop via per-hop deterministic resolution | PASS | Abstract (same bound passage) + §3.2 CAR |
| 5 | Matched comparison +10.8pp (67.2→78.0) `[[ev-p095-matched-comparison]]` | PASS | Quote verbatim (Abstract); §5.2 |
| 6 | Gap widens to +21pp@262K | PASS | Abstract, §5.2 |
| 7 | Two failure modes with mechanism + quantification (drift 75%→61%) `[[ev-p095-prior-override-drift]]` | PASS | Quote verbatim (§1.2, p.3); §5.4 |
| 8 | "union-accuracy 下界" | NARROW | The 88.5% union accuracy is the paper's "retrieval upper bound"/soft ceiling (§1.5 contribution 4, §5.5: soft ceiling ~88–95%); the *lower bound* is the 11.5% remainder on retrieval failure. Smallest correction: "union-accuracy 软天花板（88.5%；剩余 11.5% 为检索失败下界）". |
| 9 | McNemar pairing + complementarity 21.3% vs 10.5% as reusable operators | PASS | §5.5: 85 vs 42, χ²=14.6, p<0.001 |
| 10 | +10.8pp is pipeline-level attribution, author-noted repeatedly ("四处自注") | PASS | Abstract, §1.5(1), §1.6, §4.3/§5.2 — ≥4 self-notes confirmed |
| 11 | Two intervention points (index-time metadata retention + assembly); matched contrast isolates only the assembly stage | PASS | §3.1 (fact-level indexing, serial as key); §5.2 holds chunking fixed on both arms |
| 12 | Missing LLM-picks-newest control | PASS | §5.2/§6 (left to future work) |
| 13 | LongMemEval tie | PASS | §5.7: 57.8% vs 64.4%, n=45, overlapping CIs |
| 14 | Three backbones all OpenAI | PASS | §1.6, §4.2 (gpt-4o-mini, gpt-4o, o4-mini) |
| 15 | "SubEM 口径利好短实体输出" | REJECT | Refutation: §4.5 SubEM caveat states the opposite direction — substring credit means a *verbose* answer incidentally containing the gold string counts correct, inflating long-context oracle baselines; for the short-entity pipeline it is "a non-issue". SubEM additionally *penalizes* the pipeline ("no answer" counted wrong §3.1; Yes/No prefix mismatch §5.7). Replacement: "SubEM 子串匹配利好冗长输出（作者自注会略抬高长上下文 oracle 基线）；对短实体/弃答输出反而更严。" |
| 16 | Cross-system comparisons have unaligned chunking | PASS | §3.1 (fact-level vs MAB chunk-512, Hu et al. Table 15) |
| 17 | OP5 problem-type routing proposed-untested | PASS | §6.6 (composable extension left to future work) |
| 18 | Evidence ledger | PASS | Mechanical |
| 19 | Retrieval vocabulary | PASS | Grounded (CAR = Chain-Aware Resolution §3.2; SOTA claim §1.5(2)) |

Card verdict: REVISE (rows 3, 8 NARROW; row 15 REJECT).

### 2.2 `failure-llm-freshness-judgment-prior-override-and-drift`

| # | Atomic claim | Verdict | Anchor / correction |
|---|---|---|---|
| 1 | Prior-override: strong-prior real-world entities beat explicit "newer wins" rule | PASS | Quote verbatim (§1.2) |
| 2 | Serial-comparison drift: pool grows with context; 75%@64K→61%@262K | PASS | Quote verbatim; §5.4 |
| 3 | Carrier = MAB FactConsolidation with explicit total-order markers | PASS | §2.1/§4.1 |
| 4 | Matched control dimensions + +10.8pp + author pipeline-level note (resolver/prompt/temperature jointly vary) | PASS | Quote verbatim; §1.6 adds output format — card's list is non-exhaustive but not wrong |
| 5 | Two-author preprint; three OpenAI backbones; no cross-family | PASS | Title page/manifest; §1.6 |
| 6 | "SubEM 口径利短实体输出（作者已披露）" | REJECT | Same refutation as 2.1 row 15; the author-disclosed caveat points the other way. |
| 7 | Failed intervention framing (rule in prompt, markers in data, failure still systematic) | PASS | §1.2, §6.1 |
| 8 | Missing shared-extraction + LLM-picks-newest control (author future work); resolver share not isolable | PASS | §5.2 ("we leave this clean isolation to future work") |
| 9 | "LongMemEval 移植仅打平（57.8 vs 64.4）——在无显式全序标记的载体上不证优势" | NARROW | LongMemEval-KU *does* carry explicit total-order markers (chat-session timestamps; pipeline ran max(timestamp), §5.7), and §1.6 groups timestamps under "explicit version markers". The paper attributes the tie to question-type mismatch (Yes/No, historical, aggregation), and states the freshness mechanism itself ports. Smallest correction: "LongMemEval 移植仅打平（57.8 vs 64.4）——载体有时间戳全序标记，平局源于问题型超出 current-value 域（max 为错算子），不证跨载体优势。" |
| 10 | Gap widening (+8pp@6K→+21pp@262K) supports drift mechanism | PASS | Abstract, §1.2 |
| 11 | Warning: rule-following freshness adjudication not usable as hypothesis; Yes/No, historical, aggregation = wrong-operator domain for max() | PASS | §5.7 items 1–3 |
| 13 | Repair-boundary hypothesis (deterministic assembly requires explicit markers; markerless adjudication open) | PASS | §1.6 assumption statement; hypothesis-tagged |
| 14 | Evidence ledger | PASS | Mechanical |
| 15 | Retrieval vocabulary | PASS | Grounded |

Card verdict: REVISE (row 6 REJECT; row 9 NARROW).

### 2.3 `operator-extract-then-deterministic-max-assembly`

| # | Atomic claim | Verdict | Anchor / correction |
|---|---|---|---|
| 1 | Intervention target (post-retrieval assembly; move adjudication out of LLM) | PASS | §1, §3 |
| 2 | Before/after description; extraction verbatim not-best; per-hop decomposition; "整管线约 50 行" `[[ev-p095-matched-comparison]]` | NARROW (binding only) | All content verified (§3.1 steps 1–3, "do not pick a best"/verbatim instruction, ≈50 lines; §3.2 CAR). But the bound abstract passage does not contain the verbatim/not-best instruction or the ~50-line figure. Smallest correction: add a §3.1 passage binding (or locator note "§3.1") for those two details. |
| 3 | Index-time fact-level chunking preserving version metadata = second (upstream) intervention point | PASS | §3.1 contrast 1 |
| 4 | Mechanism: extraction removes entity text (no prior-override) and shrinks pool (no drift; max exact) `[[ev-p095-prior-override-drift]]` | PASS | Bound passage contains the elimination sentence head; full sentence continues p.4; §6.1 restates. Support is passage-anchored. |
| 5 | Signature: gain widens with context; degradation localized to judgment layer conditional on retrieval (union 88.5% ceiling + McNemar p<0.001) | PASS | §1.5(3), §5.4, §5.5 |
| 6 | Hard precondition: explicit total-order markers (FactCon construction property) | PASS | §1.6 assumption; §3.1 |
| 7 | "LongMemEval 上仅打平——无该结构时不证可用" | NARROW | Same correction as 2.2 row 9: LongMemEval-KU has timestamp total order; the tie is a question-type scope result, not a missing-marker result. |
| 8 | +10.8pp pipeline-level; strict extraction over-rejects; hybrid fallback ineffective (+0.2pp) | PASS | §1.6; §5.5 (predicate-strictness over-rejection); §6.6 ("a wash (+0.2 pp)") |
| 9 | Source lineage | PASS/N/A | Consistent |
| 10 | Evidence ledger line | PASS | Mechanical |
| 11 | Retrieval vocabulary | PASS | Grounded |

Card verdict: REVISE (row 7 NARROW content; row 2 binding note).

## 3. P096 — VeriSimpl

### 3.1 `paper-p096`

| # | Atomic claim | Verdict | Anchor / correction |
|---|---|---|---|
| 1 | ICML 2026, PMLR 306 published anchor | PASS | PDF front matter (Proceedings of the 43rd ICML, PMLR 306, 2026) |
| 3 | Problem framing | PASS | §1 |
| 4 | Changed computation core: solver-constructed reduced-complexity queries, LLM adjudication, workflow inversion `[[ev-p096-simplification-inversion]]` | PASS | Quote verbatim (§1, p.2) |
| 5 | Details in the same sentence: three constraint mutations / singleton+full variable masks / type check / lexicographic aggregation / best-of-K (K≤10) selector / all-pass gate | NARROW (binding only) | All details verified: §3 (c<, c=, c> mutations; Algorithms 2–3; singleton and full-set masks; TYPEVERIFY; "aggregated into a lexicographic ranking"; "up to K = 10") and §4.2 (all-queries-succeed gate). The bound page-2 passage contains none of these specifics. Smallest correction: bind an additional §3 Algorithm-overview passage (p.4–5) or retag the detail clause with locator "§3/Alg.1". |
| 6 | Main results across three base models; GPT-4o avg 65.5 / R1 72.8 | PASS | Tables 1–2; Mistral in App. C (Table 10) |
| 7 | Self-verification precision 91.5% (GPT-4o) / coverage 23–34% | PASS | Table 3 (precision avg 91.5/78.5; coverage avg 34.2/23.0) |
| 8 | Oracle no leakage: verification oracle computed by solver on the candidate's own model | PASS | §3 (witness valuations from mutated candidate constraints; optimal valuation of candidate model M) |
| 9 | best-of-K confound without compute parity | PASS | Verified by absence: no self-consistency/majority/random-pick-of-K control anywhere in the PDF |
| 10 | CompOR n=17 | PASS | §4 datasets ("the 17 problems…") |
| 11 | Effective denominators inconsistent with declared counts (suspected undeclared exclusions) | PASS | Arithmetically verified from Tables 1–3 vs declared n: NLP4LP (n=67) cells 43.5/46.8/37.1/51.6/58.1 and IndOR (n=100) cells 42.7/17.7/45.8/67.7 are impossible as k/n percentages; NL4Opt SELFDEBUG 76.5 impossible at n=269. |
| 12 | A.2/A.3 case transcripts mismatch problem values | PASS | App. A.2 (pp.12–13): problem states pollution 40/70/100, capacity 10/20/50, ≥300 units, ≤20 trips, ≤8 motorcycle; transcript reasons with 2/3 pollution, 2/3 capacity, ≥5 units, ≤4 trips, ≤3, total 6.0; reported solution (0,2,0) also inconsistent with stated total pollution 600. App. A.3 (pp.13–15): problem has 6 named children, min 3/max 4, costs $750–$1650; transcript reasons about "C", cost $4, at most two children. |
| 13 | R1 two inconsistent number sets | PASS | Table 2 avg 72.8 vs Table 4 Acc 72.5; Table 3 coverage 23.0 vs Table 4 Cov 22.8 |
| 14 | Accuracy adjudication criterion undefined | PASS | Verified by absence: §4/Tables 1–2 report "accuracy" with no stated correctness criterion (no tolerance/objective-match definition anywhere) |
| 15 | R1 verification precision below GPT-4o (78.5 vs 91.5), unexplained | PASS | Table 3; §4.2 discusses trends but offers no explanation for the reversal |
| 16 | Lineage | N/A→consistent | Internal |
| 17 | Evidence ledger ("其余缺陷记录于 reconciliation") | PASS (mechanical part) / N/A (reconciliation not read — forbidden) | |
| 18 | Retrieval vocabulary | PASS | Grounded |

Card verdict: REVISE (binding-only, row 5; all content verified — including every adversarial defect claim, several of which this audit independently re-derived from the PDF).

### 3.2 `failure-generator-aligned-verification-passes-shared-misreads`

| # | Atomic claim | Verdict | Anchor |
|---|---|---|---|
| 1 | Observed failure: shared NL misread → formalization and LLM reasoning agree on same wrong model ("start time" variable semantics; profit objective missing costs); internally coherent; verification passes; decision variables assumed given; completely missed aspects generate no queries `[[ev-p096-shared-misinterpretation]]` | PASS | Quote near-verbatim (p.8); shift-scheduling and workforce cases also in App. A.5/A.6 |
| 2 | Conditions: ICML 2026; mechanism; three signals lexicographically aggregated best-of-K; adjudicator = generator LLM `[[ev-p096-simplification-inversion]]` | PASS | Core anchored by quote; details verified §3/§4 (same base model generates candidates and adjudicates queries) |
| 3 | Failed intervention framing (all-pass gives high-confidence signal on shared misreads) | PASS | p.8 ("verification succeeded because … shared misinterpration") |
| 4 | best-of-K confound numbers: single-signal 10-candidate selectors 62.2–64.8 vs BASELLM 56.8; verification-signal margin ~0.7–3.3; no compute parity | PASS | Tables 1, 4 (A-FULLVAR 62.2 … A-SINGLEVAR 64.8; VERISIMPL 65.5); absence of parity control verified |
| 5 | CompOR column n=17 | PASS | §4 |
| 6 | A.2/A.3 transcripts mismatch — not usable as mechanism evidence | PASS | See 3.1 row 12 |
| 8 | Repair-boundary hypothesis (decouple adjudicator from generator) | PASS | Hypothesis-tagged; consistent with p.8 limitation statement |
| 9 | Evidence ledger | PASS | Mechanical |
| 10 | Retrieval vocabulary | PASS | Grounded |

Card verdict: PASS.

### 3.3 `operator-solver-simplification-query-verification`

| # | Atomic claim | Verdict | Anchor |
|---|---|---|---|
| 1 | Intervention target | PASS | §1 |
| 2 | Before/after: inversion of the conventional verification workflow `[[ev-p096-simplification-inversion]]` | PASS | Quote verbatim |
| 3 | I/O and timing (probe adjudication sequence + all-pass gate; selector/self-verification dual use) | PASS | §3 Alg.1, §4.2 |
| 4 | Mechanism hypothesis | PASS | Hypothesis-tagged; matches §1 rationale |
| 5 | Signature: 91.5% precision / 23–34% coverage; ~2/3 correct solutions unflagged; cite gains only with best-of-K confound | PASS | Table 3 (GPT-4o coverage 34.2 → 65.8% of correct unflagged); Table 4; parity-control absence verified |
| 6 | Preconditions (author-admitted structural boundary): variables assumed shared; missed NL aspects produce no queries `[[ev-p096-shared-misinterpretation]]` | PASS | Quote verbatim |
| 7 | Same-LLM adjudication is failure-correlated source; transfer needs solver-like reliable witness generator | PASS | p.8; §1 (solver reliability in constructing witnesses) |
| 8 | Source lineage | PASS | §1, related work |
| 9 | Evidence ledger line | PASS | Mechanical |
| 10 | Retrieval vocabulary | PASS | Grounded |

Card verdict: PASS.

## 4. P097 — ReLoop

### 4.1 `paper-p097`

| # | Atomic claim | Verdict | Anchor / correction |
|---|---|---|---|
| 1 | Verbatim quote anchor "solver feedback catches syntax errors, not missing constraints"; 90pp gap quantification | PASS | §1 p.2, byte-exact in PDF extraction and in bound quote |
| 2 | Silent failures: 91.1% Exec vs 0.5% Acc `[[ev-p097-feasibility-gap]]` | PASS | Quote verbatim; §5.2 Table 5 (DeepSeek) |
| 3 | Changed computation: two training-free mechanisms; four-stage single-call generation; L1 (IIS/unbounded-ray, ≤3 regenerations); L2 (non-blocking, graded thresholds, conservative repair + rollback) `[[ev-p097-behavioral-perturbation]]` | NARROW (binding only) | Core (two mechanisms, four-stage chain, L1, L2) is inside the bound passage (§3 opening, p.3). Verified details outside it: single LLM call (§3.2/App. E.2), IIS/ray diagnostics (§3.3), N=3 (§5.1), thresholds/τr rollback (§3.3–3.4). Smallest correction: add locator note "§3.2–3.4/App.E" or a §3.3–3.4 passage binding for the L1/L2 parameter details. |
| 4 | CoT primary accuracy driver on compositional problems (Claude +8.5pp) | PASS | §5.4 |
| 5 | L2 largest single item on localized-defect domain (MAMO +4.4pp); zero on structural domain | PASS | §5.4 (MAMO +4.4pp, 11 corrected/2 regressed; RetailOpt strict accuracy unchanged, errors predominantly structural) |
| 6 | CoT collapses DeepSeek execution 91.1→53.2 | PASS | §5.2/§5.4 |
| 7 | CoT destroys SFT model (84 crashes + 65 regressions) | PASS | §5.3 (OptMATH on MAMO), Limitations |
| 8 | IndustryOR repairable-band-hollow bimodal (34%<1% + 47%>10%) | PASS | §5.4 ("leaving almost no instances in the correctable range") |
| 9 | Repair-LLM data fabrication documented | PASS | §3.4 safety check rationale |
| 10 | Retry-budget confound (~3× tokens, no equal-budget control) | PASS | §5.1 ("∼3× base cost"); equal-budget/blind-retry control verified absent |
| 11 | Cross-benchmark Base cited from SIRL; harness alignment undescribed | PASS | App. G.3 (cited from SIRL Table 1 for 4 of 5 models); no alignment description anywhere |
| 12 | Single-run, no error bars; gains cited directionally | PASS | App. G.4 ("All results are single-run (pass@1)") |
| 13 | RetailOpt prompt carries scaffolding aligned with reference MILP; absolute values don't extrapolate to unscaffolded settings | PASS | App. C.1 ("moderately scaffolded … aligned with the reference MILP"; unscaffolded prompts near-zero) |
| 14 | L2 shares the generating LLM | PASS | Limitations |
| 15 | Lineage | N/A→consistent | Internal |
| 16 | Evidence ledger | PASS | Mechanical |
| 17 | Retrieval vocabulary | PASS | Grounded |

Card verdict: REVISE (binding-only, row 3; all content verified).

### 4.2 `failure-solver-feasibility-near-zero-information-proxy`

| # | Atomic claim | Verdict | Anchor / correction |
|---|---|---|---|
| 1 | 91.1% vs 0.5%, 90-point gap; causes (verbatim quote; self-critique inherits gaps; reranking needs unavailable ground truth) `[[ev-p097-feasibility-gap]]` | PASS | Quote verbatim (§1 p.2) |
| 2 | Conditions: NL→Gurobi; RetailOpt-190 (38 archetypes × 5 variants); MAMO/IndustryOR; preprint | PASS | §4 Table 4 caption ("38 × 5 = 190"); §5.1; p.1 "Preprint." |
| 4 | Failed intervention: exec+feasible as correctness signal; after full ReLoop Claude still ~2/3 silent failures | PASS | §5.2 ("two-thirds remain silent failures", 100% Exec / 31.1% Acc) |
| 5 | Evidence boundary: retry-budget confound (~3× tokens, ≤3 regens vs single-shot Base, no equal-budget blind-retry control); cross-benchmark Base 4/5 cited from SIRL not re-run; single-run pass@1 no error bars; gap itself same-pipeline and robust | PASS | §5.1, App. G.3–G.4; 4-of-5 cited models enumerated in App. G.3 |
| 6 | Perturbation boundary: only locally-perturbable defects detectable; structural silent failures (internally consistent wrong decompositions) undetectable `[[ev-p097-behavioral-perturbation]]` | NARROW (binding only) | Claim true — §5.4 (structural errors "produce plausible perturbation responses"; strict accuracy unchanged) and Limitations (τr calibrated for localized defects). The bound related-work passage states the mechanism, not this boundary. Smallest correction: add a §5.4/Limitations passage binding or locator note "§5.4". |
| 7 | Warning for execution/feasibility-observable candidates | PASS | Follows directly from row 1 |
| 8 | Repair boundary: perturbation (local) vs independent checker (structural) complementary; coefficient-magnitude and formulation-equivalence errors author-admitted beyond scope | PASS | Limitations: three failure modes beyond scope — coefficient magnitude, formulation equivalence, unrepresented structures (card names two of three; not false) |
| 9 | Evidence ledger | PASS | Mechanical |
| 10 | Retrieval vocabulary | PASS | Grounded |

Card verdict: REVISE (binding-only, row 6).

### 4.3 `operator-behavioral-perturbation-existence-test`

| # | Atomic claim | Verdict | Anchor / correction |
|---|---|---|---|
| 1 | Intervention target | PASS | §1/§3.3 |
| 2 | Before/after: repurpose sensitivity analysis — test existence, not value; zero response to should-matter parameter indicates missing component; bypasses LLM self-review; no ground truth needed `[[ev-p097-behavioral-perturbation]]` | PASS | Quote verbatim; self-critique/external-signal support also inside the same bound passage |
| 3 | I/O: typed factors (capacity ×0.001, demand ×100, cost ×0.001, revenue ×100); graded verdicts (r<5% WARNING, 5–30% INFO, >30% or induced infeasible PASS); post-L1, non-blocking; conservative repair with rollback τr=4% | PASS | §3.3 (also "other ×0.01" for both CPT/OPT — card lists named four; non-exhaustive but accurate), §3.4, App. B |
| 4 | Mechanism hypothesis (zero-sensitivity fingerprint; solver as behavioral oracle) | PASS | Hypothesis-tagged; matches §2/§3.3 |
| 5 | Signature: MAMO +4.4pp largest single item; RetailOpt structural domain zero contribution; cite with retry-budget confound | PASS | §5.4; §5.1; parity-control absence verified |
| 6 | Preconditions: locally perturbable defects; data-code separation (data["key"] access) enables runtime perturbation; AST source-perturbation fallback on extraction failure; repair-LLM data fabrication motivates safety check `[[ev-p097-feasibility-gap]]` | NARROW (mis-binding) | All content verified: §3.2 Stage 3 (data["key"] patterns essential for L2), App. E.2 ("L2 falls back to source-code AST perturbation"), §3.4 (fabrication → safety check). But the bound evidence (ev-p097-feasibility-gap, §1 gap paragraph) contains none of this sentence's content — the token neither anchors nor supports it. Smallest correction: rebind to `ev-p097-behavioral-perturbation` (partial anchor) or, better, bind a §3.2/App.E.2 passage; content text unchanged. |
| 8 | Source lineage: sensitivity analysis → existence test, self-claimed novel | PASS | §2 ("to our knowledge, novel") |
| 9 | Evidence ledger line | PASS | Mechanical |
| 10 | Retrieval vocabulary | PASS | Grounded |

Card verdict: REVISE (row 6 mis-binding; content verified).

## 5. Summary table

| card_id | Verdict | Reason (smallest correction) |
|---|---|---|
| paper-p094 | REVISE | Binding-only: overwrite-ablation clause in an AUTHOR_FACT line is unsupported by its bound quotes; add App. K.2/Table 19 binding or retag clause (content verified true). |
| failure-selective-forgetting-collapses-with-context-length | REVISE | TTL <4% zero-shot floor is a TTL-task control (App. H.2), not a FactCon prior-exclusion; replace with FactCon's MQUAKE-counterfactual construction argument or scope the claim to TTL. |
| operator-incremental-injection-benchmark-reconstruction | PASS | — |
| paper-p095 | REVISE | (a) Pipeline has no LLM generation step — third step returns the max-serial candidate's extracted entity (§3.1); (b) union-accuracy is a soft ceiling/retrieval upper bound, not "下界"; (c) SubEM claim direction inverted (REJECT — §4.5 says substring credit inflates verbose outputs and is a non-issue for the short-entity pipeline). |
| failure-llm-freshness-judgment-prior-override-and-drift | REVISE | (a) SubEM claim inverted (REJECT, as above); (b) LongMemEval-KU has explicit timestamp total order — tie is a question-type-scope result, not a missing-marker result. |
| operator-extract-then-deterministic-max-assembly | REVISE | LongMemEval characterization as above; plus binding note for "verbatim/not-best" and "≈50 行" details (§3.1). |
| paper-p096 | REVISE | Binding-only: mutation/mask/type/lexicographic/K≤10/all-pass details in the AUTHOR_FACT line are not in the bound page-2 passage; add §3/Alg.1 binding (all details verified true; all adversarial defect claims independently confirmed, incl. denominator arithmetic and A.2/A.3 transcript mismatches). |
| failure-generator-aligned-verification-passes-shared-misreads | PASS | — |
| operator-solver-simplification-query-verification | PASS | — |
| paper-p097 | REVISE | Binding-only: L1/L2 parameter details (IIS/ray, ≤3, thresholds, rollback) outside the bound §3-opening passage; add §3.2–3.4/App.E locator or binding (content verified true). |
| failure-solver-feasibility-near-zero-information-proxy | REVISE | Binding-only: perturbation-boundary AUTHOR_FACT is supported by §5.4/Limitations, not by the bound related-work quote; add §5.4 binding (content verified true). |
| operator-behavioral-perturbation-existence-test | REVISE | Mis-binding: preconditions AUTHOR_FACT cites ev-p097-feasibility-gap, which contains none of the sentence; rebind (all content verified true at §3.2/App.E.2/§3.4). |

Atomic totals (excluding N/A internal items): PASS 138, NARROW 11, REJECT 2.

Named-risk check (invocation §Exact request): all four overstatement risks are correctly handled by the cards — P094 cross-row rankings are explicitly not treated as same-backbone/same-chunk conclusions; P095 +10.8pp is consistently cited as pipeline-level and non-transferable (with the LongMemEval mischaracterization noted above); P096 gains are always coupled to the best-of-K compute confound and A.2/A.3 transcripts are explicitly excluded as mechanism evidence; P097 gains are always coupled to the retry-budget confound and the cited-baseline caveat. No CODEX_SYNTHESIS/HYPOTHESIS line overstates in the direction of any named risk; the errors found run in the conservative direction or are provenance-binding issues, except the two SubEM REJECTs (inverted direction of a disclosed metric caveat) and the LongMemEval marker mischaracterization.

## 6. Provenance

- End time: 2026-07-27T02:58+08:00 (start 2026-07-27T02:35:00+08:00 per invocation)
- Model/version: Claude (Fable 5, model id claude-fable-5), running as an independent audit subagent under Claude Code / Claude Agent SDK
- Procedural blinding: honored. Files read (complete list):
  - `knowledge_base/corpus/card_audits/w06-audit-b/invocation.md`
  - The 12 named cards under `knowledge_base/cards/{paper,failure,operator}/`
  - `knowledge_base/corpus/evidence.json` (parsed programmatically; only the 9 P094–P097 evidence objects examined)
  - `knowledge_base/corpus/manifest.json` (P094–P097 records only)
  - `knowledge_base/knowledge.w06_next.sqlite` (schema + the P094–P097 passages referenced by the 9 evidence objects, plus targeted substring checks on those same passages; read-only usage)
  - `knowledge_base/papers/P094_memoryagentbench.pdf`, `P095_deterministic_freshness.pdf`, `P096_verisimpl.pdf`, `P097_reloop.pdf` (bytes for sha256; full text re-extracted with pymupdf to session scratchpad)
- Not read: any reconciliation.md, any read_1.md, any read-2 report (no source ambiguity remained that required one), all earlier Card audits/dispositions including other W06 audits, production calibration/blind queries/judgments/results/reports, any other Cards or papers (incl. P091/P092 — cross-references to them are marked N/A above), any Candidate/Commissioning/Reviewer asset.
- Start/end context: fresh session; no prior conversation state; all intermediate artifacts (extracted PDF text, verification scripts) written only to the session scratchpad, not to the repository.
- Tool limits: PDF text via pymupdf layout-order extraction — table cell alignment is inferred from reading order (all table-derived numbers were cross-checked against surrounding prose where available); no OCR needed; no network access used; no write statements executed against the sqlite database.
- Mechanical result: 9/9 evidence quotes byte-exact vs sqlite passages; 9/9 passage sha256 self-consistent and matching evidence records; 4/4 PDF sha256 matching cards, manifest, and evidence `fulltext_sha256`; 12/12 card metas well-formed.
- Report SHA-256: computed over this file's final bytes immediately after write; reported in the auditor's final response and reproducible via sha256 of `report.md`.
