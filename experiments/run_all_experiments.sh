#!/bin/bash
set -eo pipefail

run_names=('baseline_150k' 'baseline_450k' 'baseline' 'just_five_fonts' 'just_one_font' 'plain_white_background'
    'remove_blur' 'remove_distorsion' 'remove_skew' 'train_on_kpti.yaml')

for run_name in "${run_names[@]}"; do
    echo "Training $run_name"
    # Train model
    python3 -m paddle.distributed.launch --gpus '2,3' /home/gusandmich@GU.GU.SE/PaddleOCR/tools/train.py -c configs/$run_name.yaml
    # Evaluate model on baseline test data
    echo "Evaluating $run_name"
    python3 -m paddle.distributed.launch --gpus '2,3' /home/gusandmich@GU.GU.SE/PaddleOCR/tools/eval.py -c configs/$run_name.yaml
done
