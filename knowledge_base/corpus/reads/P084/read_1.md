# P084 first read — semantically related toolkit expansion destabilizes function calling

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: On the Robustness of Agentic Function Calling
- Authors: Ella Rabinovich; Ateret Anaby Tavor
- Venue: TrustNLP 2025, ACL Anthology `2025.trustnlp-main.20`
- Official PDF: `knowledge_base/staging/plan05_v004_gap/P084_function_calling_robustness.pdf`
- PDF SHA-256: `8276bcab484eef370bc63afca580ea19d8f6e2ccc6c2afcdaf684225d5e635c7`
- Parse check: 7 physical pages

## Canonical failure contribution

The paper holds the original single-turn BFCL requests and evaluated model fixed while expanding each thin toolkit with semantically related but functionally different definitions. This is direct negative evidence that adding plausible neighboring tools can destabilize both function selection and argument construction; it closes the v004 critical gap without treating tool filtering as an already validated repair.

## Evidence and closest lineage

- Expansion starts from 200 BFCL examples. Related requests are generated, corresponding JSON tool definitions are produced in the original style, and tools judged functionally equivalent to the original are filtered by a signature-similarity threshold.
- The mean visible toolkit increases from 2.7 seemingly unrelated functions to 5.6 functions, adding about three semantically related functions per case.
- Across nine evaluated agents, expanded-toolkit AST accuracy drops by 1%–8% relative to the original setup.
- Expansion-induced failures include wrong function selection, wrong number of functions, wrong parameter assignment and parameter hallucination.

## Measurement and fairness boundaries

- The comparison fixes each tested model and original user request, but it does not report matched prompt-token length; extra tool definitions necessarily increase context.
- The added functions are LLM-generated and only one author manually inspected a limited subset of generation quality. A similarity filter reduces, but cannot eliminate, functional-equivalence ambiguity.
- Evaluation uses AST construction accuracy on a single 200-example BFCL subset, not actual tool execution or multi-turn task success.
- The paper reports aggregate expansion rather than a dose-response curve over function count, so it supports an interference failure under this intervention, not a universal monotonic law.

## Draft knowledge objects

### Failure draft: `Semantically Related Toolkit Expansion Destabilizes Function Calling`

When the same request and model are exposed to additional related-but-distinct functions, function-call construction can regress through both selection and argument errors. Future tool-routing candidates must compare against all-tools exposure and preserve the same model, requests, demonstrations, allowed calls and evaluator while reporting visible-tool count and prompt cost.

### Operator disposition

No successful routing or filtering Operator is extracted. The paper measures a failure surface; its generation/filtering procedure constructs the diagnostic intervention rather than proving a deployment repair.

## Draft Evidence locators

- Physical pp.3–4: toolkit-expansion construction, equivalence filtering and mean toolkit sizes.
- Physical pp.4–5: fixed evaluation setup, accuracy degradation and error taxonomy.
- Physical p.5: single-dataset and generated-tool limitations.

All claims remain draft until independent read and reconciliation.
