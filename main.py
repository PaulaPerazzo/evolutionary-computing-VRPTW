"""
Main script to run the Evolutionary Algorithm for VRPTW with r101.csv data
"""
import os
from vrptw_data import VRPTWData
from evolutionary_algorithm import EvolutionaryVRPTW
import config


def main():
    """Main function to run the evolutionary algorithm"""
    
    print("="*80)
    print("EVOLUTIONARY ALGORITHM FOR VRPTW - R101 Dataset")
    print("="*80)
    print(f"\nLoading data from: {config.DATA_FILE}")
    
    # Load data
    data = VRPTWData(config.DATA_FILE)
    print(f"Loaded {data.get_num_customers()} customers")
    print(f"Depot location: ({data.depot['XCOORD']}, {data.depot['YCOORD']})")
    
    # Algorithm parameters from config
    params = {
        'population_size': config.POPULATION_SIZE,
        'generations': config.GENERATIONS,
        'crossover_rate': config.CROSSOVER_RATE,
        'mutation_rate': config.MUTATION_RATE,
        'tournament_size': config.TOURNAMENT_SIZE,
        'elitism_count': config.ELITISM_COUNT,
        'vehicle_capacity': config.VEHICLE_CAPACITY
    }
    
    print("\nAlgorithm Parameters:")
    for key, value in params.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*80)
    print("STARTING EVOLUTION")
    print("="*80 + "\n")
    
    # Create and run evolutionary algorithm
    ea = EvolutionaryVRPTW(data, **params)
    best_solution = ea.evolve()
    
    # Print results
    ea.print_solution(best_solution)
    
    print("\n" + "="*80)
    print("OPTIMIZATION COMPLETE")
    print("="*80)
    
    # Save results to file
    with open(config.OUTPUT_FILE, 'w') as f:
        f.write("VRPTW Solution for r101.csv\n")
        f.write("="*80 + "\n\n")
        f.write(f"Number of vehicles: {best_solution.num_vehicles}\n")
        f.write(f"Total distance: {best_solution.total_distance:.2f}\n")
        f.write(f"Feasible: {best_solution.feasible}\n")
        f.write(f"Fitness: {best_solution.fitness:.2f}\n\n")
        f.write("Routes:\n")
        f.write("-"*80 + "\n\n")
        
        for i, route in enumerate(best_solution.routes, 1):
            f.write(f"Vehicle {i}:\n")
            f.write(f"  Customers: 0 -> {' -> '.join(map(str, route.customers))} -> 0\n")
            f.write(f"  Distance: {route.total_distance:.2f}\n")
            f.write(f"  Demand: {route.total_demand}/{params['vehicle_capacity']}\n")
            f.write(f"  Feasible: {route.feasible}\n\n")
    
    print(f"\nSolution saved to: {config.OUTPUT_FILE}")


if __name__ == "__main__":
    main()
