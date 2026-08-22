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
        return 0, 0, False
    
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
    Analyze the data to count search actions and over-search/under-explore samples, grouped by metadata level or type.
    """
    file_path = os.path.join(folder_path, filename)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"错误: 文件未找到: {file_path}")
        return None

    groups = defaultdict(lambda: {
        'search_count': 0,
        'over_search_count': 0,
        'under_explore_count': 0,
        'finish_data_num': 0,
        'em_total': 0.0,
        'f1_total': 0.0,
        'acc_total': 0.0,
        'item_count': 0
    })

    if is_search_o1:
        begin_of_answer_token, end_of_answer_token = "\\boxed{", "}"
    else:
        begin_of_answer_token, end_of_answer_token = "<answer>", "</answer>"

    print("Total samples", len(data))
    for item in data:
        metadata = item.get("metadata", {})
        # category = metadata.get("level") or metadata.get("type") or "unknown"
        # category = metadata.get("type")
        category = len(metadata.get("supporting_facts").get("title"))
        if category >= 5:
            category = ">=5"

        groups[category]['item_count'] += 1
        
        question = item.get("question")
        golden_answers = item.get("golden_answers")
        output = item.get("output", {})
        prompt = output.get("prompt")
        simulated_outputs = output.get("simulated_outputs", [])
        groups[category]['search_count'] += output.get("retrieved_times", 0)
        final_pred = output.get("pred")
        metric_score = output.get("metric_score", {})
        
        em_score, f1_score, acc_score, is_correct = evaluate_prediction(final_pred, golden_answers, threshold=f1_threshold)
        groups[category]['em_total'] += em_score
        groups[category]['f1_total'] += f1_score
        groups[category]['acc_total'] += acc_score
        
        over_search_flag = False  # To ensure we only count over-search once per item
        for step_idx, sim in enumerate(simulated_outputs):
            answer_only_output = sim.get("answer_only_output")
            if step_idx >= len(simulated_outputs):
                continue
                        
            forced_pred = extract_answer(answer_only_output, begin_of_answer_token, end_of_answer_token)
            _, forced_f1, _, is_forced_correct = evaluate_prediction(forced_pred, golden_answers, threshold=f1_threshold)
            
            # Over-search: answer_only correct, original chose search, and there are more steps
            if step_idx + 1 < len(simulated_outputs):
                if is_forced_correct and not over_search_flag:
                    groups[category]['over_search_count'] += 1
                    groups[category]['finish_data_num'] += 1
                    over_search_flag = True
                    break

            # Under-explore: original chose answer but wrong
            elif step_idx + 1 == len(simulated_outputs):
                if not is_correct:  # Use final is_correct here
                    groups[category]['under_explore_count'] += 1

                groups[category]['finish_data_num'] += 1

    results = {}
    for category, stats in groups.items():
        item_count = stats['item_count']
        finish_num = stats['finish_data_num']
        if item_count > 0:
            search_avg = stats['search_count'] / item_count
            em_avg = stats['em_total'] / item_count
            f1_avg = stats['f1_total'] / item_count
            acc_avg = stats['acc_total'] / item_count
        else:
            search_avg = em_avg = f1_avg = acc_avg = 0
        
        if finish_num > 0:
            over_rate = stats['over_search_count'] / finish_num
            under_rate = stats['under_explore_count'] / finish_num
        else:
            over_rate = under_rate = 0
        
        results[category] = {
            'average_search': search_avg,
            'over_search_rate': over_rate,
            'under_explore_rate': under_rate,
            'em': em_avg,
            'f1': f1_avg,
            'acc': acc_avg
        }
        
        print(f"\nCategory: {category}")
        print(f"Item count: {item_count}")
        print(f"Finish data number: {finish_num}")
        print(f"Search count: {stats['search_count']}")
        print(f"Over search count: {stats['over_search_count']}")
        print(f"Under explore count: {stats['under_explore_count']}")
        print(f"Average number of search actions: {search_avg}")
        print(f"Over-search rate: {over_rate}")
        print(f"Under-explore rate: {under_rate}")
        print(f"Average EM: {em_avg}")
        print(f"Average F1: {f1_avg}")
        print(f"ACC: {acc_avg}")

    return results

if __name__ == "__main__":
    folder = "output/hotpotqa_2025_09_18_16_15_decision-schr1-search-r1-7b"
    # folder = "output_models/hotpotqa_2025_09_17_20_59_decision-scho1-deepseek-v3"
    results = analyze_dpo_pairs(folder, is_search_o1=False, f1_threshold=0.8)
    if results is not None:
        # You can further process results if needed
        pass