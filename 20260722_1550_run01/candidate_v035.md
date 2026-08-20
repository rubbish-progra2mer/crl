# Candidate v035: Symmetric Differential Evidence Judgment

## Name

Symmetric Differential Evidence Judgment (`SDEJ`).

## Frozen computation

For each pair of proposed next actions:

1. Parse each action into mode, tool name and recursively flattened argument
   paths. If parsing fails, treat the action as a non-call text action.
2. Remove fields with exactly equal canonical values. Retain only
   candidate-specific mode, tool, key and value differences. For two text
   actions, retain deterministic word/punctuation-token difference spans; for a call versus
   text pair, retain the canonical call and text as the mode contrast.
3. Select only tool contracts whose names occur in either parsed call. If no
   exact contract is available, retain the system-message tool description as
   an explicitly marked fallback.
4. Present the frozen interaction history, implicated contracts and the two
   candidate-specific differences to the frozen Qwen3-0.6B judge.
5. Score the bare next-token probabilities of `A` and `B` in both response
   orders. Align the reverse-order probability to the original candidates and
   average the two probabilities. Prefer the action with the larger aligned
   probability.

The method performs no supervised fitting, no source-specific calibration, no
external retrieval, no rollout and no execution.

## Mandatory matched controls

- `full_pair`: both complete actions, full history and implicated contracts,
  scored in both orders;
- `full_pointwise`: each complete action independently scored with bare
  `Yes`/`No` probabilities using full history and implicated contracts;
- `delta_no_evidence`: the same minimal differences without history or
  contracts, scored in both orders;
- `delta_forward`: the Candidate prompt in only the original order.

All language-model controls use the same frozen model, tokenizer, prompt cap
and bytes. Ties score `0.5`.

## Development

Frozen inputs are ToolPRMBench GTA (118), BFCL (111) and ToolTalk (86), for 315
pairs. Metrics are overall accuracy, source accuracy, aligned order
consistency, paired candidate-minus-control deltas and a deterministic
source-cluster bootstrap.

Development passes only if all conditions hold:

1. SDEJ accuracy is at least `0.70`;
2. SDEJ exceeds the strongest mandatory control by at least `0.025`;
3. the 95% source-cluster bootstrap lower bound for that delta is strictly
   greater than `0`;
4. SDEJ accuracy is at least `0.58` on every source;
5. its delta versus the strongest control is nonnegative on every source and
   strictly positive on at least two sources;
6. SDEJ strictly exceeds both `full_pair` and `full_pointwise`;
7. `delta_no_evidence` does not equal or exceed SDEJ;
8. the independent raw-output audit reproduces every prompt, probability,
   prediction, metric and bootstrap value within `1e-6`.

All eight conditions are conjunctive. No threshold, projection or control may
change after execution.

## Conditional Confirmation

Only after all Development conditions pass and the main Codex writes a
positive Promotion Audit may it acquire the fixed ToolSandbox file. The
Development-frozen program and state then run unchanged.

Confirmation passes only if:

1. SDEJ accuracy is at least `0.60`;
2. SDEJ strictly exceeds both `full_pair` and `full_pointwise`;
3. SDEJ exceeds the strongest mandatory control by more than `0`;
4. the paired bootstrap median delta is more than `0`;
5. the independent audit reproduces all outputs within `1e-6`.

## Claim ceiling

If both phases pass, the maximum Claim is that this fixed differential evidence
projection improved this frozen small judge on these pairwise tool-action
splits against the listed matched controls. It is not a claim of general judge
superiority, formal correctness or downstream Agent success.
