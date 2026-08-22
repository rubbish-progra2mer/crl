#!/usr/bin/env bash
set -euo pipefail

: "${LLAMA_FACTORY_DIR:?Set LLAMA_FACTORY_DIR to your LLaMA-Factory checkout}"
: "${BASE_MODEL:?Set BASE_MODEL to the SearchR1 base model path or Hugging Face repo}"
: "${DATASET_REPO:=reasonrag/das-dpo-data-searchr1-7b}"
: "${OUTPUT_DIR:=$LLAMA_FACTORY_DIR/saves/das/searchr1-dpo}"
: "${CUDA_VISIBLE_DEVICES:=0}"

: "${DATA_NAME:=das_dpo_data_searchr1_7b}"
: "${DATA_FILE:=das_dpo_data_searchr1_7b.json}"
: "${MAX_SAMPLES:=}"
: "${LORA_RANK:=}"
: "${LORA_ALPHA:=}"
: "${LORA_DROPOUT:=}"
: "${PREF_BETA:=}"
: "${MAX_STEPS:=}"
DATA_DIR="$LLAMA_FACTORY_DIR/data"
CONFIG_PATH="$OUTPUT_DIR/train_das_dpo.yaml"

mkdir -p "$OUTPUT_DIR" "$DATA_DIR"

python - <<PY
import json
from pathlib import Path
from huggingface_hub import hf_hub_download, snapshot_download

data_dir = Path("$DATA_DIR")
try:
    path = hf_hub_download(
        repo_id="$DATASET_REPO",
        repo_type="dataset",
        filename="$DATA_FILE",
        local_dir=str(data_dir),
    )
except Exception:
    snapshot_dir = Path(snapshot_download(
        repo_id="$DATASET_REPO",
        repo_type="dataset",
        local_dir=str(data_dir),
    ))
    candidates = sorted(snapshot_dir.glob("*.json"))
    if not candidates:
        raise FileNotFoundError(f"No JSON DPO data file found in {snapshot_dir}")
    path = str(candidates[0])
data_file = Path(path).name

info_path = data_dir / "dataset_info.json"
if info_path.exists():
    info = json.loads(info_path.read_text())
else:
    info = {}
info["$DATA_NAME"] = {
    "file_name": data_file,
    "ranking": True,
    "columns": {
        "prompt": "prompt",
        "chosen": "chosen",
        "rejected": "rejected",
        "system": "system"
    }
}
info_path.write_text(json.dumps(info, indent=2, ensure_ascii=False))
print("Registered dataset:", "$DATA_NAME", "->", path)
PY

cat > "$CONFIG_PATH" <<YAML
### model
model_name_or_path: $BASE_MODEL
trust_remote_code: true

### method
stage: dpo
do_train: true
finetuning_type: lora
${LORA_RANK:+lora_rank: $LORA_RANK}
${LORA_ALPHA:+lora_alpha: $LORA_ALPHA}
${LORA_DROPOUT:+lora_dropout: $LORA_DROPOUT}
lora_target: all
${PREF_BETA:+pref_beta: $PREF_BETA}
pref_loss: sigmoid

### dataset
dataset: $DATA_NAME
template: qwen
cutoff_len: 4096
${MAX_SAMPLES:+max_samples: $MAX_SAMPLES}
overwrite_cache: true
preprocessing_num_workers: 8

### output
output_dir: $OUTPUT_DIR
logging_steps: 5
save_steps: 50
plot_loss: true
overwrite_output_dir: true
save_only_model: false

### train
per_device_train_batch_size: 1
gradient_accumulation_steps: 8
learning_rate: 1.0e-6
${MAX_STEPS:+max_steps: $MAX_STEPS}
lr_scheduler_type: cosine
warmup_ratio: 0.03
bf16: true
ddp_timeout: 180000000
YAML

cd "$LLAMA_FACTORY_DIR"

if command -v llamafactory-cli >/dev/null 2>&1; then
  llamafactory-cli train "$CONFIG_PATH"
else
  torchrun --nnodes 1 --nproc_per_node "$(python - <<'PY'
import os
print(len(os.environ.get("CUDA_VISIBLE_DEVICES", "0").split(",")))
PY
)" src/train.py "$CONFIG_PATH"
fi
