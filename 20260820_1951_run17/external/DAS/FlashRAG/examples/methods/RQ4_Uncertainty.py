import json
import os
import re
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu
from sklearn.metrics import roc_curve, auc
from flashrag.utils.utils import extract_between

# ==============================================================================
# Data Processing and Evaluation Functions (No changes needed here)
# ==============================================================================

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

def evaluate_prediction(pred, golden_answers, config={"dataset_name": None}, threshold=0.8):
    if not pred or not golden_answers:
        return 0, 0, False
    normalized_pred = normalize_answer(pred)
    normalized_golden = [normalize_answer(ans) for ans in golden_answers]
    if not normalized_pred or not any(normalized_golden):
        return 0, 0, False
    
    # --- Using a temporary mock implementation ---
    if not hasattr(evaluate_prediction, "em_metric"):
        print("Warning: Using mock evaluation functions. Ensure flashrag is correctly installed for real use.")
        evaluate_prediction.em_metric = lambda p, g: 1.0 if p in g else 0.0
        evaluate_prediction.f1_metric = lambda p, g: {"f1": 1.0} if p in g else {"f1": 0.0}
    em_score = evaluate_prediction.em_metric(normalized_pred, normalized_golden)
    f1_score_dict = evaluate_prediction.f1_metric(normalized_pred, normalized_golden)
    # --- End of mock implementation ---

    f1_score = f1_score_dict.get("f1", 0)
    is_correct = (f1_score >= threshold)
    return em_score, f1_score, is_correct

