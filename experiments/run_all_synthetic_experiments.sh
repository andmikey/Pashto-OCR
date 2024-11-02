#!/bin/bash
set -eo pipefail

run_names=('just_one_font' 'plain_white_background' 'remove_blur' 'remove_distorsion' 'remove_skew' 'train_on_kpti' 'baseline_150k' 'baseline_450k')

for run_name in "${run_names[@]}"; do
    echo "Training $run_name"
    # Train model
    python3 -m paddle.distributed.launch --gpus '2,3' /home/gusandmich@GU.GU.SE/PaddleOCR/tools/train.py -c configs/$run_name.yaml

    # Evaluate model on baseline test data
    # Note I have commented this out because
    # (1) It sometimes fails due to PaddleOCR issues I've not been able to figure out
    # (2) I haven't run it because performance was demonstrably poor during training anyway

    # echo "Evaluating $run_name"
    # python3 -m paddle.distributed.launch --gpus '2,3' /home/gusandmich@GU.GU.SE/PaddleOCR/tools/eval.py -c configs/$run_name.yaml
done
