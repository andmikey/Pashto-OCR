# Synthetic Data Generation for Pashto OCR

## Setup 
Create the Conda environment:

```sh
conda env create -f setup_files/environment.yaml --prefix /scratch/gusandmich/conda_envs/final_assignment_conda/
conda activate /scratch/gusandmich/conda_envs/final_assignment_conda/
```

Clone the test data:
```sh
cd /scratch/gusandmich/final_assignment/
git clone https://github.com/rahmad77/KPTI.git
```

Set up TRDG to generate Pashto text. 
Download the Pashto fonts:
```sh 
cd /scratch/gusandmich/final_assignment/
git clone https://github.com/zahidaz/pashto_fonts.git
```

Edit the TRDG repo to include the new fonts following the instructions [here](https://github.com/Belval/TextRecognitionDataGenerator?tab=readme-ov-file#add-new-fonts). The package is installed in `/scratch/gusandmich/conda_envs/final_assignment_conda/lib/python3.8/site-packages/trdg`. The two-letter code for Pashto is ps.

- Copy the fonts: `cp /scratch/gusandmich/final_assignment/pashto_fonts/all_fonts/*.ttf /scratch/gusandmich/conda_envs/final_assignment_conda/lib/python3.8/site-packages/trdg/fonts/ps`

- Generate the dictionary: `python3 code/create_pashto_dictionary.py --output-file /scratch/gusandmich/conda_envs/final_assignment_conda/lib/python3.8/site-packages/trdg/dicts/ps.txt`

- Copy the dictionary: 

## Experiment setup
Rough idea:
- 'Best' baseline: test TesseractOCR on the Pasho testing data. 
- 'Good' baseline: train MMOCR on the Pasho training data, test on the Pashto testing data. 
- 'Acceptable' baseline: train MMOCR on a selection of synthetic data, test on the Pashto testing data.

Expect (obviously) performance of (1) > (2) > (3), but question of how close we can get to (2) from (3) - does the recipe specified in the paper hold? 

Limitations:
- Training on fonts but testing on handwritten data 
- Train and test for 'good' baseline are from the same distribution - paper didn't do this but I couldn't find any languages which had two sets of available training data

Problems:
- Couldn't find a good dataset for OCR that was freely available... this Pashto one was the only one 
- Using different architecture (wanted to learn something that was closer to SOTA)
- Found a monolingual dataset for Pashto but costs $$: https://live.european-language-grid.eu/catalogue/corpus/2462 

Possible models:
- https://github.com/open-mmlab/mmocr/blob/main/configs/textrecog/sar/README.md 
- https://github.com/open-mmlab/mmocr/blob/main/configs/textrecog/satrn/README.md 

