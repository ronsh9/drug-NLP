#!/bin/bash
#SBATCH -N 1
#SBATCH -n 40
#SBATCH --nodelist=node1238
#SBATCH --mem=200G
#SBATCH --time=200:00:00
#SBATCH --constraint=centos7
#SBATCH --partition=sched_mit_ccoley

python -u final_scarpe.py > dataset_generation.txt