# Benchmarks

This directory contains benchmark metadata and preparation utilities. It does not redistribute the original datasets.

Run `search-prepare-benchmark` to convert each supported dataset into the local JSONL format used by this repository:

```json
{"id":"...","question":"...","answers":["..."],"metadata":{"benchmark":"...","split":"..."}}
```

The command only reorganizes the original question records into the fields required by the evaluation code. It does not rewrite questions, generate new answers, or modify the official evaluation content.

Keeping the original datasets out of Git reduces the risk of mixing evaluation examples with training data and complies with GAIA's non-redistribution requirement. `manifest.json` records the official source, split, license or access requirements, and evaluation metrics for all seven supported benchmarks.

The following datasets can be loaded directly from their official sources:

```bash
search-prepare-benchmark --benchmark hotpotqa --output data/benchmarks/hotpotqa.jsonl
search-prepare-benchmark --benchmark frames --output data/benchmarks/frames.jsonl
search-prepare-benchmark --benchmark gaia --output data/benchmarks/gaia_text_only.jsonl
```

MuSiQue, 2WikiMultiHopQA, Bamboogle, and BrowseComp-Plus must first be downloaded or generated through their official release procedures. After obtaining the official source file, pass its local path with `--source-path` to convert the question records into the JSONL format expected by this repository.

For BrowseComp-Plus, this conversion only prepares the official decrypted query records for the local evaluation pipeline. Retrieval and answer evaluation must still use the official fixed corpus, relevance annotations, and evaluator provided by BrowseComp-Plus.

Do not combine evaluation files with training questions. In the reported experiments, preference-construction data may only come from the HotpotQA and MuSiQue training splits and from the separately generated synthetic questions.
