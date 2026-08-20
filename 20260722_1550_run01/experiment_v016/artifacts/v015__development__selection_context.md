# v014 Selection Context

## Recovery boundary

- Run: `20260722_1550_run01`
- System state: `DEVELOPMENT_NOT_COMMISSIONED`
- Run state: `ACTIVE`
- Previous durable result: `experiment_v013/result.md`
- Previous result SHA-256: `DA6C5296CC823B78F079900A98883F17248C5CB95983002F730F7B9C9CEC7FBE`
- v014 began with no Candidate, implementation, Experiment Plan, Development capture, Confirmation bytes, Review Packet, Reviewer report, Decision, or Delivery.
- v014 does not retune the v013 BoR audit, TPPA, RCED, prompt controls, or any failed Development gate.

## Mandatory formal Card queries

The main Codex executed all three required entry queries before selecting v014. An initial command pointed at a nonexistent index and exited `1` before returning any Card; it was corrected to the formal `cards_fts.sqlite` index, after which all three queries exited `0`:

- Failure: `tool execution partial completion final success aggregate metric state transition failure localization`
- Operator: `counterfactual verification state transition trajectory evidence causal tool outcome`
- Paper: `public agent trajectory benchmark tool execution state verification errors logs`

Relevant formal Cards included:

- `failure-tool-use-metrics-collapse-distinct-errors`
- `failure-confident-completion-without-state-success`
- `operator-verified-single-branch-repair`
- `operator-terminal-state-reliability-evaluation`
- `paper-p039` (ToolFailBench)
- `paper-p037` (ToolSandbox)
- `paper-p074` (ToolGate)

The formal evidence supports two premises only: aggregate task success can hide distinct tool-use failure modes, and terminal success should be tied to verified state. It does not establish the specific ToolFailBench classifier-order defect or the performance of the v014 computation.

## Four-view open-network audit

On 2026-07-23, the main Codex searched and directly inspected four distinct views:

1. **Exact target and correction view** — ToolFailBench's paper, official repository, commit history, Issues, Pull Requests, and classifier source. The GitHub API returned zero Issues and zero Pull Requests. The remote repository's latest commit remained `c8be7fb0f1d295b1e116d7bd0e01d4c5e91f1653`; `evaluation/detect.py` has one originating commit and no later edit.
2. **Answer-equivalence view** — Bulian et al. (2022) and Kamalloo et al. (2023) directly establish that exact or token-level answer matching misses semantically equivalent answers and that regex or learned semantic matching can recover surface variants.
3. **Deterministic normalization view** — the fixed BFCL changelog records a 2024 evaluator change that removes whitespace and selected punctuation to make AST matching more robust.
4. **Grounding and attribution view** — ToolFailBench's own two judge prompts require evidence attribution against the tool return and allow formatting tolerance, while its deterministic classifier uses a global leaf-coverage threshold and keyword list.

No public source found in this bounded audit disclosed or repaired the exact deterministic combination used by v014: a `<30%` count over all mock-return leaves, two global structured-keyword hits, and a short-circuit to `output_fabrication` before the official required-answer contract is tested. This is a bounded search result, not proof that no private, future, or unindexed correction exists.

## Fixed target and nearest-prior bytes

| Source | Fixed identity | Local path | SHA-256 |
|---|---|---|---|
| ToolFailBench paper | arXiv:2607.04686v1 | `crl_agent_v3/knowledge_base/papers/P039_toolfailbench.pdf` | `6588AF66FD477D9764C20C52C2ADB7D92FCBF6A788FE09713BC71916862D3009` |
| Official ToolFailBench repository | commit `c8be7fb0f1d295b1e116d7bd0e01d4c5e91f1653` | `sources_v014/ToolFailBench/` | clean Git checkout |
| Official deterministic classifier | same commit | `sources_v014/ToolFailBench/evaluation/detect.py` | `AEE4D77596BDACB9025D85CCCDE766FF2A2DDBE1A291B6C143EA46D22863DBD0` |
| Shared judge rubric | same commit | `sources_v014/ToolFailBench/evaluation/judges/prompts/base_rubric.md` | `A07F89A088A1F822FCAB36C2370B9917598FE0353B2B4B92C327F513A7FA50E9` |
| Decision-tree judge overlay | same commit | `sources_v014/ToolFailBench/evaluation/judges/prompts/variant_a_decision_tree.md` | `F481AC6F12AA25F675DF582941F955167293CF3E0F4E07E4D364DDA75F872325` |
| Evidence-attribution judge overlay | same commit | `sources_v014/ToolFailBench/evaluation/judges/prompts/variant_b_evidence.md` | `15B3BD429C3A2E317A6DCC8B8E322B7AB8B0C0FC3C5E1631C9FFE69CE2319F63` |
| Tomayto, Tomahto | arXiv:2202.07654 | `sources_v014/Bulian_2022_answer_equivalence.pdf` | `BD320A5183A6FB507F4E3EBFBFF27EB76AF647E68F55980EA4C6762907F62B40` |
| Evaluating Open-Domain QA | ACL 2023 | `sources_v014/Kamalloo_2023_evaluating_open_domain_qa.pdf` | `61676B02AA277893A9AD9A4C9CF691A29ACE32A47E6FE3B024D598632D318BD2` |
| BFCL changelog | Gorilla commit `6ea57973c7a6097fd7c5915698c54c17c5b1b6c8` | `sources_v014/BFCL_CHANGELOG_6ea57973c7a6.md` | `27CBABDB95424B5B03B6B9B34EEBDF99A5C5B64FC5D2964726EF42ECBAC104DB` |

