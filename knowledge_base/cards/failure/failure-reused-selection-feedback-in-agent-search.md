<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-reused-selection-feedback-in-agent-search","card_kind":"failure","paper_id":null,"evidence_ids":["ev-p057-search-evaluation-budget","ev-p058-validation-selection-loop"],"source_refs":[{"path":"papers/P057_adas.pdf","sha256":"32eb1c1a6888e35fae0f618e33c58698b54d9c49bc063fef91ee591719fca376"},{"path":"papers/P058_aflow.pdf","sha256":"9be15f695f11dd5bc634c1c026bd2270eff3d3c4a53c4d9b51c012b7bd03d521"}]} -->
# Reused Evaluation Feedback Inflates Agent-Search Selection Evidence

## Observed failure
[AUTHOR_FACT] ADAS 的 ARC search 多轮读取 held-out test feedback；AFlow 的 selection/backpropagation 反复使用 validation subset。[[evidence:ev-p057-search-evaluation-budget]] [[evidence:ev-p058-validation-selection-loop]]

## Conditions and scope
[CODEX_SYNTHESIS] 适用于 automated code/workflow discovery，不表示搜索出的程序必然无效。

## Failed intervention
[CODEX_SYNTHESIS] 把多轮 search selection 后的最好分数当作单次模型/机制效果。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 收益可来自 changed workflow，也可来自更大的 candidate/evaluation budget；两篇是相邻搜索谱系，不计作完全独立机制证据。

## Warning for future candidates
[CODEX_SYNTHESIS] 报告总候选数、总 token/calls、selection split 与未触碰 final holdout。

## Possible repair boundary
[CODEX_HYPOTHESIS] matched discovery budget 与一次性 final evaluation 能分离搜索能力和选择偏差。

## Evidence ledger
[CODEX_SYNTHESIS] 两条 Evidence 分别固定 program search 与 workflow MCTS 的复用方式。

## Retrieval vocabulary
[CODEX_SYNTHESIS] agent search selection bias; validation reuse; best-of-many workflow; discovery budget; test feedback leakage
