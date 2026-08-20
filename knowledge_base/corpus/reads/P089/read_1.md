# P089 first read — hypothetical-tool retrieval is a direct query-rewriting prior

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: ToolDreamer: Instilling LLM Reasoning Into Tool Retrievers
- Authors: Saptarshi Sengupta; Zhengyu Zhou; Jun Araki; Xingbo Wang; Bingqing Wang; Suhang Wang; Zhe Feng
- Venue: EACL 2026 Long Papers, Anthology `2026.eacl-long.254`
- Official landing page: `https://aclanthology.org/2026.eacl-long.254/`
- PDF: `knowledge_base/staging/plan06_prior_gap/P089_tooldreamer.pdf`
- PDF SHA-256: `d13b84ab7c2a66069f8d160ab78dfb3e7efd5dabab06c219995c5f92b2093918`
- Parse check: 18 physical pages

## Canonical operator contribution

ToolDreamer moves part of tool-selection reasoning into the retrieval query. An LLM generates hypothetical tool thoughts, names and descriptions; a retriever trained to align those hypothetical tools with gold tools searches the real catalogue; and reciprocal-rank fusion merges lists from multiple hypothetical tools. This is direct prior for any candidate that generates intermediate interface descriptions or decomposes a request into latent tools before retrieval.

## Evidence and closest lineage

- Training generates as many hypothetical tools as the known number of gold tools, aligns hypothetical and gold tools with Qwen3-8B similarities plus Hungarian matching, and trains query-plus-hypothetical representations with InfoNCE negatives.
- At inference the number of needed tools is unknown. The LLM generates an open-ended set of hypothetical tools, the retriever returns one ranked list per tool, and RRF merges them.
- On ToolRet, query-plus-hypothetical retrieval improves reported average NDCG/Recall for both BM25 and Qwen3 settings. Training the Qwen retriever on aligned hypothetical tools also improves over query-only training.
- Ablations show weaker hypothetical-tool prompts hurt more than swapping the alignment embedder/algorithm. Adding the original question generally improves over hypothetical metadata alone.
- LLM list fusion improves metrics over RRF but introduces API cost, non-determinism, instruction failures and hallucinations; the proposed default retains deterministic RRF.

## Measurement and fairness boundaries

- GPT-4.1 generates the main hypothetical tools. Training generation is told the exact gold-tool count, which is unavailable at inference and can strengthen the supervision channel.
- Hungarian matching always produces a one-to-one assignment even when no semantically correct alignment exists; the authors treat it as a noisy proxy.
- Main training uses only 5,000 samples from ToolRet's roughly 200k training instances, and the paper excludes ToolRet's instruction field. The comparisons therefore answer a specific minimal-annotation setting.
- Evaluation reports retrieval metrics, not end-to-end tool execution or semantic argument correctness.
- The method adds generation latency (reported roughly 2.5–8 seconds for one example path), depends on hypothetical-tool quality and, for GPT-based generation, incurs external API cost.

## Draft knowledge objects

### Operator draft: `Hypothetical-Tool Query Expansion with Retriever Alignment`

Generate tool-interface descriptions implied by the request, align a retriever to map those descriptions to real tools, search once per hypothetical tool and fuse the ranked lists. The changed computation is query-side latent-tool expansion plus learned tool-to-tool alignment.

### Failure draft: `User Queries and Tool Descriptions Occupy Misaligned Semantic Spaces`

The request may imply a needed capability without naming it, so direct query–tool similarity misses the correct tool. Untrained hypothetical descriptions also underperform because the retriever has not learned hypothetical-to-real interface relations.

## Draft Evidence locators

- Physical pp.1–3: query/tool semantic gap, closest hypothetical-query lineage and training objective.
- Physical pp.3–6: generation, Hungarian alignment, InfoNCE representation, inference and RRF.
- Physical pp.6–9: ToolRet setup, main results, ablations, cost and limitations.

All claims remain draft until independent read and reconciliation.
