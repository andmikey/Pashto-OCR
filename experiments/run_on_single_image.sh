#!/bin/bash
set -eo pipefail

# Use this script to run a trained model on a single image

python3 /home/gusandmich@GU.GU.SE/PaddleOCR/tools/infer_rec.py -c configs/baseline.yaml \
    -o Global.pretrained_model=/scratch/gusandmich/final_assignment/experiment_outputs/baseline_initial_train/latest \
    Global.load_static_weights=false \
    Global.infer_img=/scratch/gusandmich/final_assignment/synthetic_data/baseline/0.png
