# Experiment Plan

```json
{
  "experiment_id": "v030",
  "candidate_sha256": "0c32820a453be37564888f69d4e829af12dfd9b73845ae76c64c4be0a503a2fc",
  "evidence_packet_sha256": "0c022e5bbf354681449f19fecf497572931d1c85068927b95bd9a1894a85385a"
}
```

## Codex Plan

# v030 Frozen RTCA Plan

Status: `FROZEN_BEFORE_DEVELOPMENT`.

This publish-once Plan authorizes one deterministic Development execution, one independent source-to-output replay and the Main Codex Development Promotion Audit. Only a positive written Promotion Audit may acquire the fixed untouched Confirmation sources. No gate count, script or file existence may authorize Confirmation, Review, Decision, Delivery or a system-state transition. No subagent is permitted before a complete formal Review Packet is frozen.

## Frozen identity

- Candidate `0c32820a453be37564888f69d4e829af12dfd9b73845ae76c64c4be0a503a2fc`; Evidence Packet `0c022e5bbf354681449f19fecf497572931d1c85068927b95bd9a1894a85385a`.
- Problem `83766bea1548e72787dc9072072cf639fc59ef877c57a8ca66eafbc37bf4592d`; Research Map `afc2129d3882d7d7e27f5409dcaedd393902a89c727e8e1a3e94114a021f69d0`; Selection Context `e413fe37551dd0b3f195887491698734b0d061ee7056cec19d8e42d4c6c3f3ff`; nearest prior `d178befec244dcd8f5a8db8778143569ed404e6b6a925e983e884dcd379ba680`.
- Program `e400d51e39ea886f82ec6bcc187b7923d4004a0a487204f98f036f2ff8b9c290`; independent auditor `695bbbeaab08fc9176832222608904c046fa11b6edf5db4ed65d47dc3de43f8d`; phase config builder `22a7e2bbb20f2ce91bd671bc93c1ece93a6c534ee8bab7d7ea6bf93488643baa`; conditional acquisition `7e3e699c9fdfe2b8a9b956f70b52e4871ffbd6d7b55299f8f78467abcc1bf25a`; tests `366b4ca9fd9f2ff95878bb645b9527407084dcfdfc339a753c8addefd112d6b6`; Development config `d09872217c94d11cea04c56282656e2a298ba885e724e6f85ad42ce99923e2a1`; runner `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`; Implementation Audit `7cf97a4dc38959c181b931f24ea3e164f3d12cc61d62179a332e4c1717803535`.
- Source manifest `45e30446bbe312c2acc1770f9ce0517c1d3aea1089f1d4162f2bfd3cf37850ed`; Artifact Manifest `208c67bee8c67eb0feafad232ca3fc26c7363f02cb549d6d0b5104daac9d931a`.

The Artifact Manifest binds 55 preexecution files totaling 10,187,718 bytes. Its `development_source/` contains exactly 31 config-bound metadata, patch-list, base-query and base-answer files. Rehash mismatch count is zero, head-data file count is zero and fixed Confirmation-content count is zero.

## Fixed computation and controls

For each entry in each pre-fix PR file, RTCA independently parses query text, recursive schemas and the embedded or joined reference calls, then counts six preregistered violation channels:

```text
4*schema_reference
+ 4*path_dependency
+ 4*unit_contract
+ 4*calendar_contract
+ 2*literal_provenance
+ 4*identity_integrity
```

Controls are `schema_only`, `dependency_only`, `temporal_unit_only`, `literal_only`, pre-fix `size_only` and `unweighted_union`. Ties use ascending SHA-256 of `pr_number || entry_id`. Changed IDs recovered from removed patch rows are labels only; no head value enters scoring.

The eight fixed Development pools contain 1,506 scored rows and 9 changed IDs. The computation is local single-process CPU work plus a fixed 20,000-resample PR-cluster bootstrap. It uses no LLM, model acquisition, generated judgment, fit, threshold search, retry or per-entry manual rule.

## One Development execution

Before execution, verify `captures`, `dev_output_001` and `dev_audit_output_001` are absent. Create only the empty `captures` directory.

Invoke the frozen `run_local_experiment.py` exactly once with:

