#!/bin/bash
#SBATCH --job-name TDB_partial_index
#SBATCH --account=project_200xxxx
#SBATCH --time 00:10:00
#SBATCH --partition=small
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G

module load geoconda/3.10.9

srun python src/main_join_partial_layers.py 4 2005 0