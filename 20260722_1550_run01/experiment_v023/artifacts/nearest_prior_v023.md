# Nearest Prior v023

## Terminal Wrench

Terminal Wrench releases real baseline and rewarded exploit trajectories and reports that removing reasoning lowers its LLM-judge AUC from about 0.97 to 0.92. Its study scores the trajectory as a mixed input; it does not isolate command and terminal-output coefficient roles with capacity-matched sparse controls.

## Cheap Reward Hacking Detection

Cheap Reward Hacking Detection trains a small transformer encoder on whole trajectories and reports cleaned-test AUC 0.9467, but stripping natural-language reasoning at probe time drops AUC to 0.6213. It does not test shared-vocabulary linear role factorization, and its representation/label objective is not a capacity-matched action-versus-observation ablation.

## Trajectory Guard

Trajectory Guard uses a task tower plus a GRU trajectory autoencoder and hybrid contrastive/reconstruction loss. It models action-step order and is the direct collision for a generic sequence-aware Candidate. Its anomalies are mostly GPT-5 perturbations; external RAS-Eval and Who&When sets lack normal samples and are reported by recall. AORF makes no sequence-model claim and instead tests whether observed terminal feedback needs a coefficient role distinct from issued commands on real reward hacks.

## AgentDiagnose and monitoring lineage

AgentDiagnose explicitly represents trajectories as observation–reasoning–action tuples, but its five competencies are LLM-scored diagnostics and its action/state views are visualizations. It does not train a task-disjoint reward-hack detector or isolate role factorization from duplicated-role capacity. Reliable Weak-to-Strong Monitoring further shows monitor scaffolding matters, but operates through LLM monitor orchestration rather than this sparse representation.

## Local nearest composition

v022's reference-based signed residual is a stronger-information local result, not a like-for-like reference-free baseline, and its Confirmation failed the task-bootstrap gate. v023 does not reuse or modify that computation. Its valid maximum contribution is a fixed-protocol representation finding: independent action/output coefficient roles add signal beyond mixed or duplicated single-role sparse detectors.

The bounded search does not prove universal novelty. Any later claim is restricted to the frozen Terminal Wrench buckets, stripped command/output surface, shared vocabulary and stated comparator ladder.
