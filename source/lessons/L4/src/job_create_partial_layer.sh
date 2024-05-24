#!/bin/bash
#SBATCH --job-name TDB_partial_index
#SBATCH --account=project_200xxxx
#SBATCH --time 00:10:00
#SBATCH --partition=small
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --array=0-3

module load geoconda/3.10.9

srun python src/main_create_partial_layer.py ${SLURM_ARRAY_TASK_ID} 4 2005 0