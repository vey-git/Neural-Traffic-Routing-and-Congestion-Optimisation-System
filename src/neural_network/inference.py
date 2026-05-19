import numpy as np

from neural_network.neural_network import (
    NeuralNetwork
)

from utils.config import (

    INPUT_SIZE,

    HIDDEN_LAYER_1,

    HIDDEN_LAYER_2,

    OUTPUT_SIZE

)


model = NeuralNetwork(

    INPUT_SIZE,

    HIDDEN_LAYER_1,

    HIDDEN_LAYER_2,

    OUTPUT_SIZE

)

model.load_model()


def predict_congestion(features):
    """
    Predict congestion multiplier.
    """

    sample = np.array(features)

    prediction = model.predict(sample)

    return float(prediction[0][0])