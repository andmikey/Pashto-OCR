from pathlib import Path

import click


@click.command()
@click.option("--dir-path", type=click.Path(path_type=Path, exists=True))
@click.option("--output-file", type=click.Path(path_type=Path))
def create_label_file(dir_path, output_file):
    img_files = dir_path.glob("*.jpg")

    lines_to_write = []

    for i in img_files:
        fname = i.name
        label = i.with_suffix(".txt")
        contents = label.read_text()
        lines_to_write.append(f'{fname}, "{contents}"\n')

    with open(output_file, "w+") as f:
        for line in lines_to_write:
            f.write(line)


if __name__ == "__main__":
    create_label_file()
