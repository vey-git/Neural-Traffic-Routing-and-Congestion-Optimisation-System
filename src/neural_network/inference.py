import numpy as np

from neural_network.neural_network import (
    NeuralNetwork
)

from utils.config import (

    MODEL_WEIGHTS_PATH,

    HIDDEN_LAYER_1,

    HIDDEN_LAYER_2,

    OUTPUT_SIZE,

    INPUT_SIZE
)


# ==========================================================
# INITIALISE MODEL
# ==========================================================

model = NeuralNetwork(

    INPUT_SIZE,

    HIDDEN_LAYER_1,

    HIDDEN_LAYER_2,

    OUTPUT_SIZE
)


# ==========================================================
# LOAD MODEL SAFELY
# ==========================================================

MODEL_LOADED = False

try:

    # --------------------------------------------------
    # LOAD TARGET NORMALISATION
    # --------------------------------------------------

    y_min = np.load(
        "models/y_min.npy"
    )

    y_max = np.load(
        "models/y_max.npy"
    )

    # --------------------------------------------------
    # LOAD MODEL
    # --------------------------------------------------

    model.load_model()

    # --------------------------------------------------
    # LOAD FEATURE NORMALISATION
    # --------------------------------------------------

    X_mean = np.load(
        MODEL_WEIGHTS_PATH / "X_mean.npy"
    )

    X_std = np.load(
        MODEL_WEIGHTS_PATH / "X_std.npy"
    )

    MODEL_LOADED = True

    print(
        "Neural network model loaded."
    )

except Exception as error:

    print(
        f"Model not loaded yet: {error}"
    )

    X_mean = np.zeros(5)

    X_std = np.ones(5)

    y_min = 0.0

    y_max = 1.0


# ==========================================================
# PREDICTION FUNCTION
# ==========================================================

def predict_congestion(features):
    """
    Predict congestion multiplier.
    """

    if not MODEL_LOADED:

        return 1.0

    # --------------------------------------------------
    # CONVERT TO NUMPY
    # --------------------------------------------------

    X = np.array(
        features,
        dtype=np.float64
    )

    # --------------------------------------------------
    # FEATURE NORMALISATION
    # --------------------------------------------------

    X = (

        X - X_mean

    ) / (

        X_std + 1e-8
    )

    # --------------------------------------------------
    # FORWARD PROPAGATION
    # --------------------------------------------------

    prediction = model.forward(X)

    # --------------------------------------------------
    # INVERSE TARGET SCALING
    # --------------------------------------------------

    prediction = (

        prediction *

        (y_max - y_min)

    ) + y_min

    # --------------------------------------------------
    # SAFETY CLAMP
    # --------------------------------------------------

    prediction = np.clip(

        prediction,

        1.0,

        5.0
    )

    return float(
        prediction[0][0]
    )