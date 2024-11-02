# Setup instructions

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

And convert the test data label files into the format expected by PaddleOCR:
```sh
bash code/create_label_files.sh
```

Download the Pashto fonts:
```sh 
cd /scratch/gusandmich/final_assignment/
git clone https://github.com/zahidaz/pashto_fonts.git
```

Copy the fonts to the TRDG directory: 

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

Add to .bashrc to ensure you can run PaddleOCR:
```sh
export LD_LIBRARY_PATH=/scratch/gusandmich/conda_envs/final_assignment_conda/lib:$LD_LIBRARY_PATH
```
