# To Search or Not to Search: Aligning the Decision Boundary of Deep Search Agents via Causal Intervention

This repository provides the code, data generation pipeline, training scripts, and evaluation scripts for **DAS**, the method introduced in our WWW 2026 paper:

**To Search or Not to Search: Aligning the Decision Boundary of Deep Search Agents via Causal Intervention**

DAS improves deep search agents by aligning the boundary between two actions: continuing to search and stopping to answer. The method diagnoses two types of decision errors, **over-search** and **under-search**, uses causal intervention to identify better decision preferences, and converts the resulting feedback into DPO data for post-training Search-R1 style agents.

The goal is to improve both:

- **Accuracy**: answer more questions correctly.
- **Efficiency**: reduce unnecessary search calls.

## Paper

- Conference: WWW '26, The ACM Web Conference 2026
- DOI: [10.1145/3774904.3792235](https://doi.org/10.1145/3774904.3792235)
- arXiv: [2602.03304](https://arxiv.org/abs/2602.03304)

## Released Artifacts

| Artifact | Link |
|---|---|
| DAS LoRA | [reasonrag/das-lora-searchr1](https://huggingface.co/reasonrag/das-lora-searchr1) |
| DAS dpo data-searchr1-7b | [reasonrag/das-dpo-data-searchr1-7b](https://huggingface.co/datasets/reasonrag/das-dpo-data-searchr1-7b) |

The released LoRA and DPO data are provided for reproducing DAS-style post-training with LLaMA-Factory and FlashRAG.

## Repository Layout

```text
.
|-- FlashRAG/
|   `-- examples/methods/
|       |-- run_exp.py                         # Search-R1 / Search-O1 evaluation entry
|       |-- decision_data_generation.py        # over-search DPO pair construction
|       |-- hint_under_opd_generation.py       # under-search hint generation
|       |-- under_search_hint_chosen_generator.py
|       |-- merge_under_hint_reviewed.py
|       |-- dpo_quality_tool.py                # DPO data quality checks
|       `-- decision_dpo.yaml                  # legacy DPO config template
|-- scripts/
|   |-- das_generate_data.sh                   # end-to-end data generation scaffold
|   |-- das_train_dpo.sh                       # LLaMA-Factory DPO training
|   |-- das_infer_searchr1.sh                  # Search-R1 rollout / inference
|   `-- das_eval_searchr1.sh                   # FlashRAG evaluation
`-- README.md
```

## Setup

Create the FlashRAG environment:

```bash
conda create -n flashrag python=3.10 -y
conda activate flashrag
pip install flashrag-dev --pre
pip install "flashrag-dev[full]"
pip install "vllm>=0.10.0" deepspeed peft huggingface_hub
```

Create the LLaMA-Factory environment:

```bash
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
conda create -n llama_factory python=3.10 -y
conda activate llama_factory
pip install -e ".[torch,metrics]"
```

Prepare FlashRAG datasets and retrieval index following the FlashRAG documentation. For the experiments in this project, the evaluation datasets are NQ, HotpotQA, and 2WikiMultiHopQA.

## Data Generation

DAS data generation has three stages:

1. Run Search-R1 rollouts and save intermediate search trajectories.
2. Detect over-search and under-search decision errors through causal intervention.
3. Convert the causal feedback into DPO preference pairs.

Run the scaffold:

```bash
bash scripts/das_generate_data.sh \
  --dataset hotpotqa \
  --model search-r1 \
  --gpu 0
```

For convenience, the released data can be downloaded directly:

```bash
python - <<'PY'
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="reasonrag/das-dpo-data-searchr1-7b",
    repo_type="dataset",
    local_dir="data/das-dpo-data-searchr1-7b",
)
PY
```

## Training

Train DAS with DPO in LLaMA-Factory:

Run:

```bash
export LLAMA_FACTORY_DIR=/path/to/LLaMA-Factory
export DATASET_REPO=reasonrag/das-dpo-data-searchr1-7b
export BASE_MODEL=/path/to/base/searchr1/model
export OUTPUT_DIR=$LLAMA_FACTORY_DIR/saves/das/searchr1-das

bash scripts/das_train_dpo.sh
```

The script downloads the DAS DPO data, registers it in `dataset_info.json`, writes a LLaMA-Factory training YAML, and launches DPO LoRA training.

## Evaluation

Evaluate the base model:

```bash
bash scripts/das_eval_searchr1.sh \
  --dataset hotpotqa \
  --model search-r1 \
  --gpu 0
```

Evaluate with the released LoRA:

```bash
bash scripts/das_eval_searchr1.sh \
  --dataset hotpotqa \
  --model search-r1 \
  --lora reasonrag/das-lora-searchr1 \
  --gpu 0
```

## Inference / Rollout

For rollout-style inference without changing the training data pipeline, use:

```bash
bash scripts/das_infer_searchr1.sh \
  --dataset nq \
  --model search-r1 \
  --lora reasonrag/das-lora-searchr1 \
  --gpu 0
```

## Acknowledgements

We thank [FlashRAG](https://github.com/RUC-NLPIR/FlashRAG), [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory), and [Search-R1](https://github.com/PeterGriffinJin/Search-R1) for their valuable open-source contributions.

## Citation

If you find this repository helpful, please cite:

```bibtex
@inproceedings{zhang2026search,
  author    = {Wenlin Zhang and Kuicai Dong and Junyi Li and Yingyi Zhang and Xiaopeng Li and Pengyue Jia and Yi Wen and Derong Xu and Maolin Wang and Yichao Wang and Yong Liu and Xiangyu Zhao},
  title     = {To Search or Not to Search: Aligning the Decision Boundary of Deep Search Agents via Causal Intervention},
  booktitle = {Proceedings of the ACM Web Conference 2026},
  series    = {WWW '26},
  pages     = {2049--2059},
  year      = {2026},
  publisher = {ACM},
  doi       = {10.1145/3774904.3792235},
  url       = {https://doi.org/10.1145/3774904.3792235}
}
```
