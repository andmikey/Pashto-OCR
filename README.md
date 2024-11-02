# Synthetic Data Generation for Pashto OCR

This repository details my final project for LT2926 at the University of Gothenburg (Machine learning for statistical NLP: advanced). I investigate the feasibility of synthetic data generation for the OCR of Pashto, a low-resource language. 

Key points for navigating this repository:
- [Final report](./report/LT2926_report.pdf)
- [Experiment definitions and run scripts](./experiments/)
- [Setup instructions](./setup_instructions.md) (how to pull the data, add support for Pashto to TRDG and PaddleOCR)

To run the experiments, you can use [this script](./experiments/run_kpti_baseline.sh) to train models on the KPTI data; and [this script](./experiments/run_all_synthetic_experiments.sh) to train models on the synthetic data. 

Some things to note:
- Make sure you activate the conda environment: `conda activate /scratch/gusandmich/conda_envs/final_assignment_conda/`. 
- The code does run on mltgpu (outputs are at `/scratch/gusandmich/final_assignment/experiment_outputs`) but the environment it runs in is quite brittle, firstly because I made changes to the packages within the conda env (bad practice!) to get them to work with Pashto, and secondly because the packages I'm using don't play very nice with each other; there's some issues with conflicting dependencies (mostly around Pillow) that I've solved by brute force and it seems to sometimes break anyway.
- The synthetic data experiment configs all point to using the baseline test data as the testing data because I wanted to try some experiments training-and-testing on the baseline data, but in the end I didn't get a chance to do so.