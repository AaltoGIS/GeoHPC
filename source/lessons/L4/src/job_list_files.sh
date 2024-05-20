#!/bin/bash
#SBATCH --job-name TDB_join
#SBATCH --account=project_00
#SBATCH --time 00:10:00
#SBATCH --partition=small
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G

module load geoconda/3.10.9

srun python main_list_files.py 2005
