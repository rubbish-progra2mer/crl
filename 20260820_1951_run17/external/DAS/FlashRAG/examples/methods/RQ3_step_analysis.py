import json
import os
import re
from collections import Counter, defaultdict
from flashrag.evaluator.metrics import ExactMatch, F1_Score, Sub_ExactMatch
from flashrag.utils.utils import extract_between

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

def is_search_output(output_str):
    """Check if the output is a valid search action."""
    return "<search>" in output_str and "</search>" in output_str and extract_between(output_str, "<search>", "</search>") is not None

def is_answer_output(output_str, begin_of_answer_token="<answer>", end_of_answer_token="</answer>"):
    """Check if the output is a valid answer action."""
    return (
        begin_of_answer_token in output_str
        and end_of_answer_token in output_str
        and extract_answer(output_str, begin_of_answer_token, end_of_answer_token) is not None
    )

def evaluate_prediction(pred, golden_answers, config={"dataset_name": None}, threshold=0.8):
    """Evaluate the prediction using FlashRAG's EM and F1 metrics."""
    if not pred or not golden_answers:
        return 0, 0, 0, False
    
    em_metric = ExactMatch(config=config)
    f1_metric = F1_Score(config=config)
    acc_metric = Sub_ExactMatch(config=config)
    
    em_score = em_metric.calculate_em(pred, golden_answers)
    f1_score = f1_metric.token_level_scores(pred, golden_answers)["f1"]
    acc_score = acc_metric.calculate_sub_em(pred, golden_answers)

    is_correct = (f1_score >= threshold)
    return em_score, f1_score, acc_score, is_correct

def evaluate_metric(metric_score, f1_threshold=0.8):
    f1 = metric_score.get('f1', 0)
    is_correct = f1 >= f1_threshold
    return is_correct

def analyze_dpo_pairs(folder_path, filename="intermediate_data.json", f1_threshold=0.8, is_search_o1=False):
    """
    Analyze the data to compute proportions of over-search and under-explore at each step_idx.
    """
    file_path = os.path.join(folder_path, filename)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"错误: 文件未找到: {file_path}")
        return None

    over_at = defaultdict(int)
    under_at = defaultdict(int)
    reached_at = defaultdict(int)

    if is_search_o1:
        begin_of_answer_token, end_of_answer_token = "\\boxed{", "}"
    else:
        begin_of_answer_token, end_of_answer_token = "<answer>", "</answer>"

    print("Total samples", len(data))
    for item in data:
        question = item.get("question")
        golden_answers = item.get("golden_answers")
        output = item.get("output", {})
        simulated_outputs = output.get("simulated_outputs", [])
        final_pred = output.get("pred")
        
        num_steps = len(simulated_outputs)
        for step_idx in range(num_steps):
            reached_at[step_idx] += 1
            
            sim = simulated_outputs[step_idx]
            answer_only_output = sim.get("answer_only_output")
                        
            forced_pred = extract_answer(answer_only_output, begin_of_answer_token, end_of_answer_token)
            em_score, f1_score, acc_score, is_forced_correct = evaluate_prediction(forced_pred, golden_answers, threshold=f1_threshold)
            
            if step_idx < num_steps - 1:
                if is_forced_correct:
                    over_at[step_idx] += 1
            else:
                if not is_forced_correct:
                    under_at[step_idx] += 1

    results = {}
    for step in sorted(reached_at.keys()):
        r = reached_at[step]
        over_p = over_at[step] / r if r > 0 else 0
        under_p = under_at[step] / r if r > 0 else 0
        
        print(f"\nStep: {step}")
        print(f"Reached: {r}")
        print(f"Over search count: {over_at[step]}")
        print(f"Over-search proportion: {over_p}")
        print(f"Under explore count: {under_at[step]}")
        print(f"Under-explore proportion: {under_p}")
        
        results[step] = {
            'over_search_proportion': over_p,
            'under_explore_proportion': under_p
        }

    return results

if __name__ == "__main__":
    # folder = "output/nq_2025_09_15_12_35_decision-schr1-all"
    # folder = "output_models/hotpotqa_2025_09_17_20_59_decision-scho1-deepseek-v3"
    folder = "output/2wikimultihopqa_2025_09_13_13_56_decision-schr1-all"
    results = analyze_dpo_pairs(folder, is_search_o1=False, f1_threshold=0.8)
    if results is not None:
        # You can further process results if needed
        pass