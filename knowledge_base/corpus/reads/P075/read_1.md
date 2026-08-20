# P075 first read — black-box extraction from Agent long-term memory

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Unveiling Privacy Risks in LLM Agent Memory
- Authors: Bo Wang, Weiyi He, Shenglai Zeng, Zhen Xiang, Yue Xing, Jiliang Tang, Pengfei He
- Venue: ACL 2025 Long Papers
- PDF: `knowledge_base/staging/plan05_sat_a2/P075_memory_privacy.pdf`
- PDF SHA-256: `8c2cfcee69d60f4c20a959cd6b1a6a14d5f6e8d732792cf2a2b4864ac38a88cb`
- Parse check: 20 physical pages

## Changed computation

This paper is admitted primarily as negative knowledge, not as an implement Operator. MEXTRA exploits the normal retrieval path: a black-box query is phrased so that retrieved historical queries become the task target and are emitted through an action format already allowed by the Agent. Diverse queries are then generated to cover different retrieval neighborhoods. The key research lesson is that memory privacy depends on the complete retrieve-to-action path, not merely on whether raw memory is directly readable.

## Evidence and closest lineage

- On memory size 200 with 30 prompts, the paper reports extracting 50 unique historical queries from EHRAgent (top-4 edit-distance memory) and 26 from RAP/WebShop (top-3 cosine memory).
- Removing the workflow-alignment portion sharply reduces extraction, especially for the web-action Agent, supporting the mechanism that leakage must be expressed through an allowed action channel.
- Greater memory size, larger retrieval depth, more attack attempts, and knowledge of the scoring function generally increase unique extraction.
- A later QA-Agent check extracts roughly one quarter of a 200-record memory, indicating the observation is not confined to code and web-action output formats.

## Measurement and fairness boundaries

- Primary experiments use two single-agent systems with GPT-4o and static memories; the authors explicitly leave shared multi-agent memory and session control untested.
- Queries are sampled from MIMIC-III, WebShop, or MMLU, but the paper does not establish that all stored records are real private user data in a deployed service.
- Up to three execution attempts are allowed per attack prompt, so attack budget must include retries as well as nominal prompt count.
- Lower extraction with a weaker backbone can be caused by lower normal task competence, not better privacy.
- The work diagnoses leakage; it does not experimentally validate a defense. Input/output filtering, de-identification, and session isolation are discussion proposals with known utility trade-offs.
- Operational attack strings are not preserved in CRL Cards; only the failure mechanism, conditions, and measured boundaries are retained.

## Draft knowledge objects

### Failure draft: `Retrieved Long-Term Memory Can Be Laundered Through Allowed Actions`

If historical user records are inserted as demonstrations without ownership/session isolation and the Agent can be induced to treat them as the requested task object, black-box users can progressively expose memory through ordinary code, web, or answer outputs.

### Operator disposition

No positive Operator is extracted. Session isolation, de-identification, and output control are plausible repair boundaries but are not validated interventions in this source.

## Draft Evidence locators

- pp.1–4: threat model, retrieve-to-action leakage mechanism, locator/aligner distinction, and diverse-query coverage.
- pp.5–8: agent setups, metrics, main ablations, memory/retrieval/backbone factors, and prompt-budget effects.
- pp.8–9 and 15: scope, conclusion, explicit limitations, QA-Agent replication, and defense discussion.

All claims remain draft until independent read and reconciliation.
