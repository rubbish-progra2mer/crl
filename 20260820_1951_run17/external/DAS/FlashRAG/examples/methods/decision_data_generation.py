import json
import os
import re
from collections import Counter
from flashrag.evaluator.metrics import ExactMatch, F1_Score

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
    return content.strip() if content else None

def is_search_output(output_str):
    """Check if the output is a valid search action."""
    return "<search>" in output_str and "</search>" in output_str and extract_between(output_str, "<search>", "</search>") is not None

def is_answer_output(output_str):
    """Check if the output is a valid answer action."""
    return "<answer>" in output_str and "</answer>" in output_str and extract_answer(output_str) is not None

def extract_between(text, start_token, end_token):
    """Extract content between start_token and end_token."""
    try:
        start = text.index(start_token) + len(start_token)
        end = text.index(end_token, start)
        return text[start:end]
    except ValueError:
        return None

def evaluate_prediction(pred, golden_answers, config={"dataset_name": None}, threshold=0.8):
    """Evaluate the prediction using FlashRAG's EM and F1 metrics."""
    if not pred or not golden_answers:
        return 0, 0, False
    
    em_metric = ExactMatch(config=config)
    f1_metric = F1_Score(config=config)
    
    em_score = em_metric.calculate_em(pred, golden_answers)
    f1_score = f1_metric.token_level_scores(pred, golden_answers)["f1"]
    
    is_correct = f1_score >= threshold
    return em_score, f1_score, is_correct

def parse_prompt_segments(prompt):
    """Parse the accumulated prompt to extract step outputs after 'Question:'."""
    question_start = prompt.find("Question:")
    if question_start == -1:
        return [], []
    
    agent_content = prompt[question_start + len("Question: "):].strip()
    
    think_patterns = re.findall(r"<think>(.*?)</think>", agent_content, re.DOTALL)
    action_patterns = re.findall(r"(<search>.*?</search>|<answer>.*?</answer>)", agent_content, re.DOTALL)
    
    step_outputs = []
    for i in range(len(action_patterns)):
        think = think_patterns[i].strip() if i < len(think_patterns) else ""
        action = action_patterns[i].strip()
        step_output = f"<think>{think}</think>{action}"
        step_outputs.append(step_output)
    
    return step_outputs, action_patterns

def get_step_prompt(prompt, step_idx, step_outputs):
    """Approximate the prompt up to the current step."""
    question_start = prompt.find("Question:")
    if question_start == -1:
        return prompt
    
    agent_content = prompt[question_start:]
    current_step_start = 0
    for i in range(step_idx + 1):
        next_think = agent_content.find("<think>", current_step_start)
        if next_think == -1:
            break
        current_step_start = next_think + agent_content[next_think:].find("</think>") + len("</think>")
        next_action_end = agent_content.find("</search>", current_step_start) + len("</search>") if "</search>" in agent_content[current_step_start:] else agent_content.find("</answer>", current_step_start) + len("</answer>")
        if next_action_end > 0:
            current_step_start = next_action_end
    
    return prompt[:question_start + current_step_start]

def merge_think_tags(output_str):
    """Merge multiple <think> tags into a single <think> tag."""
    think_contents = re.findall(r"<think>(.*?)</think>", output_str, re.DOTALL)
    if not think_contents:
        return output_str
    merged_think = " ".join(content.strip() for content in think_contents)
    # Replace all <think>...</think> with a single <think>merged_content</think>
    think_start = output_str.find("<think>")
    think_end = output_str.rfind("</think>") + len("</think>")
    if think_start == -1 or think_end < len("</think>"):
        return output_str
    # Keep the action part (<search>...</search> or <answer>...</answer>)
    action_part = output_str[think_end:]
    return f"<think>{merged_think}</think>{action_part}"

def analyze_dpo_pairs(folder_path, filename="intermediate_data.json", save_dir="dpo_pairs", f1_threshold=0.2):
    file_path = os.path.join(folder_path, filename)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: file not found: {file_path}")
        return None, None

    over_search_pairs = []
    under_explore_pairs = []

    for item in data:
        question = item.get("question")
        golden_answers = item.get("golden_answers")
        output = item.get("output", {})
        prompt = output.get("prompt")
        simulated_outputs = output.get("simulated_outputs", [])
        final_pred = output.get("pred")

        original_step_outputs, action_patterns = parse_prompt_segments(prompt)
        num_steps = len(action_patterns)
        
        _, final_f1, is_final_correct = evaluate_prediction(final_pred, golden_answers, threshold=f1_threshold)
        
        for step_idx, sim in enumerate(simulated_outputs):
            search_only_output = sim.get("search_only_output")
            answer_only_output = sim.get("answer_only_output")
            
            if not is_search_output(search_only_output) or not is_answer_output(answer_only_output):
                continue
            
            if step_idx >= len(original_step_outputs):
                continue
            original_step_output = original_step_outputs[step_idx]
            original_action = action_patterns[step_idx]
            
            step_prompt = get_step_prompt(prompt, step_idx, original_step_outputs)
            
            forced_pred = extract_answer(answer_only_output)
            _, forced_f1, is_forced_correct = evaluate_prediction(forced_pred, golden_answers, threshold=f1_threshold)
            
            # Over-search: answer_only correct, original chose search, and there are more steps
            if is_forced_correct and is_search_output(original_action) and num_steps > step_idx + 1:
                over_search_pairs.append({
                    "system": "",
                    "prompt": step_prompt,
                    "chosen": merge_think_tags(answer_only_output),
                    "rejected": merge_think_tags(original_step_output)
                })
            
            # Under-explore: original chose answer but wrong
            if is_answer_output(original_action):
                original_pred = extract_answer(original_action)
                _, orig_f1, is_orig_correct = evaluate_prediction(original_pred, golden_answers, threshold=f1_threshold)
                if not is_orig_correct:
                    under_explore_pairs.append({
                        "system": "",
                        "prompt": step_prompt,
                        "chosen": merge_think_tags(search_only_output),
                        "rejected": merge_think_tags(original_step_output)
                    })

    os.makedirs(save_dir, exist_ok=True)

    over_search_path = os.path.join(save_dir, "over_search_dpo.json")
    with open(over_search_path, 'w', encoding='utf-8') as f:
        json.dump(over_search_pairs, f, ensure_ascii=False, indent=4)
    print(f"Over-search DPO pairs saved: {over_search_path}")

    under_explore_path = os.path.join(save_dir, "under_explore_dpo.json")
    with open(under_explore_path, 'w', encoding='utf-8') as f:
        json.dump(under_explore_pairs, f, ensure_ascii=False, indent=4)
    print(f"Under-explore DPO pairs saved: {under_explore_path}")

    over_count = len(over_search_pairs)
    under_count = len(under_explore_pairs)

    combined_dpo_pairs = over_search_pairs + under_explore_pairs
    dpo_pairs_path = os.path.join(save_dir, "dpo_pairs.json")
    with open(dpo_pairs_path, 'w', encoding='utf-8') as f:
        json.dump(combined_dpo_pairs, f, ensure_ascii=False, indent=4)
    print(f"DPO pairs saved: {dpo_pairs_path}")
    
    return over_count, under_count

if __name__ == "__main__":
    folder = "output/search-r1-7b/hotpotqa_2025_09_23_15_11_decision-schr1"
    save_dir = "dpo_data/decision_hotpotqa"
    over_count, under_count = analyze_dpo_pairs(folder, save_dir=save_dir)
    if over_count is not None and under_count is not None:
        print(f"Count of over-search DPO pairs: {over_count}")
        print(f"Count of under-explore DPO pairs: {under_count}")
