from multiprocessing import Pool
from pathlib import Path

from trdg.generators import GeneratorFromDict

# Experiment definitions

FONT_PREFIX = Path(
    "/scratch/gusandmich/conda_envs/final_assignment_conda/lib/python3.8/site-packages/trdg/fonts/ps/"
)

baseline_experiment = GeneratorFromDict(
    language="ps",
    count=30_000,  # Generate 30k training samples
    skewing_angle=10,  # Skew to a 10-degree angle
    random_skew=True,  # Randomize skew
    random_blur=True,  # Randomize blur
    distorsion_type=3,  # Random
    background_type=0,  # Gaussian noise
    size=64,  # 64 pixel height
)

baseline_150k_samples = GeneratorFromDict(
    language="ps",
    count=150_000,  # Generate 150k training samples
    skewing_angle=10,
    random_skew=True,
    random_blur=True,
    distorsion_type=3,
    background_type=0,
    size=64,
)

baseline_450k_samples = GeneratorFromDict(
    language="ps",
    count=450_000,  # Generate 450k training samples
    skewing_angle=10,
    random_skew=True,
    random_blur=True,
    distorsion_type=3,
    background_type=0,
    size=64,
)

just_one_font = GeneratorFromDict(
    language="ps",
    count=30_000,
    skewing_angle=10,
    random_skew=True,
    random_blur=True,
    distorsion_type=3,
    background_type=0,
    size=64,
    fonts=[str(FONT_PREFIX / "Scheherazade-Regular.ttf")],  # Chosen arbitrarily
)

just_five_fonts = GeneratorFromDict(
    language="ps",
    count=30_000,
    skewing_angle=10,
    random_skew=True,
    random_blur=True,
    distorsion_type=3,
    background_type=0,
    size=64,
    fonts=[
        # Chosen arbitrarily to get a mix of styles
        str(FONT_PREFIX / "Scheherazade-Regular.ttf"),
        str(FONT_PREFIX / "MarkaziText-Bold.ttf"),
        str(FONT_PREFIX / "Bahij Helvetica Neue-Roman.ttf"),
        str(FONT_PREFIX / "Bahij Muna-Black.ttf"),
        str(FONT_PREFIX / "Bahij TheSansArabic-Light.ttf"),
    ],
)

remove_skew = GeneratorFromDict(
    language="ps",
    count=30_000,
    skewing_angle=10,
    random_skew=False,  # No skew
    random_blur=True,
    distorsion_type=3,
    background_type=0,
    size=64,
)

remove_distorsion = GeneratorFromDict(
    language="ps",
    count=30_000,
    skewing_angle=10,
    random_skew=True,
    random_blur=True,
    distorsion_type=0,  # No distorsion
    background_type=0,
    size=64,
)

remove_blur = GeneratorFromDict(
    language="ps",
    count=30_000,
    skewing_angle=10,
    random_skew=True,
    random_blur=False,  # No blur
    distorsion_type=3,
    background_type=0,
    size=64,
)

plain_white_background = GeneratorFromDict(
    language="ps",
    count=30_000,
    skewing_angle=10,
    random_skew=True,
    random_blur=True,
    distorsion_type=3,
    background_type=1,  # Plain white background
    size=64,
)


EXPERIMENTS = {
    # "baseline": baseline_experiment,
    # "baseline_150k": baseline_150k_samples,
    # "baseline_450k": baseline_450k_samples,
    "just_one_font": just_one_font,
    "just_five_fonts": just_five_fonts,
    # "remove_skew": remove_skew,
    # "remove_distorsion": remove_distorsion,
    # "remove_blur": remove_blur,
    # "plain_white_background": plain_white_background,
}

# 30k images = 300MB approx
# So 2.1GB for the 30k images
# And 1.5GB for 150k, 5GB for 450k
# So just under 10GB in total
# Better to put on the SSD...
# DATA_PATH = Path("/srv/data/gusandmich/synthetic_data")
DATA_PATH = Path("/scratch/gusandmich/final_assignment/synthetic_data")


def generate(exp):
    print(f"Starting {exp}")
    write_path = DATA_PATH / exp
    write_path.mkdir(exist_ok=True)

    generator = EXPERIMENTS[exp]

    labels = []

    i = 0
    for img, lbl in generator:
        img_name = f"{i}.png"
        labels.append(f'{img_name}, "{lbl}"\n')
        img.save(write_path / img_name)
        i += 1

    with open(write_path / "_gt.txt", "w+") as f:
        for line in labels:
            f.write(line)

    return exp


if __name__ == "__main__":

    for e in EXPERIMENTS:
        generate(e)

    # thread_count = 2  # Number of experiments
    # p = Pool(thread_count)

    # for result in p.imap(generate, EXPERIMENTS):
    #     print(f"Finished processing: {result}", flush=True)
