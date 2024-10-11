#!/bin/bash
set -eo pipefail

# Train
python3 create_label_files.py --dir-path /scratch/gusandmich/final_assignment/KPTI/KPTI-TrainData --output-file /scratch/gusandmich/final_assignment/KPTI/KPTI-TrainData/_gt.txt

# Test
python3 create_label_files.py --dir-path /scratch/gusandmich/final_assignment/KPTI/KPTI-TestData --output-file /scratch/gusandmich/final_assignment/KPTI/KPTI-TestData/_gt.txt

# Validate
python3 create_label_files.py --dir-path /scratch/gusandmich/final_assignment/KPTI/KPTI-ValidData --output-file /scratch/gusandmich/final_assignment/KPTI/KPTI-ValidData/_gt.txt
