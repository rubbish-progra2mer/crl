# Production retrieval v006: one-shot hidden evaluation invocation

- Task ID: `prod-v006-one-shot-evaluator`
- Started at: `2026-07-20T22:03:00+08:00`
- Role: fresh mechanical evaluator, not scientific Reviewer and not Candidate judge.

## Frozen inputs

- Blind queries: `knowledge_base/evaluation/production_eval/v006/blind_queries.json`
- Blind-query SHA-256: `d8695840b89cf56501984e8cf0a06bcf8a10cf0a5c4098e577aa6d7473f9b743`
- Blind judgments: `knowledge_base/evaluation/production_eval/v006/blind_judgments.json`
- Blind-judgment SHA-256: `b8855ba8c2bd450715761b3c668bb9fc2525e692670a858bc0b164cd555bc7ea`
- Manifest: `801d44135f74a05653c4ee26c2731694460bd75047996dd22557d50ac0dc29bf`
- Evidence: `704731a935eafaa921f55d812259d96b44ad38b0de463d0e40b793ee4de60bfd`
- Knowledge DB: `29b43f517af5e3f04b46a681e128ce4cde132740cfdf4b32568b722f411ac56c`
- Passage vector index: `0c2554340178942c029464eb92359ab9e7381ba178e7cb8df8b563a13a0f464b`
- Card FTS index: `174198091e3200eec9d0c89c571325d8b8aa9e05ea784e7f630969546842e8fc`
- Card source signature: `db8d7ef02f1bc084bea075d8f36bb9da12c2a17dcf52aee43b0639eee412f4de`
- `crl_v3/retrieval.py`: `13e73c964984f970458cb09de8754eb6ef9e90df2fa42920fea618eee06308e4`
- `crl_v3/cards.py`: `bc4cbe510286f003a27d51196b0e9d922f81dd0a18f0ad431f842d532272b9d6`
- One-shot script: `work/plan06_v006_retrieval_eval.py`
- One-shot script SHA-256: `c559948be54f44a6d2344dc6eb4b1f1ce325ba92f76e80ca95fbce71d88d4b2d`

The hidden annotator's raw judgment and the pre-result semantic revision are preserved. The main Codex saw `v006_bq_03` only to resolve a pre-retrieval exact-conjunction misapplication; it has not seen any v006 blind rank or result. This is a disclosed procedural limitation, not permission to alter relevance after execution.

## Required command

First verify that both official outputs are absent and the one-shot script hash matches. Then run exactly once, with a timeout of at least 180 seconds:

`D:\Desktop\crl_judge\crl_agent_v3\.venv\python.exe D:\Desktop\crl_judge\work\plan06_v006_retrieval_eval.py --project-root D:\Desktop\crl_judge\crl_agent_v3 --split blind --queries knowledge_base/evaluation/production_eval/v006/blind_queries.json --queries-sha d8695840b89cf56501984e8cf0a06bcf8a10cf0a5c4098e577aa6d7473f9b743 --judgments knowledge_base/evaluation/production_eval/v006/blind_judgments.json --judgments-sha b8855ba8c2bd450715761b3c668bb9fc2525e692670a858bc0b164cd555bc7ea --output knowledge_base/evaluation/production_eval/v006/blind_results.json --report knowledge_base/evaluation/production_eval/v006/report.md`

Do not restart after any rank/result is produced. Do not rewrite a query, alter relevance, boost, rerank, tune, or modify any frozen source. The script runs target-kind Card FTS once per query, Card→Evidence→Passage validation, and diagnostic Passage hybrid once per query. Card top-5 plus the exact source chain is the critical Gate; Passage top-k is diagnostic only.

## Isolation

Allowed: this invocation, the one-shot script, frozen v006 query/judgment files, current Card/Evidence/source assets mechanically accessed by the script, and exact output hashing after completion.

Forbidden: all v001–v005 evaluation files, v006 calibration results, CRL Runs, Candidates, experiments, reviewer reports, history/memory, and any manual inspection of per-query ranks before both outputs are saved.

After completion, return only total/critical counts, critical pass/fail, ordinary Card top-5 miss count, Passage diagnostic hit count, verdict, output SHA-256 values and integrity concerns. Do not expose query text, relevant IDs or ranks.
