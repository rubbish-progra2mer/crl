# v007 Relocation Replay Invocation

## Scope

This is a relocation acceptance replay of the byte-identical v006 calibration and blind inputs. It is not a newly generated blind set and makes no new retrieval-quality claim. The only intended source change is the canonical `knowledge.sqlite` update of 87 `papers.fulltext_path` values recorded in `relocation_manifest.json`.

The initial executions used working copies of the two scripts. Immediately afterward, those exact bytes were frozen here as:

- `relocation_replay.py` — SHA-256 `4f2df8f60791bb6c8ffdaf9c3f68086e2cfe1ec59d2b84090e1377b4bc545bcd`
- `relocation_replay_compare.py` — SHA-256 `ace5a9bbd5df34f86cef13cc15998973abda4e5112ca4de4202ea59ac3e0ffe9`

The commands below are the product-local replay form of those byte-identical executions. Working directory: `D:\Desktop\crl\crl_agent_v3`. Interpreter: `D:\Desktop\crl\crl_agent_v3\.venv\python.exe` (Python 3.11.15).

## Calibration

```powershell
& '.\.venv\python.exe' -X utf8 'knowledge_base\evaluation\production_eval\v007\relocation_replay.py' --project-root 'D:\Desktop\crl\crl_agent_v3' --split calibration --queries 'knowledge_base/evaluation/production_eval/v007/calibration_queries.json' --queries-sha '5c6b08c2e1d63f66c68c159a52a5611a03267139ba285b04e4ec000e84e293c3' --judgments 'knowledge_base/evaluation/production_eval/v007/calibration_judgments.json' --judgments-sha '9c6b25016ae9c8c2692e7c0935fdcddaeac4b48f7d060aab00db0783fcc7c3aa' --output 'knowledge_base/evaluation/production_eval/v007/calibration_results.json'
```

Actual result created at `2026-07-22T12:19:26.328761+08:00`: 20 queries; critical 8/8; four ordinary Card top-5 misses (`prod-cal-operator-002`, `prod-cal-operator-006`, `prod-cal-paper-002`, `prod-cal-operator-007`); five Passage diagnostic hits; no degraded queries; verdict `PASS`.

## Blind

```powershell
& '.\.venv\python.exe' -X utf8 'knowledge_base\evaluation\production_eval\v007\relocation_replay.py' --project-root 'D:\Desktop\crl\crl_agent_v3' --split blind --queries 'knowledge_base/evaluation/production_eval/v007/blind_queries.json' --queries-sha 'd8695840b89cf56501984e8cf0a06bcf8a10cf0a5c4098e577aa6d7473f9b743' --judgments 'knowledge_base/evaluation/production_eval/v007/blind_judgments.json' --judgments-sha 'b8855ba8c2bd450715761b3c668bb9fc2525e692670a858bc0b164cd555bc7ea' --output 'knowledge_base/evaluation/production_eval/v007/blind_results.json' --report 'knowledge_base/evaluation/production_eval/v007/report.md'
```

Actual result created at `2026-07-22T12:19:57.121974+08:00`: 18 queries; critical 4/4; two ordinary Card top-5 misses (`v006_bq_17`, `v006_bq_18`); seven Passage diagnostic hits; no degraded queries; verdict `PASS`.

Both runs emitted an unauthenticated Hugging Face Hub warning while loading the cached encoder weights; neither result reported retrieval degradation or a frozen-input mismatch.

## Exact normalized comparison

```powershell
& '.\.venv\python.exe' -X utf8 'knowledge_base\evaluation\production_eval\v007\relocation_replay_compare.py' --project-root 'D:\Desktop\crl\crl_agent_v3' --output 'D:\Desktop\crl\crl_agent_v3\knowledge_base\evaluation\production_eval\v007\revealed_regressions\relocation_replay_comparison.json'
```

`relocation_replay_comparison.json` proves exact equality of the complete per-query objects and summaries for both splits. Therefore rankings, hits, source-chain results and decisions are all unchanged. Only `created_at`, `evaluation_id`, `frozen_inputs` and `index_status` differ at the top level, as required by the database-path relocation.
