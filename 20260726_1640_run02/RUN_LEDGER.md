# RUN_LEDGER

- EVENT: RUN_CREATED
  AT: 2026-07-26T16:40:58+08:00
  MODE: COMMISSIONING
  VERSION: v001

- EVENT: CHARTER_COMPLETED
  AT: 2026-07-26T16:42:18+08:00
  VERSION: v001
  FACT: RUN_CHARTER.md completed with user intent and paid-API preauthorization
    keys (all NONE), which manage_run.py does not generate. Machine defect
    observation MD-01 recorded; preflight had passed with exit 0 on all three
    commands before Run creation.

- EVENT: PROBLEM_V001_WRITTEN
  AT: 2026-07-26T16:47:00+08:00
  VERSION: v001
  ARTIFACT: problem_v001.md
  SHA256: 2b25b5d22a4bb8176ad6787e1bcc2c2a29c9acd23c594323262d7b731ed426ff
  FACT: Problem, Use Thesis, Value Bridge and carrier-independent Mechanism
    Demand fixed before any carrier selection or outcome exposure, via
    ResearchWorkspace.

- EVENT: RESEARCH_MAP_V001_WRITTEN_ALL_KERNELS_KILLED_PRE_FREEZE
  AT: 2026-07-26T16:58:00+08:00
  VERSION: v001
  ARTIFACT: research_map_v001.md
  SHA256: 30eee5da5181e42a4761db882ab5746d45e27063f846ffaceb11e241d4833e2f
  FACT: Three formal card queries plus cross-cluster probe executed; four
    kernels formed via the generation channels; all four killed by cheap
    pre-freeze novelty probes (K1 full-pipeline collision with MemGAS
    arXiv:2505.19549, PDF read directly, local SHA 256eba2430611820eb4b1897
    8fdd35f05a3bcf26c7b808b03ef0971ab3bc49c8; K4 collision with
    arXiv:2605.24660; K2/K3 incumbent occupation). No dataset downloaded, no
    outcome read, no data role consumed. Problem/family RESET per Family
    Viability. Machine ambiguity MD-02 recorded (no defined versioning for
    pre-Candidate problem-level kills; handled as: v001 closed with frozen
    history, next problem enters v002).

- EVENT: STATUS_TO_BLOCKED_EXTERNAL
  AT: 2026-07-26T17:00:00+08:00
  VERSION: v001
  FACT: Next high-value step (problem reset into mechanism space requiring
    real LLM rollouts and self-generated fresh confirmation data) requires
    paid API; RUN_CHARTER preauthorization is NONE. Per the paid-API
    preauthorization protocol the Run stops before the first paid call.
    Local-only continuation remains possible at user's direction but the
    Main Codex judges its expected value low after two probe-killed
    kernels exhausted the strongest locally-executable routes.

- EVENT: V002_PROBLEM_AND_RESEARCH_MAP_WRITTEN
  AT: 2026-07-26T17:55:00+08:00
  VERSION: v002
  ARTIFACTS: problem_v002.md SHA256 b84f9092b6acd4d889c4e7838fb66d324b7f07c5971640325db0ebe114b12e4b;
    research_map_v002.md SHA256 b3fc0a44fd64f8261f1bf261adb0caeb714a1f96d79579678d9572029d197aa0
  FACT: v002 problem fixed carrier-independently (temporal semantics of
    similarity-association edges in propagation-based memory retrieval;
    staleness amplification failure + edge-local temporal repair). Three
    formal card queries executed; kernels K5 keep / K6 kill / K7 reframed
    to ablation; novelty probes recorded (Zep/Graphiti, MemStrata
    arXiv:2606.26511, MemGAS full text, A-Mem in-corpus). Probe-search
    rounds in v001/v002 killed five kernels pre-freeze before K5 survived.

- EVENT: DATA_SPLIT_COMMITMENT_V002_LONGMEMEVAL_S
  AT: 2026-07-26T18:05:00+08:00
  VERSION: v002
  ARTIFACT: data_split_commitment_v002/longmemeval_s_split.tsv.md
  SHA256: 00A30A73B532E1334EC4AA23976C53381DDB359E2BE995B72D83FBC30849F4E3
  FACT: LongMemEval-s downloaded (file SHA256 08d8dad4be43ee2049a22ff5674
    eb86725d0ce5ff434cde2627e5e8e7e117894); deterministic W/D/C split
    (sha256(question_id)[0] mod 5 -> 20/40/40) committed BEFORE any
    content, answer or annotation was read. Totals: W=93 D=222 C=185;
    knowledge-update W=14 D=37 C=27. CONFIRMATION_RESERVED bucket must
    stay unread until delivery; verification is re-running the rule.
  NEXT: workbench decisive falsifier on W bucket only (does symmetric
    propagation amplify stale versions vs direct retrieval).