- capture `experiment_v030/captures/dev_001`;
- cwd `experiment_v030/artifacts`;
- declared inputs: runner-independent program, config, Candidate, Evidence Packet, Source Manifest, Artifact Manifest and every lexically ordered file in `development_source/` (exactly 31);
- declared outputs: `experiment_v030/dev_output_001/raw.jsonl` and `summary.json`.

Exact payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v030\artifacts\program.py --config D:\Desktop\crl\20260722_1550_run01\experiment_v030\artifacts\config.json --source-root D:\Desktop\crl\20260722_1550_run01\experiment_v030\artifacts\development_source --output-dir D:\Desktop\crl\20260722_1550_run01\experiment_v030\dev_output_001
```

Preserve stdout, stderr, execution metadata and any declared outputs regardless of exit. On exit `0`, API-freeze all output/capture bytes before the independent audit.

## One independent Development audit

Invoke the frozen auditor exactly once through the runner with:

- capture `experiment_v030/captures/dev_audit_001`;
- cwd `experiment_v030/artifacts`;
- declared inputs: auditor, config, raw, summary, Source Manifest, Artifact Manifest and the same 31 source files;
- declared output: `experiment_v030/dev_audit_output_001/report.json`.

Exact payload:

```text
D:\Desktop\crl\crl_agent_v3\.venv\python.exe D:\Desktop\crl\20260722_1550_run01\experiment_v030\artifacts\audit.py --config D:\Desktop\crl\20260722_1550_run01\experiment_v030\artifacts\config.json --source-root D:\Desktop\crl\20260722_1550_run01\experiment_v030\artifacts\development_source --raw D:\Desktop\crl\20260722_1550_run01\experiment_v030\dev_output_001\raw.jsonl --summary D:\Desktop\crl\20260722_1550_run01\experiment_v030\dev_output_001\summary.json --report D:\Desktop\crl\20260722_1550_run01\experiment_v030\dev_audit_output_001\report.json
```

Support requires capture exit `0`, `AUDIT_OK`, 1,506 source-feature rows, 31 verified sources and zero channel, score, rank and metric error.

## Development gates and Main Codex audit

All Research Map gates are conjunctive: exact 8-PR/9-label/base-only integrity; Candidate MRR `>=0.60`; Recall@10 `>=8/9`; MRR at least `0.10` above the strongest frozen comparator; 20,000-resample bootstrap lower bound `>0`; top-10 hit in at least `6/8` PRs; nonidentity to every comparator; exact independent audit.

The Main Codex must personally read all raw rows, every changed entry, each channel/score/rank, the strongest comparator, per-PR reciprocal ranks and bootstrap. It must judge whether any apparent gain is a real typed cross-layer combination rather than exposed Development tailoring, size, one channel or tie ordering. Only a positive `promotion_audit_v030.md` authorizes Confirmation.

## Conditional untouched Confirmation

Only after a positive Promotion Audit may the frozen acquisition script run once for PRs `1084, 1085, 1086, 1087, 1175, 1177`. Freeze every metadata, patch-list and available base/head byte before reading. Then run the frozen builder once with `--phase confirmation`, freeze the resulting config, and run the same program once plus the same independent auditor once.

Confirmation gates are exact acquisition/base-only integrity; Recall@10 `>=0.60`; MRR `>=0.45`; MRR at least `0.05` above the strongest comparator; bootstrap lower `>0`; top-10 hit in at least `4/6` PRs; exact audit. The Main Codex must then perform a separate raw Confirmation Audit.

Only positive Development and Confirmation audits permit a formal frozen Review Packet. Only after that Packet is complete may exactly three simultaneous fresh `default`, `fork_turns=none`, direct leaf Reviewers start, each exact request containing `REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN`.

## Failure handling

Any nonzero scientific/capture execution, missing output, integrity/audit mismatch, failed gate or negative Main-Codex audit freezes v030 and advances the same Run to v031. No same-version retry, channel/weight/comparator/gate/Claim retuning, reduced pool, post-hoc subgroup Claim, early Reviewer, Delivery or Ready transition is allowed. Run remains `ACTIVE`; system remains `DEVELOPMENT_NOT_COMMISSIONED`.
