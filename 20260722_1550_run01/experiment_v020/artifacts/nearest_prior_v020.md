# Nearest Prior v020

This commitment is written before any v020 model fitting or metric output.

## Bounded current-prior search

The main Codex searched four perspectives: action-surface reward-hack detectors, task-relative/contrastive trajectory comparison, benign workflow envelopes, and Terminal Wrench-specific monitors. Primary PDFs were read directly.

## Closest works and exact boundary

### Terminal Wrench

The benchmark provides hack and successful baseline trajectories plus stripped action-visible variants. Its GPT-5.4 judge obtains stripped AUC `0.9168` and TPR@5%FPR `0.44` on the paper's population. It is a strong conceptual baseline but requires an LLM judge and is not released as per-row frozen scores on the v020 partition.

Source: `experiment_v012/artifacts/source_terminal_wrench_2604.17596.pdf`, SHA-256 `140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a`.

### Cheap Reward Hacking Detection

The paper learns a 13.8M-parameter transformer representation from reward/metadata signal distances. Its separately stripped-trained encoder reaches AUC `0.7631`, TPR@5%FPR `0.2275`; full reasoning-visible performance is much higher. v020 uses no transformer, reasoning, reward-vector metric learning, or published split. The paper prevents any claim that v020 is the first cheap action-surface detector.

Source: `experiment_v012/artifacts/source_cheap_reward_hacking_2606.08893.pdf`, SHA-256 `c5fd945125b1b6cd4739b2aacf150156bbfc8e47aff2d7240ea05ed697075ce0`.

### TRACE

TRACE shows LLM detection improves when trajectories are presented contrastively rather than in isolation, with its strongest reported Detection Rate moving from 45% to 63%. v020 adopts the contrastive premise but replaces cluster-level LLM judgment with a single-reference signed sparse residual and a fixed cheap learner. It does not claim first contrastive analysis.

Source: `experiment_v012/artifacts/source_trace_2601.20103.pdf`, SHA-256 `98a3121de46018f08f47a8db18b4ed55c9d117beb5e984eaa9f3c2a47f3a5649`.

### Praetor

Praetor builds a pDFA and parameter guards from many verified benign traces for runtime enforcement in structured workflows. v020 instead performs post-hoc task-disjoint classification from one same-task reference and exact sparse text/action residuals. Praetor prevents a broad “first benign-envelope agent monitor” claim.

Source: `experiment_v012/artifacts/source_praetor_2604.26274.pdf`, SHA-256 `842d593f53486481d384c8407d2fd688bbfbf90b69e505db54bc31008a15aa98`.

### v012 RCED

RCED is the nearest byte-compatible local predecessor. It used the same Development carrier, reference rule, split, TF-IDF base, and learner, but compressed reference difference into 29 numeric effect/path features and failed. v020's sole scientific change is the signed sparse residual representation, and RCED remains a mandatory comparator.

## Collision judgment

Contrastive trajectory evaluation, cheap trajectory detectors, benign behavior envelopes, signed feature differences, and sparse linear classifiers are all prior ideas. The only candidate contribution is their exact task-relative action-surface composition and its fixed-corpus empirical effect against four same-byte comparators. No universal novelty claim is justified. A positive result may support a narrow representation finding; a negative result kills the route.
