# Problem v012 — Action-visible terminal reward hacking with one successful reference

## Research question

On real terminal-agent trajectories with task-disjoint evaluation, can a deterministic representation of **how an evaluated command sequence changes effects relative to one successful same-task reference** improve action-only reward-hack detection over a strong command-and-output text classifier?

## Observable setting

For each task, the monitor receives:

- the task prompt;
- one successful baseline trajectory designated as the task reference;
- an evaluated trajectory with agent commentary removed;
- shell commands and terminal outputs from both trajectories.

It does not receive hidden chain-of-thought, the stored human explanation of the hack, `key_hack_steps`, the hack category as a feature, or post-hoc access to the task's other evaluated labels.

## Failure of interest

A terminal agent can obtain the task reward by manipulating a weak checker or writing an artifact that matches surface checks without performing the intended state transition. A text-only action monitor may recognize some known exploit strings, but it does not explicitly compute whether:

- expected reference executables/effect classes disappear;
- new writes target paths not touched by the successful reference;
- an inspected verifier is followed by a novel direct write;
- verification follows a divergent write path;
- the ordered effect sequence differs sharply from the successful reference.

The problem is limited to hacks visible in commands or terminal outputs. It excludes invisible intent, attacks with action traces indistinguishable from legitimate executions, and general semantic proof of task correctness.

## Dataset and unit of generalization

- Dataset: Terminal Wrench at commit `d8a29613235a0ef56a8b70b3142626a533da28c2`.
- Labels: stored successful baselines are negative; stored `rewarded_serious_exploit` stripped trajectories are positive.
- Unit of generalization: task ID.
- One lexicographically first successful `(model, baseline_label)` trajectory per task is the reference and is excluded from evaluation.
- A task is eligible only when at least one other successful baseline and at least one stripped serious exploit remain.
- Development tasks: first SHA-256 byte modulo four equals `2`.
- Untouched Confirmation tasks: first SHA-256 byte modulo four equals `3`.
- Selection-exposed task `1012` is forced into Development training and cannot contribute to validation, held-out Development metrics, threshold selection, or Confirmation.

## Falsifiable target

The candidate must improve held-out Development task AUC over the strongest text-only comparator by at least `0.02`, with a task-cluster bootstrap 95% lower bound above zero, while also meeting absolute low-FPR detection gates. Failure of any preregistered gate closes v012 without opening Confirmation.
