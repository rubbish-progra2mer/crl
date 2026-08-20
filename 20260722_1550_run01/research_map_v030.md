# Research Map v030

## Failure evidence

- `failure-semantically-related-toolkit-expansion`: P084 shows that related-function menus induce wrong-function and argument failures under a controlled expanded-tool condition.
- `paper-p085`: ToolRet warns that tool-retrieval labels can be non-exhaustive because similar tools from other sources may be valid alternatives.
- BFCL's official merged history contains concrete repairs to questions and possible answers, demonstrating that syntactic validity alone does not establish benchmark-contract consistency.

## Nearest prior boundary

EigenData directly audits and repairs BFCL schemas, implementations, intents and trajectories with a multi-agent platform, then evaluates repaired tasks with outcome-aware and human judgments. It is a stronger and broader system prior.

v030 does not claim to replace EigenData or invent benchmark auditing. Its testable delta is:

1. a deterministic typed-fact projection with no generated judgments;
2. a patch-localization endpoint evaluated on the original pre-fix bytes;
3. maintainer-merged changed entries as external revision labels;
4. a chronological, content-unopened Confirmation set.

PairReranker, PRP, PRP-Graph and MagicSelector are negative collision evidence for the rejected reranking route and are not components of v030.

## Candidate computation

For each entry, create typed facts from:

- user/system text;
- function names and recursive parameter schemas;
- embedded or joined reference calls;
- literal strings, numbers, dates, weekdays, units and file paths;
- call order for multi-turn reference traces.

Compute six fixed violation channels:

1. `schema_reference`: referenced function or parameter keys absent from the supplied schema;
2. `path_dependency`: near-identical but unequal file paths across producer/consumer calls;
3. `unit_contract`: query units incompatible with units explicitly required by the schema;
4. `calendar_contract`: explicit weekday/date contradictions;
5. `literal_provenance`: long reference strings or nontrivial numeric values unsupported by query/reference predecessors;
6. `identity_integrity`: duplicate IDs in the candidate file.

The Candidate score is the preregistered severity-weighted sum:

```text
4*schema_reference
+ 4*path_dependency
+ 4*unit_contract
+ 4*calendar_contract
+ 2*literal_provenance
+ 4*identity_integrity
```

Ties are resolved by ascending SHA-256 of `pr_number || entry_id`. No post-fix value enters a score.

## Mandatory Development comparators

- `schema_only`: `schema_reference`;
- `dependency_only`: `path_dependency`;
- `temporal_unit_only`: `unit_contract + calendar_contract`;
- `literal_only`: `literal_provenance`;
- `size_only`: UTF-8 byte length of the pre-fix entry;
- `unweighted_union`: count of nonzero violation channels.

All comparators use the same pools, labels and deterministic tie rule.

## Development gates

All gates are conjunctive:

1. all 8 PR metadata records are merged and all scored features use only verified base bytes;
2. exactly 9 changed entry IDs are recovered from the fixed Development patches and are present in their base pools;
3. no head/post-fix value is read by the scoring path;
4. Candidate per-PR mean reciprocal rank is at least `0.60`;
5. Candidate changed-entry Recall@10 is at least `8/9`;
6. Candidate MRR exceeds the strongest mandatory comparator by at least `0.10`;
7. a 20,000-resample PR-cluster bootstrap 95% lower bound for that MRR delta is above zero;
8. at least `6/8` PRs place a changed entry in the top 10;
9. Candidate rankings are not identical to any mandatory comparator;
10. the independent auditor reproduces every feature, label, ranking and metric exactly from frozen bytes.

The main Codex must read the raw ranked pools and patched cases before promotion. A script's gate field cannot authorize Confirmation.

## Conditional Confirmation

Only after a positive Main-Codex Development Promotion Audit may the exact file listings and pre/post bytes for PRs `1084, 1085, 1086, 1087, 1175, 1177` be acquired.

The Candidate code, channels, weights, parsing, tie rule and comparators remain frozen. Confirmation gates are:

1. exact acquisition and base-only scoring integrity;
2. changed-entry Recall@10 at least `0.60`;
3. per-PR MRR at least `0.45`;
4. MRR exceeds the strongest comparator by at least `0.05`;
5. PR-cluster bootstrap 95% lower bound for the MRR delta is above zero;
6. at least `4/6` PRs place a changed entry in the top 10;
7. independent audit agreement is exact.

## Maximum Claim

If and only if Development, untouched Confirmation, three independent Reviewers and the main-Codex decision all pass:

> On the fixed historical BFCL repair PRs, Revision-Grounded Typed Contract Audit uses only pre-fix query/schema/reference bytes to prioritize the entries maintainers later patched, outperforming the specified single-channel and size baselines on both chronological partitions.

No claim may state that all patches are correct, all benchmark defects are detected, RTCA repairs data, or patch localization equals downstream model validity.
