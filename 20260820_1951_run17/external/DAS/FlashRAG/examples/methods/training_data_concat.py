import json
from pathlib import Path
import random
import os

base_input_dir = Path("dpo_data")
output_dir = base_input_dir / "experiments_datasets_v2"

hotpotqa_input_dir = base_input_dir / "combined_hotpotqa_data"
input_files = {
    "hotpotqa_over": hotpotqa_input_dir / "over_search_dpo.json",
    "hotpotqa_under": hotpotqa_input_dir / "under_search_dpo_regenerated.json",
}

OVER_SEARCH_SAMPLE_COUNT = 5000


def clean_and_validate_data(data_list: list, file_name_for_logging: str) -> list:
    cleaned_data = []
    discarded_count = 0
    
    print(f"  Performing generic validation and cleaning for '{file_name_for_logging}'...")
    
    for item in data_list:
        required_keys = ["prompt", "chosen", "rejected"]
        if not all(key in item for key in required_keys):
            discarded_count += 1
            continue
        
        clean_item = {
            "system": item.get("system", ""),
            "prompt": item["prompt"],
            "chosen": item["chosen"],
            "rejected": item["rejected"],
        }
        cleaned_data.append(clean_item)
    
    if discarded_count > 0:
        print(f"  Cleaning complete: Kept {len(cleaned_data)} items, discarded {discarded_count} items.")
    else:
        print(f"  Cleaning complete: All {len(cleaned_data)} items conform to the basic format.")
        
    return cleaned_data

def clean_and_validate_under_search_data(data_list: list, file_name_for_logging: str) -> list:
    """
    Specialized cleaning function for under-search data.
    - Applies generic cleaning rules.
    - Additional rule: 'chosen' must contain '<search>' and must end with '</search>'.
    """
    # First, perform generic cleaning
    base_cleaned_data = clean_and_validate_data(data_list, file_name_for_logging)
    
    final_cleaned_data = []
    skipped_no_search_tag = 0
    added_closing_tag = 0
    
    print(f"  Performing under-search specific rule checks for '{file_name_for_logging}'...")

    for item in base_cleaned_data:
        chosen_content = item["chosen"]

        # Rule 1: If <search> is not in chosen, skip
        if "<search>" not in chosen_content:
            skipped_no_search_tag += 1
            continue

        # Rule 2: If <search> exists but </search> does not, append it
        if "</search>" not in chosen_content:
            item["chosen"] = chosen_content.strip() + "</search>"
            added_closing_tag += 1
        
        final_cleaned_data.append(item)
    
    print("  Specific rule check complete:")
    print(f"    - Discarded due to missing '<search>' tag in chosen: {skipped_no_search_tag} items")
    print(f"    - Appended closing '</search>' tag to chosen: {added_closing_tag} items")
    print(f"    - Finally kept: {len(final_cleaned_data)} items")

    return final_cleaned_data

def process_datasets(inputs: dict, output_base_path: Path, over_search_count: int):
    """
    Main process for handling DPO datasets
    """
    print("--- Starting dataset processing ---")
    output_base_path.mkdir(parents=True, exist_ok=True)
    print(f"Output directory '{output_base_path}' confirmed or created.")

    # --- Processing over-search data ---
    over_search_src = inputs["hotpotqa_over"]
    over_search_dest = output_base_path / "over_search_only.json"
    sampled_over_data = []
    if over_search_src.exists():
        print(f"\nProcessing over-search file: '{over_search_src}'")
        try:
            with open(over_search_src, 'r', encoding='utf-8') as f:
                all_over_data_raw = json.load(f)
            # Use the generic cleaning function
            all_over_data_clean = clean_and_validate_data(all_over_data_raw, str(over_search_src))
            
            # Sampling...
            if len(all_over_data_clean) < over_search_count:
                sampled_over_data = all_over_data_clean
            else:
                # random.seed(42)
                # sampled_over_data = random.sample(all_over_data_clean, over_search_count)
                sampled_over_data = all_over_data_clean[:over_search_count]

            # Saving...
            with open(over_search_dest, 'w', encoding='utf-8') as f:
                json.dump(sampled_over_data, f, indent=4, ensure_ascii=False)
            print(f"  Successfully sampled and saved {len(sampled_over_data)} over-search data items.")
        except Exception as e:
            print(f"  An error occurred while processing over-search data: {e}")
    else:
        print(f"Warning: over-search input file '{over_search_src}' not found, skipping.")

    # --- Processing under-search data ---
    under_search_src = inputs["hotpotqa_under"]
    under_search_dest = output_base_path / "under_search_only.json"
    cleaned_under_data = []
    if under_search_src.exists():
        print(f"\nProcessing under-search file: '{under_search_src}'")
        try:
            with open(under_search_src, 'r', encoding='utf-8') as f:
                all_under_data_raw = json.load(f)
            # ! Use the new, specialized cleaning function
            cleaned_under_data = clean_and_validate_under_search_data(all_under_data_raw, str(under_search_src))
            
            # Saving...
            with open(under_search_dest, 'w', encoding='utf-8') as f:
                json.dump(cleaned_under_data, f, indent=4, ensure_ascii=False)
            print(f"  Successfully cleaned and saved {len(cleaned_under_data)} under-search data items.")
        except Exception as e:
            print(f"  An error occurred while processing under-search data: {e}")
    else:
        print(f"Warning: under-search input file '{under_search_src}' not found, skipping.")

    # --- Merging processed data ---
    all_dpo_data_dest = output_base_path / "all_dpo_data.json"
    if not sampled_over_data or not cleaned_under_data:
        print("\nError: Cannot perform merge operation due to missing data.")
    else:
        print(f"\nMerging {len(sampled_over_data)} over-search items and {len(cleaned_under_data)} under-search items...")
        all_dpo_data = sampled_over_data + cleaned_under_data
        random.shuffle(all_dpo_data)
        print(f"Merge complete, total of {len(all_dpo_data)} items.")

        with open(all_dpo_data_dest, 'w', encoding='utf-8') as f:
            json.dump(all_dpo_data, f, indent=4, ensure_ascii=False)
        print(f"Merged file '{all_dpo_data_dest}' saved successfully.")
    
    print("\n--- Processing finished ---")

# --- 3. Execute script ---
if __name__ == "__main__":
    process_datasets(
        inputs=input_files, 
        output_base_path=output_dir, 
        over_search_count=OVER_SEARCH_SAMPLE_COUNT
    )
