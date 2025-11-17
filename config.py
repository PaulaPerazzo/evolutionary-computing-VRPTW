"""
Configuration file for Evolutionary Algorithm parameters
Adjust these parameters to tune the algorithm's performance and solution quality
"""

# Data configuration
DATA_FILE = 'data/r101.csv'

# Population configuration
POPULATION_SIZE = 30        # Number of individuals in population
                           # Larger values: better exploration, slower computation
                           # Recommended: 30-100

# Evolution configuration  
GENERATIONS = 50           # Number of generations to evolve
                           # Larger values: better convergence, longer runtime
                           # Recommended: 50-500

# Genetic operator rates
CROSSOVER_RATE = 0.8       # Probability of crossover (0.0-1.0)
                           # Typical values: 0.7-0.9
                           
MUTATION_RATE = 0.2        # Probability of mutation (0.0-1.0)
                           # Typical values: 0.1-0.3
                           
# Selection configuration
TOURNAMENT_SIZE = 3        # Number of individuals in tournament selection
                           # Larger values: more selection pressure
                           # Recommended: 2-5

# Elitism configuration
ELITISM_COUNT = 2          # Number of best individuals to preserve
                           # Recommended: 1-5

# Problem constraints
VEHICLE_CAPACITY = 200     # Maximum capacity per vehicle
MAX_VEHICLES = 25          # Maximum number of vehicles available

# Fitness weights (for multi-objective optimization)
# Primary objective: minimize vehicles
# Secondary objective: minimize distance
VEHICLE_WEIGHT = 10000     # Weight for number of vehicles in fitness
DISTANCE_WEIGHT = 1        # Weight for distance in fitness
PENALTY_WEIGHT = 100000    # Penalty for infeasible solutions

# Output configuration
OUTPUT_FILE = 'vrptw_solution.txt'
PROGRESS_INTERVAL = 10     # Print progress every N generations
