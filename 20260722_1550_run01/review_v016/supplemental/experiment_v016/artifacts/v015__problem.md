# Problem v015 — Execute the frozen Required-Grounding Precedence confirmation without changing its science

## Research question

On the untouched ToolFailBench generator-model partition, does moving the unchanged official required-answer test ahead of the unchanged coarse output-fabrication heuristic reduce deterministic false `output_fabrication` labels relative to two independent unanimous judges, across models and domains?

## Frozen computation

For a tool-required trace, let `T` indicate that the expected tool was executed, `G` that the official exact `answer_must_contain`/`match_mode` contract is satisfied, and `F` the official output-fabrication predicate. Required-Grounding Precedence remains:

```text
if not T: tool_skip
elif G: correct
elif F: output_fabrication
else: result_ignore
```

CTRL rows retain the official CTRL classifier. Released external pipeline labels are passed through unchanged. No predicate, normalization, matching rule, label, sample, or metric is changed from v014.

## Execution defect being repaired

The v014 runner tied valid inputs to Development-specific cardinalities even though its scientific computation was already phase independent. It therefore could not execute the preregistered 36-file Confirmation contract without violating frozen bytes. v015 changes only that input contract: manifest identity, artifact prefix, expected file counts, and phase-specific gates become explicit frozen config values.

This defect produced no Confirmation scientific output and offers no basis for selecting a favorable result.

## Evaluation unit and evidence

- Unit: one released ToolFailBench trace row joined to both released independent judge rows by `(model_id, task_id)`.
- Comparator: fixed official `evaluation/detect.py` at ToolFailBench commit `c8be7fb0f1d295b1e116d7bd0e01d4c5e91f1653`.
- Reference: only rows where the two judges agree on the failure-mode label.
- Confirmation: 12 generator models in the frozen bucket-2 partition, 12,000 traces before unanimity filtering, five domains.
- Excluded: the released majority ensemble, because it contains the official rule.

## Falsifiable Confirmation target

All gates are conjunctive:

1. exact 36-file manifest integrity, 12 traces, 24 judges, zero ensembles, and no Development path overlap;
2. complete unique joins, exact official baseline identity, and structural invariance;
3. paired unanimous-reference accuracy delta at least `+0.005`;
4. 20,000-resample model-cluster bootstrap 95% lower bound `> 0`;
5. corrections strictly exceed regressions;
6. positive delta on at least `9/12` models and `4/5` domains;
7. at least 100 supported `official output_fabrication -> RGP correct -> unanimous correct` transitions across at least four domains.

## Claim boundary

If Confirmation, three independent Reviewers, and the main-Codex evidence decision pass, the strongest allowed claim is:

> On the fixed released ToolFailBench traces, checking the benchmark's unchanged required-answer contract before its coarse fabrication heuristic reduces deterministic false fabrication labels relative to two unanimous independent judges across multiple generator models and domains.

This does not make the judges human gold, prove that required values exclude every extra fabrication, introduce semantic equivalence, validate every taxonomy label, or establish generalization outside the fixed dataset and judge pair.
