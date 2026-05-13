import pandas as pd
import numpy as np
from shapely import predicates

from neural_network import NeuralNetwork

data = pd.read_csv("training_data.csv")


#input features
X = data[['edge_usage',
          'road_length',
          'speed_limit',
          'nearby_congestion',
          'road_type']].values

#output

y=data[['multiplier']].values

#normalisation
X = (X - X.mean(axis=0)) / X.std(axis=0)

#create network

model = NeuralNetwork(
    input_size=5,
    hidden1_size=16,
    hidden2_size=8,
    output_size=1
)

#train the model

model.train(X, y, epochs=5000, learning_rate=0.001)

#test prediction

sample = np.array([[
    10, #edge_usage
    100, #road_length
    50, #road_speed
    8, #nearby_congestion
    2 #road_type
]])

sample = (sample - X.mean(axis=0)) / X.std(axis=0)

prediction = model.predict(sample)
print("\nPredicted Congestion Multiplier: ")
print(prediction)