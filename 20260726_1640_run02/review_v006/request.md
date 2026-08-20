# Review Request Note (v006)

- Common Packet: D:\Desktop\crl\20260726_1640_run02\review_v006\packet.md
  SHA-256 2fe7fcebf4395b53a37cd1ff514d53df743f0e76a9f75643368c22921acaa5cd
- Common Protocol snapshot: review_v006/snapshots/CRL_REVIEWER_PROTOCOL.md
  SHA-256 D1DC1D603D562585FBE06A22597F8BD3D31182FDC000BDBA45EB1F999C8026B8
- Role snapshots:
  R1 Prior and Lineage Attacker: snapshots/crl_prior_reviewer.md
     SHA-256 6261EEAB830BB827371BB45442A92EE8A2908A41E55CEA66417FEA029508E048
  R2 Scientific Skeptic: snapshots/crl_scientific_skeptic.md
     SHA-256 C9A401432A898F7A90EF282B60C5EF8CA3FEDD16AC10C87A383F5656326DC9BD
  R3 Implement Potential: snapshots/crl_potential_reviewer.md
     SHA-256 90DC36C2F8AF59DF1D115E8FEDA191B1E63CD1CE435D036DEA5B8A61148E04D7
- Exact requests: three fresh subagents launched simultaneously
  2026-07-26 ~22:25 +08:00, each request verbatim contains
  `REVIEWER_SUBAGENT_DELEGATION: FORBIDDEN`; each received ONLY the
  common Packet path/SHA, common Protocol snapshot path/SHA, its own
  role snapshot path/SHA, and its neutral exact request; fresh context
  (no main-thread history inheritance); peer reports invisible; the
  Main Codex private prior body (nearest_prior_v005/v006) explicitly
  excluded and forbidden to read.
- Reviewers must open the Packet, Protocol, own role snapshot and every
  manifest item, and report per-item path/SHA readback; any unread,
  missing or mismatched item invalidates completeness.
- Subagent tool identity: general-purpose fresh subagents (the
  environment's equivalent of agent_type=default, fork_turns=none);
  task IDs held by the Main Codex session; model info as provisioned by
  the session runtime; fields not visible to the Main Codex are
  recorded as not visible per protocol.
- Reports return to the main thread only; save-report x3 happens only
  after all three complete reports have returned.
