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


How to choose max length?
Maximum seen in all the data is 31, so go for 35 to be safe: 

cat KPTI-TrainData/_gt.txt | cut -f2 -d"," | cut -f2 -d"\"" | awk '{ print NF; }' | sort -nr | head -n1
31

cat KPTI-TestData/_gt.txt | cut -f2 -d"," | cut -f2 -d"\"" | awk '{ print NF; }' | sort -nr | head -n1
27

cat KPTI-ValidData/_gt.txt | cut -f2 -d"," | cut -f2 -d"\"" | awk '{ print NF; }' | sort -nr | head -n1
29

Trained baseline model to 500 epochs (/scratch/gusandmich/final_assignment/experiment_outputs/baseline_initial_train). 
    - Training accuracy very good! 
    - Evaluation accuracy garbage. 'Best' performance was around epoch 35, but cannot predict:
    Best accuracy on a gray-background image:
    ```
    2024/10/12 13:56:08] ppocr INFO: infer_img: /scratch/gusandmich/final_assignment/KPTI/KPTI-TestData/Abasn-0002-10.jpg                                 
    [2024/10/12 13:56:09] ppocr INFO:        result: "      0.9668120741844177
    ```
    Best accuracy on a brown-background image:
    ```
    [2024/10/12 13:56:39] ppocr INFO: infer_img: /scratch/gusandmich/final_assignment/KPTI/KPTI-TestData/GhorZa-0015-1194-7.jpg
    [2024/10/12 13:56:39] ppocr INFO:        result: "ک " 0.7113693356513977
    ```

Hypotheses:
- Grayscale vs RGB
    - Tried running trained model on grayscaled image, still doesn't predict anything
- Model not complicated enough
    - Train same model on KPTI train set and see if it performs ok 
    - Also does really poorly! 
- Try a more complex model
    - Documentation here on algorithms: https://github.com/PaddlePaddle/PaddleOCR/blob/de457325cd2bd7bca11219eb83763086a5b61e00/doc/doc_en/algorithm_overview_en.md 
    - Try training on ResNet 50
- Can't handle right-to-left
    - Try running the pre-trained Arabic model
    - Try running on English (TRDG issue?)
- Is the problem that the training data is individual words but the test data is sets of words in a line?
    - 

- Generate a second baseline (for comparison)
- Run comparison vs baseline 

- Realized: max_text_length is the maximum number of *characters*. Will simply discard samples with more length than that. 
    - https://github.com/PaddlePaddle/PaddleOCR/issues/4825
    - https://github.com/PaddlePaddle/PaddleOCR/discussions/8964 
    - Need to do word-level segmentation first to pull out images. 