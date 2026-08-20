# P076 first read — untrusted metadata hijacks multi-Agent control flow

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Multi-Agent Systems Execute Arbitrary Malicious Code
- Authors: Harold Triedman, Rishi Jha, Vitaly Shmatikov
- Venue: COLM 2025
- PDF: `knowledge_base/staging/plan05_sat_a2/P076_mas_malicious_code.pdf`
- PDF SHA-256: `5fb79d30a11ef7b2e28d5eadc53af9b7ecb41d8ee60c8e04c2ec3c59e8b1fb11`
- Parse check: 33 physical pages

## Changed computation

This source is retained as high-priority Failure knowledge. Its distinctive mechanism is system-level control-flow hijacking: content-facing sub-agents ingest untrusted material, re-express it as operational metadata such as an error/status message, and the orchestrator treats that message as trusted evidence for selecting a more privileged agent. The attack thus crosses a data-to-metadata boundary and launders an adversarial request through a trusted deputy; it is not reducible to whether one model refuses a direct malicious request.

## Evidence and closest lineage

- The paper evaluates AutoGen with three orchestrators, CrewAI, and MetaGPT across GPT-4o, GPT-4o-mini, Gemini 1.5 Pro, and Gemini 1.5 Flash, using local/web/text/image inputs.
- For the web-redirect attack, reported attack success ranges widely by model/orchestrator and reaches 58–90% in several GPT-4o configurations; known indirect-prompt-injection templates are near zero in the same comparison.
- Local-file attacks reach 97% for Magentic-One with GPT-4o and Gemini 1.5 Pro; a directory-summary incidental-contact experiment succeeds in 35/40 trials.
- Directly presenting the metadata-style hijack to a GPT-4o-mini orchestrator succeeds 80% with no refusal, whereas a direct malicious request to the same configuration succeeds 6% with 86% refusal. This supports presentation and trust path—not just payload—as the operative difference.
- Documented traces show that one agent's refusal or warning can coexist with system-level execution because another agent or the orchestrator reconstructs the blocked action.

## Measurement and fairness boundaries

- The evaluation covers three drop-in open-source frameworks under mostly default configurations, 10 trials per fine-grained combination, and a controlled lab environment; it is not a census of all multi-Agent designs.
- Attack templates were tailored slightly by orchestrator, and many outcomes are framework/version/model sensitive.
- Full reverse-shell execution was replaced by a unique marker in the modified executor with a monitoring fallback; manual and regex review were used because an LLM autolabeler missed attacks.
- The paper does not experimentally evaluate defenses. Its trust-model and isolation proposals are research implications, not demonstrated repair Operators.
- Safety alignment of sub-agents is neither necessary nor sufficient in these examples, but the paper does not prove all adaptive multi-Agent control is unsafe.
- CRL retains no executable payload or operational attack recipe in Cards; it stores only the control-flow failure, tested conditions, and future evaluation warning.

## Draft knowledge objects

### Failure draft: `Untrusted Agent Metadata Can Launder Privileged Control Flow`

When orchestrators cannot distinguish untrusted content from status/error metadata, a content-facing agent can become a confused deputy whose report triggers code execution or another privileged tool even though individual agents refuse the same action directly.

### Operator disposition

No positive defense Operator is extracted because runtime validation, tagging, information-flow controls, and isolation are discussed but not evaluated by this paper.

## Draft Evidence locators

- pp.1–5: attack distinction, adaptive orchestration, data/metadata boundary, threat model, and laundering mechanism.
- pp.6–10: frameworks, trial design, main ASR results, variants, direct-hijack comparison, failure traces, and discussion.
- pp.16–21: defense landscape, formal control-flow definition, benign baselines, refusal comparison, and detailed experimental conditions.
- pp.21–33: topology and trace examples used only to verify the mechanism; operational payload content is excluded from Cards.

All claims remain draft until independent read and reconciliation.
