# Main Codex Execution Audit v024

Disposition: `NO_GO_FOR_SAME_VERSION_RETRY`.

The frozen Plan is current at SHA-256 `30e6a7071686e036a7738b9af4d42b5f705949862b906740032799cd71c1f217`, but its first authorized acquisition invocation returned exit 1 before the acquisition payload started. Frozen runner `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a` called `capture_dir.mkdir()` on `experiment_v024/captures/dev_acquire_001`; the uncreated `captures` parent caused `FileNotFoundError [WinError 3]` at line 74.

Post-failure read-only checks returned false for the planned capture directory, Development output directory, acquisition work root, and both `captures` and `work` parents. The runner invokes the payload only after capture-directory creation, so `acquire.py` did not start. No Terminal Wrench metadata, label or trajectory byte from bucket 1 or bucket 0 was acquired.

This is an execution-path defect, not a VIAF scientific result. There are no Development rows, scores, metrics, audit report, Confirmation, Review or Delivery bytes. The Plan's fixed failure rule says any nonzero acquisition/execution freezes v024 and advances the same Run; therefore creating parents and retrying under v024 is forbidden. v025 may carry the identical Candidate, Evidence Packet and scientific computation as an execution-only correction, with parent directories created before its one immutable acquisition invocation. This audit does not lower gates, retune the anchor, alter data buckets or authorize any subagent.
