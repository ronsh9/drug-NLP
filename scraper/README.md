Files:
- `data/fda-drugs-raw.csv` is the raw list of drug details from Drugs @ FDA
- `data/drug-actives.csv` is the processed csv. Each row is drug name and the associated active ingredients + smiles
- `mini_drug_actives.csv` is a sub-sampled dataset from `data/drug-actives.csv`
- `mini_drug_info.json` is the output of the final dataset generation code on `mini_drug_actives.csv`

The scraper is currently located in scrape.ipynb, hopefully there's enough comments to be roughly sensible

Final dataset generation code is in `scrape_drug_info.ipynb` and in the equivalent .py file `final_scarpe`
