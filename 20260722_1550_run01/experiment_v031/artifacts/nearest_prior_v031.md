# Nearest Prior v031

| Prior | Direct collision | Remaining v031 delta |
|---|---|---|
| Terminal Wrench, 2026 | Supplies the real stripped command/terminal benchmark and an LLM-judge detection baseline | v031 is a local deterministic-feature monitor under stricter task-and-generator holdout |
| Cheap Reward Hacking Detection, 2026 | Trains global full and stripped trajectory encoders and a linear probe | v031 freezes the encoder and tests command-level task relevance pooled by operation role; it does not claim a new encoder |
| Trajectory Guard, 2026 | Learns task-trajectory alignment and sequence reconstruction for anomaly detection | v031 uses no learned alignment objective or autoencoder and targets real Terminal Wrench reward hacks |
| v020-v022 task-relative residuals | Uses successful same-task traces as references | v031 uses only the task specification and never reads support trajectories |
| v023-v025 AORF/VIAF | Splits action surfaces by role or first verifier-inspection time | v031 does not split TF-IDF text; it pools frozen semantic relevance by command operation |
| v026 CMCD | Learns query/support absolute-deviation pairs and averages cross-model supports | v031 has no support pair, support eligibility rule or model consensus |

## Primary bytes

- Terminal Wrench PDF SHA-256 `140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a`.
- Cheap Reward Hacking Detection PDF SHA-256 `c5fd945125b1b6cd4739b2aacf150156bbfc8e47aff2d7240ea05ed697075ce0`.
- Trajectory Guard PDF SHA-256 `ab6d2c66b081b32a90ff3f230854058199c049362ffb49f46bef9f869fc18d34`.
- P040 formal source SHA-256 `ab1307fdaaf97841bd09296bca225b736e8e9a712002ac123b1fab663f35ba6a`.

## Novelty ceiling

Task-conditioned monitoring, cross-encoders, sequence-aware anomaly detection and reward-hack classifiers are established. At most, MGTR can contribute a compact operation-role pooling computation and a doubly held-out Terminal Wrench result. Delivery requires a real bucket-0 replication and cannot be justified by Development alone.
