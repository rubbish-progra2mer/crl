<!-- crl-v3-evidence-ids
["ev-p039-failure-core","ev-p039-aggregate-score-masking"]
-->
# Candidate v014 — Required-Grounding Precedence

## Minimal implement

1. Load and verify the frozen trace and two-judge files from a manifest.
2. Import the fixed official classifier and verify exact identity with every released classifier-supported label; preserve and report released external pipeline labels such as `other_error` without reinterpretation.
3. Preserve all CTRL logic and expected-tool detection.
4. For tool-required rows whose expected tool was executed, evaluate the unchanged official exact `answer_must_contain`/`match_mode` contract before the unchanged official output-fabrication predicate.
5. Emit one row per `(generator_model, task_id)` with official label, RGP label, both judge labels, unanimity, domain, tool-required status, expected-tool-called status, required-contract status, and label transition.
6. Compute paired accuracy, macro-F1, per-model and per-domain deltas, corrections, regressions, transition matrices, and the frozen model-cluster bootstrap.
7. Recompute every metric from raw rows in an independent entry point.

There are no learned parameters and no tunable thresholds.

## Exact RGP computation

```text
if task is CTRL:
    use official CTRL classifier unchanged
elif released label is an external pipeline error:
    preserve the released label unchanged
elif expected tool was not executed:
    tool_skip
elif official exact required-answer contract is satisfied:
    correct
elif official output-fabrication predicate is true:
    output_fabrication
else:
    result_ignore
```

The selected computation does not normalize punctuation, Unicode, currency, units, dates, aliases, or semantic paraphrases.

## Fair comparator and reference

- **Primary comparator:** fixed official `evaluation/detect.py` at commit `c8be7fb0f1d295b1e116d7bd0e01d4c5e91f1653`.
- **Evaluation reference:** only rows where both released independent LLM judges agree on the failure-mode label.
- **Excluded reference:** released majority ensemble, because it contains the official rule.
- **Rows:** official and RGP predictions receive identical trace bytes, task metadata, joins, and reference labels.

## Development data and exposure

- Dataset: `SoHarshh/toolfailbench-traces`
- Revision: `77ef18dadfc1ad96ce29c863f0913d990659432a`
- Frozen partition: `sources_v014/toolfailbench_partition.json`
- Development manifest: `sources_v014/toolfailbench_development_manifest.json`
- Development files: 10 traces + 20 judge files + 10 unused ensemble files
- Rows: 10,000 traces before unanimity filtering

All Development trace and judge contents were inspected during selection. The experiment is an exposed Development test and must not be described as confirmation.

## Development gates

The ten gates in `research_map_v014.md` are mandatory and conjunctive. In summary:

1. exact input bytes and 10-by-2 judge coverage;
2. complete unique joins;
3. exact reproduction of every classifier-supported release label plus explicit unchanged passthrough of any external-error row;
4. no changes to CTRL, external-error, or expected-tool-not-executed rows;
5. unanimous-reference accuracy delta at least `+0.01`;
6. 20,000-resample model-cluster bootstrap lower bound above zero;
7. corrections at least twice regressions;
8. positive delta on at least 8/10 models;
9. positive delta in at least 4/5 domains;
10. at least 100 supported OF-to-correct transitions across at least four domains.

The main Codex, not the experiment program, decides promotion after reading raw rows, sampled transitions, and the independent audit.

## Untouched Confirmation

Only after a positive Development Promotion Audit:

- acquire the 12 frozen Confirmation trace files and their 24 two-judge files from the same fixed dataset revision;
- do not acquire ensemble files;
- prove no acquired path overlaps the Development manifest;
- apply the frozen RGP code, joins, metrics, bootstrap seed, and resample count without modification.

The seven Confirmation gates in `research_map_v014.md` are mandatory. No threshold, normalization, label mapping, judge subset, model subset, domain subset, or fallback dataset may change after Confirmation acquisition.

## Allowed claim

If and only if Development, untouched Confirmation, three independent Reviewers, and the main-Codex evidence decision all pass:

> On the fixed released ToolFailBench traces, checking the unchanged required-answer contract before the coarse fabrication heuristic reduces deterministic false fabrication labels relative to two unanimous independent judges across multiple generator models and domains.

## Forbidden claims

- RGP detects all output fabrication.
- Required values in an answer guarantee that no extra unsupported claim exists.
- The LLM judges are human truth.
- A general semantic-equivalence or normalization method was invented.
- ToolFailBench's complete taxonomy or all published rankings are invalid.
- The result generalizes beyond the frozen dataset, generator-model partitions, and judge pair.
- File existence, an automated PASS field, Reviewer voting, or fixture sanity constitutes Delivery.
