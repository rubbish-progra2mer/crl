# Third-party notices

## The distinction that governs everything here

Two different activities get confused, and only one of them involves licences at all:

| activity | licence implication |
|---|---|
| **Running published software and reporting what it does** | **None.** No permission, no agreement, no fee. Licences govern *copying and distributing*, not *observing*. Every benchmark, product review, and security audit works this way. |
| **Copying source into this repository** | This *is* redistribution, and the licence applies. |

Nearly all of this artifact's use is the first kind: it imports the installed
package, calls it at its own default, and reports the result.

## 1. Components exercised but NOT redistributed — nothing owed

Imported from their published packages, called at their own defaults, results
reported. No code of theirs is copied into this repository.

| project | licence | what the harness does |
|---|---|---|
| `run-llama/llama_index` (`llama-index-core`) | MIT | runs `SemanticSimilarityEvaluator` at its default `similarity_threshold` (read from the installed package) |
| `langchain-ai/langchain` | MIT | replicates the documented `EmbeddingsRedundantFilter` logic at its documented default |
| `langchain-ai/langchain-experimental` | MIT | reads `SemanticChunker`'s `BREAKPOINT_DEFAULTS` from the installed package |
| `zilliztech/GPTCache` | MIT | replicates semantic-cache hit logic at the typical documented threshold |
| `explodinggradients/ragas` | Apache-2.0 | reports `SemanticSimilarity`'s threshold semantics (threshold defaults to None) |
| `sentence-transformers` (UKPLab / Hugging Face) | Apache-2.0 | runs `util.paraphrase_mining` and encoder checkpoints |
| `microsoft/semantic-kernel` | MIT | reads relevance-score defaults from source (referenced, not imported) |

Apache-2.0 §4 asks that modifications be marked and NOTICE files preserved
where present — relevant only if code is ever copied in, which it is not for
any row above.

## 2. `unworthyzeus/HyperRAG` — described, never redistributed

`harness/r13_hyperbolic/wild_instance_check.py` demonstrates the §9 no-op
pattern on a third-party repository that has **no LICENSE file** (under the
Berne default, all rights reserved; public visibility on GitHub implies no
permissive terms). No code from that repository ships here: the two functions
in that file are **written from a prose description** of what their code does
(repository, file paths, function names, and read date are recorded in the
file), not copied from it. Algorithms are not copyrightable; expression is.
The Poincaré distance formula itself is the standard textbook form, which no
one project can grant in any case.

## 3. Model weights — used, never redistributed

`nomic-ai/nomic-embed-text-v1.5`, `sentence-transformers/all-MiniLM-L6-v2`,
`sentence-transformers/all-mpnet-base-v2`, `BAAI/bge-base-en-v1.5`,
`thenlper/gte-base`, `intfloat/e5-base-v2`,
`mixedbread-ai/mxbai-embed-large-v1`, and
`cross-encoder/nli-MiniLM2-L6-H768` are downloaded from the Hugging Face Hub
at run time (once, with the network on) and pinned by revision where it
matters. **No weights are in this repository.** Each checkpoint carries its
own model licence; consult its model card before any use beyond reproducing
the paper's measurements.
