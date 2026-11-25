# LAB 5: Problem-Solving Agent - Vacuum Cleaner Agent

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import product

sns.set(style="whitegrid")

print("Lab 5 - Problem-Solving Agent: Vacuum Cleaner")

environment = {"A": "Dirty", "B": "Dirty"}
position = "A"

def goal_reached(environment):
    return all(status == "Clean" for status in environment.values())

print("Initial Environment:", environment)
print("Agent Position     :", position)
print("Goal Reached?      :", goal_reached(environment))

def choose_action(environment, position):
    if environment[position] == "Dirty":
        return "SUCK"
    if position == "A":
        return "MOVE_RIGHT"
    return "MOVE_LEFT"

def run_agent(env, pos, max_steps=20):
    env = env.copy()
    trace, step = [], 0

    while not goal_reached(env) and step < max_steps:
        action = choose_action(env, pos)
        trace.append({"Step": step, "Position": pos,
                      "Room A": env["A"], "Room B": env["B"], "Action": action})

        if action == "SUCK":
            env[pos] = "Clean"
        elif action == "MOVE_RIGHT":
            pos = "B"
        else:
            pos = "A"
        step += 1

    return trace, env, pos, step

trace, final_env, final_pos, steps = run_agent(environment, position)

print(pd.DataFrame(trace).to_string(index=False))
print("\nFinal Environment:", final_env)
print("Final Position   :", final_pos)
print("Steps Taken      :", steps)
print("Goal Reached     :", goal_reached(final_env))

results = []
for a, b, pos in product(["Clean", "Dirty"], ["Clean", "Dirty"], ["A", "B"]):
    start = {"A": a, "B": b}
    dirty_rooms = list(start.values()).count("Dirty")
    _, env_end, _, steps = run_agent(start, pos)

    results.append({
        "Start A": a, "Start B": b, "Start Position": pos,
        "Steps": steps,
        "Goal Reached": goal_reached(env_end),
        "Performance Score": 10 * dirty_rooms - steps
    })

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))

labels = [f"{r['Start A'][0]}{r['Start B'][0]}-{r['Start Position']}" for r in results]

plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.bar(labels, results_df["Steps"], color="steelblue")
plt.title("Steps Needed per Starting State", fontsize=14)
plt.xlabel("Start (RoomA RoomB - Position)")
plt.ylabel("Steps")

plt.subplot(1,2,2)
plt.bar(labels, results_df["Performance Score"], color="seagreen")
plt.title("Performance Score per Starting State", fontsize=14)
plt.xlabel("Start (RoomA RoomB - Position)")
plt.ylabel("Score")

plt.tight_layout()
plt.show()

print("Goal reached in all cases:", results_df["Goal Reached"].all())
print("Average steps:", results_df["Steps"].mean())

# Algorithm
# Memorize these seven steps:
# 1. Import the required libraries and define the two-room environment.
# 2. Define the goal test to check whether both rooms are clean.
# 3. Define the agent policy to select SUCK, MOVE_RIGHT or MOVE_LEFT.
# 4. Create run_agent() to simulate the agent for a maximum of 20 steps and record its trace.
# 5. Run the simulation for both rooms dirty, starting in room A.
# 6. Test the agent on all eight possible starting states and positions.
# 7. Calculate performance scores and plot the results.