- EVENT: V002_WORKBENCH_FALSIFIER_EXECUTED_K5_KILLED_V002_CLOSED
  AT: 2026-07-26T18:25:00+08:00
  VERSION: v002
  ARTIFACTS: research_map_v002.md updated SHA256 5860a855fe1dcd1a64da8ae1
    f99202b9febd702afe28d2e1e019247fc923890d; falsifier script/results
    preserved at data_split_commitment_v002/ (falsifier_k5.py SHA256
    E73E7947CEA87B68F9C5A4B3E8AF97C186049D27F67A5BCA7ABC34096F30EBAA,
    falsifier_k5_results.json SHA256 58B6242A60CC15011283B455CEC85742AB63
    181337D803F3E228EC24831A18E1)
  FACT: Preregistered kill condition met - symmetric PPR does not amplify
    stale versions vs direct retrieval (+0.07 stale@10, unstable
    direction, 14 W-bucket knowledge-update items). K5 killed at the
    cheapest stage; no candidate frozen, no D/C data touched. First-hand
    workbench observation recorded: stale version outranks current in
    9/14 items already in DIRECT retrieval (base-similarity staleness
    inversion). v002 closed per problem-level-kill semantics; next
    problem enters v003. W bucket now exposed workbench for this dataset.

- EVENT: V003_OPENED_PROBES_IN_PROGRESS
  AT: 2026-07-26T18:40:00+08:00
  VERSION: v003
  FACT: v003 candidate direction K8 = retrieval-layer temporal arbitration
    within near-duplicate unit pairs (schema-free, old units remain
    reachable, not global recency), seeded by the first-hand v002
    workbench observation (stale outranks current in 9/14 items in DIRECT
    retrieval). Probe status so far: MemStrata (2606.26511) argues
    similarity cannot separate contradiction from duplication (AUROC
    0.59) to justify structured supersession - but uniform temporal
    down-weighting inside the near-duplicate band does not require that
    separation (possible gap in their argument, must be tested);
    2606.01435 does deterministic max(timestamp) at ANSWER-ASSEMBLY level
    on synthetic serialized facts - not the retrieval ranking layer, but
    it is a mandatory closest-composition comparator for any K8
    experiment (large-k retrieval + assembly-recency vs K8 rank repair at
    small budgets / non-extractive downstream). K8 problem_v003 NOT yet
    written; remaining before candidate: problem_v003 via workspace,
    formal card queries, complete probe round, workbench falsifier on W
    bucket (does pair arbitration fix inversion without harming
    non-update queries - fully local).
  RECOVERY_NOTE: session context near limit; all state durable; resume
    from this ledger + RUN_STATUS NEXT_ACTION.

- EVENT: V006_PROMOTION_DEV_COMPLETE_ALL_KILLS_UNTRIGGERED_PACKET_FROZEN_REVIEW_STARTED
  AT: 2026-07-26T22:30:00+08:00
  VERSION: v006
  ARTIFACTS: problem_v006 77fede9c...; research_map_v006 final
    c9974091...; candidate_v006 3dcadcdb...; evidence_packet_v006 built;
    selection_context_v006 DE842979...; nearest_prior_v006 (private
    prior commitment) A5419590...; experiment_v006/plan.md 6ac36d2a...;
    artifacts config.json daf7c2e7... (max_tokens=1000; scripts
    unchanged from v005); capture dev_reader_001 exit 0 (111/111 rows,
    0 empty); result_v006 de2b4dda...
  FACT: Corrected reader arm complete. Auto-scores 21/24/22 of 37;
    manual review per plan (all changed verdicts itemized in result)
    -> turn 30/37, sentence 34/37, oracle 32/37. Kill 3 NOT triggered:
    turn arm deficit exists and its unique errors are five confident
    STALE answers, removed by sentence-level retrieval. All three
    preregistered kills now resolved untriggered. Promotion Audit
    post-answers and Seed Readiness Audit appended to map. Review
    Packet frozen: review_v006/packet.md SHA 2fe7fcebf4395b53a37cd1ff51
    4d53df743f0e76a9f75643368c22921acaa5cd, 52 supplemental files;
    snapshots copied (protocol D1DC1D60..., roles 6261EEAB...,
    C9A40143..., 90DC36C2...); private prior committed A5419590...,
    body excluded from packet. Three fresh leaf reviewers launched
    simultaneously (Prior/Skeptic/Potential), fresh contexts, peer
    reports invisible, delegation forbidden. No report has been saved
    yet; save-report only after all three return, per protocol.
  API_USAGE_CUMULATIVE: 247,408 in / 24,663 out tokens (~<1 USD).

