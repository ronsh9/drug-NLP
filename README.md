# drug-NLP

## Get PMO benchmark

`git submodule update --init --recursive`

## Description

An exeprienced medicinal chemist could have a fair guess of binder structure for a given disease target, which could serve as a start point of a drug discovery compaign. This project aims to train an LLM to enhance their ability in this, in few/zero-shot manner.

The input is a description of the disease and the associated target protein. The expected output is a SMILES string of the initial guess.
We evaluate the success by measuring the similarity between the proposed drug and a list of known drugs that match the input description.

# Run

`bash scripts/run_baseline.sh`



