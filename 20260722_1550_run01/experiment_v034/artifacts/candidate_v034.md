<!-- crl-v3-evidence-ids
["failure-incomplete-tool-contracts-false-verified-state", "operator-contract-gated-tool-state-commit", "paper-p074"]
-->
# Candidate v034 — Contract-Calibrated Conjunctive Bottleneck

## Changed computation

For each pointwise next-action candidate, a deterministic compiler forms five
complementary evidence projections from only the frozen history, tool metadata
and action: mode, tool choice, argument contract, grounding, and
prerequisite/order/progress.

The same frozen Qwen3-0.6B model assigns independent next-token
`Yes`-versus-`No` log odds to every obligation. Each obligation is calibrated
to an empirical percentile using unlabeled action scores from the other two
Development sources. The Candidate score is the minimum of the five
percentiles:

```text
CCCB(action) = min_k F_k(log p(Yes_k) - log p(No_k))
```

The minimum implements the falsifiable conjunctive claim: a mandatory
tool-action obligation cannot be averaged away by high confidence elsewhere.

## Mandatory controls

- holistic full-evidence judgment from the same model;
- every individual obligation;
- raw minimum;
- calibrated arithmetic mean and product;
- pairwise majority vote;
- the best single obligation selected only on the other two sources;
- a supervised fixed-C linear ensemble trained only on the other two sources.

CCCB must strictly beat all controls. A gain over only the holistic prompt is
insufficient.

## Data and exposure

GTA, BFCL and ToolTalk at fixed ToolPRMBench commit
`b43164fbb2cd2963e1906a6fe62a86e7ce05973e` are exposed Development. Selection
after exploratory shortcut probes is optional stopping and is disclosed in
`selection_context_v034.md`.

ToolSandbox remains absent and untouched. It can be acquired only after every
Development gate and a positive written main-Codex Promotion Audit.

## Claim Contract

The exact compiler, model revision, answer tokens, obligations, calibration,
controls, source holdout, metrics, gates and conditional Confirmation are fixed
in `research_map_v034.md`.

At most, a passing result can support the narrow fixed-protocol empirical Claim
written there. It cannot establish generic PRM quality, first-ever rubric
decomposition, formal tool correctness, executable state verification,
larger-model transfer, search improvement or online safety.