- EVENT: RUN_DELIVERED
  AT: 2026-07-27T01:15:00+08:00
  VERSION: v007
  ARTIFACTS: reviewer_1.md c85a1af3079e0e1fb09e2578d1ee6611765ba8b6fdf2
    18533d6d2a25cc6a9d6d (Prior: no collision, 7 fresh queries + 11 new
    documents incl. June-July 2026 sweep; neighbor characterizations
    verified accurate); reviewer_2.md c26a045458cebb2c2de4ec1d46333727
    fab281eef5e9bb9170f9f85126941559 (Skeptic: byte-identical judge
    reproduction; C gates verified severe - false-pass 2.6%, power 17%
    at own point estimate; three text residuals); reviewer_3.md
    02b7ec3bc5e9ba0f14ff4de1d736aa156e6e3da8feec52997a7bd5cbb680d181
    (Potential: deliver at measurement-paper-skeleton grade; judge
    reproduced byte-identically; precedent boundary answered YES on
    three byte-verifiable grounds); decision_v007.md e6ec3f718646e820
    6563093094eb2eee3f445d7034841b7de787b85a017c8cd9 =
    DELIVER_IMPLEMENT with binding errata E1-E10 (the record-repair
    path all three reviewers explicitly endorsed); DELIVERY.md
    0e1d17dcecbf2786464c13b6d5432c5b87826905138bf72519ddb3038f8ff6fb.
  FACT: Run02 reaches the sole success terminal. Delivered: stale-bias
    measurement harness + decomposition findings at the corrected
    claim ceiling + reserved C bucket (185 q, untouched, commit-reveal
    verifiable) with severe preregistered gates + cost-ordered
    falsifiable scale-up roadmap. Two full review rounds, six fresh
    leaf reviewers, all manifest SHAs verified by every reviewer, all
    numbers independently recomputed. MACHINE OBSERVATION MD-12
    recorded: the saved copies of the three v007 reports compress
    Section-1 readbacks (disclosed inside each file and in
    decision_v007) - the reviewer-returns-text-only protocol conflicts
    with verbatim-preservation under long reports; recommend allowing
    reviewers to write their report to a designated scratch path for
    mechanical copying. C bucket remains unread by the machine.

- EVENT: V007_REPAIR_EXECUTED_PACKET_FROZEN_REVIEW_STARTED
  AT: 2026-07-27T00:45:00+08:00
  VERSION: v007
  ARTIFACTS: problem_v007 f52b776eb17456a73c4abf05e5e7f3361b4c3486051e
    69516e0fec0d8f40196a (corrected claim ceiling + severe C gates);
    research_map_v007 97e12e96d7999702a59287dbe1444c151f846f384e6c14ac
    7b72a1ff6987d534 (named neighbors, retraction of item-level
    conversion sentence); candidate_v007 eba1d5c72c2fe852d89d087db340e
    e06baf184d102d5fb225f7743f952626466; evidence_packet_v007 built;
    selection_context_v007, nearest_prior_v007 (commitment SHA
    38C0853ED07611DDFB525341E57CEB13FA1E8BE700E7EDFFA804437916C780BC);
    implementation_v007/judge.py frozen; workbench_v007/verdict_table_
    v006_reader.jsonl (reproduces 29/34/32 deterministically);
    review_v007/packet.md SHA cce10f04e517653a5c2194a7fddd54a7f457109a
    d9c78a2f94da0e6ae88217e1 (65 supplemental files incl. the complete
    v006 review record as data).
  FACT: All six decision_v006 repair points executed; no new
    experiment, no new data exposure; C bucket still unread. Three
    fresh leaf reviewers launched simultaneously for v007 with repair-
    audit focus. Tool friction noted: freeze-packet rejects paths
    inside review dirs (prior review copied to implementation_v007/
    prior_review_v006/) and pre-created snapshot dirs (moved aside and
    restored) - mechanical guard behavior, not defects.

