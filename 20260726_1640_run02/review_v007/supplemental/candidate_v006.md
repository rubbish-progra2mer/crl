<!-- crl-v3-evidence-ids
["ev-p010-index-retrieve-read","ev-p030-failure-core","ev-p011-failure-core","ev-p064-experience-following-error"]
-->
# Candidate Implement

## Version lineage

candidate_v006 = candidate_v005 (SHA aa99d8c63cc631ca3ce8057408c7f7edea
060820098a3d50ac9c6b9a28e22da0) with a single Implement-contract
amendment; all sections not restated here are incorporated by reference
and remain binding.

## Amended Implement contract

implementation_v006/config.json: reader.max_tokens = 1000 (was 100).
Reason: v005 dev_reader_001 established that deepseek-v4-flash spends
reasoning tokens inside max_tokens; 100 starved 47/111 answers
(arm-varying, confounding). All other parameters, prompts, arms, data
roles, kill conditions, claim contract and forbidden extensions are
unchanged from candidate_v005.

## Data roles and freshness (restated for clarity)

WORKBENCH: W bucket (exposed). PROMOTION_DEVELOPMENT: D bucket - its
retrieval-stage outcomes were read in v005 (decomposition replicated;
kills 1-2 not triggered); the reader-stage outcomes were structurally
invalid (empty/truncated) and carried no usable signal, but v006
honestly treats D as PARTIALLY EXPOSED: the consequence-arm rerun tests
a preregistered directional hypothesis fixed before any valid reader
outcome existed, and the unchanged kill condition 3 remains its only
gate. CONFIRMATION: C bucket untouched, reserved.
