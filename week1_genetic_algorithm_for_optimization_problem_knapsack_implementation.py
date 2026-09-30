import random

# --------------------------------------------------
# Knapsack Problem
# --------------------------------------------------

weights = [2, 3, 5, 4, 1]
values = [10, 15, 23, 20, 5]

capacity = 10
n = len(weights)

# Genetic Algorithm parameters
population_size = 10
generations = 100
mutation_rate = 0.1


# --------------------------------------------------
# Generate Initial Population
# --------------------------------------------------

def generate_population():
    population = []

    for _ in range(population_size):
        chromosome = []

        for _ in range(n):
            chromosome.append(random.randint(0, 1))

        population.append(chromosome)

    return population


# --------------------------------------------------
# Calculate Fitness
# --------------------------------------------------

def fitness(chromosome):

    total_weight = 0
    total_value = 0

    for i in range(n):

        if chromosome[i] == 1:
            total_weight += weights[i]
            total_value += values[i]

    # Invalid solution
    if total_weight > capacity:
        return 0

    return total_value


# --------------------------------------------------
# Selection
# Select two best individuals
# --------------------------------------------------

def selection(population):

    population.sort(key=fitness, reverse=True)

    return population[0], population[1]


# --------------------------------------------------
# Crossover
# --------------------------------------------------

def crossover(parent1, parent2):

    point = random.randint(1, n - 1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2


# --------------------------------------------------
# Mutation
# --------------------------------------------------

def mutation(chromosome):

    for i in range(n):

        if random.random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]

    return chromosome


# --------------------------------------------------
# Genetic Algorithm
# --------------------------------------------------

def genetic_algorithm():

    # Step 1: Generate initial population
    population = generate_population()

    best_solution = None
    best_fitness = 0

    # Step 2: Repeat for given number of generations
    for generation in range(generations):

        # Find best solution of current generation
        population.sort(key=fitness, reverse=True)

        if fitness(population[0]) > best_fitness:

            best_solution = population[0].copy()
            best_fitness = fitness(population[0])

        # Step 3: Selection
        parent1, parent2 = selection(population)

        new_population = []

        # Step 4: Create new population
        while len(new_population) < population_size:

            # Crossover
            child1, child2 = crossover(parent1, parent2)

            # Mutation
            child1 = mutation(child1)
            child2 = mutation(child2)

            # Add children
            new_population.append(child1)

            if len(new_population) < population_size:
                new_population.append(child2)

        # Step 5: Replacement
        population = new_population

    return best_solution, best_fitness


# --------------------------------------------------
# Run Genetic Algorithm
# --------------------------------------------------

best_solution, best_value = genetic_algorithm()


# --------------------------------------------------
# Display Result
# --------------------------------------------------

total_weight = 0

print("Best Chromosome:", best_solution)

print("Selected Items:")

for i in range(n):

    if best_solution[i] == 1:

        item = chr(65 + i)

        print(
            "Item", item,
            "- Weight:", weights[i],
            "kg, Value:", values[i]
        )

        total_weight += weights[i]


print("\nTotal Weight:", total_weight, "kg")
print("Total Value:", best_value)