# Main-Codex Promotion Audit v020

Disposition: `NO_GO_FOR_CONFIRMATION_COMPARATOR_INCOMPLETE`

System remains `DEVELOPMENT_NOT_COMMISSIONED`; Run remains `ACTIVE`. This judgment is not an automated gate result.

## Execution integrity

- Development execution: exit `0`, 132.4257076 seconds, SHA-256 `8D25D4F07CA60944FC5C17D9D4C13F3250ACA886B22B49A2CA3C3DA385E62088`.
- Development raw predictions: 352 rows, SHA-256 `B7437213E300AD2A2EB9A07E9B6A8C6213E16C123BF8BFE450D0D67C70CFB081`.
- Summary SHA-256 `54802B4D015693CE333F86953B07B0EDC5B9105FD17DF3A91EB10581050E3191`.
- Frozen model SHA-256 `4FA248B56D9F013711CCFCF3F21EB6F967C0EC9961EF5A148E40F0A246F07293`.
- Independent audit: exit `0`, `AUDIT_OK`, zero errors, 94 references, 352 evaluated rows, five models, 1,760 replayed scores, maximum score error `0`, maximum metric error `0`.
- Audit report SHA-256 `CD4BCC1D2CA46D582BF544F3805BFD0E28D95E7A4FAFC595B0701BD256C0DC51`.
- Reference/evaluated overlap and task split violations: zero.

## Real positive result

| Method | AUC | TPR@5%FPR | Frozen FPR | Frozen TPR | Dimensions |
|---|---:|---:|---:|---:|---:|
| text | 0.900280 | 0.547511 | 0.045802 | 0.538462 | 30,000 |
| reference concat | 0.903043 | 0.561086 | 0.061069 | 0.565611 | 60,000 |
| absolute delta | 0.922317 | 0.683258 | 0.045802 | 0.638009 | 60,000 |
| v012 RCED | 0.826189 | 0.031674 | 0.145038 | 0.651584 | 30,029 |
| signed residual Candidate | 0.940866 | 0.778281 | 0.030534 | 0.687783 | 90,000 |

The strongest listed comparator was absolute delta. Candidate AUC delta was `+0.0185486`; 2,000-resample task-cluster bootstrap 95% interval `[+0.0081269,+0.0259549]`. All seven preregistered gates were true.

At the independently selected validation thresholds, Candidate was correct where absolute delta was wrong on 14 rows, while absolute delta was uniquely correct on one row. AUC was equal for Claude Opus 4.6 and higher for Candidate on Gemini 3.1 Pro and GPT-5.4. Frozen-threshold positive recall was non-decreasing across every released exploit-category slice and materially higher for constraint loopholes, keyword gaming, metric spoofing, mutable-input tampering, hollow implementations, and structural extraction.

Main-Codex case readback found the gains include both recovered clean trajectories and detected exploits. Examples include avoiding false positives on legitimate diagnostic workflows in task 352, and detecting reference-novel verifier inspection, expected-hash copying, hollow MCTS implementation, and mutable input writes. The only strongest-only correct threshold case was an output-spoofing font task. These facts support the task-relative signal and are not explained by reference leakage.

## Fatal comparator objection discovered before Confirmation

The Candidate representation has three 30,000-dimensional blocks: `[x, novel, missing]`. The strongest unsigned comparator has two: `[x, abs]`. Splitting `abs` into `novel` and `missing` is the intended method, but it also changes the number of independently regularized coefficient blocks from 60,000 to 90,000 dimensions.

With L2-regularized logistic regression, duplicated or split feature channels can change the effective penalty even when no new information is added. The current experiment omitted two direct controls:

- `[x, abs, abs]`, which matches Candidate dimensionality and residual duplication without direction;
- `[x, x, x]`, which matches three-block capacity without reference-difference information.

Therefore v020 cannot attribute its gain specifically to signed task-relative direction rather than a capacity/regularization change. This is a closest-composition fairness defect under the CRL protocol. The strong result is real but scientifically insufficient to expose the untouched Confirmation.

## Required v021 continuation

v020 is frozen without Confirmation or Reviewers. v021 may change only the comparator set, raw output schema, strongest-comparator choice, and unavoidable version/hash bindings needed to add the two frozen capacity controls. It must preserve:

- Candidate feature map and learner;
- dataset, reference rule, all task splits, vocabulary fit, labels, C, seed, thresholds, bootstrap, and gates;
- all four existing comparators;
- untouched bucket-3 Confirmation.

v021 must rerun the complete same-budget Development once because the new controls require fitted coefficients. Candidate must beat the enlarged strongest comparator under the unchanged gates. No same-version retry or post-result threshold change is allowed.
