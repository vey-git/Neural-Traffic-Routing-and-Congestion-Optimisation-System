import numpy as np

from src.artificial_intelligence.neural_network import NeuralNetwork


# =========================
# LOAD TRAINED MODEL
# =========================

model = NeuralNetwork(

    input_size=5,
    hidden1_size=16,
    hidden2_size=8,
    output_size=1

)

model.load_model()


# =========================
# PREDICT CONGESTION
# =========================

def predictCongestion(features):

    sample = np.array([features])

    prediction = model.predict(sample)

    return float(prediction[0][0])