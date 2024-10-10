from trdg.generators import GeneratorFromDict

# Experiment definitions

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
    fonts=["Scheherazade-Regular.ttf"],  # Chosen arbitrarily
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
        "Scheherazade-Regular.ttf",
        "MarkaziText-Bold.ttf",
        "Bahij Helvetica Neue-Roman.ttf",
        "Bahij Muna-Black.ttf",
        "Bahij TheSansArabic-Light.ttf",
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
