Punna Chowdhury

October 28, 2024



**Instructions**:
- Please run `boxes.py` first to define the boxes with their weights and importance values, respectively.
- Then, run `main.py` to execute the genetic algorithm, which contains all parameters, assumptions, and the main solution for the knapsack problem.

**Dependencies Used**:
- `random` is used for generating initial population genomes, selecting parents for reproduction, applying mutation, and selecting candidates in the tournament selection process.

**Methodology and Assumptions**:
- **Genetic Algorithm**:
  - A genetic algorithm uses randomized heuristic search strategy that uses a natural selection metaphor to find the best solution. 
  - For this problem, the goal is to maximize the total importance (value) of selected boxes without exceeding the knapsack's weight limit (250 lbs).
  - The algorithm uses the following steps:
    - Initialization: Generated an initial random population of the possible genomes using binary values, where 1 is for included boxes and 0 for excluded ones. 
    - Fitness Calculation: Calculate the genome’s fitness based on the total importance of selected boxes while ignoring genomes that exceed the weight limit.
    - Tournament Selection: Choose genomes for reproduction using a tournament selection method, where individual with the best fitness wins the tournament and are selected as a parent (x and y). 
    - Reproduction (Crossover): Create a one-point crossover on selected parents to create a new offspring genome. 
    - Mutation: Apply mutations to the offspring genomes to create diversity. 
    - Culling (Truncated rank-based selection): After each generation, take only the top n individuals (50% in this case) in the ranked list and making the same number of offspring for each selection.
- **Assumptions**:
  - Box Preference: User has the choice to pre-select specific boxes they want included in the knapsack, ensuring these boxes are always part of the solution. If preferred boxes are specified, they will always be set to '1' (included) in the initial population. If no preferences are specified, boxes are randomly included/excluded.
  - Weight limit: The knapsack's weight limit is set to 250, and genomes that exceeds the limit has a fitness of 0. 
  - Population: A population size of 200
  - Generation: A generation size of 1000 
  - Mutation Rate: The mutation rate is set to 0.01 (1%) to introduce some variations without fulling changing the optimal solutions.
  - Culling Step: The population is culled by 50% once per generation, allowing diversity while ensuring the fittest solutions.
- **Final Output**:
  - Output: The output should display all the generations, including the selected boxes, their total weight, and total importance.
  - Example Output:
        Generation 998 - Best Fitness: 44
        Generation 999 - Best Fitness: 44
        Generation 1000 - Best Fitness: 44
        
        Best possible solution found:
        Boxes selected: [1, 2, 3, 6, 8, 10, 11]
        Total weight: 250
        Total importance: 44
  - The user can choose to re-run the algorithm with the same, different or no box preferences to see how different results vary.


