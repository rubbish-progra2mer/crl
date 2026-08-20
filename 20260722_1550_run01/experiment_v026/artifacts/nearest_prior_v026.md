# Nearest Prior Commitment v026

## Directly read sources

- Terminal Wrench and Cheap Reward Hacking Detection remain the exact task/data lineage. Neither uses successful same-task cross-generator trajectories as test-time supports or evaluates simultaneous held-out-task and held-out-generator transfer.
- Trajectory Guard (PDF SHA-256 `ab6d2c66b081b32a90ff3f230854058199c049362ffb49f46bef9f869fc18d34`) learns task–trajectory alignment and sequential reconstruction with a Siamese recurrent autoencoder, trained largely with synthesized anomalies. It does not compare a query action trace to known-good same-task traces from other generators.
- D²4FAD (arXiv 2603.01713; PDF SHA-256 `c8f9aa621915f8e1ecb3945155eb5bf06580f74214f3d9d88be520154a5231f7`) performs episodic few-shot medical-image anomaly transfer. It uses a frozen teacher, learned student, support self-distillation and query-conditioned learn-to-weight support aggregation. This is the strongest support/query collision, but its representation, labels, objective and visual domain differ.
- UniVAD (arXiv 2412.03342; PDF SHA-256 `c20e32751c4f7b6332606a810ec07be854af0afb4c9202619a5822936d5b55a9`) is training-free visual few-shot anomaly detection using normal reference images, component segmentation, patch matching and graph-enhanced component modeling. It establishes that unseen-task normal-reference matching is not novel by itself.
- LOTTERY (arXiv 2606.08460; PDF SHA-256 `1bc52603140c3afee187346364aaa160f90c1e0678a36c10c3618e370b055096`) learns multiple global/local reference-dependent scalar representations only from an abundant reference distribution and aggregates them for few-query two-sample testing with pooled-permutation validity. v026 instead trains a supervised row detector on labeled Development queries and produces one reward-hack score per trajectory; it makes no type-I guarantee.

## Closest runnable local composition

v021–v022 is the closest local implementation. It compares one evaluated trajectory with one successful same-task reference through signed sparse residual channels and does not hold out the evaluated generator family. v026 instead trains query–support pair classifiers, excludes the target generator from every training/query/support byte, uses all available successful supports from the other generators, and mean-aggregates pair probabilities. The mandatory `single_support`, `consensus_no_abs`, and `triple_query` controls isolate support multiplicity, explicit absolute deviation and three-block capacity.

The open search found no exact real agent-action detector with this combined task-fold/generator-holdout protocol and cross-generator successful-support consensus. That is not proof of first-ever novelty. Maximum contribution is a fixed Terminal Wrench representation-and-transfer result under the explicit assumption that successful same-task traces from other generator families are available at inference.
