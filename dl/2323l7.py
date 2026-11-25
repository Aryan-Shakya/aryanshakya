# LAB 7: Non-Gradient-Based Optimization - Genetic Algorithm

import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

print("Lab 7 - Non-Gradient-Based Optimization: Genetic Algorithm")

random.seed(42)

BITS = 5
POPULATION_SIZE = 10
GENERATIONS = 30
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.05

def create_chromosome():
    return [random.randint(0, 1) for _ in range(BITS)]

def decode(c):
    value = 0
    for bit in c:
        value = value * 2 + bit
    return value

def fitness(c):
    return decode(c) ** 2

def select(population):
    a = random.choice(population)
    b = random.choice(population)
    return a.copy() if fitness(a) > fitness(b) else b.copy()

def crossover(a, b):
    if random.random() < CROSSOVER_RATE:
        point = random.randint(1, BITS - 1)
        return (a[:point] + b[point:],
                b[:point] + a[point:])
    return a.copy(), b.copy()

def mutate(c):
    for i in range(BITS):
        if random.random() < MUTATION_RATE:
            c[i] = 1 - c[i]
    return c

population = [create_chromosome() for _ in range(POPULATION_SIZE)]
initial_population = [c.copy() for c in population]

best_history = []
avg_history = []

for generation in range(GENERATIONS):
    best = max(population, key=fitness)
    best_history.append(fitness(best))
    avg_history.append(np.mean([fitness(c) for c in population]))
    print(f"Generation {generation+1:2d} | Best x: {decode(best):2d} | "
          f"Best Fitness: {fitness(best):3d} | Average Fitness: {avg_history[-1]:.1f}")

    new_population = []
    while len(new_population) < POPULATION_SIZE:
        p1, p2 = select(population), select(population)
        c1, c2 = crossover(p1, p2)
        new_population.append(mutate(c1))
        if len(new_population) < POPULATION_SIZE:
            new_population.append(mutate(c2))
    population = new_population

best = max(population, key=fitness)
print("\nBest chromosome:", best)
print("Best x          :", decode(best))
print("Best Fitness    :", fitness(best))
print("Theoretical optimum: x = 31, fitness = 961")

plt.figure(figsize=(9,5))
plt.plot(best_history, marker="o", color="green", label="Best Fitness")
plt.plot(avg_history, marker="s", color="blue", linestyle="--", label="Average Fitness")
plt.axhline(961, color="red", linestyle=":", label="Optimum (961)")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.title("Convergence of the Genetic Algorithm", fontsize=14)
plt.legend()
plt.grid(True)
plt.show()

final_df = pd.DataFrame({
    "Chromosome": ["".join(map(str, c)) for c in population],
    "x": [decode(c) for c in population],
    "Fitness": [fitness(c) for c in population]
}).sort_values("Fitness", ascending=False)
print("Final Population:\n")
print(final_df.to_string(index=False))

xs = np.arange(0, 32)
plt.figure(figsize=(9,5))
plt.plot(xs, xs ** 2, color="gray", label="f(x) = x^2")
plt.scatter([decode(c) for c in initial_population], [fitness(c) for c in initial_population],
            color="orange", s=80, label="Initial Population")
plt.scatter([decode(c) for c in population], [fitness(c) for c in population],
            color="green", s=80, marker="x", label="Final Population")
plt.xlabel("x")
plt.ylabel("Fitness")
plt.title("Population Movement towards the Optimum", fontsize=14)
plt.legend()
plt.grid(True)
plt.show()

# Algorithm
# 1. Import required libraries.
# 2. Set GA parameters.
# 3. Generate random 5-bit chromosomes.
# 4. Decode binary chromosomes into decimal numbers.
# 5. Calculate fitness using x^2.
# 6. Select parents using tournament selection.
# 7. Perform single-point crossover.
# 8. Apply bit-flip mutation.
# 9. Repeat for 30 generations.
# 10. Display the best chromosome and fitness.
# 11. Plot fitness convergence and population movement.