def analyze_dpo_pairs(folder_path, filename="intermediate_data.json", f1_threshold=0.8, is_search_o1=False):
    file_path = os.path.join(folder_path, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None
    
    search_oversearch_uncertainties = []
    search_correct_uncertainties = []
    answer_underexplore_uncertainties = []
    answer_correct_uncertainties = []

    begin_of_answer_token, end_of_answer_token = ("\\boxed{", "}") if is_search_o1 else ("<answer>", "</answer>")

    print(f"Total samples: {len(data)}")
    
    for item in data:
        golden_answers = item.get("golden_answers")
        output = item.get("output", {})
        simulated_outputs = output.get("simulated_outputs", [])
        
        if not simulated_outputs:
            continue

        final_step = simulated_outputs[-1]
        final_original_output = final_step.get("original_output")
        final_pred = extract_answer(final_original_output, begin_of_answer_token, end_of_answer_token)
        _, _, is_final_correct = evaluate_prediction(final_pred, golden_answers, threshold=f1_threshold)
        final_uncertainty = (final_step.get("original_perplexity"), final_step.get("original_entropy"))
        
        if final_uncertainty[0] is not None and final_uncertainty[1] is not None:
            if not is_final_correct:
                answer_underexplore_uncertainties.append(final_uncertainty)
            else:
                answer_correct_uncertainties.append(final_uncertainty)

        for sim_step in simulated_outputs[:-1]:
            answer_only_output = sim_step.get("answer_only_output")
            if not answer_only_output:
                continue
            forced_pred = extract_answer(answer_only_output, begin_of_answer_token, end_of_answer_token)
            _, _, is_forced_correct = evaluate_prediction(forced_pred, golden_answers, threshold=f1_threshold)
            step_uncertainty = (sim_step.get("original_perplexity"), sim_step.get("original_entropy"))

            if step_uncertainty[0] is not None and step_uncertainty[1] is not None:
                if is_forced_correct:
                    search_oversearch_uncertainties.append(step_uncertainty)
                else:
                    search_correct_uncertainties.append(step_uncertainty)

    return {
        "search_over_raw": search_oversearch_uncertainties,
        "search_correct_raw": search_correct_uncertainties,
        "answer_under_raw": answer_underexplore_uncertainties,
        "answer_correct_raw": answer_correct_uncertainties
    }

# ==============================================================================
# Method 2: Violin Plots (MODIFIED with centralized font control)
# ==============================================================================
def plot_uncertainty_distributions(raw_data, metric='Entropy'):
    """
    Visualizes uncertainty distributions using violin plots with unified font settings.
    """
    print(f"\n--- Generating '{metric}' distribution plot... ---")

    # ==================== UNIFIED FONT & PLOT CONFIGURATION ====================
    # NOTE: Ensure 'Times New Roman' font is installed on your system.
    FONT_CONFIG = {
        "family": "Times New Roman",
        "caption_size": 42,
        "axis_label_size": 40, # Slightly smaller than caption
        "tick_label_size": 36  # Slightly smaller than axis label
    }

    try:
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['font.serif'] = [FONT_CONFIG["family"]] + plt.rcParams['font.serif']
        # Use a math font that pairs well with Times New Roman
        plt.rcParams['mathtext.fontset'] = 'stix' 
    except Exception as e:
        print(f"Warning: Could not set font to '{FONT_CONFIG['family']}'. Using default. Error: {e}")
    # ========================================================================

    metric_idx = 0 if metric == 'Perplexity' else 1

    plot_data = []
    for item in raw_data.get("search_over_raw", []):
        plot_data.append({"Step Type": "Search", "Category": "Over\nSearch", metric: item[metric_idx]})
    for item in raw_data.get("search_correct_raw", []):
        plot_data.append({"Step Type": "Search", "Category": "Correct\nSearch", metric: item[metric_idx]})
    for item in raw_data.get("answer_under_raw", []):
        plot_data.append({"Step Type": "Answer", "Category": "Under\nSearch", metric: item[metric_idx]})
    for item in raw_data.get("answer_correct_raw", []):
        plot_data.append({"Step Type": "Answer", "Category": "Correct\nAnswer", metric: item[metric_idx]})
        
    df = pd.DataFrame(plot_data)
    
    if df.empty:
        print(f"No valid data for '{metric}', skipping plot generation.")
        return

    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    palette = {
        "Correct\nSearch": "cornflowerblue", 
        "Over\nSearch": "tomato",
        "Correct\nAnswer": "cornflowerblue",
        "Under\nSearch": "tomato"
    }

    # --- Left Plot: Search Step ---
    df_search = df[df["Step Type"] == "Search"]
    if not df_search.empty:
        sns.violinplot(
            ax=axes[0], data=df_search, x="Category", y=metric,
            order=["Correct\nSearch", "Over\nSearch"], palette=palette
        )
        axes[0].set_xlabel('(a) Search Step', fontsize=FONT_CONFIG["caption_size"])
        axes[0].set_ylabel(metric, fontsize=FONT_CONFIG["axis_label_size"])
        axes[0].tick_params(axis='both', which='major', labelsize=FONT_CONFIG["tick_label_size"])
        axes[0].set_xticklabels(axes[0].get_xticklabels(), size=FONT_CONFIG["tick_label_size"])
    else:
        axes[0].text(0.5, 0.5, 'No Search Data', ha='center', va='center', fontsize=16)

    # --- Right Plot: Answer Step ---
    df_answer = df[df["Step Type"] == "Answer"]
    if not df_answer.empty:
        sns.violinplot(
            ax=axes[1], data=df_answer, x="Category", y=metric,
            order=["Correct\nAnswer", "Under\nSearch"], palette=palette
        )
        axes[1].set_xlabel('(b) Answer Step', fontsize=FONT_CONFIG["caption_size"])
        axes[1].set_ylabel('') # No label for the right plot
        axes[1].tick_params(axis='both', which='major', labelsize=FONT_CONFIG["tick_label_size"])
        axes[1].tick_params(axis='y', labelleft=False)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), size=FONT_CONFIG["tick_label_size"])
    else:
        axes[1].text(0.5, 0.5, 'No Answer Data', ha='center', va='center', fontsize=16)

    # --- Y-axis Scaling and Layout ---
    y_min, y_max = -0.05, 0.4
    axes[0].set_ylim(y_min, y_max)
    axes[1].set_ylim(y_min, y_max)
    
    plt.tight_layout(pad=2.0)
    
    base_filename = f"uncertainty_distribution_{metric.lower()}"
    plt.savefig(f"{base_filename}.pdf", bbox_inches='tight')
    plt.savefig(f"{base_filename}.png", bbox_inches='tight', dpi=300)
    
    plt.show()

