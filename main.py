import random
from boxes import boxes 

# Parameters 
population_size = 200
generations = 1000  # Increase generation to allow for better selections
weight_limit = 250
mutation_rate = 0.01
cull_rate = 0.5  # Cull rate of 50% at every generation

# Main loop to allow the user to rerun the algorithm
while True:
    # User input to ask whether there is a preference in the choice of boxes to have in the knapsack
    has_preference = input("Do you have a preference on the boxes to include in the knapsack? (yes or no): ").strip().lower()

    # User input to enter the preferred boxes if 'yes' from previous input
    if has_preference == "yes":
        preferred_boxes_input = input("Enter the preferred boxes (comma-separated indices, e.g., 1,3,5): ")
        preferred_boxes = [int(i) - 1 for i in preferred_boxes_input.split(",") if i.isdigit()]  
    # No preferred boxes if the user says 'no', the algorithm will just choose at random based on the best results 
    else:
        preferred_boxes = []  

    # Measures the total importance of the selected boxes in a genome while ensuring the 250 weight limit is maintained 
    def fitness(genome):
        total_weight = sum(boxes[i+1][0] for i in range(len(genome)) if genome[i] == 1)
        total_importance = sum(boxes[i+1][1] for i in range(len(genome)) if genome[i] == 1) 
        
        # Discard any genomes that exceed the weight limit of 250 lbs 
        if total_weight > weight_limit:
            return 0
        return total_importance

    # Generate initial population with optional user preferences
    # This generates a random binary list of 1s and 0s for each individual in the population
    # Each genome represents a possible solution where 1 means inclusion and 0 means exclusion of each box 
    def generate_population(size): 
        population = []
        for _ in range(size):
            genome = [random.randint(0, 1) for _ in range(len(boxes))]
            # Include preferred boxes in the genome if preferences are given from user input 
            if preferred_boxes:
                for box in preferred_boxes:
                    genome[box] = 1
            population.append(genome)
        return population

    # This function implements tournament selection to choose genomes from the current population, ensuring the highest fitness are most likely chosen  
    def selection(population): 
        selected = []
        # Use the entire population for selection without additional culling
        for _ in range(len(population)):
            # Chooses a random set of 5 genomes from the population for each tournament 
            # Choosing 5 will allow diversity between choosing highest fitness but ensuring exploration of different solutions 
            candidates = random.sample(population, 5)
            selected.append(max(candidates, key=fitness))   
        return selected 

    # Creates a new child genome using recombination (one-point crossover) between the two parent genomes (x and y) 
    def reproduce(x, y): 
        # Helps to choose a crossover point, in which both parents contribute genetic material around this point
        n = len(x) 
        c = random.randint(1, n - 1)
        # Combination of both parents 
        return x[:c] + y[c:] 

    # Introduces random changes in phenotype to allow for genetic diversity in population 
    # Defined mutation rate of 0.01, allowing for variation while maintaining optimal solutions 
    def mutate(child): 
        for i in range(len(child)):
            if random.random() < mutation_rate:
                child[i] = 1 - child[i]  # Flip the bit
        return child

    # Randomized heuristic search strategy that uses a natural selection metaphor to find the best solution  
    def genetic_algorithm(population):
        for generation in range(generations):
            # New children created will be stored here
            new_population = []  
            # Reproduce and mutate to create the new population
            for _ in range(population_size):
                # Parent x
                x = random.choice(population)   
                # Parent y
                y = random.choice(population)   
                # Crossover of both the parents 
                child = reproduce(x, y)  
                # Apply mutation on certain conditions but ensure it is rare 
                if random.random() < mutation_rate:   
                    child = mutate(child)
                new_population.append(child)
            
            # Cull the population to retain only the top 50% based on the cull_rate parameter
            # Sorts genomes by fitness and keeps only the top half  
            population = sorted(new_population, key=fitness, reverse=True)[:int(population_size * cull_rate)]

            # Find and print the best individual in the current population
            best_genome = max(population, key=fitness)
            print(f"Generation {generation + 1} - Best Fitness: {fitness(best_genome)}")

        return best_genome

    initial_population = generate_population(population_size)
    best_solution = genetic_algorithm(initial_population)

    # Output the best solution found
    print("\nBest possible solution found:")
    selected_boxes = [i+1 for i, bit in enumerate(best_solution) if bit == 1]
    print("Boxes selected:", selected_boxes)
    print("Total weight:", sum(boxes[i][0] for i in selected_boxes))
    print("Total importance:", sum(boxes[i][1] for i in selected_boxes))
    
    # User input that provides the choice to re-run the algorithm again
    run_again = input("\nDo you want to run the algorithm again? (yes or no): ").strip().lower()
    if run_again != "yes":
        print("Goodbye!")
        break
