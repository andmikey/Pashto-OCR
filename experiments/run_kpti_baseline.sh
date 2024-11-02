#!/bin/bash
set -eo pipefail

# Train the MobileNet v3 model on KPTI
python3 -m paddle.distributed.launch --gpus '1,2,3' /home/gusandmich@GU.GU.SE/PaddleOCR/tools/train.py -c configs/train_on_kpti.yaml

# Train the ResNet model on KPTI
python3 -m paddle.distributed.launch --gpus '2,3' /home/gusandmich@GU.GU.SE/PaddleOCR/tools/train.py -c configs/train_on_kpti_more_complex.yaml
