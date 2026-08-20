# OADD-Bench

OADD-Bench evaluates whether a system can identify database columns that can
scientifically support a broad research question. This release contains 160
questions about the Health and Retirement Study (HRS), exact-column targets,
short operationalization explanations, a detailed evidence ledger, and six
no-API baseline implementations.

The repository intentionally ships **before execution**: all required source
data and code are present, but generated metadata, indexes, model caches,
predictions, and score files are not.

## Fastest start: run BM25

Run the following commands from the repository root. Python 3.10 or newer is
required.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

# Check that the release is complete.
python verify_artifact.py

# Reconstruct the complete searchable HRS metadata from bundled snapshots.
python benchmark/HRS_metadata/prepare_metadata.py

# Produce predictions and score them.
python Methods/run.py --method bm25
python evaluate.py results/bm25.jsonl
```

The metadata reconstruction is offline and creates
`benchmark/HRS_metadata/metadata.jsonl`. The baseline creates reusable indexes
under `cache/` and predictions under `results/`. All three locations are
ignored by Git. The evaluator prints recall at the target-relative output
budgets $R$, $2R$, and $5R$, where $R$ is the number of reference columns for
that question.

## Run the other methods

BM25 and TF–IDF use `requirements.txt`. Install the neural dependencies once
before running BGE-base, SPLADE++, or rank fusion:

```bash
python -m pip install -r requirements-neural.txt
```

| Method | Command | Additional requirement |
|---|---|---|
| BM25 | `python Methods/run.py --method bm25` | None |
| TF–IDF | `python Methods/run.py --method tfidf` | None |
| BGE-base | `python Methods/run.py --method bge-base` | Neural dependencies; downloads public weights on first use |
| SPLADE++ | `python Methods/run.py --method splade++` | Neural dependencies; downloads public weights on first use |
| Four-way rank fusion | `python Methods/run.py --method rank-fusion` | Runs or reuses all four indexes above |

Each command writes `results/<method>.jsonl`. Score it with:

```bash
python evaluate.py results/tfidf.jsonl
```

Replace the filename with the method just run.

Neural methods use CPU inference by default. If ONNX Runtime with a compatible
CUDA provider is installed, add `--provider cuda`. Index construction is the
longest step and is reused on later runs.

### Adapted RESDSQL ranker

The sixth method adapts RESDSQL's released, non-generative schema-item
classifier. Its third-party source and large checkpoint are not redistributed.
Only the `text2sql_schema_item_classifier` checkpoint is needed; the T5 SQL
decoder is not.

1. Clone the [official RESDSQL repository](https://github.com/RUCKBReasoning/RESDSQL)
   and check out commit `7472f7a51fdd054d8139b1bc2627d955aff855e4`.
2. Download and extract the official `text2sql_schema_item_classifier`
   checkpoint linked under **Inference → Prepare Checkpoints** in its README.
3. Run:

```bash
python -m pip install -r requirements-resdsql.txt
python Methods/resdsql.py \
  --official-repo /path/to/RESDSQL \
  --checkpoint-dir /path/to/text2sql_schema_item_classifier
python evaluate.py results/resdsql.jsonl
```

CPU execution is supported. With compatible PyTorch and ONNX Runtime CUDA
installations, add `--provider cuda --device cuda`.

## Evaluate a new OADD method

A method should use the research question, allowed years, and HRS metadata. It
must not use the source paper, explanation, provenance, or target identifiers
while producing predictions. The reference size $R$ is supplied only to set
the output budgets.

Write one JSON object per benchmark record:

```json
{"record_id":"oadd-hrs-...","predictions":{"1":["COL_A"],"2":["COL_A","COL_B"],"5":["COL_A","COL_B","COL_C"]}}
```

The `1`, `2`, and `5` arrays must contain unique exact HRS identifiers and may
contain at most $R$, $2R$, and $5R$ identifiers, respectively. Include all 160
record IDs, then run:

```bash
python evaluate.py /path/to/predictions.jsonl
```

Use `--benchmark /path/to/OADD_Bench.csv` with either a runner or evaluator to
select a different benchmark file. `python Methods/run.py --help` lists the
remaining path, cache, device, and diagnostic options.

## Release contents

```text
benchmark/
  HRS_metadata/
    raw_codebooks/             official raw HRS documentation snapshots
    raw_manifest.json          snapshot source and product provenance
    metadata_fixes.jsonl       29 verified parser omissions
    prepare_metadata.py        offline metadata reconstruction
  OADD-Bench/
    OADD_Bench.csv             questions, targets, and explanations
    OADD_Bench_evidence.jsonl  detailed paper-use and grounding records
Methods/
  run.py                       five direct-retrieval methods
  retrieval.py                 shared family-level retrieval implementation
  resdsql.py                   adapted non-generative schema ranker
  schema.py                    table-column representation for schema linking
evaluate.py                    target-relative exact-column recall
verify_artifact.py             release-integrity check
```

`OADD_Bench.csv` is the convenient benchmark view. Its leading fields are the
record ID, research question, allowed years, target identifiers, and concise
explanation. `OADD_Bench_evidence.jsonl` preserves the more detailed grounding
record and accounts for every released target identifier.

## Common problems

- **`Missing ... metadata.jsonl`:** run
  `python benchmark/HRS_metadata/prepare_metadata.py` from the repository root.
- **A neural model cannot be downloaded:** the first neural run requires an
  internet connection; subsequent runs use `cache/models/`.
- **`CUDAExecutionProvider is unavailable`:** omit `--provider cuda` to use
  CPU, or install an ONNX Runtime build compatible with the local CUDA stack.
- **RESDSQL checkpoint error:** pass the extracted directory that directly
  contains `dense_classifier.pt`.

The raw codebooks are snapshots of public HRS documentation. Consult the
[HRS website](https://hrs.isr.umich.edu/) for current documentation and terms.
