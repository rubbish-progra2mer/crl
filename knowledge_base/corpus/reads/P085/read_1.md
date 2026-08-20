# P085 first read — large-corpus tool retrieval is a distinct Agent bottleneck

Status: `DRAFT_BEFORE_INDEPENDENT_READ`  
Reader: main Codex  
Read date: 2026-07-20 (Asia/Shanghai)

## Canonical source and bytes

- Title: Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models
- Authors: Zhengliang Shi; Yuhan Wang; Lingyong Yan; Pengjie Ren; Shuaiqiang Wang; Dawei Yin; Zhaochun Ren
- Venue: Findings of ACL 2025, Anthology `2025.findings-acl.1258`
- Official landing page: `https://aclanthology.org/2025.findings-acl.1258/`
- PDF: `knowledge_base/staging/plan06_prior_gap/P085_toolret.pdf`
- PDF SHA-256: `26ce2766e8c4b72e88dfd2cf93bfe56ff758fea6fe0ec0bea34228f555311d2a`
- Parse check: 28 physical pages

## Canonical failure contribution

Tool retrieval from a large heterogeneous corpus is not equivalent to choosing from a small pre-annotated menu. TOOLRET aggregates 7,615 retrieval tasks and 43,215 tools from 34 existing datasets across Web, Code and Customized domains. Strong general-purpose retrievers remain weak on complete target-tool recovery, and substituting retrieved tools for an oracle menu reduces downstream ToolBench pass rate. This is direct evidence that a CRL candidate about function calling must compare against a real retrieval stage and cannot infer semantic selection quality from JSON validity or execution rate.

## Evidence and closest lineage

- TOOLRET has 4,916 Web, 950 Code and 1,749 Customized retrieval tasks; the corresponding corpora contain 36,978, 3,794 and 2,443 tools.
- Queries are paired with one or more target tools. The benchmark reports Recall@10 and Completeness@10 because partial retrieval can still omit a tool needed by a multi-tool task.
- The evaluated sparse, dense, late-interaction, cross-encoder and LLM reranking families all remain below 35% average Completeness@10 and 52% average Recall@10 in the reported zero-shot comparison.
- Reranking is not automatically beneficial: some rerankers degrade first-stage results, so “add a reranker” is not a safe repair.
- The paper's tool-specific training data use target-aware generated retrieval instructions and hard negatives. Training materially improves retrieval, and better retrieval increases downstream ToolBench pass rates by roughly 10–20 points in the reported setting.

## Measurement and fairness boundaries

- TOOLRET merges existing datasets whose labels are not exhaustive. Functionally similar unlabelled tools can be valid alternatives, creating one-to-many false negatives; the authors retain the original labels as the intended targets.
- Generated instructions are not perfect: the reported audit finds 89.2% comprehensively describe target features and 5.9% contain hallucination.
- Fine-grained differences can reside in parameter types, language filters or scope, but the benchmark does not prove that any particular parameter-aware scoring rule solves those distinctions.
- Retrieval metrics use dataset target labels. The downstream test is limited to the paper's ToolBench setup and does not establish a universal mapping from retrieval gain to task success.
- The benchmark is English and one-shot retrieval; it does not cover iterative retrieval interleaved with execution feedback.

## Draft knowledge objects

### Failure draft: `Large-Corpus Tool Retrieval Breaks the Oracle-Menu Assumption`

When candidate tools are drawn from a heterogeneous corpus containing semantically similar functions, conventional IR models often fail to recover the complete target set. A function-calling improvement measured with an oracle or tiny menu cannot be transferred to open-world tool selection without a retrieval comparator and complete-set metric.

### Operator draft: `Tool-Specific Contrastive Retriever with Hard Negatives`

Train a retriever on tool-retrieval instructions and target tools, with hard negatives mined from the actual corpus, rather than assuming a general-purpose embedding model is tool-savvy. Its changed computation is learned query–tool scoring; it is a retrieval baseline/operator, not a semantic correctness guarantee for downstream calls.

## Draft Evidence locators

- Physical pp.1–4: problem statement, corpus scale, dataset composition and retrieval metrics.
- Physical pp.5–10: benchmark construction, model families, main retrieval results and downstream ToolBench effect.
- Physical pp.18–21: training-data construction, hard negatives and detailed data quality.
- Physical pp.9–10 and limitations: false-negative, parameter/scope, language and one-shot boundaries.

All claims remain draft until independent read and reconciliation.
