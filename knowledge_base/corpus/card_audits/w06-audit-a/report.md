# W06 Card Source Audit A — Report

- Audit ID: `w06-audit-a`
- Scope: 12 Cards (P090–P093 × paper/failure/operator) vs the four official PDFs, their Evidence objects in `knowledge_base/corpus/evidence.json`, and exact passages in `knowledge_base/knowledge.w06_next.sqlite`.
- Verdict scale per atomic claim: PASS / NARROW (smallest exact correction given) / REJECT (PDF-anchored refutation).
- No card, evidence, manifest, PDF, or database was modified.

## Mechanical integrity (all 12 cards)

For every evidence id cited by the 12 cards (`ev-p090-fixed-granularity-selection`, `ev-p090-entropy-router`, `ev-p090-association-graph`, `ev-p091-cosine-auroc`, `ev-p091-supersession-rule`, `ev-p091-retain-fabrication`, `ev-p092-whitebox-metrics`, `ev-p092-crs-low`, `ev-p093-foil-collapse`, `ev-p093-poison-rag`, `ev-p093-paired-protocol`):

- The record exists in `evidence.json`; `source_content` is byte-identical to `passages.text[quote_start:quote_end]` in `knowledge.w06_next.sqlite` (11/11).
- `passages.text_sha256` recomputes correctly from the stored text and matches the evidence record's `passage_text_sha256` (11/11).
- Each evidence `fulltext_sha256`, each card's `source_refs.sha256`, and each manifest record `sha256` all match the actual PDF bytes (recomputed SHA-256):
  - P090 `256eba2430611820eb4b18978fdd35f05a3bcf26c7b808b03ef0971ab3bc49c8`
  - P091 `10349a31de86116b7e4cc5a8cb5e60766a55ab7dbab7894906841a6e3234171f`
  - P092 `1918dd32c20affd501ac314ab4f1c5b67ab71dc2178784d31b6596030abbebce`
  - P093 `e62a61bf3e0bfbfcbd08f9fe09cdb29079f9e87035c32b3ee7eee89df1630fb1`
- Metadata note (not a card defect): `ev-p091-retain-fabrication.section` is labeled "References"; the passage actually sits in Appendix D on PDF page 20 (verified: page 20 contains "Removing supersession collapses mean evolving accuracy…"). Quote integrity unaffected.

## Per-card atomized findings

### paper-p090 — REVISE

