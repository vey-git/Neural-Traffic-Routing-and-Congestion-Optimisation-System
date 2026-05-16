import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from src.artificial_intelligence.neural_network import NeuralNetwork

# =========================================================
# LOAD DATA
# =========================================================

print("Loading dataset...")

data = pd.read_csv("training_data.csv")

# =========================================================
# INPUT FEATURES
# =========================================================

X = data[['edge_usage',
          'road_length',
          'speed_limit',
          'nearby_congestion',
          'road_type']].values

# OUTPUT TARGET

y = data[['multiplier']].values

print("Dataset loaded successfully")
print("X shape:", X.shape)
print("y shape:", y.shape)

# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

split_index = int(len(X) * 0.8)

X_train = X[:split_index]
X_test = X[split_index:]

y_train = y[:split_index]
y_test = y[split_index:]

# =========================================================
# NORMALISATION
# =========================================================

X_mean = X_train.mean(axis=0)
X_std = X_train.std(axis=0)

# prevent divide-by-zero

X_std[X_std == 0] = 1

X_train = (X_train - X_mean) / X_std
X_test = (X_test - X_mean) / X_std

print("Normalisation complete")

# =========================================================
# CREATE NETWORK
# =========================================================

model = NeuralNetwork(
    input_size=5,
    hidden1_size=16,
    hidden2_size=8,
    output_size=1
)

print("Neural network created")

# =========================================================
# TRAIN MODEL
# =========================================================

print("Starting training...")

model.train(
    X_train,
    y_train,
    epochs=1000,
    learning_rate=0.0001
)

print("Training complete")

# =========================================================
# SAVE MODEL
# =========================================================

model.save_model()

print("Model saved")

# =========================================================
# PREDICTIONS
# =========================================================

prediction = model.predict(X_test)

print("Predictions generated")

# =========================================================
# FLATTEN ARRAYS
# =========================================================

y_test = np.array(y_test).flatten()
prediction = np.array(prediction).flatten()

# =========================================================
# DEBUG OUTPUT
# =========================================================

print("\nActual values:")
print(y_test[:20])

print("\nPredicted values:")
print(prediction[:20])

print("\nNaN check:", np.isnan(prediction).any())
print("Inf check:", np.isinf(prediction).any())

# =========================================================
# METRICS
# =========================================================

mse = np.mean((y_test - prediction) ** 2)

rmse = np.sqrt(mse)

mae = np.mean(np.abs(y_test - prediction))

print(f"\nMSE = {mse}")
print(f"RMSE = {rmse}")
print(f"MAE = {mae}")

# =========================================================
# TRAINING LOSS GRAPH
# =========================================================

plt.figure(figsize=(8,6))

plt.plot(model.losses)

plt.title("Training Loss")
plt.xlabel("Epoch")
plt.ylabel("MSE Loss")

plt.grid(True)

plt.show()

# ==========================================
# ACTUAL VS PREDICTED GRAPH
# ==========================================

plt.figure(figsize=(10,7))

# scatter points

plt.scatter(
    y_test,
    prediction,
    alpha=0.6,
    s=40
)

# perfect prediction line

min_val = min(np.min(y_test), np.min(prediction))
max_val = max(np.max(y_test), np.max(prediction))

plt.plot(
    [min_val, max_val],
    [min_val, max_val],
    linestyle='--',
    linewidth=2
)

plt.xlabel("Actual Congestion Multiplier")
plt.ylabel("Predicted Congestion Multiplier")

plt.title("Actual vs Predicted Congestion Multipliers")

plt.grid(True)

plt.show()

import matplotlib.pyplot as plt
import numpy as np

# Calculate residuals
residuals = y_test - prediction

# Create histogram
plt.figure(figsize=(8,6))

plt.hist(
    residuals,
    bins=30
)

plt.xlabel("Residual Error")

plt.ylabel("Frequency")

plt.title("Residual Error Distribution")

plt.grid(True)

plt.savefig("residual_histogram.png")

plt.show()