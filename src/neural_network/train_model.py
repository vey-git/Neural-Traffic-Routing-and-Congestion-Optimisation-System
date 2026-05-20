import matplotlib.pyplot as mpl
import numpy as np
import pandas as pd

from src.neural_network.neural_network import NeuralNetwork

from utils.config import (

    INPUT_SIZE,

    HIDDEN_LAYER_1,

    HIDDEN_LAYER_2,

    OUTPUT_SIZE,

    LEARNING_RATE,

    TRAINING_EPOCHS,

    TRAINING_DATA_PATH,

    MODEL_WEIGHTS_PATH,

    PLOTS_DIR

)


# ==========================================================
# RANDOM SEED
# ==========================================================

np.random.seed(42)


# ==========================================================
# LOAD DATASET
# ==========================================================

print("Loading training dataset...")

training_data = pd.read_csv(
    TRAINING_DATA_PATH
)

print("Dataset loaded successfully.")


# ==========================================================
# INPUT FEATURES
# ==========================================================

feature_columns = [

    "edge_usage",

    "road_length",

    "speed_limit",

    "nearby_congestion",

    "road_type"

]

# force numeric conversion

for column in feature_columns:

    training_data[column] = pd.to_numeric(

        training_data[column],

        errors="coerce"

    )

# remove invalid rows

training_data = training_data.dropna(

    subset=feature_columns + ["congestion_ratio"]

)

# convert to float arrays

X = training_data[
    feature_columns
].values.astype(float)

y = training_data[[
    "congestion_ratio"
]].values.astype(float)


# ==========================================================
# TARGET OUTPUT
# ==========================================================

y = training_data[['congestion_ratio']].values


print(f"Feature shape: {X.shape}")

print(f"Target shape: {y.shape}")


# ==========================================================
# TRAIN / TEST SPLIT
# ==========================================================

split_index = int(
    len(X) * 0.8
)

X_train = X[:split_index]
X_test = X[split_index:]

y_train = y[:split_index]
y_test = y[split_index:]


# ==========================================================
# FEATURE NORMALISATION
# ==========================================================

X_mean = X_train.mean(axis=0)

X_std = X_train.std(axis=0)

# prevent divide-by-zero

X_std[X_std == 0] = 1


# ==========================================================
# SAVE SCALER PARAMETERS
# ==========================================================

np.save(

    MODEL_WEIGHTS_PATH /

    "X_mean.npy",

    X_mean

)

np.save(

    MODEL_WEIGHTS_PATH /

    "X_std.npy",

    X_std

)

print("Feature scaler saved.")


# ==========================================================
# APPLY NORMALISATION
# ==========================================================

X_train = (

    X_train - X_mean

) / X_std

X_test = (

    X_test - X_mean

) / X_std

print("Feature normalisation complete.")


# ==========================================================
# CREATE NEURAL NETWORK
# ==========================================================

model = NeuralNetwork(

    INPUT_SIZE,

    HIDDEN_LAYER_1,

    HIDDEN_LAYER_2,

    OUTPUT_SIZE

)

print("Neural network initialised.")


# ==========================================================
# TRAIN MODEL
# ==========================================================

print("Training model...")

model.train(

    X_train,

    y_train,

    TRAINING_EPOCHS,

    LEARNING_RATE

)

print("Training complete.")


# ==========================================================
# SAVE MODEL WEIGHTS
# ==========================================================

model.save_model()

print("Model weights saved.")


# ==========================================================
# GENERATE PREDICTIONS
# ==========================================================

predictions = model.predict(
    X_test
)

predictions = np.array(
    predictions
).flatten()

y_test = np.array(
    y_test
).flatten()

print("Predictions generated.")


# ==========================================================
# EVALUATION METRICS
# ==========================================================

mse = np.mean(
    (y_test - predictions) ** 2
)

rmse = np.sqrt(mse)

mae = np.mean(
    np.abs(y_test - predictions)
)

# R² SCORE

ss_total = np.sum(
    (y_test - np.mean(y_test)) ** 2
)

ss_residual = np.sum(
    (y_test - predictions) ** 2
)

r2_score = (
    1 - (ss_residual / ss_total)
)

print("\n===== MODEL EVALUATION =====\n")

print(f"MSE: {mse:.6f}")

print(f"RMSE: {rmse:.6f}")

print(f"MAE: {mae:.6f}")

print(f"R² Score: {r2_score:.6f}")


# ==========================================================
# TRAINING LOSS GRAPH
# ==========================================================

mpl.figure(figsize=(8, 6))

mpl.plot(model.losses)

mpl.title("Training Loss")

mpl.xlabel("Epoch")

mpl.ylabel("Loss")

mpl.grid(True)

save_path = (

    PLOTS_DIR /

    "training_loss.png"

)

mpl.savefig(

    save_path,

    dpi=300,

    bbox_inches="tight"

)

mpl.close()

print("Training loss graph saved.")


# ==========================================================
# ACTUAL VS PREDICTED GRAPH
# ==========================================================

mpl.figure(figsize=(10, 7))

mpl.scatter(

    y_test,

    predictions,

    alpha=0.6,

    s=40

)

min_val = min(

    np.min(y_test),

    np.min(predictions)

)

max_val = max(

    np.max(y_test),

    np.max(predictions)

)

mpl.plot(

    [min_val, max_val],

    [min_val, max_val],

    linestyle="--",

    linewidth=2

)

mpl.xlabel(
    "Actual Values"
)

mpl.ylabel(
    "Predicted Values"
)

mpl.title(
    "Actual vs Predicted Congestion"
)

mpl.grid(True)

save_path = (

    PLOTS_DIR /

    "actual_vs_predicted.png"

)

mpl.savefig(

    save_path,

    dpi=300,

    bbox_inches="tight"

)

mpl.close()

print("Prediction comparison graph saved.")


# ==========================================================
# RESIDUAL ERROR GRAPH
# ==========================================================

residuals = (
    y_test - predictions
)

mpl.figure(figsize=(8, 6))

mpl.hist(

    residuals,

    bins=30

)

mpl.xlabel(
    "Residual Error"
)

mpl.ylabel(
    "Frequency"
)

mpl.title(
    "Residual Error Distribution"
)

mpl.grid(True)

save_path = (

    PLOTS_DIR /

    "residual_distribution.png"

)

mpl.savefig(

    save_path,

    dpi=300,

    bbox_inches="tight"

)

mpl.close()

print("Residual distribution graph saved.")


print("\nTraining pipeline complete.")