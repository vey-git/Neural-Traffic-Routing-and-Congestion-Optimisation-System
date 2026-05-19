from pathlib import Path


# ======================================================
# PROJECT ROOT
# ======================================================

BASE_DIR = (

    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent

)


# ======================================================
# ROAD NETWORK SETTINGS
# ======================================================

PLACE_NAME = "Oxford, England"

NETWORK_TYPE = "drive"


# ======================================================
# SIMULATION SETTINGS
# ======================================================

DEFAULT_ROUTING_ALGORITHM = "dijkstra"

DEFAULT_VEHICLE_COUNTS = [

    10,
    25,
    50,
    100,
    250,
    500,
    1000

]


# ======================================================
# CONGESTION SETTINGS
# ======================================================

LOW_CONGESTION_THRESHOLD = 0.5

MODERATE_CONGESTION_THRESHOLD = 1.0

HIGH_CONGESTION_THRESHOLD = 1.5

LOW_CONGESTION_MULTIPLIER = 1.0

MODERATE_CONGESTION_MULTIPLIER = 1.1

HIGH_CONGESTION_MULTIPLIER = 1.4

SEVERE_CONGESTION_MULTIPLIER = 2.5

DEFAULT_SPEED_LIMIT = 30

DEFAULT_ROAD_TYPE = "residential"


ROAD_TYPE_MAPPING = {

    "motorway": 0,

    "trunk": 1,

    "primary": 2,

    "secondary": 3,

    "tertiary": 4,

    "residential": 5

}


# ======================================================
# NEURAL NETWORK SETTINGS
# ======================================================

INPUT_SIZE = 5

HIDDEN_LAYER_1 = 16

HIDDEN_LAYER_2 = 8

OUTPUT_SIZE = 1

LEARNING_RATE = 0.0001

TRAINING_EPOCHS = 1000


# ======================================================
# VISUALISATION SETTINGS
# ======================================================

FIGURE_DPI = 300

HEATMAP_BACKGROUND = "black"

LOW_CONGESTION_COLOUR = "lime"

MODERATE_CONGESTION_COLOUR = "yellow"

HIGH_CONGESTION_COLOUR = "orange"

SEVERE_CONGESTION_COLOUR = "red"


# ======================================================
# DIRECTORIES
# ======================================================

RESULTS_DIR = (
    BASE_DIR / "results"
)

DATA_DIR = (
    RESULTS_DIR / "data"
)

TRAINING_DATA_DIR = (
    DATA_DIR / "training"
)

PROCESSED_DATA_DIR = (
    DATA_DIR / "processed"
)

PLOTS_DIR = (
    RESULTS_DIR / "plots"
)

MODELS_DIR = (
    BASE_DIR / "models"
)

MODEL_WEIGHTS_PATH = (
    MODELS_DIR / "weights"
)


# ======================================================
# FILE PATHS
# ======================================================

TRAINING_DATA_PATH = (

    TRAINING_DATA_DIR /

    "training_data.csv"

)

RESULTS_CSV_PATH = (

    PROCESSED_DATA_DIR /

    "results_nn.csv"

)


# ======================================================
# CREATE DIRECTORIES
# ======================================================

for directory in [

    RESULTS_DIR,

    DATA_DIR,

    TRAINING_DATA_DIR,

    PROCESSED_DATA_DIR,

    PLOTS_DIR,

    MODELS_DIR,

    MODEL_WEIGHTS_PATH

]:

    directory.mkdir(

        parents=True,

        exist_ok=True

    )