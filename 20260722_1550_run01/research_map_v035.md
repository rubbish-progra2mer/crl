# Research Map v035

## Evidence-backed failure

ToolPRMBench supplies correct and plausible incorrect next actions conditioned
on interaction history and tool metadata. ToolRM reports that pairwise
tool-action judgment remains difficult and that models may identify errors yet
mis-rank their severity. PRePair and Pairwise or Pointwise show that direct
comparison can amplify surface features, while independent pointwise reasoning
can reduce some pairwise bias. SCOPE establishes that order-swapped probability
aggregation is an existing control, not a v035 contribution.

## Nearest computation families

| Family | Existing computation | v035 boundary |
| --- | --- | --- |
| ToolRM | learned full-pair tool-use critic | frozen model; no reward-model training |
| PRePair | independent pointwise reasoning, then pairwise decision | deterministic field difference before judging |
| SCOPE | bidirectional preference probabilities and entropy | same order control; no conformal selection Claim |
| Tool contract checks | inspect required fields and state conditions | text evidence only; no formal or executable proof |
| Contrastive retrieval/verifiers | compare alternatives or seek distinguishing inputs | no active search, rollout or retrieved external evidence |

## Candidate causal story

If the correct and rejected actions share most tokens, shared material is
nuisance for the binary decision. Removing exact shared fields should increase
the proportion of decision-relevant evidence. Restricting tool metadata to
contracts implicated by either action should reduce unrelated schema load.
Bidirectional scoring prevents a fixed A/B position from becoming the signal.

This story is falsified if the Candidate fails to beat either the full-pair or
independent pointwise control, if its gain comes from action text without
history/contracts, or if gains are confined to one exposed source.

## Mandatory controls

1. order-symmetric full pair with full actions and the same evidence;
2. independent full pointwise action scoring with the same model;
3. order-symmetric minimal difference without history or contract evidence;
4. unidirectional minimal-difference scoring;
5. exact per-source reporting and source-cluster bootstrap.

The strongest observed mandatory control defines the comparator. No control is
selected after looking at Confirmation.

## Untouched boundary

Development is GTA + BFCL + ToolTalk. ToolSandbox is the only v035
Confirmation and remains unacquired and unread until a positive main-Codex
Promotion Audit.

