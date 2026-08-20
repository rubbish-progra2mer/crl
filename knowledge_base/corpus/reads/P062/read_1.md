# P062 first read — unified learnable LTM/STM control

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents
- Authors: Yi Yu et al.
- Venue: ACL 2026 long paper
- PDF: `knowledge_base/staging/plan05_sat_a1/P062_agentic_memory_unified.pdf`
- PDF SHA-256: `ba41464f84dbd8e0d0aeb1e6e0d7fd83b4086b2922579b88f7947448a8e1958f`
- Parse check: 27 physical pages

## Changed computation

AgeMem exposes ADD/UPDATE/DELETE for LTM and RETRIEVE/SUMMARY/FILTER for STM as actions of the same LLM policy. A three-stage curriculum separates information acquisition, distractor/context pressure and final task execution. A GRPO variant broadcasts a group-normalized terminal advantage to every preceding memory and reasoning action, while a composite reward scores task completion, context behavior and memory quality.

## Evidence and closest lineage

The paper compares against LangMem, A-Mem, Mem0 and Mem0g on five long-horizon benchmarks with Qwen2.5-7B and Qwen3-4B. Full AgeMem outperforms no-memory and memory baselines on average; staged ablations attribute gains to LTM, RL and STM components. Augmented baselines with the same STM/RL extensions improve but remain below full AgeMem on the reported three-task comparison.

## Measurement and fairness boundaries

- RL is trained only on HotpotQA and transferred to other controlled benchmarks; persistent real-user interaction is untested.
- Reward uses expected answers during training and LLM judges for task/memory quality, so the learned policy is partly shaped by evaluator and ground-truth availability.
- The claimed “step-wise” credit signal is the same terminal advantage broadcast to all steps; it connects delayed reward but does not isolate which memory action was critical.
- Full reward uses slightly more tokens and more tool calls than answer-only; gains are not a pure efficiency effect.
- The fixed six-tool action set and synthetic distractor curriculum constrain generality.
- Training uses eight RTX 4090 GPUs and Qwen-Max evaluation, well beyond a small local prototype budget.

## Draft knowledge objects

### Operator draft: `Unified Policy over Long- and Short-Term Memory Actions`

Put persistent-memory updates and active-context control in one learned action space, then train their coordination under delayed downstream reward instead of composing separately tuned memory managers.

### Failure draft: `Broadcast Terminal Advantage Does Not Identify Critical Memory Steps`

Assigning one normalized final advantage to every action links storage and later outcomes, but cannot distinguish a useful write/filter/retrieve from irrelevant actions on the same trajectory.

## Draft Evidence locators

- pp.1–6: unified action space, staged curriculum, broadcast advantage and composite reward.
- pp.7–9: main results, tools, component and reward ablations.
- p.10: controlled-setting, fixed-tool and HotpotQA-training limitations.
- pp.24–27: judge prompts, baseline setup, GPU configuration and augmented-baseline comparison.

All claims remain draft until independent read and reconciliation.