- EVENT: V006_THREE_REVIEWS_RETURNED_DECISION_REVISE_AS_NEW_VERSION
  AT: 2026-07-26T23:59:00+08:00
  VERSION: v006
  ARTIFACTS: reviewer_1.md SHA fb4ac733bb9cfc8be5b9a258b81d1d70b18281f5
    5b05bd4fdee8f86674d2ab4c (Prior/Lineage: no fatal collision, 11
    query families, 10 documents; requires named neighbors MemConflict
    2605.20926 / Collapse of Dense Retrievers 2503.05037 / MAB
    FactConsolidation); reviewer_2.md SHA b707d54b6eab9bad3d6e812275c76
    f9972719ad9551b4075814d69954abaaaf0 (Skeptic: three claim-text
    fatal objections F1 consequence-not-quantified, F2 item-level
    conversion contradicted by frozen raw, F3 chance bar; all verified);
    reviewer_3.md SHA 8c0e13b9a47812d91f6e9cc0d917d5727a781453bff7a88c
    77e5f09c7255d598 (Potential: proceed-conditional; re-adjudicated
    all 111 rows: 29/34/32); decision_v006.md SHA 3442b769f615d85c85e2
    18e128634cda6d3cc0755b66ca59354f59904eccf43b.
  FACT: All three reviewers verified all 55 manifest SHAs with zero
    mismatch and reproduced every headline number from frozen bytes.
    Two reviewers independently found the same manual-scoring error
    (031748ae_abs turn arm; 30/37 -> 29/37, conservative direction).
    Main Codex independently verified F2 against development_raw
    before deciding. Decision: REVISE_AS_NEW_VERSION - execution
    record sound, claim text over-strong; v007 = record-and-claim
    repair (no kernel change, no new experiment), then refreeze and
    fresh re-review. DELIVERY forbidden for v006. Run ACTIVE.

- EVENT: V005_PROMOTION_DEV_EXECUTED_RETRIEVAL_VALID_READER_CONFIG_DEFECT
  AT: 2026-07-26T21:30:00+08:00
  VERSION: v005
  ARTIFACTS: problem_v005 3ffc013a...; research_map_v005 db970e14...;
    candidate_v005 aa99d8c6...; evidence_packet_v005 built;
    selection_context_v005, nearest_prior_v005 written;
    experiment_v005/plan.md a8ca5e0d... (frozen);
    artifacts measure_decomposition.py c171a710... reader_arm.py
    dbbd3233... config.json 15a49c24...; captures dev_local_001 and
    dev_reader_001 (both exit 0); result b72a09f1...
  FACT: D bucket opened for the first time by the frozen harness.
    RETRIEVAL DECOMPOSITION REPLICATED on fresh data: inversion 22/37
    (59.5%) turn/direct; sentence 16/37 with margin -0.049->-0.020;
    ppr ~= direct (propagation ~0); recency 6/37 but non-update hits
    6.52->5.91. Kills 1,2 NOT triggered. READER ARM INVALIDATED:
    deepseek-v4-flash is a reasoning model; max_tokens=100 consumed by
    reasoning_tokens in 47/111 rows (empty answers, arm-varying 19/18/10
    = confound). Per attempt discipline config change -> v006. Kill 3
    UNDECIDED. Usage: 123,704 in / 10,167 out tokens (<1 USD). MD-11
    recorded (smoke must include near-real-scale payload shape).
  V006_PLAN: inherit v005 docs by reference; corrected reader config
    (max_tokens 1000); rerun reader arm only; then manual-review
    scoring, promotion audit, seed readiness audit, packet freeze,
    three reviewers, decision.

- EVENT: V004_FIVE_EXPERIMENT_MECHANISM_MAP_COMPLETED_V004_CLOSED
  AT: 2026-07-26T20:15:00+08:00
  VERSION: v004
  ARTIFACTS: problem_v004.md SHA256 0bd83b39c2e13c7a26695bb220bc5e03ba2f6c
    48a9700b8f3690fa7428bedb21 (contains PROCESS DEVIATION DISCLOSURE);
    research_map_v004.md SHA256 518b89f5a0d9cc99d6c1fd7d077f5a7d296300e8e3
    2b3704f42f4ec4d57e6c12; workbench_v004/ six files (falsifier_k11.py
    3E6F0B75..., falsifier_k11_results.json 1B815961...,
    verify_ellipsis_hypothesis.py DBCA575A..., ellipsis_hypothesis_
    results.json FDEFA0D8..., verify_dilution_sentence_level.py
    D18A3528..., dilution_sentence_results.json 3C9278A8...).
  FACT: K11 killed by preregistered condition (a): repaired 1/9
    inversions; 10/14 items have competitive-band size 1 - current is
    out of band entirely. Ellipsis hypothesis refuted in length form
    (current units LONGER, 761 vs 264 chars); mechanism is dilution.
    Sentence-level check: inversions 9->7, margin -0.064->+0.011 -
    dilution secondary, phrasing isomorphism dominant. Stale-bias causal
    decomposition complete: isomorphism (dominant) + dilution
    (secondary) + propagation (zero). Retrieval-layer repair family
    CLOSED by mechanism evidence. MD-10 recorded and repaired (CRL.md
    workbench ordering rule): K11 falsifier ran before problem_v004 was
    frozen - deviation disclosed in problem_v004.
  V005_PLAN: attribution-study candidate - preregistered D-bucket
    replication of the decomposition + deepseek reader arm quantifying
    answer-level consequences at equal budget; then audits, packet,
    three reviewers, decision; C bucket stays reserved for delivery.
    This intentionally tests the v007-precedent boundary (measurement
    contribution with a real Use Thesis) through the full chain.

