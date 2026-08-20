# Code for "How Many Tools Should an LLM Agent See?"

Vyzantinos Repantis, Ameya Gawde, Harshvardhan Singh, Joey Blackwell II

arXiv Preprint https://arxiv.org/abs/2605.24660

## Structure

Two Jupyter notebooks reproduce all results in the paper. Each cell is self-contained and runs independently (Google Colab or local).

### `01_tool_selection_downstream_validation.ipynb` — Tool selection + downstream validation (5 cells)

| Cell | Experiment | Produces |
|------|-----------|----------|
| 0 | BFCL downstream, embedding scorer, Claude Sonnet 4.6 | Section 4.3 embedding replication: BoR choice acc 96.1%, FK=5 choice acc 84.6%, medium-query 80.1% vs 50.0% |
| 1 | BFCL, BM25, 3 seeds | Table 2 row 1: BoR 90.3±2.4% at K=7.4±2.5, F1 88.9±1.4% at K=6.4±1.9, all FK baselines |
| 2 | BFCL downstream, BM25 scorer, Claude Sonnet 4.6 | Table 1: BoR 93.1% choice acc vs FK=5 87.1%, medium-query 76.8% vs 60.9%, all end-to-end numbers |
| 3 | BFCL, embedding scorer, 3 seeds | Table 2 row 2: BoR 85.0±3.0% at K=1.4±0.1, found@1=73.2%, all FK baselines |
| 4 | ToolBench, 3,251 tools, 3 seeds | Table 2 row 9: BoR 61.9±0.6% at K=4.4±0.4, F1 47.6±1.3%. Figure 1 difficulty buckets: K=2.5 (easy) to K=6.9 (very hard), hard-query found=16.7±4.3% |

### `02_retrieval_validation_and_metatool.ipynb` — Retrieval validation + MetaTool conditions (7 cells)

| Cell | Experiment | Produces |
|------|-----------|----------|
| 0 | SciFact, BM25, tabular Q-learning | Table 3 row 1: BoR K=7.2, found=78.9%, F1 K=5.0, found=66.7%, K std=3.34 vs 0.00 |
| 1 | NFCorpus, BM25, DQN | Table 3 row 2: BoR K=22.9, found=71.1%, F1 K=24.5, found=68.0%, per-R_q breakdown (dense queries K=10.3 vs 13.7) |
| 2 | MS MARCO, BM25, DQN | Table 3 row 3: BoR K=24.0, found=82.7%, FK=50 found=80.7% |
| 3 | MetaTool + BM25 scorer | Table 2 row 3, Section 4.2: BoR K=80.7, found=96.2%, 1.04 bits. F1 K=57.2, found=82.8%. Broken-scorer detection |
| 4 | MetaTool + MiniLM embeddings (step_cost=0.01, gamma=0.95) | Table 2 row 4: BoR K=2.3, found=73.3%, 4.44 bits. F1 K=3.0, found=69.0% |
| 5 | MetaTool vary-N (N=20, 50, 100), MiniLM | Table 2 rows 6-8: reward scaling (2.75/3.66/4.36), difficulty buckets at N=50 (medium 79.3%, hard 26.5%) |
| 6 | MetaTool vary-N (N=20, 50, 100), BGE | Table 2 row 5: BoR K=2.4, found=71.4% |

## Dependencies

- Python 3.10+
- PyTorch (CPU sufficient)
- sentence-transformers (MiniLM-L6-v2, BGE-base-en-v1.5)
- rank-bm25
- numpy, scikit-learn
- anthropic (notebook1 cells 0 and 2 only, requires API key)
- huggingface_hub
- ir_datasets (notebook2 cell 2 only)
- beir (notebook2 cells 0-1 only)

All dependencies auto-install via `pip` at the top of each cell.

## Running

Each cell installs its own dependencies, downloads data, trains the RL agent, and prints results. No shared state between cells.

- **Hardware**: All RL training runs on CPU. Embedding inference benefits from GPU but is not required.
- **Runtime**: Individual cells take 2-10 minutes on CPU. Downstream validation cells (notebook1 cells 0 and 2) require a Claude API key set as `ANTHROPIC_API_KEY`.
- **Reproducibility**: 3-seed cells (notebook1) use seeds 42, 123, 456. Single-seed cells (notebook2) use seed 42.

## Implementation notes

- The paper defines $P_{\text{rand}}$ using the hypergeometric distribution in the main BoR definition. For single-tool queries ($R_q=1$), this reduces exactly to $K/N$. The retrieval-validation cells (`notebook2.ipynb` cells 0-2) use the binomial approximation $1 - (1 - R_q/N)^K$ for multi-relevant queries, which is standard when $N$ is large relative to $K$.
- The `Reward (bits)` values reported for retrieval-validation results are the mean over successful queries only, i.e., conditioned on at least one relevant item appearing in the presented set.

## Mapping to paper claims

Every numerical result in Tables 1-3, all inline claims, and all difficulty-bucket breakdowns are produced by exactly one cell identified above. Cell outputs are preserved in the notebooks. To verify without re-running, inspect the saved outputs.
