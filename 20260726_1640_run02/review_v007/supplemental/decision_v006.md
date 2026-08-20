# Main Codex Decision

```json
{
  "review_id": "v006",
  "packet_sha256": "2fe7fcebf4395b53a37cd1ff514d53df743f0e76a9f75643368c22921acaa5cd",
  "reviewer_1_sha256": "fb4ac733bb9cfc8be5b9a258b81d1d70b18281f55b05bd4fdee8f86674d2ab4c",
  "reviewer_2_sha256": "b707d54b6eab9bad3d6e812275c76f9972719ad9551b4075814d69954abaaaf0",
  "reviewer_3_sha256": "8c0e13b9a47812d91f6e9cc0d917d5727a781453bff7a88c77e5f09c7255d598"
}
```

## Main Codex Decision Text

# v006 Main Codex Decision

## Disposition

`REVISE_AS_NEW_VERSION`

This is the Main Codex's scientific adjudication after re-reading the
frozen Packet, the frozen bytes, all three independent reports and their
cited evidence, and after independently re-verifying the decisive
objections against the frozen raw data. It is not a vote count.

## Bound materials

- Packet: review_v006/packet.md, SHA-256
  2fe7fcebf4395b53a37cd1ff514d53df743f0e76a9f75643368c22921acaa5cd
- Reviewer 1 (Prior and Lineage Attacker): reviewer_1.md, SHA-256
  fb4ac733bb9cfc8be5b9a258b81d1d70b18281f55b05bd4fdee8f86674d2ab4c
- Reviewer 2 (Scientific Skeptic): reviewer_2.md, SHA-256
  b707d54b6eab9bad3d6e812275c76f9972719ad9551b4075814d69954abaaaf0
- Reviewer 3 (Implement Potential): reviewer_3.md, SHA-256
  8c0e13b9a47812d91f6e9cc0d917d5727a781453bff7a88c77e5f09c7255d598
- Private prior commitment honored: nearest_prior_v006.md SHA
  A54195906975A32BC26901DE8828CF6EB78B213C74B9AD7710F79B2DDEE6D588,
  body excluded from the Packet; no reviewer read it (each attests so).

## What all three reviews establish jointly

