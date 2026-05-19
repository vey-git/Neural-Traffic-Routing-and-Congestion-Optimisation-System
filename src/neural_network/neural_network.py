import numpy as np

from utils.config import MODEL_WEIGHTS_PATH


class NeuralNetwork:
    """
    Feed-forward neural network for congestion prediction.

    Architecture:
        Input -> Hidden Layer 1 -> Hidden Layer 2 -> Output

    Hidden layers use ReLU activation.
    Output layer uses linear activation for regression.
    """

    def __init__(
        self,
        input_size,
        hidden1_size,
        hidden2_size,
        output_size
    ):

        # --------------------------------------------------
        # Weight Initialisation
        # --------------------------------------------------

        self.W1 = (
            np.random.randn(
                input_size,
                hidden1_size
            ) * 0.01
        )

        self.b1 = np.zeros(
            (1, hidden1_size)
        )

        self.W2 = (
            np.random.randn(
                hidden1_size,
                hidden2_size
            ) * 0.01
        )

        self.b2 = np.zeros(
            (1, hidden2_size)
        )

        self.W3 = (
            np.random.randn(
                hidden2_size,
                output_size
            ) * 0.01
        )

        self.b3 = np.zeros(
            (1, output_size)
        )

    # ======================================================
    # ACTIVATION FUNCTIONS
    # ======================================================

    def relu(self, x):
        """
        ReLU activation function.
        """

        return np.maximum(0, x)

    def relu_derivative(self, x):
        """
        Derivative of ReLU activation.
        """

        return (x > 0).astype(float)

    # ======================================================
    # FORWARD PROPAGATION
    # ======================================================

    def forward(self, X):
        """
        Forward propagation through the network.
        """

        # Hidden Layer 1

        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.relu(self.z1)

        # Hidden Layer 2

        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.relu(self.z2)

        # Output Layer

        self.z3 = np.dot(self.a2, self.W3) + self.b3

        # Linear output for regression

        self.output = self.z3

        return self.output

    # ======================================================
    # LOSS FUNCTION
    # ======================================================

    def compute_loss(
        self,
        y_true,
        y_pred
    ):
        """
        Mean Squared Error loss.
        """

        return np.mean(
            (y_true - y_pred) ** 2
        )

    # ======================================================
    # BACKPROPAGATION
    # ======================================================

    def backward(
        self,
        X,
        y,
        learning_rate
    ):
        """
        Backpropagation and gradient descent.
        """

        m = X.shape[0]

        # --------------------------------------------------
        # Output Layer Gradients
        # --------------------------------------------------

        d_output = (
            2 / m
        ) * (
            self.output - y
        )

        dW3 = np.dot(
            self.a2.T,
            d_output
        )

        db3 = np.sum(
            d_output,
            axis=0,
            keepdims=True
        )

        # --------------------------------------------------
        # Hidden Layer 2
        # --------------------------------------------------

        dA2 = np.dot(
            d_output,
            self.W3.T
        )

        dZ2 = (
            dA2 *
            self.relu_derivative(self.z2)
        )

        dW2 = np.dot(
            self.a1.T,
            dZ2
        )

        db2 = np.sum(
            dZ2,
            axis=0,
            keepdims=True
        )

        # --------------------------------------------------
        # Hidden Layer 1
        # --------------------------------------------------

        dA1 = np.dot(
            dZ2,
            self.W2.T
        )

        dZ1 = (
            dA1 *
            self.relu_derivative(self.z1)
        )

        dW1 = np.dot(
            X.T,
            dZ1
        )

        db1 = np.sum(
            dZ1,
            axis=0,
            keepdims=True
        )

        # --------------------------------------------------
        # Gradient Descent Updates
        # --------------------------------------------------

        self.W3 -= learning_rate * dW3
        self.b3 -= learning_rate * db3

        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2

        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1

    # ======================================================
    # TRAINING LOOP
    # ======================================================

    def train(
        self,
        X,
        y,
        epochs,
        learning_rate
    ):
        """
        Train the neural network.
        """

        self.losses = []

        for epoch in range(epochs):

            predictions = self.forward(X)

            loss = self.compute_loss(
                y,
                predictions
            )

            self.losses.append(loss)

            self.backward(
                X,
                y,
                learning_rate
            )

            if epoch % 100 == 0:

                print(
                    f"Epoch {epoch} | "
                    f"Loss: {loss:.6f}"
                )

    # ======================================================
    # MODEL SAVING
    # ======================================================

    def save_model(self):
        """
        Save trained model weights.
        """

        MODEL_WEIGHTS_PATH.mkdir(
            parents=True,
            exist_ok=True
        )

        np.save(
            MODEL_WEIGHTS_PATH / "W1.npy",
            self.W1
        )

        np.save(
            MODEL_WEIGHTS_PATH / "b1.npy",
            self.b1
        )

        np.save(
            MODEL_WEIGHTS_PATH / "W2.npy",
            self.W2
        )

        np.save(
            MODEL_WEIGHTS_PATH / "b2.npy",
            self.b2
        )

        np.save(
            MODEL_WEIGHTS_PATH / "W3.npy",
            self.W3
        )

        np.save(
            MODEL_WEIGHTS_PATH / "b3.npy",
            self.b3
        )

        print("Model saved successfully.")

    # ======================================================
    # MODEL LOADING
    # ======================================================

    def load_model(self):
        """
        Load trained model weights.
        """

        self.W1 = np.load(
            MODEL_WEIGHTS_PATH / "W1.npy"
        )

        self.b1 = np.load(
            MODEL_WEIGHTS_PATH / "b1.npy"
        )

        self.W2 = np.load(
            MODEL_WEIGHTS_PATH / "W2.npy"
        )

        self.b2 = np.load(
            MODEL_WEIGHTS_PATH / "b2.npy"
        )

        self.W3 = np.load(
            MODEL_WEIGHTS_PATH / "W3.npy"
        )

        self.b3 = np.load(
            MODEL_WEIGHTS_PATH / "b3.npy"
        )

        print("Model loaded successfully.")

    # ======================================================
    # PREDICTION
    # ======================================================

    def predict(self, X):
        """
        Generate predictions.
        """

        return self.forward(X)