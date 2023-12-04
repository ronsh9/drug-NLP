import json
import pandas as pd  # Needed for checking NaN

def analyze_json_file(filepath):
    # Load JSON data
    with open(filepath, 'r') as file:
        data = json.load(file)

    # Check if data is a dictionary
    if not isinstance(data, dict):
        print("The top level of the JSON file is not a dictionary.")
        return

    # 1. Number of keys in the level 1 dictionary
    level_1_keys_count = len(data)
    print("Number of keys in level 1 dictionary:", level_1_keys_count)

    # Initialize counters
    active_ingredient_count = 0
    disease_info_count = 0
    additional_info_count = 0
    all_criteria_count = 0

    for key, value in data.items():
        if isinstance(value, dict):
            active_ingredient_valid = "Active Ingredients" in value and \
                any(isinstance(v, str) and v for v in value["Active Ingredients"].values() if not pd.isna(v))
            
            disease_info_valid = "Disease Information" in value and \
                isinstance(value["Disease Information"], dict) and len(value["Disease Information"]) > 0

            additional_info_valid = "Additional Information" in value and \
                isinstance(value["Additional Information"], dict) and len(value["Additional Information"]) > 0

            # Update individual counters
            active_ingredient_count += active_ingredient_valid
            disease_info_count += disease_info_valid
            additional_info_count += additional_info_valid

            # Update all criteria counter
            if active_ingredient_valid and disease_info_valid and additional_info_valid:
                all_criteria_count += 1

    print("Number of keys with valid 'Active Ingredients':", active_ingredient_count)
    print("Number of keys with valid 'Disease Information':", disease_info_count)
    print("Number of keys with valid 'Additional Information':", additional_info_count)
    print("Number of keys satisfying all three criteria:", all_criteria_count)


def count_unique_contents(file_path):
    unique_contents = set()

    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            for message in data['messages']:
                content = message['content']
                unique_contents.add(content)

    return len(unique_contents)


# analyze_json_file('scraper/data/drug_info.json')
print(count_unique_contents('scraper/data/final_finetune_dataset.jsonl'))