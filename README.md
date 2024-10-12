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

And create the label files:
```sh
bash code/create_label_files.sh
```

Download the Pashto fonts:
```sh 
cd /scratch/gusandmich/final_assignment/
git clone https://github.com/zahidaz/pashto_fonts.git
```

Copy the fonts: 

```sh
cp /scratch/gusandmich/final_assignment/pashto_fonts/all_fonts/*.ttf \
    /scratch/gusandmich/conda_envs/final_assignment_conda/lib/python3.8/site-packages/trdg/fonts/ps
```

Generate the dictionary (for synthetic data generation) and character lookup (for labelling): 

```sh 
python3 code/create_pashto_dictionary.py \
    --input-path /scratch/gusandmich/final_assignment/KPTI/KPTI-TrainData \
    --output-file-dict /scratch/gusandmich/conda_envs/final_assignment_conda/lib/python3.8/site-packages/trdg/dicts/ps.txt \
    --output-file-chars /scratch/gusandmich/conda_envs/final_assignment_conda/lib/python3.8/site-packages/paddleocr/ppocr/utils/dict/ps_dict.txt
```

Edit the TRDG code on line 25 of the file `/scratch/gusandmich/conda_envs/final_assignment_conda/lib/python3.8/site-packages/trdg/utils.py` to include Pashto:

```py
    if lang in ("ar", "cn", "hi"):
    if lang in ("ar", "cn", "hi", "ps"):
```

Add to .bashrc:
```sh
export LD_LIBRARY_PATH=/scratch/gusandmich/conda_envs/final_assignment_conda/lib:$LD_LIBRARY_PATH
```

Set up the Tesseract directory:

```sh
mkdir /scratch/gusandmich/final_assignment/tesseract_model && cd $_
cp -r /usr/share/tesseract/tessdata/* . 
wget https://github.com/tesseract-ocr/tessdata_best/raw/refs/heads/main/pus.traineddata
```

You will now need to call Tesseract as:
```sh 
tesseract img_file.png - -l pus --tessdata-dir /scratch/gusandmich/final_assignment/tesseract_model/
```

## Experiment setup
Rough idea:
- 'Best' baseline: test TesseractOCR on the Pasho testing data. 
- 'Good' baseline: train MMOCR on the Pasho training data, test on the Pashto testing data. 
- 'Acceptable' baseline: train MMOCR on a selection of synthetic data, test on the Pashto testing data.

Expect (obviously) performance of (1) > (2) > (3), but question of how close we can get to (2) from (3) - does the recipe specified in the paper hold? 

Limitations:
- Training on fonts but testing on handwritten data 
- Train and test for 'good' baseline are from the same distribution - paper didn't do this but I couldn't find any languages which had two sets of available training data
- I think the annotation of symbols around letters isn't working properly

Problems:
- Couldn't find a good dataset for OCR that was freely available... this Pashto one was the only one 
- Using different architecture (wanted to learn something that was closer to SOTA)
- Found a monolingual dataset for Pashto but costs $$: https://live.european-language-grid.eu/catalogue/corpus/2462 so decided to just use the annotation text

Experiments:
- Baseline: all fonts, random skew, random distortion, random blur, 30k samples
- Go down to just one font 
- Go down to five fonts
- Remove skew
- Remove distortion 
- Remove blur
- Remove Gaussian noise background
- Using baseline, generate:
    - 30k 
    - 150k
    - 450k images

Training Paddle:
Instructions from Paddle: https://paddlepaddle.github.io/PaddleOCR/latest/en/ppocr/model_train/recognition.html#11-dataset-preparation
Better instructions: https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.3/doc/doc_en/recognition_en.md 
Example training data file: https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.1/configs/rec/multi_language/rec_french_lite_train.yml 


Todos:
- Decide on an architecture
- Train models for all those architectures <- aim to get this running by Saturday
- Test the performance of Tesseract + the trained models on the test data