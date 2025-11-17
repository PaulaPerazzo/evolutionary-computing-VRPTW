# Example Usage and Output

## Quick Start

To run the evolutionary algorithm with default parameters:

```bash
python main.py
```

## Expected Output

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
  crossover_rate: 0.8
  mutation_rate: 0.2
  tournament_size: 3
  elitism_count: 2
  vehicle_capacity: 200

================================================================================
STARTING EVOLUTION
================================================================================

Initializing population of 30 individuals...
Generation 0: Best fitness = 183217.26, Vehicles = 8, Distance = 3217.26
Generation 10: Best fitness = 182978.63, Vehicles = 8, Distance = 2978.63, Feasible = False
Generation 20: Best fitness = 182695.46, Vehicles = 8, Distance = 2695.46, Feasible = False
Generation 30: Best fitness = 182635.33, Vehicles = 8, Distance = 2635.33, Feasible = False
Generation 40: Best fitness = 182464.08, Vehicles = 8, Distance = 2464.08, Feasible = False
Generation 50: Best fitness = 182349.66, Vehicles = 8, Distance = 2349.66, Feasible = False

================================================================================
BEST SOLUTION FOUND
================================================================================
Number of vehicles: 8
Total distance: 2349.66
Feasible: False
Fitness: 182349.66

Routes:
--------------------------------------------------------------------------------

Vehicle 1:
  Customers: 0 -> 89 -> 54 -> 73 -> 38 -> 98 -> 21 -> 55 -> 39 -> 4 -> 43 -> 95 -> 61 -> 59 -> 0
  Distance: 282.57
  Demand: 199/200
  Feasible: False

Vehicle 2:
  Customers: 0 -> 30 -> 1 -> 9 -> 81 -> 35 -> 58 -> 70 -> 19 -> 32 -> 65 -> 34 -> 24 -> 29 -> 0
  Distance: 302.96
  Demand: 190/200
  Feasible: False

...

================================================================================
OPTIMIZATION COMPLETE
================================================================================

Solution saved to: vrptw_solution.txt
```

## Customization

To adjust parameters, edit `config.py`:

```python
# For better solutions (takes longer)
POPULATION_SIZE = 100
GENERATIONS = 200

# For faster testing
POPULATION_SIZE = 20
GENERATIONS = 20
```

Or use the enhanced script:

```bash
python run_enhanced.py
```

## Understanding the Output

- **Vehicles**: Number of vehicles used (objective 1)
- **Distance**: Total distance traveled by all vehicles (objective 2)
- **Feasible**: Whether all constraints are satisfied (time windows, capacity)
- **Fitness**: Combined objective value (lower is better)

## Typical Results

With default parameters (30 population, 50 generations):
- **Runtime**: ~60 seconds
- **Vehicles**: 7-9 vehicles
- **Distance**: 2300-2600 units
- **Feasibility**: May violate some time windows (common in initial runs)

With enhanced parameters (100 population, 200 generations):
- **Runtime**: 5-10 minutes
- **Vehicles**: 6-8 vehicles
- **Distance**: 2000-2400 units
- **Feasibility**: Better constraint satisfaction

## Known Behavior

The algorithm currently focuses on minimizing vehicles and distance but may produce solutions that violate time window constraints. This is expected behavior for the current implementation. To improve feasibility:

1. Increase population size and generations
2. Implement time-window-aware initialization
3. Add repair operators for constraint violations
4. Adjust fitness penalties for infeasible solutions
