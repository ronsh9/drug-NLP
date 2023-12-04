# run on our own database
python mol_opt/run.py graph_ga --smi_file eval/data/example.tab --output_dir eval/results --task production --n_runs 1 --oracles qed > eval/results/out.txt

# run on the ZINC database
# python mol_opt/run.py graph_ga --output_dir eval/results --task production --n_runs 1 --oracles qed