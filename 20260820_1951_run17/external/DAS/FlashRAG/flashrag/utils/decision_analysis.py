import json
import os
import re
from collections import Counter
from flashrag.evaluator.metrics import ExactMatch, F1_Score
from flashrag.utils.utils import extract_between

# This is a global scope helper needed by the placeholder F1_Score class
def _normalize_answer(s: str) -> str:
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


def generate_analysis_report(folder_path: str, filename: str = "intermediate_data.json", f1_threshold: float = 0.9, is_search_o1: bool = False) -> str:
    """
    Analyzes evaluation data from a specified file and returns a formatted string report.

    This function encapsulates the entire analysis process, including data loading,
    metric calculation, and categorization of search behaviors (over-search/under-explore).

    Args:
        folder_path: The path to the directory containing the data file.
        filename: The name of the JSON file to analyze.
        f1_threshold: The F1 score threshold to determine correctness.
        is_search_o1: A flag to adjust answer token parsing for specific formats.

    Returns:
        A formatted multi-line string containing the analysis results,
        or an error message if the file cannot be processed.
    """
    # Nested helper functions to keep the main function self-contained
    def evaluate_prediction(pred, golden_answers, config={"dataset_name": None}, threshold=0.9):
        """Evaluate the prediction using EM and F1 metrics."""
        if not pred or not golden_answers:
            return 0, 0, False
        
        em_metric = ExactMatch(config=config)
        f1_metric = F1_Score(config=config)
        
        em_score = em_metric.calculate_em(pred, golden_answers)
        f1_score = f1_metric.token_level_scores(pred, golden_answers)["f1"]
        
        is_correct = (f1_score >= threshold)
        return em_score, f1_score, is_correct

    def analyze_data(data, f1_threshold, is_search_o1):
        """Inner function to perform the core analysis of the loaded data."""
        search_count = 0
        over_search_count = 0
        under_explore_count = 0
        finish_data_num = 0
        total_samples = len(data)

        begin_of_answer_token, end_of_answer_token = ("\\boxed{", "}") if is_search_o1 else ("<answer>", "</answer>")

        for item in data:
            golden_answers = item.get("golden_answers")
            output = item.get("output", {})
            simulated_outputs = output.get("simulated_outputs", [])
            search_count += output.get("retrieved_times", 0)
            final_pred = output.get("pred")
            
            _, _, is_final_correct = evaluate_prediction(final_pred, golden_answers, threshold=f1_threshold)
            
            # This flag ensures we only count one outcome (over-search or under-explore) per sample
            sample_counted = False

            for step_idx, sim in enumerate(simulated_outputs):
                if sample_counted:
                    break
                    
                answer_only_output = sim.get("answer_only_output")
                forced_pred = extract_between(str(answer_only_output), begin_of_answer_token, end_of_answer_token)
                if forced_pred:
                    forced_pred = forced_pred.strip()
                if not forced_pred:
                    forced_pred = str(answer_only_output).strip()
                
                _, _, is_forced_correct = evaluate_prediction(forced_pred, golden_answers, threshold=f1_threshold)
                
                # Check for Over-search: The model could have answered correctly at this step
                # but chose to search instead. This is identified if a correct answer was possible
                # before the final step was reached.
                if step_idx + 1 < len(simulated_outputs):
                    if is_forced_correct:
                        over_search_count += 1
                        finish_data_num += 1
                        sample_counted = True
                
                # Check for Under-explore: The model stopped and gave a final answer, but it was wrong.
                # This is identified only at the last step.
                elif step_idx + 1 == len(simulated_outputs):
                    if not is_final_correct:
                        under_explore_count += 1
                    # This sample is finished, whether correct or not.
                    finish_data_num += 1
                    sample_counted = True

        return total_samples, search_count, over_search_count, under_explore_count, finish_data_num

    # Main logic of the function starts here
    file_path = os.path.join(folder_path, filename)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return f"Error: File not found at: {file_path}"
    except json.JSONDecodeError:
        return f"Error: Could not decode JSON from file: {file_path}"

    if not data:
        return "Error: The data file is empty."
        
    total_samples, search_count, over_search_count, under_explore_count, finish_data_num = analyze_data(data, f1_threshold, is_search_o1)

    # Calculate final metrics
    search_avg = search_count / total_samples if total_samples > 0 else 0
    over_rate = over_search_count / finish_data_num if finish_data_num > 0 else 0
    under_rate = under_explore_count / finish_data_num if finish_data_num > 0 else 0

    # Format the results into a single string
    output_lines = [
        f"Total samples: {total_samples}",
        f"Finish data number: {finish_data_num}",
        f"Search count: {search_count}",
        f"Over search count: {over_search_count}",
        f"Under search count: {under_explore_count}",
        f"Average number of search actions: {search_avg:.4f}",
        f"Over-search rate: {over_rate:.4f}",
        f"Under-explore rate: {under_rate:.4f}"
    ]
    
    return "\n".join(output_lines)

# Example of how to use the function
if __name__ == "__main__":
    # Define the folder containing the 'intermediate_data.json' file
    target_folder = "output/hotpotqa_2025_09_25_18_14_decision-schr1-before_dpo"
    
    # Generate the report string by calling the function
    report = generate_analysis_report(target_folder)
    
    # Print the resulting string
    print("--- Analysis Report ---")
    print(report)
    print("-----------------------")

    # Example with a non-existent folder to show error handling
    print("\n--- Testing Error Handling ---")
    report_error = generate_analysis_report("path/to/non_existent_folder")
    print(report_error)
    print("----------------------------")