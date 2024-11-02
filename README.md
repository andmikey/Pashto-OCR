# Synthetic Data Generation for Pashto OCR

This repository details my final project for LT2926 at the University of Gothenburg (Machine learning for statistical NLP: advanced). I investigate the feasibility of synthetic data generation for the OCR of Pashto, a low-resource language. 

To navigate this repository:
- [Final report](./report/report.pdf)
- [Experiment definitions and run scripts](./experiments/)
- [Setup instructions](./setup_instructions.md) (how to pull the data, add support for Pashto to TRDG and PaddleOCR)

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
