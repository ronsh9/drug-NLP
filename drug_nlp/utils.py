import rdkit
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem, Descriptors
import rdkit.Chem.QED as QED
from rdkit import rdBase

rdBase.DisableLog("rdApp.error")
from rdkit.Chem import rdMolDescriptors
from rdkit.six import iteritems

import sys
import logging

def setup_logger():
    logger = logging.getLogger("eval_contam")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)

    logger.addHandler(sh)
    return logger

logger = setup_logger()


def similarity(smiles_a, smiles_b):
    """Evaluate Tanimoto similarity between 2 SMILES strings

    Args:
      smiles_a: str, SMILES string
      smiles_b: str, SMILES string

    Returns:
      similarity score: float, between 0 and 1.

    """
    if smiles_a is None or smiles_b is None:
        return 0.0
    amol = Chem.MolFromSmiles(smiles_a)
    bmol = Chem.MolFromSmiles(smiles_b)
    if amol is None or bmol is None:
        return 0.0
    fp1 = AllChem.GetMorganFingerprintAsBitVect(amol, 2, nBits=2048, useChirality=False)
    fp2 = AllChem.GetMorganFingerprintAsBitVect(bmol, 2, nBits=2048, useChirality=False)
    return DataStructs.TanimotoSimilarity(fp1, fp2)

def score_against_known_drugs(smiles_query, smiles_list):
    """Evaluate if a given SMILES string is close to a known list of SMILES strings
    Args:
      smiles_query: str, SMILES string
      smiles_list: list of str, SMILES strings
      
      Returns:
      similarity score: float, between 0 and 1.
      
    """
    similarity_list = []
    for smi in smiles_list:
        similarity_list.append(similarity(smi, smiles_query))
    return max(similarity_list)