Execution integrity is confirmed at an unusual depth: all three
reviewers independently verified every manifest SHA (55 items, zero
mismatches); R2 and R3 independently recomputed every headline number
from frozen raw bytes and reproduced all of them exactly; R2 verified
bit-identical prompts across the v005/v006 reader attempts via
identical per-pair prompt tokens; R1's open-web search (11 query
families, 10 primary documents read) found no occupant of the
composition and confirmed every occupancy-scan characterization was
accurate. No fabrication, no leakage, no judge circularity, no
self-serving scoring bias (R2's arm-symmetry analysis). The machine's
execution chain held.

## Objection-by-objection disposition

### Credible fatal objections (accepted; they block v006 delivery)

R2-F1 (consequence not quantified): ACCEPTED. Verified: McNemar
turn-vs-oracle p=0.727, turn-vs-sentence p=0.289; all bootstrap CIs
include zero. The candidate's claim contract promised a "quantified
answer-error increase"; at n=37 only direction is supported. The claim
text as frozen is stronger than the evidence.

R2-F2 (item-level conversion sentence false): ACCEPTED and
INDEPENDENTLY VERIFIED by the Main Codex against frozen
development_raw.jsonl before this Decision: items 59524333 and c7dc5443
have cur_rank=0 (current retrieved FIRST), yet produced stale answers -
they are reader/context-composition failures, not retrieval-inversion
conversions; and inverted items show no higher error rate (4/22) than
non-inverted (3/15). The sentence "exactly the answer-level conversion
of the retrieval-stage inversion" in frozen result_v006 is false as
written. R3's reading of the same five answers as "mechanism trace" is
partially rescued at the aggregate level (5 stale answers exist under
turn context and vanish under sentence context) but the item-level
causal wording is refuted by the packet's own bytes.

R2-F3 (chance bar): ACCEPTED. The 40% threshold was preregistered but
never derived; against the natural 50% exchangeability null, 22/37
gives p=0.162. The supported finding is temporal BLINDNESS (retrieval
indifferent to currency where the task requires strong currency
preference), not "inversion above chance". This reframing survives and
remains decision-relevant, but it is a weaker sentence than the frozen
claim.

R1-fatal-genus / R3-fixable-1 (frozen result misdescribes raw bytes):
ACCEPTED, independently confirmed by two reviewers and re-checked by
the Main Codex: 031748ae_abs/turn_topk did not abstain; turn is 29/37,
not 30/37; "12 verdicts" should be 11. Error direction is conservative
(against the favored conclusion), but a frozen result that misstates
frozen raw data cannot underpin a Delivery.

### Credible fixable objections (accepted; scheduled for v007)

R2-F4 date-tie defect (618f13b2; two programs tie-break oppositely) -
accepted; verified the date collision in the split-referenced data.
R2-F6 equal-cap-not-equal-spend (realized 1399/466/1478 tokens) -
accepted; wording change plus length-matched control registered for
scale-up. R2-F7 band-size 9/14 vs 10/14 - accepted (also found by R3).
R2-F8 churn under net dilution (12 fixed / 6 created) - accepted;
transition matrix must be reported. R2-F9 / R1-5.3 / R3-fixable-4
isomorphism-as-residue - accepted; wording demoted to
"residual consistent with phrasing isomorphism (unreported proxy:
q_overlap 0.696 vs 0.501)"; paraphrase ablation registered as the
direct falsifier at scale-up. R1-5.2 missing named neighbors
(MemConflict 2605.20926; Collapse of Dense Retrievers 2503.05037;
MemoryAgentBench FactConsolidation; Dense X 2312.06648; SGMem
2509.21212) - accepted; must be added with explicit differences.
R2-F10 C-file wording ("no C item's content or outcome was ever
computed or read" replaces "never loaded") - accepted. Judge freezing
(all three reviewers) - accepted.

### Objections weighed but not blocking

R2-F11(b) rerun-after-confounded-signal: the objective 47/111
starvation defect forced the rerun regardless of direction;
bit-identical prompts verified; residual risk noted in the record.
R3's "proceed conditional on repairs" and R1's "no lineage fatality"
do not outvote R2's claim-text fatalities; no vote is taken. One
credible unresolved fatal objection blocks delivery; here there are
three against the claim text, all verified.

## Supported and unsupported claims

Supported (the v007 claim ceiling): temporal blindness of turn-level
schema-free retrieval on update questions (22/37, CI 43.5-73.7%,
direction-consistent with W); sentence-level granularity share (net
22->16 via 12 fixed/6 created; margin -0.049->-0.020; non-update hits
6.52->8.06); propagation ~0 (23/37); recency trade-off (6/37 vs
non-update harm 6.52->5.91); five verbatim stale answers under turn
context, absent under sentence context, with all pairwise accuracy
deltas inside wide CIs at n=37; residual consistent with phrasing
isomorphism per unregistered proxy. All scoped to this
dataset/encoder/reader/harness.

Unsupported (per reviews; enforced): quantified answer-error increase;
item-level inversion-to-error conversion; inversion above 50% chance;
isomorphism as measured dominant mechanism; equal budget (vs equal
cap); any cross-anything generalization; any repair-effectiveness
claim; any Confirmation-grade status (D was partially exposed; C
remains the only clean set).

## Decision and evidence reason

REVISE_AS_NEW_VERSION. The execution record is sound and the harness
is verified reusable - the artifact survives review. The claim text
does not: three verified fatal objections attack exactly the sentences
that carried the delivery case. Per CRL rules, frozen bytes are not
edited; v007 must:

1. Rewrite the Minimal Claim Contract to the supported-claims ceiling
   above (temporal-blindness framing, intervals everywhere, net-of-
   churn dilution, residual-attribution wording, equal-cap wording,
   drop the item-level conversion sentence).
2. Correct the scoring record (29/34/32 post-review; 11 verdicts),
   freeze the judge script and the full 111-row verdict table as
   artifacts.
3. Fix/disclose the date-tie item and unify tie-breaking; fix band-size
   9/14; relabel oracle arm as current-session control.
4. Add the five named nearest neighbors with explicit differences.
5. Preregister severe C-bucket gates (inversion CI excluding 0.5;
   paired reader delta excluding 0), stating openly that C's 27 update
   items are likely underpowered for the consequence gate and that the
   consequence claim therefore rides on the receiver's second-dataset
   step; the machine does not run C (reserved handover unchanged).
6. Refreeze the Packet and rerun three fresh reviewers on v007.

No kernel change, no new experiment is required for v007; this is a
record-and-claim repair version. The Run continues ACTIVE. This
negative-for-delivery outcome is the review system working as
designed: two of three reviewers and the Main Codex independently
caught a claim-evidence gap that the Promotion pipeline missed.

`DELIVERY.md`: forbidden for v006.
Run status after Decision: ACTIVE, CURRENT_VERSION advances to v007.
