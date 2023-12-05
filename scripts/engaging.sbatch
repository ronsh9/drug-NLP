#!/bin/bash
#SBATCH -n 1 # Request 1 tasks (cores)
#SBATCH -N 1 # Request 1 node
#SBATCH -t 0-08:00 # 8 hrs
#SBATCH -C centos7 # Request only Centos7 nodes
#SBATCH -p sched_mit_hill # only hill partition
#SBATCH --mem-per-cpu=8000 # 8G
#SBATCH -o output_%j.txt # redirect output to output_JOBID.txt
#SBATCH -e error_%j.txt # redirect errors to error_JOBID.txt
#SBATCH --mail-type=BEGIN,END # Mail when job starts and ends
#SBATCH --mail-user=ethany@mit.edu
#SBATCH --array=0-7

arr=("10_train_experiment.csv" "50_train_experiment.csv" "200_train_experiment.csv" "1000_train_experiment.csv" "10_production_experiment.csv" "100_train_experiment.csv" "400_train_experiment.csv")
source /home/ethany/drug-nlp/drug-NLP/nlp/bin/activate
cd /home/ethany/drug-nlp/drug-NLP/
echo "final_finetuning/results/${arr[$SLURM_ARRAY_TASK_ID]}"
./scripts/run_ga.sh "final_finetuning/results/${arr[$SLURM_ARRAY_TASK_ID]}"