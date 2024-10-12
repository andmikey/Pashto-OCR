from pathlib import Path

import click
import pandas as pd
from nlpashto import Cleaner, Tokenizer


def words_and_chars_from_content(contents):
    # Setup
    word_set = set()
    char_set = set()
    cleaner = Cleaner()
    tokenizer = Tokenizer()

    # Clean, tokenize, and get the words and chars
    cleaned = cleaner.clean(contents)
    tokenized = tokenizer.tokenize(cleaned)
    for sent in tokenized:
        for token in sent:
            word_set.add(token)
            for char in token:
                char_set.add(char)

    return word_set, char_set


@click.command()
@click.option(
    "--input-path",
    type=click.Path(path_type=Path, exists=True),
    default="/scratch/gusandmich/final_assignment/KPTI/KPTI-TrainData",
)
@click.option(
    "--output-file-dict",
    type=click.Path(path_type=Path),
    default="/scratch/gusandmich/final_assignment/pashto_dict/dict.txt",
)
@click.option(
    "--output-file-chars",
    type=click.Path(path_type=Path),
    default="/scratch/gusandmich/final_assignment/pashto_dict/char_dict.txt",
)
def create_dictionary(input_path, output_file_dict, output_file_chars):
    # Use the KPTI train dataset
    label_files = input_path.glob("*.txt")

    word_sets = []
    char_sets = []

    for l in label_files:
        contents = l.read_text()
        (words, chars) = words_and_chars_from_content(contents)
        word_sets.append(words)
        char_sets.append(chars)

    word_set = set().union(*word_sets)
    char_set = set().union(*char_sets)

    print(f"Final dataset has {len(word_set)} words and {len(char_set)} characters")

    with open(output_file_dict, "w+") as f:
        for word in word_set:
            f.write(f"{word}\n")

    with open(output_file_chars, "w+") as f:
        for char in char_set:
            f.write(f"{char}\n")


if __name__ == "__main__":
    create_dictionary()
