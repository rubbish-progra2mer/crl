# P087 first read — structured tool-document expansion is a direct retrieval prior

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval
- Authors: Xuan Lu; Haohang Huang; Rui Meng; Yaohui Jin; Wenjun Zeng; Xiaoyu Shen
- Venue status: accepted ICLR 2026 Poster; the locally read bytes are arXiv:2510.22670 v1, whose benchmark name is `TOOL-DE`; the final OpenReview version renames it `TOOL-REX`
- Official landing page: `https://openreview.net/forum?id=g9D9MgG7iW`
- Read PDF: `knowledge_base/staging/plan06_prior_gap/P087_tool_rex.pdf`
- PDF SHA-256: `0e6dc98171a7ada43eb7b2a415099853afb090f29c25887d512660501d343eff`
- Parse check: 21 physical pages

## Canonical operator contribution

The paper treats missing and heterogeneous tool documentation as the source of retrieval error. Its query-independent operator expands each tool document with structured, grounded fields—function description, when-to-use, limitations and tags—then trains a dedicated dense retriever and reranker on the enriched representation. This is a direct prior for any candidate that adds schema semantics or auxiliary descriptions to improve tool selection.

## Evidence and closest lineage

- An audit of 300 ToolRet documents reports that 41.6% lack either a clear function statement or actionable usage context.
- Expansion uses Qwen3-32B; Llama-3.1-70B judges whether each field is faithful to the original documentation; roughly 1.5% failed cases are regenerated with GPT-4o; 100 refined profiles receive human validation.
- The fields are merged with original documentation. The method produces about 50k retriever-training and 200k reranker-training instances.
- Under fixed training configurations, expansion-trained Tool-Embed variants improve more than non-expansion-trained counterparts. Tool-Rank also adds more NDCG@10 on expanded documents than its non-expanded counterpart.
- Field ablations show expansion is not uniformly beneficial: example usage is neutral or harmful and is removed, while function description and tags are more consistently useful. Some dense baselines lose Recall@10 despite small NDCG gains.

## Measurement and fairness boundaries

- Expanded fields are LLM-generated. Semantic judging and a 100-example human check reduce but do not eliminate unsupported additions or systematic judge bias.
- The benchmark is derived from ToolRet, and training/evaluation both exploit the expansion pipeline. Strong performance does not prove equal gains on independently authored live tool registries.
- Expansion changes document length and lexical content; the paper reports both useful discrimination and similarity dilution. More context is not itself the mechanism claim.
- Tool-Embed and Tool-Rank require two 80GB A100 GPUs in the reported training setup, so they are nearest-prior evidence rather than a directly runnable local comparator for every CRL experiment.
- The local PDF is arXiv v1 rather than the final ICLR bytes. Final-version naming/status are provenance metadata, not evidence imported from unread final pages.

## Draft knowledge objects

### Operator draft: `Grounded Structured Tool-Document Expansion`

Before retrieval, enrich under-specified tool documentation with grounded function, usage, limitation and tag fields; preserve the original document; omit unsupported fields; and train/evaluate retrieval against the enriched representation. The changed computation is document-side semantic expansion plus learned retrieval, not runtime argument validation.

### Failure draft: `Under-Documented Tools Cap Retrieval and Reranking`

When tool documents omit function intent, use conditions or limitations, retrievers cannot reliably distinguish similar APIs and rerankers lack semantic hooks. Merely changing the decoder or validating output syntax can leave this upstream ambiguity untouched.

## Draft Evidence locators

- Physical pp.1–4: documentation failure, audit, structured fields and four-stage expansion pipeline.
- Physical pp.5–7: model training and matched expanded/non-expanded main results.
- Physical pp.7–9: field ablations, similarity dilution and evaluation-time discrimination.
- Physical pp.9–11: nearest query/document expansion lineage and scope.

All claims remain draft until independent read and reconciliation.
