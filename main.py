import random
from boxes import boxes 

# parameters used to sort the boxes and pick the correct ones
population_size = 200
generations = 1000  # increase generation to allow for better selections if needed
weight_limit = 250
mutation_rate = 0.01
cull_rate = 0.5  # cull rate of 50% at every generation

while True:
    # user input to ask whether there is a preference in the choice of boxes to have in the knapsack
    has_preference = input("Do you have a preference on the boxes to include in the knapsack? (yes or no): ").strip().lower()

    # user input to enter the preferred boxes if 'yes' from previous input
    if has_preference == "yes":
        preferred_boxes_input = input("Enter the preferred boxes (comma-separated indices, e.g., 1,3,5): ")
        preferred_boxes = [int(i) - 1 for i in preferred_boxes_input.split(",") if i.isdigit()]  
    # no preferred boxes if the user says 'no', the algorithm will just choose at random based on the best results 
    else:
        preferred_boxes = []  

    # measures the total importance of the selected boxes in a genome while ensuring the 250 weight limit is maintained 
    def fitness(genome):
        total_weight = sum(boxes[i+1][0] for i in range(len(genome)) if genome[i] == 1)
        total_importance = sum(boxes[i+1][1] for i in range(len(genome)) if genome[i] == 1) 
        
        # discard any genomes that exceed the weight limit of 250 lbs 
        if total_weight > weight_limit:
            return 0
        return total_importance

    # generate initial population with optional user preferences
    # this generates a random binary list of 1s and 0s for each individual in the population
    # each genome represents a possible solution where 1 means inclusion and 0 means exclusion of each box 
    def generate_population(size): 
        population = []
        for _ in range(size):
            genome = [random.randint(0, 1) for _ in range(len(boxes))]
            # include preferred boxes in the genome if preferences are given from user input 
            if preferred_boxes:
                for box in preferred_boxes:
                    genome[box] = 1
            population.append(genome)
        return population

    # this function implements tournament selection to choose genomes from the current population, ensuring the highest fitness are most likely chosen  
    def selection(population): 
        selected = []
        # use the entire population for selection without additional culling
        for _ in range(len(population)):
            # chooses a random set of 5 genomes from the population for each tournament 
            # choosing 5 will allow diversity between choosing the highest fitness but ensuring exploration of different solutions 
            candidates = random.sample(population, 5)
            selected.append(max(candidates, key=fitness))   
        return selected 

    # creates a new child genome using recombination (one-point crossover) between the two parent genomes (x and y) 
    def reproduce(x, y): 
        # helps to choose a crossover point, in which both parents contribute genetic material around this point
        n = len(x) 
        c = random.randint(1, n - 1)
        # combination of both parents 
        return x[:c] + y[c:] 

    # introduces random changes in phenotype to allow for genetic diversity in the population 
    # defined mutation rate of 0.01, allowing for variation while maintaining optimal solutions 
    def mutate(child): 
        for i in range(len(child)):
            if random.random() < mutation_rate:
                child[i] = 1 - child[i]  # Flip the bit
        return child

    # randomized heuristic search strategy that uses a natural selection metaphor to find the best solution  
    def genetic_algorithm(population):
        for generation in range(generations):
            # new children created will be stored here
            new_population = []  
            # reproduce and mutate to create the new population
            for _ in range(population_size):
                # parent x
                x = random.choice(population)   
                # parent y
                y = random.choice(population)   
                # Crossover of both the parents 
                child = reproduce(x, y)  
                # apply mutation on certain conditions but ensure it is rare 
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

    # output the best solution found
    print("\nBest possible solution found:")
    selected_boxes = [i+1 for i, bit in enumerate(best_solution) if bit == 1]
    print("Boxes selected:", selected_boxes)
    print("Total weight:", sum(boxes[i][0] for i in selected_boxes))
    print("Total importance:", sum(boxes[i][1] for i in selected_boxes))
    
    # user input that provides the choice to re-run the algorithm again to test various scenarios
    run_again = input("\nDo you want to run the algorithm again? (yes or no): ").strip().lower()
    if run_again != "yes":
        print("Goodbye!")
        break
