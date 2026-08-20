# Neutral Selection Context

## Prior failures

v004 failed a universal per-source metric condition. v005 passed Development but failed untouched Confirmation donor coverage before metrics. Their frozen Results are not v006 Confirmation.

## New untouched source

Only metadata and README were read for `mangopy/ToolRet-Training-20w@fdf5a317455b1e60785de7ba587496aa6cc878e4`: one 208,826-row train split with fields `query`, `id`, `prompt`, `positive[]`, and `negative[]`. No split row has been fetched.

Development is the first 1,000 rows. Confirmation is the last 1,000 rows. Each phase is divided prospectively into ten contiguous 100-row analysis clusters. Donors are selected only inside the same 1,000-row phase, so Confirmation prompts remain inaccessible during Development.

Each phase corpus is the deduplicated union of every positive and negative tool string in that phase. Every query searches that complete phase corpus with BM25 and fixed MiniLM; the per-row supplied negative list is not used as an oracle retrieval menu.

The split uses distant fixed offsets rather than outcome selection. A v006 failure remains frozen and cannot be repaired by changing row ranges, donor count, cluster size, or thresholds.
