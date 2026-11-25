# LAB 3: Basic Artificial Neural Network (ANN) from Scratch

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.decomposition import PCA

sns.set(style="whitegrid")

print("Lab 3 - Artificial Neural Network from Scratch")

iris = load_iris()
X = iris.data
y = iris.target.reshape(-1, 1)

try:
    encoder = OneHotEncoder(sparse_output=False)
except:
    encoder = OneHotEncoder(sparse=False)

y = encoder.fit_transform(y)

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def sigmoid_derivative(a):
    return a * (1 - a)

def softmax(z):
    exp = np.exp(z - np.max(z))
    return exp / np.sum(exp, axis=1, keepdims=True)

input_dim = X_train.shape[1]
hidden_dim = 8
output_dim = y_train.shape[1]
learning_rate = 0.1
epochs = 500

np.random.seed(42)
W1 = np.random.randn(input_dim, hidden_dim)
b1 = np.zeros((1, hidden_dim))
W2 = np.random.randn(hidden_dim, output_dim)
b2 = np.zeros((1, output_dim))

losses = []
accuracies = []

for epoch in range(epochs):
    Z1 = np.dot(X_train, W1) + b1
    A1 = sigmoid(Z1)
    Z2 = np.dot(A1, W2) + b2
    A2 = softmax(Z2)

    loss = -np.mean(np.sum(y_train * np.log(A2 + 1e-8), axis=1))
    losses.append(loss)

    y_pred_train = np.argmax(A2, axis=1)
    y_true_train = np.argmax(y_train, axis=1)
    accuracy = np.mean(y_pred_train == y_true_train)
    accuracies.append(accuracy)

    dZ2 = A2 - y_train
    dW2 = np.dot(A1.T, dZ2) / X_train.shape[0]
    db2 = np.sum(dZ2, axis=0, keepdims=True) / X_train.shape[0]

    dA1 = np.dot(dZ2, W2.T)
    dZ1 = dA1 * sigmoid_derivative(A1)
    dW1 = np.dot(X_train.T, dZ1) / X_train.shape[0]
    db1 = np.sum(dZ1, axis=0, keepdims=True) / X_train.shape[0]

    W1 -= learning_rate * dW1
    b1 -= learning_rate * db1
    W2 -= learning_rate * dW2
    b2 -= learning_rate * db2

    if (epoch + 1) % 100 == 0:
        print(f"Epoch {epoch+1}/{epochs} | Loss: {loss:.4f} | Accuracy: {accuracy*100:.2f}%")

Z1_test = np.dot(X_test, W1) + b1
A1_test = sigmoid(Z1_test)
Z2_test = np.dot(A1_test, W2) + b2
A2_test = softmax(Z2_test)

y_pred = np.argmax(A2_test, axis=1)
y_true = np.argmax(y_test, axis=1)

test_accuracy = np.mean(y_pred == y_true)
print(f"\nFinal Test Accuracy: {test_accuracy*100:.2f}%")

plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(losses, color='red', linewidth=2)
plt.title("Loss Curve", fontsize=14)
plt.xlabel("Epochs")
plt.ylabel("Loss")

plt.subplot(1,2,2)
plt.plot(accuracies, color='green', linewidth=2)
plt.title("Training Accuracy Curve", fontsize=14)
plt.xlabel("Epochs")
plt.ylabel("Accuracy")

plt.tight_layout()
plt.show()

cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, cmap="Blues", fmt="d",
            xticklabels=iris.target_names,
            yticklabels=iris.target_names)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

print("\nClassification Report:\n")
print(classification_report(y_true, y_pred, target_names=iris.target_names))

pca = PCA(n_components=3)
pca_data = pca.fit_transform(X_test)

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')

scatter = ax.scatter(pca_data[:,0], pca_data[:,1], pca_data[:,2],
                     c=y_pred, cmap="viridis", s=60)

ax.set_title("3D Visualization of ANN Predictions", fontsize=14)
ax.set_xlabel("PCA 1")
ax.set_ylabel("PCA 2")
ax.set_zlabel("PCA 3")

legend1 = ax.legend(*scatter.legend_elements(), title="Predicted Classes")
ax.add_artist(legend1)
plt.show()

# Algorithm
# Memorize these eight steps:
# 1. Import the required libraries and load the Iris dataset.
# 2. One-hot encode the target labels and standardize the input features.
# 3. Split the dataset into 80% training and 20% testing.
# 4. Define sigmoid, sigmoid derivative and softmax functions.
# 5. Initialize weights and biases for the 4-8-3 neural network.
# 6. Train the network using forward propagation, cross-entropy loss, backpropagation and gradient descent for 500 epochs.
# 7. Evaluate the network using test accuracy, confusion matrix and classification report.
# 8. Plot loss, accuracy and 3D PCA visualization.
