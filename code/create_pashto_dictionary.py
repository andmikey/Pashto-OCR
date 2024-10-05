from pathlib import Path

import click
import pandas as pd
from nlpashto import Cleaner, Tokenizer

# Train dataset has 12005 sentences.
# Test dataset has 3002 sentences.
# Final dataset has 12039 words.


def words_from_df(df):
    # Setup
    word_set = set()
    cleaner = Cleaner()
    tokenizer = Tokenizer()

    # The column names are actually a data entry, so pull that and process it too
    first_entry = df.columns.values[1]
    cleaned = cleaner.clean(first_entry)
    tokenized = tokenizer.tokenize(cleaned)
    for sent in tokenized:
        for token in sent:
            word_set.add(token)

    # Overwrite column names and iterate through the rest of the data
    df.columns = ["English", "Pashto"]
    for idx, row in df.iterrows():
        contents = row["Pashto"]
        if contents:  # Skip rows with empty Pashto
            cleaned = cleaner.clean(contents)
            tokenized = tokenizer.tokenize(cleaned)
            for sent in tokenized:
                for token in sent:
                    word_set.add(token)

    return word_set


@click.command()
@click.option(
    "--output-file",
    type=click.Path(path_type=Path),
    default="/scratch/gusandmich/final_assignment/pashto_dict/dict.txt",
)
def create_dictionary(output_file):
    # Dataset pulled from here: https://huggingface.co/datasets/adnankhan769/english_to_pashto_sentences_dataset
    splits = {
        "train": "data/train-00000-of-00001.parquet",
        "test": "data/test-00000-of-00001.parquet",
    }
    train_df = pd.read_parquet(
        "hf://datasets/adnankhan769/english_to_pashto_sentences_dataset/"
        + splits["train"]
    )
    test_df = pd.read_parquet(
        "hf://datasets/adnankhan769/english_to_pashto_sentences_dataset/"
        + splits["test"]
    )

    print(f"Train dataset has {train_df.shape[0] + 1} sentences.")
    print(f"Test dataset has {test_df.shape[0] + 1} sentences.")

    train_set = words_from_df(train_df)
    test_set = words_from_df(test_df)

    word_set = train_set.union(test_set)

    print(f"Final dataset has {len(word_set)} words.")
    print(f"Writing final dataset to {output_file}")

    with open(output_file, "w+") as f:
        for word in word_set:
            f.write(f"{word}\n")


if __name__ == "__main__":
    create_dictionary()
