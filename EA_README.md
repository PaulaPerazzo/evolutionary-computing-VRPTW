# Evolutionary Algorithm for VRPTW

This repository contains an implementation of an **Evolutionary Algorithm (Genetic Algorithm)** to solve the **Vehicle Routing Problem with Time Windows (VRPTW)** using the **r101.csv** dataset.

## Problem Description

The VRPTW is a combinatorial optimization problem where the goal is to:

1. **Primary Objective**: Minimize the number of vehicles needed
2. **Secondary Objective**: Minimize the total distance traveled

### Constraints

- **Customer Demands**: Each customer has a specific demand that must be satisfied
- **Vehicle Capacity**: Each vehicle has a maximum capacity of 200 units
- **Time Windows**: Each customer must be visited within their specified time window (READY_TIME to DUE_DATE)
- **Service Time**: Each customer requires a fixed service time (10 units)
- **Fleet Size**: Maximum of 25 vehicles available

### Dataset

The **r101.csv** dataset contains:
- 1 depot (customer 0)
- 100 customers
- Each location has coordinates (XCOORD, YCOORD)
- Each customer has: DEMAND, READY_TIME, DUE_DATE, SERVICE_TIME

## Algorithm Implementation

### Components

The implementation consists of the following modules:

1. **vrptw_data.py**: Data loader for reading and processing r101.csv
2. **vrptw_solution.py**: Solution representation (routes and fitness evaluation)
3. **genetic_operators.py**: Genetic operators (selection, crossover, mutation)
4. **evolutionary_algorithm.py**: Main evolutionary algorithm
5. **main.py**: Entry point to run the algorithm

### Evolutionary Algorithm Features

- **Representation**: Solutions are represented as sequences of customers split into routes
- **Population**: Random initialization of solutions
- **Selection**: Tournament selection
- **Crossover**: Order crossover (OX) to preserve customer sequences
- **Mutation**: 
  - Swap mutation: Randomly swap two customers
  - Insertion mutation: Remove and reinsert a customer at a different position
- **Elitism**: Best solutions are preserved across generations
- **Fitness Function**: Multi-objective combining number of vehicles and total distance

### Algorithm Parameters

Default parameters (can be adjusted in `main.py`):

```python
population_size: 30      # Number of individuals in population
generations: 50          # Number of generations to evolve
crossover_rate: 0.8      # Probability of crossover (80%)
mutation_rate: 0.2       # Probability of mutation (20%)
tournament_size: 3       # Number of individuals in tournament selection
elitism_count: 2         # Number of best solutions to preserve
vehicle_capacity: 200    # Maximum capacity per vehicle
```

## Installation

### Requirements

```bash
pip install pandas numpy
```

### Files Structure

```
evolutionary-computing-VRPTW/
├── data/
│   └── r101.csv              # VRPTW dataset
├── vrptw_data.py             # Data loader module
├── vrptw_solution.py         # Solution representation
├── genetic_operators.py      # Genetic operators
├── evolutionary_algorithm.py # Main EA implementation
├── main.py                   # Entry point
├── EA_README.md             # This file
└── README.md                 # Original project README
```

## Usage

### Running the Algorithm

Simply run the main script:

```bash
python main.py
```

### Output

The algorithm will:
1. Load the r101.csv dataset
2. Initialize a population of solutions
3. Evolve the population for the specified number of generations
4. Print progress every 10 generations
5. Display the best solution found
6. Save the solution to `vrptw_solution.txt`

### Example Output

```
================================================================================
EVOLUTIONARY ALGORITHM FOR VRPTW - R101 Dataset
================================================================================

Loading data from: data/r101.csv
Loaded 100 customers
Depot location: (35, 35)

Algorithm Parameters:
  population_size: 30
  generations: 50
  ...

================================================================================
STARTING EVOLUTION
================================================================================

Initializing population of 30 individuals...
Generation 0: Best fitness = 183199.37, Vehicles = 8, Distance = 3199.37
Generation 10: Best fitness = 182816.70, Vehicles = 8, Distance = 2816.70
...

================================================================================
BEST SOLUTION FOUND
================================================================================
Number of vehicles: 8
Total distance: 2346.90
Feasible: False
Fitness: 182346.90

Routes:
--------------------------------------------------------------------------------

Vehicle 1:
  Customers: 0 -> 89 -> 54 -> 73 -> ... -> 0
  Distance: 282.57
  Demand: 199/200
  Feasible: False
...
```

## Customization

### Adjusting Parameters

To get better solutions, you can modify the parameters in `main.py`:

```python
params = {
    'population_size': 100,    # Increase for better exploration
    'generations': 500,        # Increase for better convergence
    'crossover_rate': 0.8,
    'mutation_rate': 0.2,
    'tournament_size': 3,
    'elitism_count': 2,
    'vehicle_capacity': 200
}
```

**Note**: Increasing population_size and generations will improve solution quality but increase computation time.

### Modifying Genetic Operators

You can add or modify operators in `genetic_operators.py`:
- Add new mutation operators (inversion, 2-opt, etc.)
- Implement different crossover methods
- Try different selection strategies (roulette wheel, rank-based, etc.)

### Improving Initialization

The current implementation uses random initialization. For better results, you can:
- Implement constructive heuristics (nearest neighbor, savings algorithm)
- Use problem-specific initialization methods
- Seed the population with good solutions

## Performance Considerations

- **Data Loading**: Optimized using vectorized numpy operations (~0.004s)
- **Evolution**: Depends on population size and generations
  - 30 individuals × 50 generations: ~60 seconds
  - 100 individuals × 500 generations: ~10-20 minutes

## Known Limitations

1. **Time Window Feasibility**: The current implementation may produce solutions that violate time windows. This requires:
   - Better initialization respecting time windows
   - Repair operators to fix infeasible solutions
   - More sophisticated constraint handling

2. **Solution Quality**: With default parameters (30 pop, 50 gen), solutions are decent but not optimal. Increase parameters for better results.

3. **Local Optima**: Like all metaheuristics, the algorithm may get stuck in local optima. Consider:
   - Increasing mutation rate
   - Adding diversity mechanisms
   - Implementing hybrid approaches (EA + local search)

## Future Improvements

- [ ] Implement time-window-aware initialization
- [ ] Add repair operators for constraint violations
- [ ] Implement local search operators (2-opt, 3-opt)
- [ ] Add visualization of routes
- [ ] Implement adaptive parameters
- [ ] Add benchmarking against known solutions
- [ ] Parallel evaluation of population
- [ ] Multi-objective optimization (Pareto front)

## References

- Solomon, M. M. (1987). "Algorithms for the Vehicle Routing and Scheduling Problems with Time Window Constraints"
- Dataset source: https://www.sintef.no/projectweb/top/vrptw/100-customers/

## License

This implementation is for educational purposes as part of the evolutionary computing course.
