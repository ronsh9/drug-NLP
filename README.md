# drug-NLP

## Description

An exeprienced medicinal chemist could have a fair guess of binder structure for a given disease target, which could serve as a start point of a drug discovery compaign. This project aims to train an LLM to enhance their ability in this, in few/zero-shot manner.

The input is a description of the disease and the associated target protein. The expected output is a SMILES string of the initial guess.
We evaluate the success by measuring the similarity between the proposed drug and a list of known drugs that match the input description.

## Setup

### Initialize submodules
`git submodule update --init --recursive`

Python 3.11+ should work, with the standard scientific computing libraries installed. 


## Run

### Creating the initial drug dataset

Use `scrape.ipynb` to pull from FDA and get active ingredients + SMILES strings from DrugBank.

Then use `final_scarpe.py` to get the disease and other drug info and store it.

### Creating the fine tuning dataset

From the drug info, use `generate_finetune.py` in order to generate the prompt for each drug. 

### Running Baseline

`bash scripts/run_baseline.sh`

### Run graph GA
After fine-tuning and generating the fine-tuned outputs of our model, we can use graph GA to evolve it.

In /mol_opt/: `python run_drug_nlp.py ../final_finetuning/results/10_production_experiment.csv`
Or in base directory, run `./scripts/run_ga.sh`
