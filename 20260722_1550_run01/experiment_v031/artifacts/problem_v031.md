# Research Problem v031

## Problem

Terminal reward hacks can be difficult to distinguish from legitimate command-line work because both use ordinary shell actions such as `cat`, `grep`, `echo`, package managers and test runners. Global action-text classifiers can exploit surface regularities but do not identify whether suspicious semantic mismatch is concentrated in state-changing commands.

The task specification supplies a label-free reference available before execution. A command may be locally plausible yet weakly related to that specification, especially when it mutates files, permissions, packages, services or network state. Conversely, exploration and verification commands may be semantically broad without being malicious.

The empirical question is:

> Does pooling frozen task-command relevance scores by deterministic operation role improve stripped-trajectory reward-hack detection over direct action text, task/action concatenation, structural counts, global relevance and equal-capacity chronological pooling?

## Observable

All methods receive the same stripped command and terminal-output surfaces. The Candidate additionally receives the task description already present in each row and a frozen pretrained cross-encoder. It cannot use reasoning, exploit categories, model identity, source identity, same-task support trajectories or labels during feature extraction.

Development uses three-fold task OOF evaluation crossed with complete target-generator holdout. Every row is scored once by a model trained on other task folds and other generator families.

## Scope

- Development: exposed immutable Terminal Wrench buckets 1, 2 and 3.
- Conditional Confirmation: untouched bucket 0 at repository commit `d8a29613235a0ef56a8b70b3142626a533da28c2`.
- Endpoint: binary serious-exploit versus successful-baseline detection.
- No online intervention, causal attribution, exploit localization, hidden-intent inference, chain-of-thought, human truth or cross-benchmark claim.
