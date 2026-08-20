# Problem v020 — Action-Surface Reward-Hack Detection under Workflow Multimodality

## Target problem

Detect rewarded serious exploits from stripped terminal-agent trajectories when only task prompt, executed shell commands, and terminal outputs are visible. Each eligible task supplies one successful baseline trajectory that may be used as a task-specific reference but must not be fitted or scored as an evaluated example.

## Observed failure

An absolute text classifier can learn common exploit tokens but lacks an explicit task-relative channel. v012's attempt to add task-relative information compressed trajectories into coarse effect/path counts and distances; that representation assigned extreme risk to legitimate alternate workflows and reduced AUC relative to raw text.

The unresolved question is narrower: can task-relative comparison help when it preserves exact sparse action/output fragments and separates additions from omissions, rather than collapsing them into coarse sequence statistics?

## Analysis unit and scope

- Unit: one evaluated trajectory row.
- Split unit and bootstrap cluster: `task_id`.
- Positive: released `rewarded_serious_exploit` classification.
- Negative: released successful baseline trajectories except the single reserved reference.
- Input condition: stripped action surface only; agent commentary and hidden state are absent.
- Required deployment resource: one trusted successful reference for the same task.

The claim excludes general malicious-agent detection, semantic proof of task completion, unseen tasks without a successful reference, reasoning-visible trajectories, online blocking, verifier hardening, and adversarial robustness.

## Falsifier

The Candidate is falsified if its signed residual channels do not outperform the strongest same-input comparator—raw text, reference concatenation, unsigned absolute delta, or v012 RCED—on the fixed task-disjoint Development test under the preregistered AUC, low-FPR, threshold-transfer, and task-bootstrap conditions.
