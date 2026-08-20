<!-- crl-v3-evidence-ids
["ev-p039-failure-core","ev-p039-aggregate-score-masking"]
-->
# Candidate v015 — Required-Grounding Precedence, execution-only continuation

## Candidate identity

v015 is the same scientific candidate as v014. The version increment exists only because the frozen v014 runner encoded Development-specific file counts and could not validly execute the already preregistered Confirmation manifest. No v014 Confirmation scientific output was produced.

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

No punctuation, Unicode, currency, unit, date, alias, or semantic normalization is permitted.

## Execution-only implementation change

The evaluator reads these frozen fields from `config.json`:

- phase and candidate identity;
- manifest SHA-256 and artifact filename prefix;
- expected total/trace/judge/ensemble file counts;
- expected rows, models, and domains;
- the fixed Confirmation gates.

Every scientific function, row definition, metric, transition, bootstrap seed, and resample count remains identical to v014. The independent auditor recomputes the metrics and phase gates from raw rows.

## Frozen comparator, reference, and inputs

- Comparator: official `evaluation/detect.py` at ToolFailBench commit `c8be7fb0f1d295b1e116d7bd0e01d4c5e91f1653`.
- Reference: rows where both released independent judges agree.
- Excluded: majority ensemble.
- Dataset revision: `77ef18dadfc1ad96ce29c863f0913d990659432a`.
- Confirmation manifest: SHA-256 `f1076a79a00810308a8ebc496ba8ef25d22873560daac6f4aabeb49a8011944`.
- Inputs: 12 traces, 24 judge files, zero ensembles, 36 files and 12,000 trace rows.
- Development overlap: zero paths.

The Confirmation files were not scientifically opened or parsed before this Candidate and its Evidence Packet were frozen.

## Inherited Development evidence

v014 Development passed all ten gates: paired accuracy delta `+0.016693418940609953`, bootstrap 95% lower bound `+0.010464272171620851`, 157 corrections versus one regression, positive effect on 9/10 models and 5/5 domains, and 157 supported transitions across all domains. The independent audit reported exact metric agreement. The main Codex authorized Confirmation.

The one regression is retained as a claim limitation rather than discarded.

## Mandatory Confirmation gates

1. exact input, join, baseline, and structural integrity;
2. paired accuracy delta at least `+0.005`;
3. model-cluster bootstrap 95% lower bound `> 0`;
4. corrections strictly exceed regressions;
5. positive delta on at least `9/12` models and `4/5` domains;
6. at least 100 supported `official output_fabrication -> RGP correct -> unanimous correct` transitions across at least four domains.

The main Codex, not a gate field or script exit code, decides whether the complete evidence can be sent to Review.

## Allowed claim

If and only if inherited Development, untouched Confirmation, three independent Reviewers, and the main-Codex evidence decision all pass:

> On the fixed released ToolFailBench traces, checking the unchanged required-answer contract before the coarse fabrication heuristic reduces deterministic false fabrication labels relative to two unanimous independent judges across multiple generator models and domains.

## Forbidden claims

RGP does not detect all fabrication, required values do not guarantee absence of extra unsupported claims, the judges are not human truth, no semantic-equivalence method was invented, and the result does not generalize beyond the frozen dataset, partitions, and judge pair. Automated PASS fields, voting, files, or fixtures cannot constitute Delivery.
