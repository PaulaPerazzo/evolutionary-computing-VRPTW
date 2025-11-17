"""
Example: Run evolutionary algorithm with better parameters for higher quality solutions
This takes longer but produces better results
"""
from vrptw_data import VRPTWData
from evolutionary_algorithm import EvolutionaryVRPTW


def main():
    """Run EA with enhanced parameters"""
    
    print("="*80)
    print("ENHANCED EVOLUTIONARY ALGORITHM FOR VRPTW")
    print("="*80)
    
    # Load data
    data = VRPTWData('data/r101.csv')
    print(f"\nLoaded {data.get_num_customers()} customers")
    
    # Enhanced parameters for better solutions
    params = {
        'population_size': 100,     # Increased population
        'generations': 200,          # More generations
        'crossover_rate': 0.8,
        'mutation_rate': 0.2,
        'tournament_size': 3,
        'elitism_count': 5,          # Keep more elite solutions
        'vehicle_capacity': 200
    }
    
    print("\nEnhanced Parameters:")
    for key, value in params.items():
        print(f"  {key}: {value}")
    
    print("\nNote: This will take approximately 5-10 minutes...")
    print("\n" + "="*80 + "\n")
    
    # Run algorithm
    ea = EvolutionaryVRPTW(data, **params)
    best_solution = ea.evolve()
    
    # Print results
    ea.print_solution(best_solution)
    
    # Save to different file
    with open('vrptw_solution_enhanced.txt', 'w') as f:
        f.write("VRPTW Solution (Enhanced Parameters)\n")
        f.write("="*80 + "\n\n")
        f.write(f"Number of vehicles: {best_solution.num_vehicles}\n")
        f.write(f"Total distance: {best_solution.total_distance:.2f}\n")
        f.write(f"Feasible: {best_solution.feasible}\n")
        f.write(f"Fitness: {best_solution.fitness:.2f}\n\n")
        
        for i, route in enumerate(best_solution.routes, 1):
            f.write(f"Vehicle {i}: 0 -> {' -> '.join(map(str, route.customers))} -> 0\n")
            f.write(f"  Distance: {route.total_distance:.2f}, Demand: {route.total_demand}/200\n\n")
    
    print("\nSolution saved to: vrptw_solution_enhanced.txt")


if __name__ == "__main__":
    main()