# ==============================================================================
# Method 3: Mann-Whitney U Test (No changes needed)
# ==============================================================================
def perform_statistical_tests(raw_data):
    """Performs Mann-Whitney U tests to compare distributions."""
    print("\n--- Performing statistical significance tests (Mann-Whitney U Test)... ---")
    
    for metric in ['Perplexity', 'Entropy']:
        metric_idx = 0 if metric == 'Perplexity' else 1
        print(f"\n--- Analyzing metric: {metric} ---")
        
        search_over = [item[metric_idx] for item in raw_data["search_over_raw"]]
        search_correct = [item[metric_idx] for item in raw_data["search_correct_raw"]]
        answer_under = [item[metric_idx] for item in raw_data["answer_under_raw"]]
        answer_correct = [item[metric_idx] for item in raw_data["answer_correct_raw"]]

        if search_over and search_correct:
            u_stat, p_val = mannwhitneyu(search_over, search_correct, alternative='two-sided')
            print(f"[Search Step] Over-search vs Correct-search:")
            print(f"  - U-statistic: {u_stat:.2f}, p-value: {p_val:.4e}")
            print(f"  - Conclusion: The difference is statistically {'significant' if p_val < 0.05 else 'not significant'} (p {'<' if p_val < 0.05 else '>='} 0.05).")

        if answer_under and answer_correct:
            u_stat, p_val = mannwhitneyu(answer_under, answer_correct, alternative='two-sided')
            print(f"[Answer Step] Under-search vs Correct-answer:")
            print(f"  - U-statistic: {u_stat:.2f}, p-value: {p_val:.4e}")
            print(f"  - Conclusion: The difference is statistically {'significant' if p_val < 0.05 else 'not significant'} (p {'<' if p_val < 0.05 else '>='} 0.05).")

