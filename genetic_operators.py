"""
Genetic Operators for VRPTW Evolutionary Algorithm
Includes selection, crossover, and mutation operators
"""
import numpy as np
import random
from typing import List, Tuple
from vrptw_solution import VRPTWSolution, VRPTWRoute


class GeneticOperators:
    """Class containing genetic operators for VRPTW"""
    
    def __init__(self, data, vehicle_capacity: int = 200):
        """
        Initialize genetic operators
        
        Args:
            data: VRPTWData instance
            vehicle_capacity: Maximum capacity per vehicle
        """
        self.data = data
        self.vehicle_capacity = vehicle_capacity
        
    def tournament_selection(self, population: List[VRPTWSolution], 
                            tournament_size: int = 3) -> VRPTWSolution:
        """
        Tournament selection
        
        Args:
            population: List of solutions
            tournament_size: Number of individuals in tournament
            
        Returns:
            Selected solution
        """
        tournament = random.sample(population, tournament_size)
        return min(tournament, key=lambda x: x.fitness)
    
    def order_crossover(self, parent1: VRPTWSolution, 
                       parent2: VRPTWSolution) -> Tuple[VRPTWSolution, VRPTWSolution]:
        """
        Order crossover (OX) for route-based representation
        Creates two offspring from two parents
        
        Args:
            parent1: First parent solution
            parent2: Second parent solution
            
        Returns:
            Tuple of two offspring solutions
        """
        # Flatten routes to get customer sequences
        seq1 = []
        for route in parent1.routes:
            seq1.extend(route.customers)
            
        seq2 = []
        for route in parent2.routes:
            seq2.extend(route.customers)
            
        # Perform order crossover on sequences
        size = len(seq1)
        if size < 2:
            return parent1, parent2
            
        # Select two random crossover points
        cx_point1, cx_point2 = sorted(random.sample(range(size), 2))
        
        # Create offspring sequences
        offspring1_seq = self._ox_crossover_sequence(seq1, seq2, cx_point1, cx_point2)
        offspring2_seq = self._ox_crossover_sequence(seq2, seq1, cx_point1, cx_point2)
        
        # Convert sequences back to routes
        offspring1 = self._sequence_to_solution(offspring1_seq)
        offspring2 = self._sequence_to_solution(offspring2_seq)
        
        return offspring1, offspring2
    
    def _ox_crossover_sequence(self, parent1: List[int], parent2: List[int],
                               point1: int, point2: int) -> List[int]:
        """Helper for order crossover on customer sequences"""
        size = len(parent1)
        offspring = [None] * size
        
        # Copy segment from parent1
        offspring[point1:point2] = parent1[point1:point2]
        
        # Fill remaining positions from parent2
        parent2_filtered = [x for x in parent2 if x not in offspring[point1:point2]]
        
        current_pos = point2
        for gene in parent2_filtered:
            if current_pos >= size:
                current_pos = 0
            while offspring[current_pos] is not None:
                current_pos = (current_pos + 1) % size
            offspring[current_pos] = gene
            current_pos = (current_pos + 1) % size
            
        return offspring
    
    def swap_mutation(self, solution: VRPTWSolution, 
                     mutation_rate: float = 0.1) -> VRPTWSolution:
        """
        Swap mutation: randomly swap two customers
        
        Args:
            solution: Solution to mutate
            mutation_rate: Probability of mutation
            
        Returns:
            Mutated solution
        """
        if random.random() > mutation_rate:
            return solution
            
        # Flatten to sequence
        sequence = []
        for route in solution.routes:
            sequence.extend(route.customers)
            
        if len(sequence) < 2:
            return solution
            
        # Perform swap
        idx1, idx2 = random.sample(range(len(sequence)), 2)
        sequence[idx1], sequence[idx2] = sequence[idx2], sequence[idx1]
        
        # Convert back to solution
        mutated = self._sequence_to_solution(sequence)
        return mutated
    
    def insertion_mutation(self, solution: VRPTWSolution,
                          mutation_rate: float = 0.1) -> VRPTWSolution:
        """
        Insertion mutation: remove a customer and insert at random position
        
        Args:
            solution: Solution to mutate
            mutation_rate: Probability of mutation
            
        Returns:
            Mutated solution
        """
        if random.random() > mutation_rate:
            return solution
            
        # Flatten to sequence
        sequence = []
        for route in solution.routes:
            sequence.extend(route.customers)
            
        if len(sequence) < 2:
            return solution
            
        # Remove and insert
        remove_idx = random.randint(0, len(sequence) - 1)
        customer = sequence.pop(remove_idx)
        insert_idx = random.randint(0, len(sequence))
        sequence.insert(insert_idx, customer)
        
        # Convert back to solution
        mutated = self._sequence_to_solution(sequence)
        return mutated
    
    def _sequence_to_solution(self, sequence: List[int]) -> VRPTWSolution:
        """
        Convert a customer sequence to a VRPTWSolution with routes
        Uses a simple greedy approach respecting capacity constraints
        
        Args:
            sequence: List of customer IDs
            
        Returns:
            VRPTWSolution with routes
        """
        solution = VRPTWSolution()
        current_route = []
        current_demand = 0
        
        for customer_id in sequence:
            customer = self.data.get_customer_data(customer_id)
            demand = customer['demand']
            
            # Check if adding customer exceeds capacity
            if current_demand + demand > self.vehicle_capacity:
                # Start new route
                if current_route:
                    solution.add_route(VRPTWRoute(current_route))
                current_route = [customer_id]
                current_demand = demand
            else:
                # Add to current route
                current_route.append(customer_id)
                current_demand += demand
                
        # Add last route
        if current_route:
            solution.add_route(VRPTWRoute(current_route))
            
        return solution
