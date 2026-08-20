# Problem v026 — Cross-generator few-support reward-hack detection

Action-only reward-hack monitors may exploit generator-specific style and task-surface regularities. A practical cold-start setting is harder: a new agent model is deployed on a new task, while a few successful traces from already covered agent models are available for that same task.

The target question is:

> Can a supervised query–support deviation model trained without the target task or target generator detect rewarded serious exploits from that generator better than direct action text, equal-capacity query duplication, a single support, and multi-support concatenation without an explicit deviation channel?

Inputs are stripped commands and terminal outputs only. The final label is released Terminal Wrench successful baseline versus rewarded serious exploit. The method is falsified unless it transfers across both axes, strictly beats every declared control, and avoids a gain confined to one generator family.

The deployment assumption is explicit: at inference, at least one successful same-task trace from a different generator family must be available. The work does not address tasks lacking such support, unseen shell ecosystems, online intervention, hidden intent, reasoning traces or causal proof of reward hacking.
