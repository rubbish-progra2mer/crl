<!-- crl-v3-evidence-ids
["ev-p084-expanded-toolkit-controlled-setting","ev-p084-related-toolkit-error-types","ev-p085-non-exhaustive-label"]
-->
# Candidate v030 — Revision-Grounded Typed Contract Audit (RTCA)

## Changed computation

RTCA maps each pre-fix benchmark entry into typed facts spanning user text, recursive tool schemas, reference calls, literals, units, dates and file dependencies. Six deterministic violation channels are scored with frozen severity weights, and entries are ranked within each historical repair PR's pre-fix file.

The changed entry IDs in a merged patch are evaluation labels only. Repaired values never enter feature extraction or scoring.

## Mandatory controls

- schema-only;
- path-dependency-only;
- temporal-and-unit-only;
- literal-provenance-only;
- pre-fix byte size;
- unweighted violation-channel union.

All controls use identical PR pools, changed-ID labels and SHA tie breaking.

## Data boundary

Development is exposed and fixed to PRs `865, 870, 871, 872, 876, 892, 962, 963`, containing 9 changed entry IDs. Development source acquisition produced two explicit HTTP 404s for inferred PR-962 `possible_answer` paths; PR 962's modified executable row embeds its own ground truth, and no absent file may be claimed.

Conditional Confirmation is fixed to later PRs `1084, 1085, 1086, 1087, 1175, 1177`. Their data contents are unacquired and unread. Public PR identifiers/titles were visible during selection.

## Isolation and cost

RTCA is a single-process CPU computation in the shared Python 3.11.15 environment. It uses no LLM, model download, generated label, subagent, training, retry, threshold search or per-item manual judgment. Development and Confirmation use the same frozen scoring/audit code, weights, parsing rules and phase-specific gate presets. A frozen builder binds each authorized source pool to a phase config; it does not select or tune a rule from that pool.

## Claim Contract

The exact conjunctive gates are in `research_map_v030.md`. The maximum allowed claim is chronological patch localization on the fixed BFCL repair PRs. It is not benchmark repair, semantic correctness proof, complete defect detection or downstream task-success evaluation.

If Development fails, Confirmation remains unopened and v030 is frozen as a negative result. If Development passes, only the main Codex may authorize the one fixed Confirmation acquisition.
