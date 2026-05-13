from logging import root
from math import sqrt

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.ma.extras import average

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

#MSE
actual_value = np.array([[1.5]])
sampleVsPrediction = (actual_value -prediction)**2  #get the squared differences between the exact, and predicted output
MSE = np.mean(sampleVsPrediction)

#RMSE
RMSE = sqrt(MSE)

#MAE
sum = 0

for i in range (len(actual_value)):
    sum += abs(actual_value[i]-prediction[i])

MAE = sum / len(actual_value)


print(f"\nMSE= {MSE}")
print(f"\nRMSE= {RMSE}")
print(f"\nMAE= {MAE}")

#plot losses compared to model

plt.plot(model.losses)
plt.title("Training Loss")
plt.xlabel("Epoch")
plt.ylabel("MSE Loss")
plt.grid(True)
plt.show()