<!-- crl-v3-evidence-ids
["ev-p040-failure-core"]
-->
# Candidate v031 — Mutation-Gated Task Relevance (MGTR)

## Changed computation

MGTR scores every emitted command segment against the frozen task description with one fixed pretrained cross-encoder. It assigns each segment a deterministic operation role and pools relevance separately for mutation, verification, read and other commands. The resulting 20 statistics augment the same direct action/terminal TF-IDF classifier used by the strongest local text baseline.

The method has no successful-trajectory reference, cross-model support, first-verifier anchor, exploit-category input, threshold search or label-dependent feature.

## Mandatory controls

- direct action/terminal text;
- task/action text concatenation;
- direct text plus operation-role fractions;
- direct text plus global relevance;
- direct text plus equal-capacity chronological relevance.

Every method uses identical double-holdout folds, learners and rows.

## Data boundary

Exposed buckets 1-3 are Development: 4,256 rows, 250 tasks, three generator families and five sources. This route was selected after earlier Terminal Wrench results, so optional stopping is explicit.

Bucket 0 remains absent and untouched. Its frozen acquisition is conditional on a positive Development Promotion Audit.

## Claim Contract

The exact computation, controls and conjunctive gates are in `research_map_v031.md`. The maximum Claim is limited to fixed Terminal Wrench stripped serious-exploit detection under held-out-task and held-out-generator evaluation.

MGTR does not infer intent, prove a command is malicious, localize a causal exploit, replace an outcome verifier or establish general task-trajectory alignment.
