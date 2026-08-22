import os
os.environ["CUDA_VISIBLE_DEVICES"] = "2,3"

import json
import re
from collections import Counter
from flashrag.evaluator.metrics import ExactMatch, F1_Score
from flashrag.utils.utils import extract_between
from vllm import LLM, SamplingParams
import numpy as np
import torch

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def normalize_answer(s: str) -> str:
    """Normalize answer string for comparison."""
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)
    def white_space_fix(text):
        return ' '.join(text.split())
    def remove_punc(text):
        exclude = set('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
        return ''.join(ch for ch in text if ch not in exclude)
    def lower(text):
        return text.lower()
    return white_space_fix(remove_punc(lower(remove_articles(s))))

def extract_answer(output_str, begin_token="<answer>", end_token="</answer>"):
    """Extract the answer content from the output string."""
    content = extract_between(output_str, begin_token, end_token)
    return content.strip() if content else output_str.strip()

def extract_search_query(output_str: str) -> str:
    """Extract search query from the agent's output."""
    content = extract_between(output_str, "<search>", "</search>")
    return content.strip() if content else None

def evaluate_prediction(pred, golden_answers, config={"dataset_name": None}, threshold=0.8):
    """Evaluate the prediction using FlashRAG's EM and F1 metrics."""
    if not pred or not golden_answers:
        return 0, 0, False
    
    normalized_pred = normalize_answer(pred)
    normalized_golden = [normalize_answer(ans) for ans in golden_answers]
    
    if not normalized_pred or not any(normalized_golden):
        return 0, 0, False

    em_score = evaluate_prediction.em_metric.calculate_em(normalized_pred, normalized_golden)
    f1_score_dict = evaluate_prediction.f1_metric.token_level_scores(normalized_pred, normalized_golden)
    f1_score = f1_score_dict.get("f1", 0)
    
    is_correct = (f1_score >= threshold)
    return em_score, f1_score, is_correct


def extract_judge_score(answer: str, split_str: str = "Total rating:") -> float:
    """从 LLM Judge 的输出中提取评分"""
    try:
        if split_str in answer:
            rating = answer.split(split_str)[1]
        else:
            rating = answer
        digit_groups = [el.strip() for el in re.findall(r"\d+(?:\.\d+)?", rating)]
        return float(digit_groups[0])
    except Exception as e:
        print(f"Error extracting score from: {answer}. Error: {e}")
        return 0.0

class LLMJudge_FactCheck:
    metric_name = "llm_judge_factcheck"
    
    FACT_CHECK_PROMPT = """
    You are a meticulous fact-checker. You will be given a Context, a Question, and an Answer.
    Your task is to provide a 'correctness rating' scoring how factually accurate the Answer is, based *only* on the provided Context.
    - A score of 10 means the Answer is perfectly correct and fully supported by the Context.
    - A score of 5 means the Answer is partially correct or contains minor inaccuracies.
    - A score of 0 means the Answer is completely incorrect, unsupported by the Context, or irrelevant.
    Provide your feedback as follows:
    Feedback:::
    Total rating: (your rating, as a float between 0 and 10)
    Now here are the Context, Question, and Answer.
    Context: {context}
    Question: {question}
    Answer: {answer}
    Feedback:::
    Total rating: """

    def __init__(self, llm_instance: LLM):
        print("Initializing FactCheck Judge with existing vLLM instance...")
        self.llm = llm_instance
        self.sampling_params = SamplingParams(max_tokens=100)

    def calculate_metric(self, context_list, question_list, answer_list, batch_size=None):
        judge_input_prompt = [
            self.FACT_CHECK_PROMPT.format(context=c, question=q, answer=a)
            for c, q, a in zip(context_list, question_list, answer_list)
        ]
        
        if not judge_input_prompt:
            return {"llm_judge_score": 0}, []

        print(f"Running LLM Judge on {len(judge_input_prompt)} items with vLLM...")
        
        vllm_outputs = self.llm.generate(judge_input_prompt, self.sampling_params)
        
        generated_texts = []
        for output in vllm_outputs:
            text = output.outputs[0].text
            clean_text = text.split(self.FACT_CHECK_PROMPT.split("Feedback:::")[0])[-1]
            generated_texts.append(clean_text)

        metric_score_list = [extract_judge_score(o) for o in generated_texts]
        
        metric_score_list_normalized = [1.0 if score >= 10.0 else 0.0 for score in metric_score_list]
        
        if not metric_score_list_normalized:
            return {"llm_judge_score": 0}, []

        score = sum(metric_score_list_normalized) / len(metric_score_list_normalized)

        return {"llm_judge_score": score}, metric_score_list_normalized


def plot_violin_distribution(over_search_scores, correct_search_scores):
    print("Generating violin plot for Knowledge Recall scores...")
    plot_data = []
    for score in over_search_scores:
        plot_data.append({"Category": "Over-search", "Knowledge Recall Score": score})
    for score in correct_search_scores:
        plot_data.append({"Category": "Correct-search", "Knowledge Recall Score": score})
    
    if not plot_data:
        print("No data to plot.")
        return

    df = pd.DataFrame(plot_data)
    
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    ax = sns.violinplot(
        data=df, 
        x="Category", 
        y="Knowledge Recall Score",
        order=["Correct-search", "Over-search"],
        cut=0,
    )
    ax.set_title("Knowledge Recall Score Distribution (Probe 1)", fontsize=16)
    ax.set_xlabel("Decision Category", fontsize=12)
    ax.set_ylabel("Knowledge Recall Score (0.0 - 1.0)", fontsize=12)
    ax.set_ylim(-0.05, 1.05) 

    plt.savefig("knowledge_recall_distribution.png")
    plt.show()
    print("Violin plot saved as 'knowledge_recall_distribution.png'")


def analyze_knowledge_decision_boundary(
    file_path: str, 
    knowledge_llm: LLM,
    llm_judge: LLMJudge_FactCheck,
    f1_threshold=0.8
):
    
    KNOWLEDGE_RECALL_PROMPT = "You are acting as a search engine. The following text is a user's raw request, which contains their intended search query inside `<search>` tags. Your task is to directly answer the user's intended query based on your internal knowledge. Provide a concise, direct answer. Do not explain your reasoning or mention that you are an AI.\n\nUser's Full Request: {question}\nDirect Answer:"
    sampling_params_recall = SamplingParams(max_tokens=100) 

    KNOWLEDGE_META_PROMPT = "You are a helpful assistant. You will see a user's full request which contains a search query inside `<search>` tags. Based on the *intended query* within that request, do you believe you have sufficient internal knowledge to answer it accurately without searching? Answer *only* with 'Yes' or 'No'.\n\nUser's Full Request: {question}\nAnswer:"
    sampling_params_meta = SamplingParams(max_tokens=5, temperature=0.0)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: file not found: {file_path}")
        return None

    print(f"Total samples to process: {len(data)}. Gathering all tasks...")
    
    all_recall_prompts = []
    all_meta_prompts = []
    all_judge_contexts = []
    all_judge_queries = []
    all_task_metadata = [] 

    for item_idx, item in enumerate(data):
        
        supporting_titles = item.get('metadata', {}).get('supporting_facts', {}).get('title', [])
        context_data = item.get('metadata', {}).get('context', {})
        all_titles = context_data.get('title', [])
        all_sentences = context_data.get('sentences', [])
        
        if not all_titles or not all_sentences:
            continue
            
        try:
            indices = [all_titles.index(t) for t in supporting_titles if t in all_titles]
        except ValueError as e:
            continue

        supporting_context = " ".join([" ".join(all_sentences[i]) for i in indices])
        if not supporting_context:
            continue
        
        simulated_outputs = item.get('output', {}).get('simulated_outputs', [])
        golden_answers = item.get('golden_answers', [])
        
        for step_idx, sim in enumerate(simulated_outputs):
            if step_idx + 1 == len(simulated_outputs):
                continue 

            answer_only_output = sim.get("answer_only_output")
            forced_pred = extract_answer(answer_only_output) 
            _, _, is_forced_correct = evaluate_prediction(forced_pred, golden_answers, threshold=f1_threshold)
            is_over_search = is_forced_correct

            original_output = sim.get("original_output")
            search_query = extract_search_query(original_output)

            if search_query:
                all_recall_prompts.append(KNOWLEDGE_RECALL_PROMPT.format(question=original_output))
                all_meta_prompts.append(KNOWLEDGE_META_PROMPT.format(question=original_output))
                
                all_judge_contexts.append(supporting_context)
                all_judge_queries.append(search_query)
                
                all_task_metadata.append({
                    "item_id": item.get('id'),
                    "is_over_search": is_over_search
                })
        
    if not all_recall_prompts:
        return None

    print(f"--- Stage 1 Complete: Collected {len(all_recall_prompts)} search tasks in total ---")

    # --- Stage 2: Batch Generation (Two Probes) ---
    
    # Step A (Probe 1: Knowledge Recall)
    print(f"--- Stage 2A: Running Knowledge Recall (Probe 1)... ---")
    recall_generated_outputs = knowledge_llm.generate(
        all_recall_prompts, 
        sampling_params_recall
    )
    cleaned_recall_answers = []
    for g in recall_generated_outputs:
        text = g.outputs[0].text
        clean_text = text.split(KNOWLEDGE_RECALL_PROMPT.split("Direct Answer:")[0])[-1].strip()
        cleaned_recall_answers.append(clean_text)
    
    # Step B (Judge Probe 1)
    print(f"--- Stage 2B: Running judgment for Knowledge Recall... ---")
    _, recall_judge_scores = llm_judge.calculate_metric(all_judge_contexts, all_judge_queries, cleaned_recall_answers)

    # Step C (Probe 2: Metacognition)
    print(f"--- Stage 2C: Running Metacognition (Probe 2)... ---")
    meta_generated_outputs = knowledge_llm.generate(
        all_meta_prompts,
        sampling_params_meta
    )
    meta_results = []
    for g in meta_generated_outputs:
        text = g.outputs[0].text.strip().lower()
        meta_score = 1.0 if "yes" in text else 0.0
        meta_results.append(meta_score)

    print("--- Stage 2 Complete: All generation and judgment finished ---")

    # --- Stage 3: Aggregation and Reporting ---
    print("--- Stage 3: Aggregating results... ---")
    all_over_search_recall_scores = []
    all_correct_search_recall_scores = []
    all_over_search_meta_scores = []
    all_correct_search_meta_scores = []
    
    for i, metadata in enumerate(all_task_metadata):
        recall_score = recall_judge_scores[i] # 0-1.0 float
        meta_score = meta_results[i]       # 0.0 or 1.0
        is_over_search = metadata['is_over_search']
        
        if is_over_search:
            all_over_search_recall_scores.append(recall_score)
            all_over_search_meta_scores.append(meta_score)
        else:
            all_correct_search_recall_scores.append(recall_score)
            all_correct_search_meta_scores.append(meta_score)
        
    # Final Analysis
    print("\n--- Experiment Finished ---")
    
    # Calculate Averages
    avg_over_search_recall = np.mean(all_over_search_recall_scores) if all_over_search_recall_scores else 0
    avg_correct_search_recall = np.mean(all_correct_search_recall_scores) if all_correct_search_recall_scores else 0
    avg_over_search_meta = np.mean(all_over_search_meta_scores) if all_over_search_meta_scores else 0
    avg_correct_search_meta = np.mean(all_correct_search_meta_scores) if all_correct_search_meta_scores else 0

    print("\n--- Final Results ---")
    
    over_search_count = len(all_over_search_recall_scores)
    correct_search_count = len(all_correct_search_recall_scores)

    print(f"Total 'Over-search' steps: {over_search_count}")
    print(f"Total 'Correct-search' steps: {correct_search_count}")
    
    print("\n--- Knowledge Boundary vs. Decision Boundary (Dual-Probe Analysis) ---")
    print("======================================================================================")
    print(f"Query Type (Decision)    | Count        | Probe 1: Knowledge Recall (Avg. Score) | Probe 2: Metacognitive Confidence (% 'Yes')")
    print("--------------------------------------------------------------------------------------")
    print(f"Over-search (Unnecessary)| {over_search_count:<12} | {avg_over_search_recall:<30.4f} | {avg_over_search_meta:<30.4f}")
    print(f"Correct-search (Necessary)| {correct_search_count:<12} | {avg_correct_search_recall:<30.4f} | {avg_correct_search_meta:<30.4f}")
    print("======================================================================================")

    return {
        "over_search_recall_avg": avg_over_search_recall,
        "correct_search_recall_avg": avg_correct_search_recall,
        "over_search_meta_avg": avg_over_search_meta,
        "correct_search_meta_avg": avg_correct_search_meta,
        "over_search_count": over_search_count,
        "correct_search_count": correct_search_count,
        "all_over_search_recall_scores": all_over_search_recall_scores,
        "all_correct_search_recall_scores": all_correct_search_recall_scores
    }


# ==============================================================================
# 5. Main Execution Entrypoint (No changes needed)
# ==============================================================================
if __name__ == "__main__":
    # --- Path Configuration ---
    data_folder = "output/search-r1-7b/hotpotqa_2025_09_23_15_11_decision-schr1-chunk1"
    # data_folder = "output/hotpotqa_2025_09_22_17_48_decision-schr1-search-r1-7b" 
    # --- Path Configuration ---
    # data_folder = "output/search-r1-7b/hotpotqa_2025_09_23_15_11_decision-schr1-chunk1"
    data_filename = "intermediate_data.json" 
    file_path = os.path.join(data_folder, data_filename)

    model_path = "./models/qwen2.5-7b" 
    
    if not os.path.exists(model_path):
        print(f"Warning: Model path {model_path} does not exist. The program will exit.")
        exit()

    # --- Initialize vLLM ---
    print("Initializing Shared vLLM Engine...")
    
    shared_llm = LLM(
        model=model_path,
        trust_remote_code=True,
        gpu_memory_utilization=0.5
    )

    llm_judge = LLMJudge_FactCheck(llm_instance=shared_llm)
    
    # --- Run Experiment ---
    results = analyze_knowledge_decision_boundary(
        file_path=file_path,
        knowledge_llm=shared_llm, 
        llm_judge=llm_judge,
        f1_threshold=0.8
    )

    # --- Run Plotting ---
    if results:
        plot_violin_distribution(
            results['all_over_search_recall_scores'],
            results['all_correct_search_recall_scores']
        )
