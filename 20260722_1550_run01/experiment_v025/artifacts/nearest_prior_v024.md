# Nearest Prior v024

## Terminal Wrench and Cheap Reward Hacking Detection

Terminal Wrench (PDF SHA-256 `140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a`) releases the real baseline/exploit trajectories and evaluates LLM judges on whole sanitized or stripped trajectories. Cheap Reward Hacking Detection (PDF SHA-256 `c5fd945125b1b6cd4739b2aacf150156bbfc8e47aff2d7240ea05ed697075ce0`) trains a whole-trajectory encoder and linear probe. Neither fixes a verifier-inspection event or compares event-relative sparse blocks to same-width duplication, fixed time, and position-free anchor controls.

## Trajectory Guard and TrajAD

Trajectory Guard (PDF SHA-256 `ab6d2c66b081b32a90ff3f230854058199c049362ffb49f46bef9f869fc18d34`) uses a task tower, recurrent trajectory autoencoder, triplet contrastive objective and reconstruction. It is the closest collision for a generic sequence-aware detector.

TrajAD (arXiv 2602.06443; PDF SHA-256 `3237bcd13e7f2926c3f3cd3891c661ea398f57f1cb347523c87a217a73278fec`) represents instruction plus ordered reasoning/action/observation triplets and fine-tunes Qwen3-4B with LoRA to generate anomaly verdict and first error step. Its 63,484 samples are constructed from golden trajectories by perturb-and-complete; its target anomalies include failure, inefficiency and unwarranted continuation. It does not identify a fixed verifier-inspection anchor, use Terminal Wrench real reward-hack labels, or isolate sparse phase factorization from the v024 controls.

## AgentRx

AgentRx (arXiv 2602.02475; PDF SHA-256 `59680fd631934d6ad3046108a504195e8cd70066bdefbfb3561b7731f7d22923`) normalizes failed trajectories, synthesizes global and dynamic constraints from schemas/policies/prefixes, runs programmatic or LLM semantic checks at each step, and gives violation logs to an LLM judge for critical-step/category attribution. It is a much richer and costlier constraint pipeline, not a label-free fixed anchor or sparse detector.

## Strained Coherence

Strained Coherence (arXiv 2606.07889; PDF SHA-256 `33a2ee601361ab3c538732133ff2a937c93f765f112451a9bf96899d9fce3271`) uses a Claude judge to find explicit reasoning acknowledgments followed by non-resolution. Its first flags occur at median 83–84% elapsed, supporting the relevance of event timing, but the signal requires think content and targets task failure rather than stripped action-only reward-hack labels. VIAF cannot claim this reasoning mechanism.

## Closest runnable composition and novelty ceiling

The closest runnable composition is the v024 `anchor_bag` plus `fixed_halves` plus `command_duplicated` ladder on identical bytes. Any gain that does not exceed all three cannot be attributed to verifier-relative order. The open search found no exact shared-vocabulary `[mixed,before-anchor,from-anchor]` comparison on real Terminal Wrench labels, but this bounded search cannot prove first-ever novelty. Maximum contribution is a fixed-protocol, action-only representation result.
