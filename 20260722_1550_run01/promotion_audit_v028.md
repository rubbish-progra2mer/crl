# Main Codex Promotion Audit v028

Disposition: `NO_GO_FOR_CONFIRMATION`.

The Development capture is mechanically valid and the independent replay is exact. The negative decision is scientific, not an execution defect.

MFCR improves the monolithic full-schema cross-encoder from top-1 `0.920` to `0.935`, with four corrections and one regression. That improvement cannot be attributed to the proposed menu-relative pairwise field contrast:

- `equal_fields`, which removes learned supervision, has the same top-1 and MRR;
- `pointwise_fields`, which removes the menu-pair objective, has the same top-1 and MRR;
- Candidate and both controls have identical per-row reciprocal rank on all 200 rows;
- Candidate-minus-strongest bootstrap is identically `[0.0, 0.0]`;
- all five fold improvements over the strongest control are `0.0`.

Thus the observed gain over the full-schema baseline belongs at most to deterministic field segmentation/aggregation, not to MFCR’s claimed changed computation. Four of seven prospective gates fail, including the absolute top-1, strict-control, bootstrap and positive-fold gates.

The exposed Development set cannot be used to retune MFCR weights, learner, fold, field composition, controls, gates or Claim. BFCL v4 live-multiple remains unacquired and unread. No Review Packet, Reviewer, Decision or Delivery is permitted for v028.

