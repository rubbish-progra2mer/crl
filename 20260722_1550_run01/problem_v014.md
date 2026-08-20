# Problem v014 — Can a coarse fabrication heuristic override satisfied required evidence?

## Research question

In ToolFailBench's deterministic classifier, does running a coarse output-fabrication heuristic before the benchmark's own required-answer contract cause systematic false `output_fabrication` labels? Does moving the unchanged required-evidence test ahead of that heuristic improve agreement with two independent unanimous judges across generator models and domains, and does the effect persist on untouched generator-model traces?

## Formal distinction

For a tool-required trace, let:

- `T` indicate that the expected tool was executed;
- `G` indicate that the official `answer_must_contain` values satisfy the official `match_mode` by exact case-insensitive substring matching;
- `F` be the official output-fabrication heuristic;
- `R` be the official result-ignore test.

The released deterministic order is:

```text
if not T: tool_skip
elif F: output_fabrication
elif R: result_ignore
else: correct
```

Because `R == not G` after a valid tool call, the selected computation is:

```text
if not T: tool_skip
elif G: correct
elif F: output_fabrication
else: result_ignore
```

No predicate is retuned or learned. Only the precedence of `G` and `F` changes.

## Why the distinction matters

The official fabrication heuristic does not find an answer claim that is unsupported by the tool return. It counts how many leaves from the entire mock return are repeated and checks whether two global structured-keyword strings appear. Concise grounded answers can report all benchmark-required evidence while omitting most nonrequired leaves. Under the released order, those answers can be labeled fabrication before their required evidence is tested.

If this occurs systematically, the deterministic component inflates a diagnostically important failure mode and creates avoidable dependence on the two expensive LLM judges. If it does not occur or moving the predicate creates comparable regressions, v014 fails.

## Evaluation unit and scope

- Unit: one released ToolFailBench trace row with its released official rule label and two released independent judge labels.
- Development: 10 generator models selected by the frozen filename-hash partition; all Development content is exposed.
- Confirmation: 12 different generator models in the frozen bucket-2 partition; content remains unacquired and unread until promotion.
- Reference subset: rows where the two released judges independently give the same failure-mode label.
- Primary comparator: the released deterministic classifier on exactly the same rows.
- Primary metric: paired classification accuracy against the unanimous two-judge label.
- Secondary metrics: macro-F1, per-model accuracy delta, per-domain accuracy delta, corrections, regressions, and label-transition counts.

The released majority-vote ensemble is excluded because it includes the official rule and would leak the comparator into the reference.

## Falsifiable target

Development must show all of the following before Confirmation can be opened:

1. exact reproduction of every classifier-supported released label, with any external pipeline-error label explicitly counted and passed through unchanged;
2. no change to CTRL rows or rows whose expected tool was not executed;
3. positive paired accuracy improvement of at least `0.01` on unanimous-judge rows;
4. a model-cluster bootstrap 95% interval whose lower bound is above zero;
5. more corrections than regressions by at least `2:1`;
6. positive accuracy delta on at least `8/10` generator models;
7. positive accuracy delta in at least `4/5` domains;
8. at least `100` corrected `official output_fabrication -> unanimous correct` rows, spanning at least four domains.

Failure of any gate closes v014 without acquiring Confirmation.

## Claim boundary

If Development, untouched Confirmation, three independent Reviewers, and the main-Codex evidence decision all pass, the strongest allowed claim is:

> On the fixed released ToolFailBench traces, checking the benchmark's unchanged required-answer contract before its coarse fabrication heuristic reduces deterministic false fabrication labels relative to two unanimous independent judges across multiple generator models and domains.

The claim does not establish that the judges are human gold labels, that required-field satisfaction rules out every possible extra fabrication, that RGP is a general semantic-equivalence metric, or that published majority-ensemble leaderboard values materially change.
