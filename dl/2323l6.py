# LAB 6: Rational Agent Simulation

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

print("Lab 6 - Rational Agent Simulation")

actions = ["CLEAN", "MOVE", "WAIT"]
percepts = [{"dirt": 0.9}, {"dirt": 0.2}, {"dirt": 0.0}]

def utility(percept, action):
    dirt = percept["dirt"]
    if action == "CLEAN":
        return 10 * dirt
    if action == "MOVE":
        return 2
    return 1 - dirt

def rational_agent(percept):
    scores = {a: utility(percept, a) for a in actions}
    return max(scores, key=scores.get), scores

rows = []
for percept in percepts:
    action, scores = rational_agent(percept)
    print("Percept:", percept)
    print("Utilities:", {k: round(v, 2) for k, v in scores.items()})
    print("Selected Action:", action)
    print()
    rows.append({"Dirt Level": percept["dirt"],
                 **{f"U({k})": round(v, 2) for k, v in scores.items()},
                 "Selected Action": action})

print(pd.DataFrame(rows).to_string(index=False))

dirt_levels = np.linspace(0, 1, 101)

plt.figure(figsize=(9,5))
for a in actions:
    plt.plot(dirt_levels, [utility({"dirt": d}, a) for d in dirt_levels], linewidth=2, label=a)

chosen = [rational_agent({"dirt": d})[0] for d in dirt_levels]
switch_point = next(d for d, a in zip(dirt_levels, chosen) if a == "CLEAN")
plt.axvline(switch_point, color="gray", linestyle="--", label=f"Switch to CLEAN at dirt = {switch_point:.2f}")

plt.xlabel("Dirt Level")
plt.ylabel("Utility")
plt.title("Utility of Actions vs Dirt Level", fontsize=14)
plt.legend()
plt.grid(True)
plt.show()

print("The rational agent prefers MOVE for low dirt and CLEAN once dirt >= %.2f" % switch_point)

np.random.seed(42)
dirt_stream = np.random.rand(200)

def run(policy):
    return np.mean([utility({"dirt": d}, policy(d)) for d in dirt_stream])

policies = {
    "Rational Agent": lambda d: rational_agent({"dirt": d})[0],
    "Random Agent": lambda d: np.random.choice(actions),
    "Always CLEAN": lambda d: "CLEAN",
    "Always MOVE": lambda d: "MOVE",
    "Always WAIT": lambda d: "WAIT",
}

scores = {name: run(policy) for name, policy in policies.items()}
score_df = pd.DataFrame({"Agent": list(scores.keys()), "Average Utility": list(scores.values())}).round(3)
print(score_df.to_string(index=False))

plt.figure(figsize=(9,5))
sns.barplot(x="Agent", y="Average Utility", data=score_df, palette="viridis", hue="Agent", legend=False)
plt.title("Average Utility of Different Agents", fontsize=14)
plt.xticks(rotation=15)
plt.show()

actions_taken = pd.Series([rational_agent({"dirt": d})[0] for d in dirt_stream]).value_counts()
print("\nActions chosen by the rational agent:\n")
print(actions_taken)
print("\nConclusion: the rational agent achieves the highest average utility because it always picks the")
print("maximum-utility action for the current percept.")
