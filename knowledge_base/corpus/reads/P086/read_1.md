# P086 first read — hypothetical tool and required-parameter retrieval is direct prior

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Meta-Tool: Unleash Open-World Function Calling Capabilities of General-Purpose Large Language Models
- Authors: Shengqian Qin; Yakun Zhu; Linjie Mu; Shaoting Zhang; Xiaofan Zhang
- Venue: ACL 2025 Long Papers, Anthology `2025.acl-long.1481`
- Official landing page: `https://aclanthology.org/2025.acl-long.1481/`
- PDF: `knowledge_base/staging/plan06_prior_gap/P086_meta_tool.pdf`
- PDF SHA-256: `02064499a8345eb333e4fdd71abaa5ee69133af5be7b81626ba09816f48d194b`
- Parse check: 25 physical pages

## Canonical operator contribution

Meta-Tool is a direct prior for query-side schema-aware tool retrieval. The LLM first hypothesizes a desired tool description and descriptions of its parameters, then a retriever scores candidate tools using both tool-description similarity and required-parameter-description similarity before invocation. This is not merely “JSON validation”: it changes which tools are selected by explicitly matching parameter semantics.

## Evidence and closest lineage

- Meta-Tool exposes one gateway tool in the prompt. When a needed function is missing, the LLM emits `tool_description` and `param_description`, retrieval returns candidate tools, and the LLM invokes the result.
- For each required parameter in the hypothesized tool, the method takes the maximum cosine similarity against required parameters of a candidate, averages those matches and combines the result with tool-description similarity by a weighted sum.
- Meta-Bench contains 2,800 dialogues and 7,361 tools across open/closed-world, simple/hard, function-missing, function-existing and chat cases. Each function-missing case uses a 1,000-tool pool.
- Against keyword retrieval, Meta-Tool improves reported hard-case retrieval across the tested models. For GPT-4o, hard HR@5 is 49.13 versus 21.30 for keyword retrieval; results vary substantially by generator/model.
- Meta-Tool separately measures function-missing detection, retrieval hit rate, tool selection, parameter selection and irrelevance detection, preventing a valid call format from standing in for the full mechanism.

## Measurement and fairness boundaries

- Training and benchmark examples are sampled from nearly identical distributions, and identical or functionally similar tools may occur in both. This limits claims about out-of-distribution open-world transfer.
- The data pipeline automatically rewrites tool and parameter descriptions and uses GPT-4o for reasoning/consistency checks. Generated supervision and its verification are therefore model-dependent.
- Parameter matching compares descriptions of required parameters; it does not bind concrete user values to paths or prove correct argument construction.
- The reported advantage combines the LLM's hypothetical-tool generation quality with the matching rule. It does not isolate the parameter term for every model/task condition.
- The fine-tuned MT-LLaMA is evaluated only at 8B scale, and the paper's own limitations do not establish preservation of general capabilities beyond irrelevance detection.

## Draft knowledge objects

### Operator draft: `Hypothesize–Retrieve–Invoke with Required-Parameter Matching`

Ask the Agent to describe the missing tool and its required parameters in tool-schema language, then score real tools by a weighted combination of tool-description similarity and best-match required-parameter similarity. The operator changes retrieval computation before invocation and is a mandatory closest-composition comparator for later parameter/schema-aware routing ideas.

### Failure draft: `Query Text Alone Under-Specifies Needed Tool Semantics`

Dialogue-history or keyword retrieval can collapse on hard open-world cases because the user text does not directly express the desired tool interface. A valid downstream call cannot repair a wrong or missing retrieved tool.

## Draft Evidence locators

- Physical pp.1–4: open-world formulation, hypothesize–retrieve–invoke framework and comparison to dialogue/keyword retrieval.
- Physical p.4 and Algorithm 1: tool-description plus required-parameter matching computation.
- Physical pp.5–8: benchmark categories, metrics, baselines and retrieval results.
- Physical pp.9 and 11–13: limitations, same-distribution construction, rewriting and verification pipeline.

All claims remain draft until independent read and reconciliation.