- EVENT: V003_WRITTEN_FALSIFIER_EXECUTED_K8_KILLED_V003_CLOSED
  AT: 2026-07-26T19:30:00+08:00
  VERSION: v003
  ARTIFACTS: problem_v003.md SHA256 6dcef1c777385e4928a84f277dcb5e468f097c
    2f0e9407fe53f857676e1fbfe0 (first use of the occupancy-scan section);
    research_map_v003.md final SHA256 32ed0185957d9dbdbbc461cd93f20ac5c2b
    423f023ec06c9b99bcedc3abe9202; workbench_v003/falsifier_k8.py SHA256
    645FB6EF2482AC11... and falsifier_k8_results.json SHA256
    60304C7771FF24C6... (first use of the workbench_vNNN slot).
  FACT: v003 card queries run; K8 (near-dup pairwise temporal arbitration
    at scoring) killed by preregistered falsifier condition (a): repaired
    1/9 inversions only. Mechanism localized first-hand: update pairs are
    not embedding near-duplicates (0.6-0.75 band, overlapping ordinary
    related pairs) - detection, not arbitration, is the binding
    constraint; global recency comparator repairs 7/9 but harms 29/79
    non-update items, confirming the preregistered trade-off prediction.
    Four coherent workbench-grade negative results accumulated (see map);
    not reflux-eligible until fresh-data verification. v003 closed;
    Problem/family reset required for v004. D/C buckets remain unread.

- EVENT: MACHINE_REPAIRS_MD06_TO_MD09_AND_PHYSICAL_BUCKET_SEPARATION
  AT: 2026-07-26T19:00:00+08:00
  VERSION: v003
  FACT: User-approved machine repairs completed outside the Run: MD-07
    workbench_vNNN/ slot defined in CRL.md section 5; MD-08 physical
    bucket separation now required alongside commit-reveal (CRL.md and
    templates); MD-09 occupancy scan before problem commitment added to
    CRL.md section 5 and problem template; MD-06 generation channels 5
    (incumbent-limitation analysis) and 6 (first-hand workbench failure)
    added with hot-zone warning. Applied to this Run: the committed
    LongMemEval-s split was physically separated into three standalone
    files under data_split_commitment_v002/ per the committed rule,
    mechanically, no content read: WORKBENCH 93 items SHA256 efa7bed14777
    14232c2562365bf3b746ff42515e3b49b912d52a04f37fd6971c; PROMOTION_
    DEVELOPMENT 222 items SHA256 25cc9c2b6be241fb0caa2689bf621bf9111c1a9d
    297f516d1c382a48022d8112; CONFIRMATION_RESERVED 185 items SHA256
    28a5710998a999bf464fa7c97585740af3a89b7816c3292e3c5c93d08a50b2ba.
    From now on main-flow code loads only the W or D files; the C file
    must not be opened before delivery. v002 falsifier artifacts remain
    at their ledger-recorded paths (not moved); workbench_v003/ applies
    from v003 onward.

- EVENT: MACHINE_REPAIRS_DURING_BLOCK_AND_UNBLOCK_TO_ACTIVE_V002
  AT: 2026-07-26T17:20:00+08:00
  VERSION: v002
  FACT: User approved machine repairs for run02-exposed defects, granted
    deepseek paid-API preauthorization (budget: user-unlimited, spend
    judiciously), and directed continuation. Repairs completed outside the
    Run: MD-01 manage_run.py charter template now emits PAID_API_* keys
    (test updated, 29 passed); MD-02 pre-Candidate problem-level kill
    versioning semantics added to CRL.md section 6. RUN_CHARTER paid-API
    boundary updated (no key stored anywhere). External blocking condition
    resolved; STATUS back to ACTIVE; CURRENT_VERSION advanced to v002 per
    the new problem-level-kill semantics. v001 files remain frozen.
