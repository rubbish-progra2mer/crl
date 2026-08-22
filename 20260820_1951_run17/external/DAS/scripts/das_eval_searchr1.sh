#!/usr/bin/env bash
set -euo pipefail

DATASET=hotpotqa
MODEL=search-r1
LORA=None
GPU=0
SAMPLE_NUM=1000
SPLIT=dev
MAX_RETRIEVAL_NUM=5
GENERATOR_MAX_INPUT_LEN=12288
GPU_MEMORY_UTILIZATION=0.55
VLLM_MAX_NUM_SEQS=4

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dataset) DATASET="$2"; shift 2 ;;
    --model) MODEL="$2"; shift 2 ;;
    --lora) LORA="$2"; shift 2 ;;
    --gpu) GPU="$2"; shift 2 ;;
    --sample-num) SAMPLE_NUM="$2"; shift 2 ;;
    --split) SPLIT="$2"; shift 2 ;;
    --max-retrieval-num) MAX_RETRIEVAL_NUM="$2"; shift 2 ;;
    --generator-max-input-len) GENERATOR_MAX_INPUT_LEN="$2"; shift 2 ;;
    --gpu-memory-utilization) GPU_MEMORY_UTILIZATION="$2"; shift 2 ;;
    --vllm-max-num-seqs) VLLM_MAX_NUM_SEQS="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
METHOD_DIR="$ROOT/FlashRAG/examples/methods"
cd "$METHOD_DIR"

export FLASHRAG_SIM_GENERATE_BATCH="${FLASHRAG_SIM_GENERATE_BATCH:-50}"

python run_exp.py \
  --method_name simulatedsearchr1 \
  --split "$SPLIT" \
  --dataset_name "$DATASET" \
  --gpu_id "$GPU" \
  --model_name "$MODEL" \
  --lora "$LORA" \
  --test_sample_num "$SAMPLE_NUM" \
  --generator_max_input_len "$GENERATOR_MAX_INPUT_LEN" \
  --gpu_memory_utilization "$GPU_MEMORY_UTILIZATION" \
  --vllm_max_num_seqs "$VLLM_MAX_NUM_SEQS" \
  --generation_max_tokens 512 \
  --max_retrieval_num "$MAX_RETRIEVAL_NUM" \
  --no_faiss_gpu
