# LAB 1: Supervised Learning - Linear Regression

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

sns.set(style="whitegrid")

print("Lab 1 - Supervised Learning: Linear Regression")

diabetes = load_diabetes(as_frame=True)
df = diabetes.frame

print("Dataset Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

print("Statistical Summary:\n")
print(df.describe().round(3))

print("\nMissing values per column:\n")
print(df.isnull().sum())

plt.figure(figsize=(9,7))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

X = df.drop(columns="target")
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Training samples:", X_train.shape[0])
print("Testing samples :", X_test.shape[0])

model = LinearRegression()
model.fit(X_train_scaled, y_train)

print("Intercept (b):", round(model.intercept_, 3))

coef_df = pd.DataFrame({"Feature": X.columns, "Weight": model.coef_}).sort_values("Weight")
print("\nLearned Coefficients:\n")
print(coef_df.to_string(index=False))

y_pred_train = model.predict(X_train_scaled)
y_pred = model.predict(X_test_scaled)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("MAE  :", round(mae, 3))
print("MSE  :", round(mse, 3))
print("RMSE :", round(rmse, 3))
print("R2 (test) :", round(r2, 3))
print("R2 (train):", round(r2_score(y_train, y_pred_train), 3))

plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.scatter(y_test, y_pred, color="royalblue", alpha=0.7)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", label="Perfect prediction")
plt.title("Actual vs Predicted", fontsize=14)
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.legend()

plt.subplot(1,2,2)
sns.histplot(y_test - y_pred, kde=True, color="green")
plt.title("Residual Distribution", fontsize=14)
plt.xlabel("Residual (Actual - Predicted)")

plt.tight_layout()
plt.show()

X_bmi = df[["bmi"]]
simple_model = LinearRegression().fit(X_bmi, y)

w = simple_model.coef_[0]
b = simple_model.intercept_
print(f"Equation: y = {w:.2f} * bmi + {b:.2f}")

plt.figure(figsize=(8,5))
plt.scatter(X_bmi, y, color="gray", alpha=0.6, label="Actual Data")
plt.plot(X_bmi, simple_model.predict(X_bmi), color="red", linewidth=2, label="Regression Line")
plt.xlabel("BMI (standardized)")
plt.ylabel("Disease Progression")
plt.title("Simple Linear Regression: BMI vs Target")
plt.legend()
plt.show()

sample = X.iloc[[0]]
sample_scaled = scaler.transform(sample)
prediction = model.predict(sample_scaled)[0]

print("Predicted value:", round(prediction, 2))
print("Actual value   :", y.iloc[0])

# Algorithm
# Memorize these nine steps:
# 1. Import the required Python libraries.
# 2. Load the built-in Diabetes dataset.
# 3. Display the dataset and perform exploratory data analysis.
# 4. Separate input features (X) and target (y).
# 5. Split the dataset into 80% training and 20% testing.
# 6. Apply StandardScaler for feature scaling.
# 7. Train the Linear Regression model using fit().
# 8. Predict values and evaluate using MAE, MSE, RMSE and R².
# 9. Visualize the results and predict a new sample.
