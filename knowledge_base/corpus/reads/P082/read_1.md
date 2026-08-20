# P082 first read — self-supervised utility filtering for tool-call learning

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Toolformer: Language Models Can Teach Themselves to Use Tools
- Authors: Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, Thomas Scialom
- Venue: NeurIPS 2023
- PDF: `knowledge_base/staging/plan05_sat_a3/P082_toolformer.pdf`
- PDF SHA-256: `6d7483d94653008e40c2058a1c22441c92e3713dae278b6361e8efc447c99522`
- Parse check: 17 physical pages

## Changed computation

Toolformer has a language model propose candidate API calls from a few demonstrations, executes them, and retains a call only when including its result reduces weighted future-token loss relative to no call or a call without a result. The filtered calls are interleaved into the original corpus for language-model fine-tuning, teaching when, which, and how to call tools.

## Evidence and closest lineage

- Calls are represented inline as textual API name, arguments, and result. Candidate positions and calls are sampled from the model itself.
- The utility test compares loss with the result against the minimum loss from no call and a call lacking its result; only calls clearing a threshold survive.
- Experiments use GPT-J-6.7B and five tools: QA, Wikipedia search, calculator, translation, and calendar. Tool-enabled zero-shot performance improves on several factual, math, QA, multilingual, and temporal datasets.
- Tool-disabled perplexity remains close to the continued-pretraining baseline, but task gains and useful calling emerge only above roughly 775M parameters in the reported scale study.

## Measurement and fairness boundaries

- The filter optimizes future-token likelihood, not task success, truthfulness, safety, or downstream utility. Some irrelevant calls still reduce perplexity and survive.
- More than one million documents can yield only a few thousand calculator examples; the pipeline is sample- and compute-intensive, using up to 25k examples per API and eight A100-40GB GPUs.
- The model can make at most one API call per input in evaluation and cannot chain tools, browse several results, reformulate a failed query, or interact with a tool.
- Call decisions are prompt-sensitive and do not incorporate tool-specific latency or monetary cost.
- The QA and search tools themselves are learned/retrieval systems, so gains are partly bounded by tool quality and dataset overlap.

## Draft knowledge objects

### Operator draft: `Loss-Utility-Filtered Self-Supervised Tool Calls`

Let the model propose tool calls, execute them, and retain only examples where the returned result improves prediction beyond both no call and a result-free call before fine-tuning on the augmented corpus.

### Failure draft: `Likelihood Utility Does Not Guarantee Agent Utility`

A call that predicts nearby text can be irrelevant, unsafe, expensive, or unhelpful to the actual task; model-derived filtering also becomes extremely sparse for some tools.

## Draft Evidence locators

- pp.1–4: sampling, execution, loss comparison and fine-tuning mechanism.
- pp.5–9: data scale, baselines, downstream results and model-size threshold.
- pp.9–11: retained-call quality and explicit limitations.
- pp.15–17: thresholds, heuristics, compute and training details.

All claims remain draft until independent read and reconciliation.