# ==============================================================================
# Method 4: ROC and AUC Analysis (MODIFIED with centralized font control)
# ==============================================================================
def analyze_predictive_power_roc(raw_data):
    """Analyzes predictive power using ROC and AUC with unified font settings."""
    print("\n--- Analyzing predictive power (ROC & AUC)... ---")
    
    for metric in ['Perplexity', 'Entropy']:
        metric_idx = 0 if metric == 'Perplexity' else 1
        print(f"\n--- Analyzing metric: {metric} ---")

        # ==================== UNIFIED FONT & PLOT CONFIGURATION ====================
        # NOTE: Ensure 'Times New Roman' font is installed on your system.
        FONT_CONFIG = {
            "family": "Times New Roman",
            "caption_size": 42,
            "axis_label_size": 40, # Slightly smaller than caption
            "legend_size": 36,     # Slightly smaller than axis label
            "tick_label_size": 36
        }

        try:
            plt.rcParams['font.family'] = 'serif'
            plt.rcParams['font.serif'] = [FONT_CONFIG["family"]] + plt.rcParams['font.serif']
            plt.rcParams['mathtext.fontset'] = 'stix'
        except Exception as e:
            print(f"Warning: Could not set font to '{FONT_CONFIG['family']}'. Using default. Error: {e}")
        # ========================================================================
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 12))

        # --- 1. Search Step ---
        search_over = [item[metric_idx] for item in raw_data.get("search_over_raw", [])]
        search_correct = [item[metric_idx] for item in raw_data.get("search_correct_raw", [])]
        
        if search_over and search_correct:
            ax = axes[0]
            # Lower uncertainty should predict correctness (class 1)
            # So, higher scores (uncertainty values) predict class 0
            y_true_search = [0] * len(search_over) + [1] * len(search_correct)
            y_score_search = [-s for s in search_over] + [-s for s in search_correct]
            
            fpr, tpr, _ = roc_curve(y_true_search, y_score_search)
            roc_auc = auc(fpr, tpr)
            print(f"[Search Step] AUC for predicting correct search (vs over-search): {roc_auc:.4f}")
            
            ax.plot(fpr, tpr, color='darkorange', lw=5, label=f'AUC = {roc_auc:.2f}')
            ax.plot([0, 1], [0, 1], color='navy', lw=4, linestyle='--')
            ax.set_xlabel('FPR', fontsize=FONT_CONFIG["axis_label_size"])
            ax.set_ylabel('TPR', fontsize=FONT_CONFIG["axis_label_size"])
            ax.legend(loc="lower right", fontsize=FONT_CONFIG["legend_size"])
            ax.set_title("(a) Search Step", y=-0.3, fontsize=FONT_CONFIG["caption_size"])
            ax.set_aspect('equal', adjustable='box')
            ticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
            ax.set_xticks(ticks)
            ax.set_yticks(ticks)
            ax.tick_params(axis='both', which='major', labelsize=FONT_CONFIG["tick_label_size"])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        # --- 2. Answer Step ---
        answer_under = [item[metric_idx] for item in raw_data.get("answer_under_raw", [])]
        answer_correct = [item[metric_idx] for item in raw_data.get("answer_correct_raw", [])]
        
        if answer_under and answer_correct:
            ax = axes[1]
            # Lower uncertainty should predict correctness (class 1)
            # So, higher scores (uncertainty values) predict class 0
            y_true_answer = [0] * len(answer_under) + [1] * len(answer_correct)
            y_score_answer = [-s for s in answer_under] + [-s for s in answer_correct]
            
            fpr, tpr, _ = roc_curve(y_true_answer, y_score_answer)
            roc_auc = auc(fpr, tpr)
            print(f"[Answer Step] AUC for predicting correct answer (vs under-search): {roc_auc:.4f}")

            ax.plot(fpr, tpr, color='darkgreen', lw=5, label=f'AUC = {roc_auc:.2f}')
            ax.plot([0, 1], [0, 1], color='navy', lw=4, linestyle='--')
            ax.set_xlabel('FPR', fontsize=FONT_CONFIG["axis_label_size"])
            ax.set_ylabel('') # No label for the right plot
            ax.legend(loc="lower right", fontsize=FONT_CONFIG["legend_size"])
            ax.set_title("(b) Answer Step", y=-0.3, fontsize=FONT_CONFIG["caption_size"])
            ax.set_aspect('equal', adjustable='box')
            ticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
            ax.set_xticks(ticks)
            ax.set_yticks(ticks)
            ax.tick_params(axis='both', which='major', labelsize=FONT_CONFIG["tick_label_size"])
            ax.tick_params(axis='y', labelleft=False)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
        fig.subplots_adjust(left=0.1, bottom=0.3, right=0.97, top=0.95, wspace=0.2)
        
        base_filename = f"roc_auc_analysis_{metric.lower()}"
        plt.savefig(f"{base_filename}.pdf", bbox_inches='tight')
        plt.savefig(f"{base_filename}.png", bbox_inches='tight', dpi=300)

        plt.show()

# ==============================================================================
# Main Execution Block
# ==============================================================================
if __name__ == "__main__":
    folder = "output/search-r1-7b/hotpotqa_2025_09_23_15_11_decision-schr1-chunk1"
    
    # Check if the folder exists, if not, you might want to create mock data or exit
    if not os.path.exists(folder):
        print(f"Warning: Folder '{folder}' does not exist. Please check the path.")
        # Optional: Add your mock data generation logic here if needed
        # For now, we will exit if the data is not found.
        exit()

    # 1. Load and process data from the file
    raw_data = analyze_dpo_pairs(folder, is_search_o1=False, f1_threshold=0.8)
    
    if raw_data:
        # 2. Call Method 2: Plot violin plots
        plot_uncertainty_distributions(raw_data, metric='Entropy')
        plot_uncertainty_distributions(raw_data, metric='Perplexity')
        
        # 3. Call Method 3: Perform statistical tests
        perform_statistical_tests(raw_data)
        
        # 4. Call Method 4: Analyze ROC and AUC
        analyze_predictive_power_roc(raw_data)
        
        print("\n--- Analysis Complete ---")
        print("Please check the generated .png/.pdf files and the console output.")
