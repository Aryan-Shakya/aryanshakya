# LAB 8: Constraint-Based Optimization - Resource Allocation

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from scipy.optimize import linprog

sns.set(style="whitegrid")

print("Lab 8 - Constraint-Based Optimization: Resource Allocation")

c = [-40, -30]
A = [[2, 1], [1, 2]]
b = [100, 80]
bounds = [(0, None), (0, None)]

result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

print("Status :", result.message)
print("Success:", result.success)

if result.success:
    x1, x2 = result.x
    print("Product A (x1):", round(x1, 2))
    print("Product B (x2):", round(x2, 2))
    print("Maximum Profit:", round(-result.fun, 2))

labour_used = 2 * x1 + x2
material_used = x1 + 2 * x2

usage = pd.DataFrame({
    "Resource": ["Labour", "Material"],
    "Used": [labour_used, material_used],
    "Available": b,
    "Slack (Unused)": result.slack.round(2)
})
usage["Utilisation %"] = (usage["Used"] / usage["Available"] * 100).round(1)
print(usage.to_string(index=False))
print("\nProfit:", 40 * x1 + 30 * x2)

shadow_prices = -result.ineqlin.marginals
print("\nShadow price of Labour  :", round(shadow_prices[0], 2))
print("Shadow price of Material:", round(shadow_prices[1], 2))

A_all = np.array([[2, 1], [1, 2], [-1, 0], [0, -1]], dtype=float)
b_all = np.array([100, 80, 0, 0], dtype=float)

corners = []
for i, j in combinations(range(len(A_all)), 2):
    try:
        point = np.linalg.solve(A_all[[i, j]], b_all[[i, j]])
    except np.linalg.LinAlgError:
        continue
    if np.all(A_all @ point <= b_all + 1e-9):
        corners.append(point)

corners = np.unique(np.round(corners, 6) + 0.0, axis=0)
corner_df = pd.DataFrame(corners, columns=["x1", "x2"])
corner_df["Profit"] = 40 * corner_df["x1"] + 30 * corner_df["x2"]
print(corner_df.sort_values("Profit", ascending=False).to_string(index=False))
print("\nThe optimum always lies at a corner point of the feasible region.")

x_vals = np.linspace(0, 60, 200)

plt.figure(figsize=(9,6))
plt.plot(x_vals, 100 - 2 * x_vals, label="Labour: 2x1 + x2 = 100", color="blue")
plt.plot(x_vals, (80 - x_vals) / 2, label="Material: x1 + 2x2 = 80", color="green")

centre = corners.mean(axis=0)
order = np.argsort(np.arctan2(corners[:,1] - centre[1], corners[:,0] - centre[0]))
plt.fill(corners[order, 0], corners[order, 1], color="orange", alpha=0.3, label="Feasible Region")

plt.scatter(corners[:,0], corners[:,1], color="black", zorder=5)
plt.scatter(x1, x2, color="red", s=200, marker="*", zorder=6, label=f"Optimum ({x1:.0f}, {x2:.0f})")

plt.plot(x_vals, (-result.fun - 40 * x_vals) / 30, "r--", label="Max profit line (Z = 2200)")

plt.xlim(0, 60)
plt.ylim(0, 60)
plt.xlabel("Product A (x1)")
plt.ylabel("Product B (x2)")
plt.title("Graphical Solution of the Linear Programming Problem", fontsize=14)
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(7,5))
plt.bar(usage["Resource"], usage["Available"], color="lightgray", label="Available")
plt.bar(usage["Resource"], usage["Used"], color="steelblue", label="Used")
plt.ylabel("Units")
plt.title("Resource Usage at the Optimal Solution", fontsize=14)
plt.legend()
plt.show()

print("Result: Product A = %.0f units, Product B = %.0f units, Maximum Profit = %.0f" % (x1, x2, -result.fun))
