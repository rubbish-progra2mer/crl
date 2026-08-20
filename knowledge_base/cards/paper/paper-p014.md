<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p014","card_kind":"paper","paper_id":"P014","evidence_ids":["ev-p014-dynamic-reflection-gate","ev-p014-external-instructor-confound"],"source_refs":[{"path":"papers/P014_instruct_of_reflection.pdf","sha256":"57a01e87496308e3345839c48f085516dd2824ec5aaacf51b71f127c12f42bb7"}]} -->
# Instruct-of-Reflection: Enhancing Large Language Models Iterative Reflection Capabilities via Dynamic-Meta Instruction

## Role in the knowledge base
[CODEX_SYNTHESIS] Reflection controller source with a clear external-instructor attribution boundary.

## Problem and setting
[CODEX_SYNTHESIS] Iterative answering where a meta-thinker selects, stops, or refreshes reflection.

## Changed computation
[CODEX_SYNTHESIS] A controller issues select/stop/refresh instructions after comparing base and reflective answers.

## Evidence-backed findings
[AUTHOR_FACT] The source supports dynamic reflection control, while the fixed GPT-3.5 meta-thinker/instructor adds external capability. [[evidence:ev-p014-dynamic-reflection-gate]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Reported gains cannot be attributed solely to the target backbone's self-reflection.

## Lineage and baselines
[CODEX_SYNTHESIS] Adds a gate above generic reflection; relevant to stopping and selector mechanisms.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p014-dynamic-reflection-gate]] [[evidence:ev-p014-external-instructor-confound]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] Instruct-of-Reflection; select stop refresh; dynamic reflection gate; external instructor confound

