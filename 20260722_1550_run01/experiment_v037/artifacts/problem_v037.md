# Research Problem v037

Pairwise verdict prompts can collapse into position selection even when both
orders are evaluated. Full action likelihood can instead be dominated by
shared syntax and generic fluency.

The v037 question is:

> Does subtracting evidence-withheld teacher-forced likelihood from
> full-evidence likelihood, only on tokens not shared by the two candidate
> actions, improve frozen next-action ranking across exposed ToolPRMBench
> sources and untouched ToolSandbox?

The target is pairwise next-action classification. This is not execution
verification, future-task utility, reward-model training or downstream Agent
success.

