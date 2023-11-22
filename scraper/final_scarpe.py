import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os

def get_drug_info(drug_name):
    """
    Get information on the drug. The returned object is a dictionary that contains all the sections on the drug info from the first (main) card
    in drugbank.
    """
    url = f"https://www.drugbank.ca/unearth/q?query={drug_name}&searcher=drugs"
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to retrieve the page"

    soup = BeautifulSoup(response.text, 'html.parser')
    drug_info = {}

    headers = soup.find_all('h2')  # Find the main headers (h2 elements)
    for header in headers:
        header_title = header.get_text().strip()
        next_element = header.find_next_sibling()
        
        drug_info[header_title] = {} # Used to store the info for a particular section

        while next_element and next_element.name != 'h2':
            if next_element.name == 'dl':
                for dt, dd in zip(next_element.find_all('dt'), next_element.find_all('dd')):
                    subtitle = dt.get_text().strip()
                    content = dd.get_text().strip()
                    drug_info[header_title][subtitle] = content
            next_element = next_element.find_next_sibling()

    return drug_info

def get_additional_info(drug_name):
    """
    Get information on the target(s). The returned object is a dictionary that contains all the sections on the drug info from the second card
    in drugbank.
    """
    url = f"https://www.drugbank.ca/unearth/q?query={drug_name}&searcher=drugs"
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to retrieve the page"

    soup = BeautifulSoup(response.text, 'html.parser')
    additional_info = {}

    containers = soup.find_all('div', class_='bond-list-container') # Find all containers with class 'bond-list-container', this is how the target information is usually found
    for container in containers:
        container_id = container.get('id')
        if container_id:
            additional_info[container_id] = []

            cards = container.find_all('div', class_='bond card') # The number of extra information cards may vary so find everything that you can
            for card in cards:
                card_data = {}

                card_header = card.find('div', class_='card-header')
                if card_header:
                    label_tag = card_header.find('strong')
                    if label_tag and label_tag.find('a'):
                        label = label_tag.find('a').get_text().strip()
                        card_data['Label'] = label

                dl_elements = card.find_all('dl') # Extract other data from the card body
                for dl in dl_elements:
                    for dt, dd in zip(dl.find_all('dt'), dl.find_all('dd')):
                        dt_text = dt.get_text().strip()
                        dd_text = dd.get_text().strip()
                        card_data[dt_text] = dd_text

                additional_info[container_id].append(card_data)

    return additional_info

def search_link(url_suffix):
    """ 
    Helper function to go to the function under the headers in the additional info section (secondary cards) in Drugbank.
    """
    base_url = "https://go.drugbank.com"
    detailed_url = f"{base_url}{url_suffix}"
    response = requests.get(detailed_url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    detailed_info = {}

    dl_elements = soup.find_all('dl') # The structure of detailed pages can be different, this is a general approach
    for dl in dl_elements:
        for dt, dd in zip(dl.find_all('dt'), dl.find_all('dd')):
            dt_text = dt.get_text().strip()
            dd_text = dd.get_text().strip()
            detailed_info[dt_text] = dd_text

    return detailed_info

def get_additional_info_detailed(drug_name):
    """
    More detailed version of the get_additional_info function. In the previous function we read all the information form the Drugbank page of the drug.
    Here, we go to the Drugbank page of the considered extra information piece (target, enzyme, trasportation, etc.) and read the information from there.
    This information is generally more detailed.
    """
    url = f"https://www.drugbank.ca/unearth/q?query={drug_name}&searcher=drugs"
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to retrieve the page"

    soup = BeautifulSoup(response.text, 'html.parser')
    additional_info = {}

    containers = soup.find_all('div', class_='bond-list-container') # Find all containers with class 'bond-list-container'
    for container in containers:
        container_id = container.get('id')
        if container_id:
            additional_info[container_id] = []

            cards = container.find_all('div', class_='bond card') # Find all individual cards within the container as we don't know how many there're in total
            for card in cards:
                card_data = {}

                card_header = card.find('div', class_='card-header') # Extract the label from the card header
                if card_header:
                    label_tag = card_header.find('strong')
                    if label_tag and label_tag.find('a'):
                        label = label_tag.find('a').get_text().strip()
                        card_data['Label'] = label

                    detail_link = card_header.find('a', class_='bond-details-link') # Find the detail link and fetch detailed info
                    if detail_link:
                        link_suffix = detail_link['href']
                        detailed_info = search_link(link_suffix)
                        if detailed_info:
                            card_data['Detailed Info'] = detailed_info

                additional_info[container_id].append(card_data)

    return additional_info

def get_wikipedia_top_section(symptom):
    """
    Get the top section content from a Wikipedia page
    """
    base_url = "https://en.wikipedia.org/wiki/"
    safe_symptom = '_'.join(symptom.split())  # Replace spaces with underscores for URL
    response = requests.get(base_url + safe_symptom)
    
    if response.status_code != 200:
        return None  # If the page does not exist or an error occurred
    
    soup = BeautifulSoup(response.text, 'html.parser')
    top_section = soup.find('p', class_=False)  # The first paragraph after the heading is usually the top section
    return top_section.get_text() if top_section else None

def get_symptoms_info(drug_info):
    """
    Extract information about associated conditions from the 'Pharmacology' section
    of the drug information and get the top section from the Wikipedia page for each symptom.
    """
    symptoms_info = {}
    try:
        associated_info_str = drug_info['Pharmacology']['Associated Conditions']
    except:
        associated_info_str = drug_info['Pharmacology']['Associated Therapies']

    if not associated_info_str:
        return None
    
    symptoms = associated_info_str.split('\n')

    
    for symptom in symptoms:
        symptom_splitted = symptom.split(' ')
        last_word = symptom_splitted[-1]
        if '(' and ')' in last_word:
            symptom = ' '.join(symptom_splitted[:-1])
            
        symptom_content = get_wikipedia_top_section(symptom.strip())
        symptoms_info[symptom.strip()] = symptom_content
    
    return symptoms_info

def scrape_drug_info(drug_name):
    try:
        drug_info = get_drug_info(drug_name)
    except:
        drug_info = None


    try:
        additional_info = get_additional_info_detailed(drug_name)
    except:
        try:
            additional_info = get_additional_info(drug_name)
        except:
            additional_info = None

            
    try:
        disease_info = get_symptoms_info(drug_info)
    except:
        disease_info = None
    
    return drug_info, additional_info, disease_info


def create_json_dataset(csv_path, json_dir):
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Initialize the final result dictionary
    result = {}

    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        drug_name = row['Drug Name']
        # Initialize the dictionary for this drug
        drug_dict = {}

        # Add active ingredients and SMILES to the drug dictionary
        active_ingredients = {
            row[f'Active Ingredient {i}']: row[f'SMILES {i}']
            for i in range(13) if pd.notna(row[f'Active Ingredient {i}'])
        }
        drug_dict["Active Ingredients"] = active_ingredients

        # Get detailed drug information using the scrape_drug_info function
        drug_info, additional_info, disease_info = scrape_drug_info(drug_name)
        drug_dict.update({
            'Drug Information': drug_info,
            'Additional Information': additional_info,
            'Disease Information': disease_info
        })

        # Add the drug dictionary to the result under the drug name key
        result[drug_name] = drug_dict

    # Define the JSON file path
    json_file_path = os.path.join(json_dir, 'drug_info.json')

    # Write the result dictionary to a JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)

    print(f"JSON file created at {json_file_path}")

if __name__ == "__main__":
    create_json_dataset('data/drug-actives.csv', 'data/')