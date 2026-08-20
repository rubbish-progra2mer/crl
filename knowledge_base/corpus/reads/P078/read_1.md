# P078 first read — validated creation and retrieval of specialized tools

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: CRAFT: Customizing LLMs by Creating and Retrieving from Specialized Toolsets
- Authors: Lifan Yuan, Yangyi Chen, Xingyao Wang, Yi R. Fung, Hao Peng, Heng Ji
- Venue: ICLR 2024
- PDF: `knowledge_base/staging/plan05_sat_a3/P078_craft.pdf`
- PDF SHA-256: `59263fffdc51e21530d9dba1aeeeacefb2b5c4048012a7e385b4f555a362f155`
- Parse check: 29 physical pages

## Changed computation

CRAFT converts solved training instances into validated, abstracted Python tools, deduplicates them, and retrieves a small task-specific subset at inference. The operative change is not merely adding an API list: executable solutions must first pass the source example, survive abstraction validation, and be recalled through problem/name/docstring views.

## Evidence and closest lineage

- Tool construction follows diversity sampling, GPT-4 solution generation, execution validation, abstraction/generalization, re-validation, then deduplication by name and argument count.
- At inference, the LLM proposes useful function names and docstrings; SimCSE retrieval over the target problem, names, and docstrings is aggregated by frequency before snippets are injected.
- Evaluation uses GPT-3.5 as the answering model and GPT-4 as tool creator on VQA, TabMWP, and MATH algebra; for CRL scope, only the text/code-function mechanism is retained.
- Ablations report that abstraction and the three retrieval views matter. General libraries and LATM can hurt on some tasks, so “more tools” is not itself the mechanism.

## Measurement and fairness boundaries

- Tool creation reportedly costs roughly USD 2,500 and depends on a stronger GPT-4 creator; CRL does not execute this paid workflow without user approval.
- The source tasks and validation examples provide supervision for tool creation, creating possible dataset leakage and tool-library scale confounds.
- The method is restricted to tasks expressible through executable code; open models in the reported setup perform near random despite receiving tools.
- Toolset size, creator model strength, and retrieval quality are not fully disentangled from the method gain.
- The visual benchmark is outside the CRL target scope and is not used to justify a multimodal Operator.

## Draft knowledge objects

### Operator draft: `Validated Specialized Tool Creation and Multi-View Retrieval`

Derive reusable tools from solved task instances, validate before and after abstraction, deduplicate them, then retrieve by task, declared function name, and docstring rather than exposing an undifferentiated library.

### Failure draft: `Generic or Unvalidated Tool Libraries Can Add Distractors`

A broad API collection does not guarantee useful composition: irrelevant libraries, invalid abstractions, or poor retrieval can reduce performance even when tool count increases.

## Draft Evidence locators

- pp.1–5: problem framing and tool-creation/retrieval pipeline.
- pp.6–10: validation, abstraction, deduplication and multi-view retrieval details.
- pp.11–16: main results and comparisons.
- pp.17–22 and appendices: ablations, tool-quality analysis, cost, prompts, and limitations.

All claims remain draft until independent read and reconciliation.