1. META/evidence/passage/sha integrity — PASS.
2. Problem [AUTHOR_FACT] (fixed granularity → incomplete recall or noise; topic-aware segmentation lacks per-query adaptive selection) — PASS. Quote is verbatim from P090 Introduction p.2 and fully supports the sentence.
3. Changed computation, write side, clause "LLM 生成四粒度记忆（session/turn/summary/keyword）" — NARROW. P090 Eq. (1) p.3: `Ui, Ki = fLLM(Si); Ti = segment(Si)` — the LLM generates only summary and keywords; the session is raw dialogue and turns come from a segmentation operation. (The Fig. 2 caption's "leverage LLM agent to generate multi-granularity information" is looser, but the mechanism section is explicit.) Smallest correction: replace with "写入：LLM 生成 summary/keyword，raw session 及其 turn 切分共同构成四粒度记忆（session/turn/summary/keyword），各粒度节点经 accept/reject 集接入关联图。"
4. Write-side clause "各粒度节点经 accept/reject 集接入关联图" — PASS (verbatim-supported by ev-p090-association-graph, §2.2 p.4).
5. Read-side [AUTHOR_FACT] "按各粒度相似度分布的 Shannon 熵计算 soft router 权重" — PASS (ev-p090-entropy-router quote, §2.3 p.4).
6. Read-side clause "PPR 图扩展后过滤" — PASS. Verified directly against §2.4 (PPR over the association graph, then LLM-based redundancy filtering). Note: this clause lies outside the attached quote's span; support is PDF-direct, not quote-direct.
7. Findings [CODEX_SYNTHESIS] (consistent gains over single-granularity and prior memory systems on QA and retrieval on LongMemEval/LoCoMo-family; detail numbers pipeline-level) — PASS. Paper: four datasets (LoCoMo, Long-MT-Bench+, LongMemEval-s/-m), gains claimed on both QA and retrieval; the pipeline-level hedge is the correct direction. (The card's reference to what reconciliation records was not verified — reconciliation files are forbidden reads for this audit.)
8. Limitations clause "粒度路由单项贡献未隔离" — NARROW. P090 Table 3 (p.8, LongMemEval-s) contains a "w/o Router" ablation including generation-free retrieval metrics (QA GPT4o-J 60.20→56.60; R@3 78.51→75.53), i.e. the router's marginal contribution IS isolated on one benchmark; the flat "未隔离" understates the paper's own evidence. Smallest correction: "粒度路由单项贡献仅在 LongMemEval-s 消融（Table 3 w/o Router）中被量化，跨基准主表增益仍系管线级效应；". Error direction is conservative (does not inflate the source).
9. Remaining limitations clauses (summary/keyword generation cost grows with dialogue; temporal validity/version conflict outside its mechanism — confirmed: no staleness/temporal-validity content anywhere in P090) — PASS.
10. Lineage / Evidence ledger / Retrieval vocabulary — PASS (ledger claim "三条均绑定 exact Passage" mechanically confirmed).

### failure-fixed-single-granularity-memory — PASS

1. Mechanical integrity — PASS.
2. Observed failure [AUTHOR_FACT] — PASS (near-verbatim restatement of the Introduction quote; every element present in the quote).
3. Conditions and scope [CODEX_SYNTHESIS] — PASS (multi-session conversational retrieval; LongMemEval/LoCoMo-family carriers confirmed; the fine-vs-coarse granularity gloss is consistent with §2.3's "lower entropy … higher confidence in precise matches").
4. Failed intervention [CODEX_SYNTHESIS] — PASS (accurately describes the single-predefined-granularity status quo the paper attacks).
5. Evidence [AUTHOR_FACT] "entropy 度量各粒度上 query-memory 相似度分布的不确定性…低熵对应精确匹配置信高" — PASS. First half verbatim in quote; the low-entropy gloss is verbatim author text in §2.3 Soft Router Weights ("lower entropy Hg typically reflects higher confidence in precise matches"), immediately following the quoted span.
6. Alternative explanations [CODEX_SYNTHESIS] — PASS. Correctly phrased: "不能把全部增益归于粒度路由单项" (true; headline gains are full-pipeline vs external baselines) while crediting "消融与动机分析" (Table 3 ablations exist). This card's phrasing is the accurate version of what paper-p090/operator overstate as "未隔离".
7. Warning [CODEX_SYNTHESIS] — PASS (governance claim consistent with manifest admission_role).
8. Repair boundary [CODEX_HYPOTHESIS] — PASS (labeled hypothesis; the claimed unoccupied combination is not contradicted by P090, which contains no temporal-validity mechanism).
9. Evidence ledger ("Introduction 与 §2.3") / vocabulary — PASS (section attributions match evidence records).

### operator-entropy-routed-multi-granularity-retrieval — REVISE

1. Mechanical integrity — PASS.
2. Intervention target [CODEX_SYNTHESIS] — PASS.
3. Before/after [CODEX_SYNTHESIS] — PASS (inverse-entropy normalization Eq. (4); GMM accept/reject edges §2.2; PPR expansion §2.4 — all confirmed).
4. Inputs/outputs [AUTHOR_FACT] with both citations — PASS ("熵 Hg 量化 query 在粒度 g 上匹配的不确定性" is verbatim; write-time graph construction supported by the association-graph quote).
5. Mechanism [CODEX_HYPOTHESIS] — PASS (labeled hypothesis, consistent with the author's motivation text).
6. Predicted observable signature [CODEX_HYPOTHESIS] — PASS (labeled hypothesis; consistent with Figure 1's suited-granularity analysis; not asserted as author result).
7. Preconditions/transfer clause "路由单项贡献未被单独隔离" — NARROW. Same refutation as paper-p090 item 8: Table 3 "w/o Router" (LongMemEval-s) quantifies the router's single-module contribution, including retrieval-only metrics. Smallest correction: "路由单项贡献仅在单基准消融（Table 3, LongMemEval-s）中被量化，主结果为检索+生成管线联动；". λ hyperparameter clause — PASS (λ is explicitly the entropy temperature, "analyzed in Appendix F").
8. Source lineage / Evidence ledger [AUTHOR_FACT] / vocabulary — PASS (ledger citations mechanically confirmed; "GMM" in vocabulary is paper-correct).

### paper-p091 — PASS

1. Mechanical integrity — PASS.
2. Role [CODEX_SYNTHESIS] "(AUROC 0.59)" — PASS. Rounded value matches the author's own abstract/contribution framing ("AUROC 0.59 (near chance)").
3. Problem [AUTHOR_FACT] — PASS. Every clause is author-verbatim on p.1: "RAG retrieves both the stale and the current value with near-identical embedding similarity", "The agent then either abstains or serves the superseded fact", "this is not a tuning problem but a structural one". Note: the attached quote (ev-p091-cosine-auroc) anchors only the structural-measurement basis; the abstain/serve-stale clauses were verified directly against the abstract.
4. Changed computation [AUTHOR_FACT] — PASS (verbatim-supported by ev-p091-supersession-rule; "静态侧保留 RAG 全召回" is in the quote).
5. Findings [AUTHOR_FACT] (0.99→0.33, indistinguishable from naive RAG 0.32; conditional fabrication ×6, peak 0.56; "更不准而且更不安全") — PASS. All numbers verbatim in the quoted Appendix D passage (p.20) and duplicated in main text p.8; "not merely less accurate but less safe" is author text.
6. Limitations [CODEX_SYNTHESIS] — PASS. Verified: "Draft v2" marking + single author (p.1); 98 pairs (§5.1); four synthetic evolving benchmarks with structured single-value templates (§5, §7); single embedder nomic-embed-text 768-d + single 7B backbone Qwen2.5-Coder-7B (§5); marker-free invariant self-built (§4.5). The P094 comparability clause is a cross-corpus governance claim outside this audit's readable set; noted, not adjudicated.
7. Lineage / ledger / vocabulary — PASS (ledger mechanically confirmed).

### failure-cosine-cannot-separate-contradiction-from-duplicate — REVISE

1. Mechanical integrity — PASS.
2. Observed failure [AUTHOR_FACT] #1 "98 个标注对上，cosine 区分 contradiction 与 duplicate 的 AUROC 仅 0.5926（近随机）" — NARROW. The four-decimal number 0.5926 is measured, per the attached quote (§5.1 p.6), as "cosine AUROC for separating duplicates from the rest" (rest = 22 merge + 22 contradict + 22 novel), not as a binary contradiction-vs-duplicate AUROC. The contradiction-vs-duplicate framing is the author's own gloss carrying the rounded 0.59 (abstract, contribution 1). "近随机" is author language. Smallest correction: "98 个标注对上（32 duplicate/22 merge/22 contradict/22 novel），cosine 区分 duplicate 与其余类的 AUROC 仅 0.5926——作者据此表述为 contradiction 与 duplicate 近随机不可分（0.59）。"
3. Observed failure [AUTHOR_FACT] #2 (0.99→0.33; conditional fabrication 均值 0.04→0.25 约 6 倍, 峰值 0.56; co-present stale+current → invents an answer) — PASS. Every number and the causal gloss are verbatim in the quoted passage.
4. Conditions and scope [CODEX_SYNTHESIS] — PASS (marker-free update streams §4.5; 7B local model + consumer hardware, abstract; four evolving benchmarks code_mutation/config_migration/dependency_bump/api_evolution §5; single-author preprint; 98 pairs).
5. Failed intervention [CODEX_SYNTHESIS] — PASS (§3: threshold-on-similarity and read-time LLM adjudication are exactly the rejected alternatives; "A learned classifier on top of similarity does not reliably help either").
6. Alternative explanations [CODEX_SYNTHESIS] — PASS. Single embedder (nomic-embed-text) confirmed, no embedder sweep; the contradiction-more-similar-than-paraphrase structural cause is author-verbatim (0.812 vs 0.800, Table 1 §5.1); fabrication amplification is an in-pipeline ablation (same read path) — supported by p.8 "isolating deterministic supersession as the single cause". P093 same-direction cross-reference is a KB-internal claim consistent with P093's literal-bias findings.
7. Warning [CODEX_SYNTHESIS] — PASS (mandates exactly the single-embedder caveat this audit would otherwise impose).
8. Repair boundary [CODEX_HYPOTHESIS] — PASS (labeled hypothesis).
9. Ledger / vocabulary — PASS ("cosine AUROC 0.59" in vocabulary uses the author's rounded framing; acceptable as a retrieval key).

### operator-deterministic-sro-supersession-ledger — PASS

1. Mechanical integrity — PASS.
2. Intervention target [CODEX_SYNTHESIS] — PASS.
3. Before/after [AUTHOR_FACT] — PASS. After-side is verbatim in ev-p091-supersession-rule and §4.1 ("normalizes the (subject, relation) key … If one exists with a different object, the new assertion supersedes it … No cosine, no LLM judge"). Before-side ("RAG 式全保留 + 读取时 LLM 裁决") matches the paper's framing (RAG retains everything; the reading model must decide which value is current, and the LLM-reranking/verification baselines do this at read time).
4. Inputs/outputs [CODEX_SYNTHESIS] — PASS (§4.2 bi-temporal ledger: "Facts are retired, not deleted", valid_from/valid_to/superseded_by; §4.4 "Active retrieval surfaces only currently-valid rows").
5. Mechanism [CODEX_HYPOTHESIS] — PASS (labeled hypothesis, mirrors §3's stated conclusion).
6. Predicted observable signature [AUTHOR_FACT] — PASS (quote-supported; "机制贡献在管线内被隔离" matches p.8 "isolating deterministic supersession as the single cause of the evolving-knowledge result").
7. Preconditions/transfer [CODEX_SYNTHESIS] — PASS (extraction as single point of failure: §1/§7, extraction ~44% on messier natural-language benchmark; non-triple prose falls to text-gate fallback and is not superseded, §4.1; synthetic templates limitation, §7).
8. Lineage / ledger / vocabulary — PASS (P030/P095 positioning is KB-internal governance, not contradicted by the PDF; ledger mechanically confirmed).

### paper-p092 — PASS

1. Mechanical integrity — PASS.
2. Role [CODEX_SYNTHESIS] — PASS (listing SEH@K/SRS/EUG as the white-box panel is consistent with the paper; see operator card for the EUG naming defect, which this card does not commit).
3. Problem [CODEX_SYNTHESIS] — PASS. Three-type taxonomy definitions match p.2: dynamic = later true update supersedes; static = later false contradiction must not overwrite; conditional = multiple memories valid under different conditions.
4. Changed computation [AUTHOR_FACT] — PASS. SEH@K/SRS verbatim in quoted §3.6 (p.14); CRS/UOCS verified in the same §3.6 continuation (p.15: UOCS Eq. 14 for dynamic, CRS Eq. 15 for static). Note: the CRS/UOCS clause lies outside the attached quote's span; support is PDF-direct.
5. Findings [AUTHOR_FACT] — PASS. "无系统全面占优" = "No system dominates all metrics and conflict types" (p.18); "静态冲突平均最难" = "static conflicts are the most difficult in terms of average AA" (p.18); CRS best 0.2501 (A-Mem, Table 3) and Memobase high static AA (0.4167) with lowest CRS (0.0694) are in the quoted §4.3 passage. Note: the first two clauses precede the quoted span (same §4.3); verified PDF-direct.
6. Limitations [CODEX_SYNTHESIS] — PASS. Preprint on ACM template confirmed; constructed conflict injection confirmed (§3); the not-fully-matched-configurations reading is fair per §4.1 ("each method is kept as close as possible to its intended memory design and default usage"). Recommended (non-blocking): "LLM judge 链的口径影响 CRS 绝对值" should mention that judgments are LLM-assisted matching followed by human verification (§3.6, p.15); the criteria-dependence caution itself remains valid.
7. Lineage / ledger / vocabulary — PASS (P094/P091 positioning is KB-internal; ledger mechanically confirmed).

### failure-answer-accuracy-without-conflict-recognition — REVISE

1. Mechanical integrity — PASS.
2. Observed failure [AUTHOR_FACT] — PASS. All elements in the quoted §4.3 passage (best CRS 0.2501; Memobase decoupling; "may return the correct stable value without explicitly recognizing the underlying contradiction"). Minor note: the card's "从未识别" drops the author's "explicitly"; the card's own alternative-explanations line restores this nuance, so no correction required.
3. Conditions and scope clause "judge 为 LLM 评分链" — NARROW. §3.6 p.15: "All answer and memory-item judgments are produced through LLM-assisted matching followed by human verification." Stating the judge as an LLM scoring chain omits the human-verification step and overstates protocol fragility. Smallest correction: replace "judge 为 LLM 评分链" with "judge 为 LLM 辅助匹配＋人工校验（§3.6）". Remaining conditions clauses (three conflict types; six systems Letta/Mem0/LangMem/A-Mem/MemOS/Memobase; ACM-template preprint) — PASS (system list matches §4.1 exactly).
4. Failed intervention [CODEX_SYNTHESIS] — PASS (black-box AA cannot distinguish adjudicated-vs-lucky retrieval; this is the paper's stated motivation for white-box metrics).
5. Evidence [AUTHOR_FACT] (SEH@K/SRS decouple evidence-presence from answer correctness) — PASS (quoted §3.6 definition supports).
6. Alternative explanations [CODEX_SYNTHESIS] — PASS (hedged as partial possibility; the cross-system consistency + decoupling robustness argument matches Tables 3–4).
7. Warning [CODEX_SYNTHESIS] — PASS.
8. Repair boundary [CODEX_HYPOTHESIS] — PASS (labeled hypothesis; aligned with P091's auditable ledger direction).
9. Ledger / vocabulary — PASS.

### operator-support-evidence-whitebox-retrieval-metrics — REVISE

1. Mechanical integrity — PASS.
2. Intervention target clause "检索质量对答案的边际贡献" — NARROW. The paper's third metric, EUG, is the Evidence Utilization Gap = SEH@3 − AA (appendix, Table 7 note and definition): it measures evidence retrieved but NOT converted into a correct answer — a utilization-failure diagnostic, not a marginal-contribution/gain measure. Smallest correction: replace "检索质量对答案的边际贡献" with "证据在场但未被答案利用的差距（EUG）".
3. Before/after [AUTHOR_FACT]: SEH@K and SRS clauses — PASS (verbatim in quoted §3.6). Clause "配合 EUG 类增益指标形成白盒层" — NARROW. Same refutation: EUG is a gap (SEH@3 − AA), defined in the appendix, not a gain-type metric, and it is outside the attached quote. Smallest correction: "配合 EUG（Evidence Utilization Gap＝SEH@3−AA，附录定义）诊断构成白盒层。"
4. Inputs/outputs [CODEX_SYNTHESIS] — PASS (gold memory-item annotation per query; per-conflict-type panels; evaluation-time).
5. Mechanism [CODEX_HYPOTHESIS] — PASS (retrieval-layer vs adjudication-layer decomposition matches the paper's SEH-vs-AA gap analysis).
6. Predicted observable signature [AUTHOR_FACT] — PASS (quoted §4.3 decoupling; Memobase case).
7. Preconditions/transfer [CODEX_SYNTHESIS] — PASS (K∈{2,3,5} sensitivity confirmed §4.2; P095 union-accuracy mapping is KB-internal, noted not adjudicated).
8. Source lineage — PASS.
9. Retrieval vocabulary term "evidence utilization gain" — NARROW. Smallest correction: "evidence utilization gap". (Single root cause for items 2, 3, 9.)

### paper-p093 — REVISE

1. Mechanical integrity — PASS.
2. Role [CODEX_SYNTHESIS] — PASS (ACL 2025 Main per manifest; PDF is the arXiv v2 of the published paper; controlled-protocol framing accurate).
3. Changed computation [AUTHOR_FACT]: Re-DocRED repurposing, single-factor document pairs, paired t-test, 250 queries/setting — PASS (quote + Table 1 caption: "Paired score differences … over 250 queries provide the paired t-statistics"; six analysis settings). Clause "5 偏差电池" — NARROW. The five single-factor settings are 4 biases (brevity, position, literal, repetition) + the answer-importance (answer's existence) factor; the paper's conclusion enumerates "literal, position, repetition, and brevity biases as well as the answer's importance". Calling all five biases miscounts the author's taxonomy. Smallest correction: "4 偏差（brevity/position/literal/repetition）+ 答案在场因素构成五个单因素设定，与 foil/poison 组合".
4. Findings [AUTHOR_FACT] — PASS. "<10%" quoted; "8 模型" verified in Table 4/A.1 (Contriever 0.4%, RetroMAE FT 0.4%, Contriever-MSMARCO 0.8%, Dragon-RoBERTa 0.8%, Dragon+ 1.2%, COCO-DR 2.4%, ColBERT v2 7.6%, ReasonIR-8B 8.0%); poison worse than no-document quoted + Table 5 (poison 30.8/32.0 vs no-doc 64.8/52.0), retriever preference for poisoned document 100% (Table A.9).
5. Limitations [CODEX_SYNTHESIS] — PASS, all five clauses verified: (a) pairwise scoring, top-k attack narrative is the authors' inference ("can potentially cause the model to select all top-k documents", §3.4); (b) GPT-4o generates the poison sentence, answers, and judges (§3.5 + footnote 10) — self-loop confirmed; (c) BM25 appears only as related-work mention, never as a control; (d) bge/gte/e5/nv-embed absent from all model lists; (e) Table 3 vs Table A.8 same-setting drift confirmed: +14.37 vs 14.32 and +16.62 vs 16.58 (≤0.05, direction unchanged).
6. Lineage / ledger / vocabulary — PASS (declining to cite end-to-end attack success is the correct hedge; ledger mechanically confirmed).

### failure-dense-retriever-surface-bias-collapse — REVISE

1. Mechanical integrity — PASS.
2. Observed failure [AUTHOR_FACT] #1 (<10%, minimum 0.4%, 8 models; foil carries biases without answer) — PASS (quote + Table 4 numbers verified; foil D1 = 2×head-repetition opening + head-not-tail sentence = repetition/position/brevity/literal composite, §3.4).
3. Observed failure [AUTHOR_FACT] #2 (preference exploitable; poisoned document makes RAG worse than no document; injects false facts) — PASS (verbatim quote + Table 5).
4. Conditions [AUTHOR_FACT] (Re-DocRED single-factor pairs, 250 queries/setting, paired t-test) — PASS.
5. Conditions [CODEX_SYNTHESIS] clause "ColBERT/ReasonIR 仅 foil 电池" — NARROW. Figure 1 (p.1, verified on the rendered page image) plots ColBERT (v2) across all five single-factor settings (its legend and polygon include ColBERT), so ColBERT is not foil-only; only ReasonIR-8B appears solely in the foil comparison (Table 4/A.1). Appendix A.1's sentence ("we evaluated ColBERT and ReasonIR-8B on the Foil dataset") is in tension with Figure 1 — a paper-internal inconsistency resolved by direct figure inspection. Smallest correction: "（微调五模型+Contriever 为主电池；ColBERT v2 另见 Fig.1 五设定与 foil；ReasonIR-8B 仅 foil 电池）". Remaining clauses (ACL 2025 published; single-vector focus per A.1; synthetic template queries, English single-evidence) — PASS.
6. Alternative explanations [CODEX_SYNTHESIS] — PASS (pairwise-not-top-k with author-inference status; GPT-4o self-produce-self-judge loop; four-condition ordering stable in Table 5 for both models; no BM25/reranker in the same battery, so dense-specificity unproven — exactly the invocation's required hedges, all present).
7. Warning [CODEX_SYNTHESIS] — PASS (bge/gte/e5/nv-embed untested in P093 confirmed; no reverse extrapolation).
8. Repair boundary [CODEX_HYPOTHESIS] — PASS (no-mitigation-experiments claim confirmed — the paper has no mitigation experiments).
9. Ledger / vocabulary — PASS.

### operator-paired-single-factor-bias-decomposition — REVISE

1. Mechanical integrity — PASS.
2. Before/after [AUTHOR_FACT] — PASS (relation→query templates, Table A.5; D1/D2 single-factor pairs with controlled filler sentences; five factors = answer presence/literal/length/position/repetition correctly enumerated with answer presence as a factor, not a bias; 250 queries/setting; paired differences + t-test).
3. Inputs/outputs [CODEX_SYNTHESIS] — PASS (paired t-statistics and preference rates; foil/poison composite batteries; offline, any scorer pluggable).
4. Mechanism [CODEX_HYPOTHESIS] — PASS.
5. Predicted signature [AUTHOR_FACT] clause "brevity/literal/position 最有害" — PASS (author-verbatim §3.4: "brevity bias, literal bias, and position bias are the most problematic"). Clause "（t 达 -21~-42）" — NARROW. That t-range belongs to the combined-bias foil-vs-evidence comparison (Table 4: −20.96 to −42.25), not to the individual brevity/literal/position settings (individual-setting t-statistics are on Figure 1's 0–20 scale; literal-bias values are positive, up to +22.04, Table 3). As placed, the parenthetical misattributes the foil-comparison statistics to the single-factor results. Smallest correction: "brevity/literal/position 最有害（Fig.1）；foil 叠加时 8 模型选含答案文档 <10%（配对 t −20.96~−42.25，Table 4）。" Clause "叠加时 <10% 崩塌" — PASS.
6. Preconditions/transfer [CODEX_SYNTHESIS] — PASS (self-contained evidence sentence with head+tail confirmed in quote; pairwise ≠ corpus-level retrieval; generation-bound conclusion).
7. Source lineage — PASS.
8. Ledger [AUTHOR_FACT] / vocabulary — PASS (mechanically confirmed).

## Summary table

| card_id | Verdict |
|---|---|
| paper-p090 | REVISE |
| failure-fixed-single-granularity-memory | PASS |
| operator-entropy-routed-multi-granularity-retrieval | REVISE |
| paper-p091 | PASS |
| failure-cosine-cannot-separate-contradiction-from-duplicate | REVISE |
| operator-deterministic-sro-supersession-ledger | PASS |
| paper-p092 | PASS |
| failure-answer-accuracy-without-conflict-recognition | REVISE |
| operator-support-evidence-whitebox-retrieval-metrics | REVISE |
| paper-p093 | REVISE |
| failure-dense-retriever-surface-bias-collapse | REVISE |
| operator-paired-single-factor-bias-decomposition | REVISE |

Atomic totals: 88 PASS, 11 NARROW, 0 REJECT (99 atomized claims). All REVISE verdicts stem from NARROW-level corrections; no fabricated numbers and no REJECT-level claims were found. Overstatement checks named in the invocation all passed in the risk direction: P090 gains are consistently hedged as pipeline-level (the two NARROWs err conservatively), P091 AUROC carries the single-embedder caveat, P092 CRS absolute values are hedged against the judging criteria, and P093 pairwise preference is nowhere presented as real top-k attack success nor as dense-specific without a BM25 caveat.

## Provenance

- Audit ID: w06-audit-a
- Start time (per invocation): 2026-07-27T02:35:00+08:00
- End time: 2026-07-27T02:49:35+08:00 (report finalized immediately after)
- Model/version: Claude (Fable 5), model id claude-fable-5, running as a fresh independent source auditor subagent (Claude Code / Claude Agent SDK)
- Thread/task ID: no orchestrator-issued thread ID was provided; session scratchpad ID a36cbd9b-9d67-4965-a961-933681b3881a
- Procedural blinding: intact. I did not read any reconciliation.md, any read_1.md, any read-2 report (no unresolved source ambiguity required one — the single paper-internal tension found, P093 Fig.1 vs Appendix A.1 on ColBERT coverage, was resolved by direct PDF figure inspection), any other Card audit or disposition, any calibration/blind queries, judgments, results, revealed regressions, or Candidate/Commissioning/Reviewer assets, and no Cards outside the twelve named.

Files read (complete list):
1. `knowledge_base/corpus/card_audits/w06-audit-a/invocation.md`
2. The twelve Cards under `knowledge_base/cards/`: `paper/paper-p090.md`, `failure/failure-fixed-single-granularity-memory.md`, `operator/operator-entropy-routed-multi-granularity-retrieval.md`, `paper/paper-p091.md`, `failure/failure-cosine-cannot-separate-contradiction-from-duplicate.md`, `operator/operator-deterministic-sro-supersession-ledger.md`, `paper/paper-p092.md`, `failure/failure-answer-accuracy-without-conflict-recognition.md`, `operator/operator-support-evidence-whitebox-retrieval-metrics.md`, `paper/paper-p093.md`, `failure/failure-dense-retriever-surface-bias-collapse.md`, `operator/operator-paired-single-factor-bias-decomposition.md`
3. `knowledge_base/corpus/evidence.json` — loaded programmatically; only the eleven P090–P093 evidence records were extracted and inspected
4. `knowledge_base/corpus/manifest.json` — loaded programmatically; only the four P090–P093 paper records were extracted and inspected
5. `knowledge_base/knowledge.w06_next.sqlite` — passages table queried only for the eleven cited passage_ids
6. The four PDFs (full text extracted locally with pymupdf; P091 pages 19–21 re-extracted for section placement; P093 page 1 rendered to PNG for Figure 1 inspection): `knowledge_base/papers/P090_memgas.pdf`, `P091_memstrata.pdf`, `P092_memconflict.pdf`, `P093_dense_retriever_collapse.pdf`

Not read: everything on the invocation's forbidden list (earlier Card audits/dispositions and other W06 audits; production calibration/blind queries, judgments, results, reports, revealed regressions; reconciliation and read_1 files; other Cards/reads; Candidate/Commissioning/CRL research Reviewer assets), and no read-2 reports.

Tool limits: PDF text extracted via pymupdf (layout artifacts in formulas were cross-checked against surrounding prose; Figure 1 of P093 required raster inspection since chart values are not text-extractable — model membership was verifiable, exact bar values were not needed). All work local; no network access used. The report SHA-256 is recorded in the audit's external return message (it cannot be embedded in the file it hashes).

- Mechanical result: 11/11 evidence quotes byte-identical to their sqlite passage slices; 11/11 passage text_sha256 recomputed and matched; 4/4 PDF SHA-256 matched across cards' source_refs, evidence fulltext_sha256, and manifest; 12/12 cards' evidence_ids resolve.
