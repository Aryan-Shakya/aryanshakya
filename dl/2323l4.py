# LAB 4: Activation Functions - Sigmoid, ReLU and Tanh

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

print("Lab 4 - Activation Functions: Sigmoid, ReLU and Tanh")

x = np.linspace(-10, 10, 400)
print("Input range:", x.min(), "to", x.max(), "| Number of points:", len(x))

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)

def tanh(x):
    return np.tanh(x)

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)

def relu_derivative(x):
    return (x > 0).astype(float)

def tanh_derivative(x):
    return 1 - np.tanh(x) ** 2

plt.figure(figsize=(8,5))
plt.plot(x, sigmoid(x), label="Sigmoid", linewidth=2)
plt.plot(x, relu(x), label="ReLU", linewidth=2)
plt.plot(x, tanh(x), label="Tanh", linewidth=2)
plt.xlabel("Input")
plt.ylabel("Output")
plt.title("Comparison of Activation Functions", fontsize=14)
plt.ylim(-2, 10)
plt.legend()
plt.grid(True)
plt.show()

fig, axes = plt.subplots(1, 3, figsize=(15,4))

axes[0].plot(x, sigmoid(x), color="blue", linewidth=2)
axes[0].set_title("Sigmoid  (range 0 to 1)")

axes[1].plot(x, relu(x), color="orange", linewidth=2)
axes[1].set_title("ReLU  (range 0 to +inf)")

axes[2].plot(x, tanh(x), color="green", linewidth=2)
axes[2].set_title("Tanh  (range -1 to 1)")

for ax in axes:
    ax.set_xlabel("Input")
    ax.set_ylabel("Output")
    ax.grid(True)

plt.tight_layout()
plt.show()

plt.figure(figsize=(8,5))
plt.plot(x, sigmoid_derivative(x), label="Sigmoid'", linewidth=2)
plt.plot(x, relu_derivative(x), label="ReLU'", linewidth=2)
plt.plot(x, tanh_derivative(x), label="Tanh'", linewidth=2)
plt.xlabel("Input")
plt.ylabel("Gradient")
plt.title("Derivatives of Activation Functions", fontsize=14)
plt.legend()
plt.grid(True)
plt.show()

sample_inputs = np.array([-5, -2, -1, 0, 1, 2, 5])

table = pd.DataFrame({
    "Input": sample_inputs,
    "Sigmoid": sigmoid(sample_inputs).round(4),
    "ReLU": relu(sample_inputs),
    "Tanh": tanh(sample_inputs).round(4)
})
print(table.to_string(index=False))

summary = pd.DataFrame({
    "Function": ["Sigmoid", "ReLU", "Tanh"],
    "Min Output": [sigmoid(x).min(), relu(x).min(), tanh(x).min()],
    "Max Output": [sigmoid(x).max(), relu(x).max(), tanh(x).max()],
    "Output at 0": [sigmoid(0), relu(0), tanh(0)],
    "Max Gradient": [sigmoid_derivative(x).max(), relu_derivative(x).max(), tanh_derivative(x).max()],
    "Zero-Centred": ["No", "No", "Yes"]
}).round(4)
print(summary.to_string(index=False))

print("\nObservations:")
print("1. Sigmoid  : output is between 0 and 1; gradient is at most 0.25 and vanishes for large |x|.")
print("2. ReLU     : output is 0 for x<0 and x for x>0; cheap to compute and does not saturate for x>0,")
print("              but neurons can 'die' (gradient 0) for negative inputs.")
print("3. Tanh     : output is between -1 and 1 and zero-centred; gradient up to 1 but still saturates.")

layers = np.arange(1, 21)
x_typical = 1.0

grad_sigmoid = sigmoid_derivative(np.array(x_typical)) ** layers
grad_tanh = tanh_derivative(np.array(x_typical)) ** layers
grad_relu = relu_derivative(np.array(x_typical)) ** layers

plt.figure(figsize=(8,5))
plt.semilogy(layers, grad_sigmoid, marker="o", label="Sigmoid")
plt.semilogy(layers, grad_tanh, marker="s", label="Tanh")
plt.semilogy(layers, grad_relu, marker="^", label="ReLU")
plt.xlabel("Number of Layers")
plt.ylabel("Gradient Magnitude (log scale)")
plt.title("Vanishing Gradient: Sigmoid/Tanh vs ReLU", fontsize=14)
plt.legend()
plt.grid(True)
plt.show()

print("Gradient after 10 layers -> Sigmoid: %.2e | Tanh: %.2e | ReLU: %.2e" %
      (grad_sigmoid[9], grad_tanh[9], grad_relu[9]))

# Algorithm
# Memorize these seven steps:
# 1. Import NumPy, Pandas, Matplotlib and Seaborn.
# 2. Generate 400 equally spaced input values between -10 and 10.
# 3. Define Sigmoid, ReLU, Tanh and their derivatives.
# 4. Plot all three activation functions together and separately.
# 5. Plot their derivatives and calculate outputs for sample inputs.
# 6. Create a comparison table containing output range, maximum gradient and zero-centering.
# 7. Simulate gradients across 1 to 20 layers and demonstrate the vanishing gradient problem.
