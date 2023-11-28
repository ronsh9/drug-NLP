import json
import tiktoken
import pandas as pd

def make_finetune_dataset(drug_info_filename, output_finetune_filename):
    """
    Given drug info dataset, turn it into an openai compatible json file for finetuning by constructing a prompt and desired response.
    """
    def num_tokens_from_string(string: str) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        num_tokens = len(encoding.encode(string))
        return num_tokens
    # Open and read the JSON file
    with open(drug_info_filename, 'r') as file:
        data = json.load(file)

    df = pd.DataFrame(data)
    drugs = df.columns
    rows = df.index
    disease_prompts = dict()


    for drug in drugs:
        diseases = df[drug]['Disease Information']
        # print(diseases)
        receptors = df[drug]['Additional Information']['targets']
        rec_data = dict()
        k = list(df[drug]['Active Ingredients'].keys())
        smile = df[drug]['Active Ingredients'][k[0]]
        #collect all receptors per drug
        for r in receptors:
            rec_data[r['Label']] = {'Amino acid sequence' : r['Detailed Info']['Amino acid sequence'], 
                                    'General Function': r['Detailed Info']['General Function'],
                                    'Specific Function' : r['Detailed Info']['Specific Function']}                   
        for dis in diseases:
            if diseases[dis]==None:
                info =''
            else:
                info = ', is '+ diseases[dis]
            other_diseases = [disease for disease in diseases if disease != dis]
            # Choose the first 5 diseases from the list of other diseases
            selected_diseases = other_diseases[:5]
            disease_prompts[dis] = {'info': info, 'receptors': rec_data, 'drug_smile' : smile, 'similar_conditions': selected_diseases}
 
    templates_prompts_w_smiles = dict()
    for d in disease_prompts:
        receptors = []
        #going over the receptors per disease:
        for r in disease_prompts[d]['receptors']:
            gf=disease_prompts[d]['receptors'][r]['General Function']
            sf = disease_prompts[d]['receptors'][r]['Specific Function']
            ac = disease_prompts[d]['receptors'][r]['Amino acid sequence']
            ac = '\n'.join(ac.split('\n')[1:]) #remove first line with not sequence stuff

            receptor_str = f'Receptor {r}: '
            if gf is not None and gf != '':
                receptor_str += f'It has general function: {gf}. '
            if sf is not None and sf != '':
                receptor_str += f'It has specific function: {sf} '
            if ac is not None and ac != '':
                receptor_str += f'Its amino acid sequence is: {ac}. '
            receptors.append(receptor_str)
        allreceptors = '\n'.join(receptors)
        i=disease_prompts[d]['info']
        
        similar_conditions = disease_prompts[d]['similar_conditions']
        if similar_conditions != None and similar_conditions != '' and similar_conditions != []:
            similar_conditions = ', '.join(similar_conditions)
            similar_disease = f'Some associated conditions are {similar_conditions}.'
            
        # if i != '':
        #     print(d, disease_prompts[d])
        #     break
        prompt = f'You are an expert in drug discovery, please generate a novel binder molecule for the following disease. Respond with a SMILES string of a hypothetical possible binder molecule. The disease is {d}{i}. {similar_disease} It has the following receptors:\n{allreceptors}'
        smile = disease_prompts[d]['drug_smile']
        num_tokens = num_tokens_from_string(prompt+smile)
        while num_tokens>3950:
            last_receptor_index = prompt.rfind("Receptor")
            prompt = prompt[:last_receptor_index]
            num_tokens = num_tokens_from_string(prompt+smile)

        templates_prompts_w_smiles[d] = {'prompt':prompt, 'smile_output': smile}
                
    data_path = output_finetune_filename

    with open(data_path, "w") as file:
        for disease, example in templates_prompts_w_smiles.items():
            data = {"messages":[{"role": "user", "content": example['prompt']}, {"role": "assistant", "content": example['smile_output']},]}
            file.write(json.dumps(data) + "\n")
if __name__=="__main__":
    make_finetune_dataset("data/subsampled_drug_info.json", "data/sample_finetune_dataset.jsonl")