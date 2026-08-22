#!/bin/bash
#SBATCH --job-name=run_exp
#SBATCH --output=output_run_exp.txt
#SBATCH --error=error_run_exp.txt
#SBATCH --cpus-per-task=4
#SBATCH --mem=160G
#SBATCH --time=12:00:00
source ~/anaconda3/etc/profile.d/conda.sh
conda activate flashrag

python run_exp.py --method_name simulatedsearcho1 --split train --dataset_name hotpotqa --gpu_id "2,3" --model_name 'gpt-4o-2024-05-13'
python run_exp.py --method_name simulatedsearcho1 --split train --dataset_name hotpotqa --gpu_id "2,3" --model_name 'gemini-2.5-flash'
python run_exp.py --method_name simulatedsearcho1 --split train -nvi-dataset_name hotpotqa --gpu_id "2,3" --model_name 'deepseek-v3'

python run_exp.py --method_name simulatedsearchr1 --split test --dataset_name nq --gpu_id "2,3" --model_name 'search-r1-7b'
