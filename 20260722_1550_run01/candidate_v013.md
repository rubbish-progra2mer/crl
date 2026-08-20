<!-- crl-v3-evidence-ids
["ev-p039-aggregate-score-masking","ev-p080-fixed-depth-under-over-search","ev-p080-gold-supervised-minimal-depth"]
-->
# Candidate v013 — Policy-Level BoR Consistency Audit

## Minimal implement

1. Parse the fixed BFCL simple file into query text, one gold tool, and a deterministic tool registry.
2. Reproduce the target notebook's lowercased whitespace BM25 ranking and fixed split.
3. Reproduce its two DQN policy families under seeds `42`, `123`, and `456`.
4. Freeze per-query rows before aggregate evaluation.
5. For each policy/seed, compute:
   - target notebook statistic `mean(hit * -log2(K/N))`;
   - paper-defined aggregate `log2(mean(hit) / mean(K/N))`;
   - mean K, found fraction, and query count.
6. Enumerate pairwise policy order under both metrics and record all strict reversals.
7. Run a coupled-query bootstrap for the preregistered fixed-K comparison.
8. Audit every metric from raw rows in an independent entry point.

## Fair comparators

- **Primary comparator:** the target official notebook statistic on identical policy/query rows.
- **Definition reference:** the direct aggregate formula and fixed official `bits-over-random` metric primitive.
- **Analytic controls:** fixed `K ∈ {1,3,5,10,20,50}`.
- **Policy controls:** target BoR-reward DQN and F1-reward DQN.

No metric receives different rows, seeds, split, or policy outputs.

## Development data and exposure

- Input: `sources_v013/bfcl_development/BFCL_v3_simple.json`
- Source commit: `c15b2a151662cac9839c96d7dfb1493b5329c975`
- SHA-256: `FBC37B2AD252BF9AF985582E0E07B456173FE627D957491472EA9CEF5FB83158`
- Lines: `400`
- This data and the target paper's saved outputs were inspected during selection. Development is a faithful reproduction and implementation test, not untouched confirmation.

## Frozen policy protocol

- Registry construction, question extraction, tool description text, and whitespace tokenization match the fixed target notebook.
- The query list is shuffled once with seed `42`; first 70% is training and remaining 30% is Development test.
- DQN architecture: `7 → 64 → 64 → 2` with ReLU.
- Seeds: `42`, `123`, `456`.
- Episodes, optimizer, replay, target updates, epsilon schedule, maximum K, gamma, and step costs must be copied into the one-shot Plan before execution.
- Fixed-K policies operate on the same test query ranks.
- All produced model weights and per-query outputs are frozen after Development.

## Development gates

The eight gates in `research_map_v013.md` are mandatory and conjunctive. In summary:

1. complete, valid per-query rows;
2. exact notebook-statistic recomputation;
3. exact independent aggregate-BoR recomputation;
4. bounded reproduction of official means;
5. preregistered `K=1`/`K=3` reversal;
6. learned-policy reversal in at least two seeds;
7. different maximizing policy under the two metrics;
8. at least 0.95 coupled-bootstrap sign support in both opposite directions.

The main Codex, not the experiment program, decides promotion after reading raw rows and the independent audit.

## Untouched Confirmation

Only after Development passes and the main Codex authorizes promotion:

- acquire `berkeley-function-call-leaderboard/bfcl_eval/data/BFCL_v4_live_simple.json`;
- fixed source commit: `6ea57973c7a6097fd7c5915698c54c17c5b1b6c8`;
- verify line hashes are disjoint from Development;
- apply the frozen parser, BM25, trained DQN weights, fixed-K set, metrics, and bootstrap without refitting.

Confirmation must pass every gate in `research_map_v013.md`. No alternate dataset, post-hoc pair choice, hyperparameter change, or threshold change is allowed after acquisition.

## Allowed claim

If and only if Development, untouched Confirmation, three independent Reviewers, and the main-Codex evidence decision all pass:

> On the fixed official BFCL protocols, the target notebook's mean success-weighted chance ceiling is not the paper-defined aggregate Bits-over-Random metric and can reverse policy order; therefore the reported “BoR bits” values do not establish optimization of defined BoR.

## Forbidden claims

- The target paper's raw coverage or depth results are fabricated or invalid.
- The target paper's downstream tool-choice accuracy is disproved.
- Aggregate BoR is a complete or deployment-optimal objective.
- A new adaptive-K algorithm was invented.
- The finding generalizes beyond the two fixed BFCL simple protocols.
- File existence, automated PASS labels, Reviewer voting, or fixture sanity constitutes Delivery.
