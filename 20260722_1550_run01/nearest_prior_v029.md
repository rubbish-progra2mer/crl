# Nearest Prior Commitment v029

## Directly read neighbors

- P084 is the exact controlled failure/data source: fixed requests, related-tool expansion and wrong-function/parameter-side errors.
- P087 TOOL-DE performs query-independent generated document expansion and offline field ablations; its full expansion is not uniformly optimal. v029 generates nothing and uses query-conditioned score deletion at inference.
- ToolPRM (ACL 2026; frozen PDF SHA-256 `f781b56a766748c261ab4c6c6804a6f3f85f7795c6894eaac9408e9dcecd0d55`) decomposes structured generation into function-name and argument decisions, trains a process reward model using function masking and guides beam search. v029 has no policy generation, masking, supervision or decoding.
- JTPRO (Findings ACL 2026; frozen PDF SHA-256 `f564463c7e64bb2980f1d2b38bf5bedb25b31b8cf5bba7d6ae36818f90e9ad6b`) iteratively co-optimizes global instructions and tool schema/argument descriptions from rollout reflection. v029 never rewrites instructions or schemas.
- MagicSelector (arXiv 2607.17751; frozen PDF SHA-256 `bce125f5d225d72bba71bbe9a5ace065bb79815c7980359be0422e3e0b538527`) uses counterfactual reward for task decomposition, self-distilled point/list-wise hard-negative reranking and dynamic top-k. v029 neither decomposes the query nor trains/reranks a model nor changes menu size.

## Collision boundary

Feature ablation, deletion attribution, cross-encoders, schema serialization, minimum aggregation and tool ranking are established components. Open web and formal Card searches did not establish first-ever novelty and v029 makes no such claim. Its only testable delta is the fixed composition `full score + min(operation-deletion drop, argument-deletion drop)` against five capacity-matched controls on two pinned compact-menu datasets.

