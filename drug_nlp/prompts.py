prompt_templates = {
    "baseline1": {
        "instruction": "You are an expert in drug discovery, exclusively focused on providing highly accurate prediction of binder molecules as the start points for discovering new drugs. Now you are investigating the disease as described below. Could you give a guess of what molecular structure could exhibit activity against it? Please answer the chemical structure in SMILES string.\n\n", 
        "prediction": "Disease: {disease_text}\nDrug:\n",
        "stop_token": "\n\n",
    },
    "baseline2": {
        "instruction": "You are an expert in drug discovery, exclusively focused on providing highly accurate prediction of binder molecules as the start points for discovering new drugs. Now you are investigating the disease as described below. Could you give a guess of what molecular structure could exhibit activity against it? Please answer the chemical structure in SMILES string.\n\n", 
        "exemplar": "Disease: {disease_text}\nDrug:\n{drug_smiles}\n\n",
        "prediction": "Disease: {disease_text}\nDrug:\n",
        "stop_token": "\n\n",
    },
}
