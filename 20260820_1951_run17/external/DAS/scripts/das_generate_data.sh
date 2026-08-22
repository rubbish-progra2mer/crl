#!/usr/bin/env bash
set -euo pipefail

DATASET=hotpotqa
MODEL=search-r1
GPU=0
SAMPLE_NUM=1000
SPLIT=dev
MAX_RETRIEVAL_NUM=5

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dataset) DATASET="$2"; shift 2 ;;
    --model) MODEL="$2"; shift 2 ;;
    --gpu) GPU="$2"; shift 2 ;;
    --sample-num) SAMPLE_NUM="$2"; shift 2 ;;
    --split) SPLIT="$2"; shift 2 ;;
    --max-retrieval-num) MAX_RETRIEVAL_NUM="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
METHOD_DIR="$ROOT/FlashRAG/examples/methods"

cd "$METHOD_DIR"

echo "[DAS] Step 1: run Search-R1 trajectories"
python run_exp.py \
  --method_name simulatedsearchr1 \
  --split "$SPLIT" \
  --dataset_name "$DATASET" \
  --gpu_id "$GPU" \
  --model_name "$MODEL" \
  --test_sample_num "$SAMPLE_NUM" \
  --max_retrieval_num "$MAX_RETRIEVAL_NUM" \
  --no_faiss_gpu

echo "[DAS] Step 2: build over-search DPO pairs"
python decision_data_generation.py

echo "[DAS] Step 3: generate / merge under-search fixes when available"
if [[ -f hint_under_opd_generation.py ]]; then
  python hint_under_opd_generation.py || true
fi
if [[ -f under_search_hint_chosen_generator.py ]]; then
  python under_search_hint_chosen_generator.py || true
fi
if [[ -f merge_under_hint_reviewed.py ]]; then
  python merge_under_hint_reviewed.py || true
fi

echo "[DAS] Step 4: run data quality checks when available"
if [[ -f dpo_quality_tool.py ]]; then
  python dpo_quality_tool.py || true
fi

echo "[DAS] Data generation scaffold finished. Check FlashRAG/examples/methods/dpo_data and output folders."
