# Main Codex Raw Analysis v030

Scope: frozen Development only. The fixed Confirmation PR contents remain unacquired.

## Mechanical integrity

- Development runner exit `0`, duration `0.35190270000020973` seconds, Python `3.11.15`, stderr bytes `0`.
- Raw: 1,506 JSONL rows, SHA-256 `add9d1d946809a991adfb8b64c4d3db9191c700e6d9f0746e9b45be95ba868e5`.
- Summary SHA-256 `ef938cacb741a0ece165a4ee7d91381c7469bdd962fb11b815d08d62857a3683`.
- Independent audit runner exit `0`, duration `0.3554212000017287` seconds, stderr bytes `0`.
- Audit report SHA-256 `c61b7f553f12e3089cf49cadeabe7be6da55b1e7f66f0562d1f08995cb6c1b54`, status `AUDIT_OK`.
- The independent source replay verified 31 files and 1,506 feature rows. Maximum channel, score, rank and metric errors were all zero.

I loaded all 1,506 raw rows. Every row had exactly the frozen eight fields; field error count was zero.

## Actual metrics

| Method | MRR | MAP | Recall@10 | PRs with top-10 hit |
|---|---:|---:|---:|---:|
| RTCA | 0.3136904762 | 0.3211309524 | 1.0000000000 | 8/8 |
| schema-only | 0.2428575796 | 0.2532742463 | 0.4444444444 | 3/8 |
| temporal/unit-only | 0.1987465326 | 0.1989684416 | 0.2222222222 | 2/8 |
| unweighted union | 0.1113577970 | 0.1131579122 | 0.3333333333 | 3/8 |
| literal-only | 0.0949119513 | 0.0951354597 | 0.2222222222 | 2/8 |
| dependency-only | 0.0559856334 | 0.0562075424 | 0.1111111111 | 1/8 |
| size-only | 0.0451181613 | 0.0476916908 | 0.1111111111 | 1/8 |

The strongest comparator was `schema_only`. RTCA's MRR delta was `+0.0708328966`, below the preregistered `+0.10`. Its 20,000-resample PR-cluster bootstrap interval was `[-0.0911172161, 0.2136900394]`.

The eight program gates were `5/8`. Failed gates were `candidate_mrr`, `mrr_delta` and `bootstrap_lower`.

## Every changed entry

| PR | Changed entry | RTCA rank | Active channel |
|---:|---|---:|---|
| 865 | `live_parallel_multiple_9-8-0` | 5 | literal provenance |
| 870 | `live_simple_44-18-0` | 6 | schema/reference |
| 870 | `live_simple_45-18-1` | 7 | schema/reference |
| 871 | `live_simple_165-98-0` | 1 | schema/reference |
| 872 | `live_simple_183-108-0` | 7 | schema/reference |
| 876 | `multi_turn_base_34` | 6 | path dependency |
| 892 | `multi_turn_base_180` | 6 | literal provenance |
| 962 | `exec_parallel_10` | 3 | unit contract |
| 963 | `live_simple_205-116-13` | 3 | calendar contract |

The inspected patch bytes matched the intended cases: a copied prompt literal, two stale nested keys, a required empty alternative, `rating` versus `avg_rating`, a trailing filename period, a missing exchange-rate call, feet/inches versus meter-only contract text, and Thursday versus the actual Tuesday.

## Channel behavior and false positives

Across all 1,506 rows, nonzero counts were:

- literal provenance `250`;
- calendar contract `12`;
- schema/reference `11`;
- path dependency `7`;
- unit contract `1`;
- identity integrity `0`.

Among the nine changed entries, the corresponding counts were `2,1,4,1,1,0`. Each changed entry activated exactly one channel. No changed entry demonstrated a multi-channel interaction.

The leading false positives were substantive rather than audit noise:

- `multi_turn_base_20` scored `22` in both multi-turn pools from five near-path pairs plus one literal flag, outranking each target repair.
- `live_simple_165-98-0` scored `16` as an unlabelled top entry in PR 870 and later pools; it was itself the target of PR 871. This exposes the incompleteness of per-PR changed-ID labels for general defect detection.
- PR 865 had four literal-provenance positives ahead of its changed entry.
- PR 962 had two unrelated literal-provenance rows tied above the unit-contract target.

Thus RTCA achieved perfect Recall@10 by pooling sparse specialist alarms, but not the preregistered top-rank localization. The gain over `schema_only` is not evidence for a cross-channel interaction: every positive was single-channel, `identity_integrity` never fired, and the exposed Development weights determined which alarm type won ties and cross-channel comparisons.

## Raw conclusion

The computation is mechanically valid but scientifically insufficient for Confirmation. Its absolute MRR, comparator delta and uncertainty gate all fail, while the actual raw rows do not support the proposed typed-combination mechanism.