The main Codex directly read the target paper. Physical page 4 acknowledges that deterministic rules can miss faithful paraphrases. Physical page 6 states that exact rules are brittle and that two judges reduce surface-form brittleness. Appendix E's decision tree checks unsupported structured data before faithful tool use. These author disclosures preclude a broad v014 novelty claim about exact-match brittleness.

## Verified classifier-order failure

For tool-required rows, the official deterministic classifier executes:

```text
tool_skip
-> output_fabrication
-> result_ignore
-> correct
```

The fabrication branch:

1. extracts every leaf value from the full mock tool return;
2. counts exact case-insensitive substrings found in the answer;
3. if fewer than `30%` of all leaves appear and at least two strings from a global field-name list appear, returns `output_fabrication`.

This test does not identify an unsupported answer atom. It can fire when a concise answer reports every required value and only supported structured fields but omits unrelated leaves from a large return. Because it runs before the official `answer_must_contain`/`match_mode` contract, satisfying that contract cannot prevent the fabrication label.

## Development source, partition, and exposure

The public `SoHarshh/toolfailbench-traces` dataset was fixed at revision:

```text
77ef18dadfc1ad96ce29c863f0913d990659432a
```

Before trace content was read, top-level trace files were partitioned by:

```text
sha256(exact_top_level_trace_filename).digest()[0] % 3
Development: buckets 0 or 1
Confirmation: bucket 2
```

The frozen partition is `sources_v014/toolfailbench_partition.json`. Development contains 10 generator-model trace files, their 20 independent judge files, and 10 ensemble files. Confirmation contains 12 different generator-model trace files and remains unacquired and unread.

A foreground source-acquisition command timed out after 60 seconds during file transfer and produced no scientific output or manifest. A minimal resumable downloader then acquired only the preregistered Development files. The completed manifest is:

- path: `sources_v014/toolfailbench_development_manifest.json`
- SHA-256 before the partition flag update: `E5FC4A15DDC7F4B17E6CC04E9BC518FC53050BA11BC7B24BA026E703B161146E`
- entries: `40`
- hash or size mismatches on verification: `0`

All 10 Development traces and both judge outputs were read during selection. Development is therefore fully exposed candidate-development data, not untouched evidence. The judge ensemble files will not be used as reference labels because each ensemble includes the official rule itself.

## Baseline discrepancy audit

On the 10 exposed Development models:

- two judges unanimously agreed on `9,345` rows;
- the official deterministic rule matched that unanimous label on `8,687` rows;
- the two judges disagreed on `655` rows, which are excluded from primary evaluation;
- `160` unanimous rows were official `output_fabrication` but both judges `correct`;
- `157/160` of those rows already satisfied the official exact `answer_must_contain` contract;
- those 160 rows span all five domains: cybersecurity `32`, finance `14`, legal `72`, medical `39`, and real estate `3`;
- nine of ten Development generator models contain at least one such row; the exception is `deepseek-r1-distill-llama-8b`.

Other discrepancies, including `result_ignore -> correct`, are disclosed but are outside the selected computation because correcting general surface-form equivalence would collide with the target paper's own limitation statement and substantial prior work.

## Rejected routes

1. **General semantic answer equivalence** was rejected because Bulian et al., Kamalloo et al., SAS, and related work already occupy that contribution family.
2. **Broad numeric/date/string normalization** was rejected because deterministic benchmark normalization is established practice and BFCL has an explicit string-standardization precedent.
3. **Replacing rules with an LLM judge** was rejected because ToolFailBench already uses two LLM judges and reports their majority ensemble.
4. **Retuning the 30% threshold or keyword list** was rejected because that would be an exposed-data threshold search and would not isolate the precedence defect.
5. **Repairing all ToolFailBench rule/judge disagreements** was rejected because several disagreement classes involve tool-call semantics, judge interpretation, or CTRL-answer equivalence rather than the identified computation.

## Selected computation

The selected v014 computation is **Required-Grounding Precedence (RGP)**. It makes one change to the official deterministic tool-required classifier:

```text
tool_skip
-> exact official required-answer contract satisfied: correct
-> official output_fabrication test
-> result_ignore
```

CTRL logic, expected-tool detection, exact `answer_must_contain` values, `match_mode`, the 30% threshold, the global structured-keyword list, and all remaining labels are unchanged. RGP is deliberately not a semantic matcher and not a new judge.
