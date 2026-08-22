# BOUND: Brief-Guided Corrective Preference Distillation at Search-Control Boundaries

Implementation of **BOUND**, a framework for constructing corrective preferences at search-control boundaries and training deep-search policies with Direct Preference Optimization (DPO).

## Overview

BOUND uses a teacher-side search-state brief to assess student search decisions relative to the original task objective.

The brief contains five fields:

- `Original Search Target`
- `Key Constraints`
- `Confirmed Evidence`
- `Missing Information`
- `Drift Status`

The brief is used only during preference construction. It is not included in the student-visible training prompt and is not required at inference time.

The overall pipeline consists of:

1. preparing training questions and collecting student search trajectories;
2. constructing local chosen/rejected preferences at selected decision-time states;
3. training the search policy with DPO;
4. evaluating the trained policy under iterative retrieval.

## Repository Structure

```text
src/
  schema.py
  context.py
  prompts.py
  preferences.py
  questions.py
  teacher.py
  jsonl_io.py

  cli/
    build_preferences.py
    train.py
    infer.py
    evaluate.py
    prepare_benchmark.py
    prepare_training_questions.py
    serve_gaia_retriever.py

  gaia/
    retriever.py

data/
  README.md
  benchmarks/
    README.md
    manifest.json

setup.py
```

## Installation

Install the core package with:

```bash
python -m pip install -e .
```

Optional dependencies are provided for different parts of the pipeline:

```bash
# DPO training
python -m pip install -e ".[train]"

# vLLM-based inference
python -m pip install -e ".[infer]"

# Benchmark and training-data preparation
python -m pip install -e ".[data]"

# Optional GAIA retrieval adapter
python -m pip install -e ".[gaia]"

# Tests
python -m pip install -e ".[test]"
```

To install all optional dependencies:

```bash
python -m pip install -e ".[all]"
```

## Training Data Construction

Training questions are prepared from the designated training sources, with evaluation splits excluded from training-question preparation. Utilities for benchmark normalization and training-question preparation are provided in `src/cli/prepare_benchmark.py` and `src/cli/prepare_training_questions.py`.

Student search trajectories are then collected on the resulting questions. BOUND constructs local preferences from decision-time states in these trajectories: the teacher first produces a search-state brief, assesses the student's search decision, and generates a preferred continuation when correction is needed.

The resulting DPO records contain only the student-visible `prompt`, `chosen`, and `rejected` fields. Teacher-side briefs and other construction metadata are not included in the student training input.

## Preference Construction

Configure an OpenAI-compatible teacher endpoint:

```bash
export TEACHER_BASE_URL="https://your-openai-compatible-endpoint/v1"
export TEACHER_API_KEY="..."
```

Construct preference pairs from collected student trajectories:

```bash
search-build-preferences \
  --rollouts /path/to/student_rollouts.jsonl \
  --output /path/to/preference_audit.jsonl \
  --train-output /path/to/dpo_train.jsonl \
  --teacher-model <teacher-model>
```

The audit output retains construction metadata, while the training output contains only the student-visible DPO records used for optimization.

## DPO Training

BOUND uses Hugging Face TRL for DPO training.

Install the training dependencies with:

```bash
python -m pip install -e ".[train]"
```

Validate preprocessing and tokenization:

```bash
search-train \
  --dataset /path/to/dpo_train.jsonl \
  --output-dir /path/to/output_checkpoint \
  --preprocess-only \
  --validate-tokenization
```

Run training:

```bash
search-train \
  --dataset /path/to/dpo_train.jsonl \
  --output-dir /path/to/output_checkpoint
```

The reference configuration uses `Qwen/Qwen3-4B-Instruct-2507`, one training epoch, learning rate `1e-6`, DPO `beta=0.1`, BF16, and a maximum sequence length of 8192 tokens.

## Inference

Iterative inference is implemented with vLLM and a compatible retrieval endpoint.

Install the inference dependencies with:

```bash
python -m pip install -e ".[infer]"
```

Run iterative inference with:

```bash
search-infer \
  --model /path/to/policy_checkpoint \
  --questions /path/to/evaluation_questions.jsonl \
  --retriever-url http://127.0.0.1:8000/ \
  --output /path/to/predictions.jsonl
```

The default configuration uses top-5 retrieval, at most 10 search steps, and temperature `0.6`.

An optional GAIA web-retrieval adapter is provided under `src/gaia/` and can be served with `search-serve-gaia-retriever`.

## Evaluation

Evaluate generated predictions with:

```bash
search-evaluate \
  --predictions /path/to/predictions.jsonl \
  --answers /path/to/answers.jsonl
```

The local evaluator reports exact match, token F1, and cover exact match. Benchmark-specific official evaluation tools should be used when applicable.

## Benchmark Preparation

Utilities for normalizing supported benchmark files are available through:

```bash
search-prepare-benchmark --help
```

Utilities for preparing training questions are available through:

```bash
search-prepare-training-questions --help
```

Benchmark sources, splits, licenses, and access information are documented in `data/benchmarks/`.
