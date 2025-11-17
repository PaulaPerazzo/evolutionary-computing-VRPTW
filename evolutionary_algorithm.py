"""
Main Evolutionary Algorithm for VRPTW
Implements the genetic algorithm to solve Vehicle Routing Problem with Time Windows
"""
import numpy as np
import random
from typing import List
from vrptw_data import VRPTWData
from vrptw_solution import VRPTWSolution, VRPTWRoute
from genetic_operators import GeneticOperators


class EvolutionaryVRPTW:
    """Evolutionary Algorithm for VRPTW"""
    
    def __init__(self, data: VRPTWData, 
                 population_size: int = 100,
                 generations: int = 500,
                 crossover_rate: float = 0.8,
                 mutation_rate: float = 0.2,
                 tournament_size: int = 3,
                 elitism_count: int = 2,
                 vehicle_capacity: int = 200):
        """
        Initialize evolutionary algorithm
        
        Args:
            data: VRPTWData instance
            population_size: Number of individuals in population
            generations: Number of generations to evolve
            crossover_rate: Probability of crossover
            mutation_rate: Probability of mutation
            tournament_size: Size of tournament for selection
            elitism_count: Number of best individuals to preserve
            vehicle_capacity: Maximum capacity per vehicle
        """
        self.data = data
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elitism_count = elitism_count
        self.vehicle_capacity = vehicle_capacity
        
        self.operators = GeneticOperators(data, vehicle_capacity)
        self.population = []
        self.best_solution = None
        self.best_fitness_history = []
        
    def initialize_population(self):
        """Create initial population using random and greedy methods"""
        customer_ids = self.data.get_customer_ids()
        
        for _ in range(self.population_size):
            # Create random permutation of customers
            sequence = customer_ids.copy()
            random.shuffle(sequence)
            
            # Convert to solution with routes
            solution = self.operators._sequence_to_solution(sequence)
            
            # Calculate metrics and fitness
            solution.calculate_metrics(self.data)
            solution.fitness = self._calculate_fitness(solution)
            
            self.population.append(solution)
            
    def _calculate_fitness(self, solution: VRPTWSolution) -> float:
        """
        Calculate fitness value for a solution
        Multi-objective: minimize vehicles and distance
        
        Args:
            solution: Solution to evaluate
            
        Returns:
            Fitness value (lower is better)
        """
        # Penalize infeasible solutions heavily
        if not solution.feasible:
            penalty = 100000
        else:
            penalty = 0
            
        # Primary objective: minimize number of vehicles
        # Secondary objective: minimize total distance
        # Weight vehicles much more than distance
        fitness = (solution.num_vehicles * 10000) + solution.total_distance + penalty
        
        return fitness
    
    def evolve(self) -> VRPTWSolution:
        """
        Run the evolutionary algorithm
        
        Returns:
            Best solution found
        """
        print(f"Initializing population of {self.population_size} individuals...")
        self.initialize_population()
        
        # Track best solution
        self.best_solution = min(self.population, key=lambda x: x.fitness)
        self.best_fitness_history.append(self.best_solution.fitness)
        
        print(f"Generation 0: Best fitness = {self.best_solution.fitness:.2f}, "
              f"Vehicles = {self.best_solution.num_vehicles}, "
              f"Distance = {self.best_solution.total_distance:.2f}")
        
        for generation in range(1, self.generations + 1):
            new_population = []
            
            # Elitism: keep best individuals
            sorted_pop = sorted(self.population, key=lambda x: x.fitness)
            new_population.extend(sorted_pop[:self.elitism_count])
            
            # Generate offspring
            while len(new_population) < self.population_size:
                # Selection
                parent1 = self.operators.tournament_selection(self.population, self.tournament_size)
                parent2 = self.operators.tournament_selection(self.population, self.tournament_size)
                
                # Crossover
                if random.random() < self.crossover_rate:
                    offspring1, offspring2 = self.operators.order_crossover(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1, parent2
                
                # Mutation
                offspring1 = self.operators.swap_mutation(offspring1, self.mutation_rate)
                offspring2 = self.operators.insertion_mutation(offspring2, self.mutation_rate)
                
                # Evaluate offspring
                offspring1.calculate_metrics(self.data)
                offspring1.fitness = self._calculate_fitness(offspring1)
                
                offspring2.calculate_metrics(self.data)
                offspring2.fitness = self._calculate_fitness(offspring2)
                
                new_population.append(offspring1)
                if len(new_population) < self.population_size:
                    new_population.append(offspring2)
            
            # Replace population
            self.population = new_population
            
            # Track best solution
            generation_best = min(self.population, key=lambda x: x.fitness)
            if generation_best.fitness < self.best_solution.fitness:
                self.best_solution = generation_best
                
            self.best_fitness_history.append(self.best_solution.fitness)
            
            # Print progress every 10 generations
            if generation % 10 == 0:
                print(f"Generation {generation}: Best fitness = {self.best_solution.fitness:.2f}, "
                      f"Vehicles = {self.best_solution.num_vehicles}, "
                      f"Distance = {self.best_solution.total_distance:.2f}, "
                      f"Feasible = {self.best_solution.feasible}")
        
        return self.best_solution
    
    def print_solution(self, solution: VRPTWSolution):
        """
        Print detailed solution information
        
        Args:
            solution: Solution to print
        """
        print("\n" + "="*80)
        print("BEST SOLUTION FOUND")
        print("="*80)
        print(f"Number of vehicles: {solution.num_vehicles}")
        print(f"Total distance: {solution.total_distance:.2f}")
        print(f"Feasible: {solution.feasible}")
        print(f"Fitness: {solution.fitness:.2f}")
        print("\nRoutes:")
        print("-"*80)
        
        for i, route in enumerate(solution.routes, 1):
            print(f"\nVehicle {i}:")
            print(f"  Customers: 0 -> {' -> '.join(map(str, route.customers))} -> 0")
            print(f"  Distance: {route.total_distance:.2f}")
            print(f"  Demand: {route.total_demand}/{self.vehicle_capacity}")
            print(f"  Feasible: {route.feasible}")
