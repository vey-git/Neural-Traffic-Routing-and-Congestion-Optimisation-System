import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden1_size, hidden2_size, output_size):
        #initialise the weights of the neurons
        self.W1 = np.random.randn(input_size, hidden1_size) * 0.01
        self.b1 = np.zeros((1, hidden1_size))

        self.W2 = np.random.randn(hidden1_size, hidden2_size) * 0.01
        self.b2 = np.zeros((1, hidden2_size))

        self.W3 = np.random.randn(hidden2_size, output_size) * 0.01
        self.b3 = np.zeros((1, output_size))

        #relu activation

        def relu(self, x):
            return np.maximum(0, x)

        #relu derivative

        def relu_derivative(self,x):
            return (x > 0).astype(float)

        #forward propagation

        def forward(self,X):
            self.z1 = np.dot(X,self.W1) + self.b1
            self.a1 = self.relu(self.z1)

            self.z2 = np.dot(X, self.W2) + self.b2
            self.a2 = self.relu(self.z2)

            self.z3 = np.dot(X, self.W3) + self.b3

            #output for linear regression
            self.output = self.z3
            return self.output

        #loss function

        def compute_loss(self, y_true, y_pred):
            return np.mean((y_true - y_pred) ** 2)

        #backpropagation

        def backward(self, X, y, learning_rate):
            m = X.shape[0]

            #output the layer gradient
            d_output = (2 / m) * (self.output - y)

            #gradients for W3 and b3
            dW3 = np.dot(self.a2.T, d_output)
            db3 = np.sum(d_output, axis=0, keepdims=True)

            #hidden layer 2
            dA2 = np.dot(d_output, self.W3.T)
            dZ2 = dA2 * self.relu_derivative(self.z2)

            dW2 = np.dot(self.a1.T, dZ2)
            db2 = np.sum(dZ2, axis=0, keepdims=True)

            #hidden layer 1
            dA1 = np.dot(dZ2, self.W2.T)
            dZ1 = dA1 * self.relu_derivative(self.z1)

            dW1 = np.dot(X.T, dZ1)
            db1 = np.sum(dZ1, axis=0, keepdims=True)

            #gradient descent

            self.W3 -= learning_rate * dW3
            self.b3 -= learning_rate * db3

            self.W2 -= learning_rate * dW2
            self.b2 -= learning_rate * db2

            self.W1 -= learning_rate * dW1
            self.b1 -= learning_rate * db1

            #Training loop
            def train(self, X, y, epochs, learning_rate):
                for epoch in range(epochs):
                    predictions = self.forward(X)
                    loss = self.compute_loss(y, predictions)
                    self.backward(X,y,learning_rate)

                    if epoch % 100 == 0:
                        print(f"Epoch {epoch} | Loss: {loss}")

            #prediction

            def predict(self, X):
                return self.forward(X)
