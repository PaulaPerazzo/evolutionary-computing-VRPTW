"""
VRPTW Solution Representation
Represents a solution (individual/chromosome) for the VRPTW problem
"""
import numpy as np
from typing import List, Tuple


class VRPTWRoute:
    """Represents a single vehicle route"""
    
    def __init__(self, customer_sequence: List[int]):
        """
        Initialize a route
        
        Args:
            customer_sequence: List of customer IDs in visit order
        """
        self.customers = customer_sequence
        self.total_distance = 0.0
        self.total_demand = 0
        self.feasible = True
        
    def __len__(self):
        return len(self.customers)
    
    def __repr__(self):
        return f"Route({self.customers})"


class VRPTWSolution:
    """Represents a complete VRPTW solution (set of routes)"""
    
    def __init__(self, routes: List[VRPTWRoute] = None):
        """
        Initialize a solution
        
        Args:
            routes: List of routes (each route is a list of customer IDs)
        """
        self.routes = routes if routes else []
        self.fitness = float('inf')  # Lower is better
        self.num_vehicles = 0
        self.total_distance = 0.0
        self.feasible = True
        
    def add_route(self, route: VRPTWRoute):
        """Add a route to the solution"""
        self.routes.append(route)
        
    def get_num_vehicles(self) -> int:
        """Get number of vehicles used"""
        return len(self.routes)
    
    def calculate_metrics(self, data):
        """
        Calculate solution metrics: number of vehicles and total distance
        
        Args:
            data: VRPTWData instance
        """
        self.num_vehicles = len(self.routes)
        self.total_distance = 0.0
        self.feasible = True
        
        for route in self.routes:
            route_distance, route_demand, route_feasible = self._evaluate_route(route, data)
            route.total_distance = route_distance
            route.total_demand = route_demand
            route.feasible = route_feasible
            
            self.total_distance += route_distance
            if not route_feasible:
                self.feasible = False
                
    def _evaluate_route(self, route: VRPTWRoute, data) -> Tuple[float, int, bool]:
        """
        Evaluate a single route
        
        Args:
            route: Route to evaluate
            data: VRPTWData instance
            
        Returns:
            Tuple of (distance, demand, feasibility)
        """
        if not route.customers:
            return 0.0, 0, True
            
        distance = 0.0
        demand = 0
        current_time = 0.0
        feasible = True
        
        # Start from depot (customer 0) to first customer
        prev_customer = 0
        
        for customer_id in route.customers:
            # Get customer data
            customer = data.get_customer_data(customer_id)
            
            # Add travel distance
            travel_dist = data.get_distance(prev_customer, customer_id)
            distance += travel_dist
            
            # Update time
            current_time += travel_dist
            
            # Check time window
            if current_time < customer['ready_time']:
                current_time = customer['ready_time']  # Wait if early
            elif current_time > customer['due_date']:
                feasible = False  # Late arrival
                
            # Add service time
            current_time += customer['service_time']
            
            # Add demand
            demand += customer['demand']
            
            prev_customer = customer_id
            
        # Return to depot
        distance += data.get_distance(prev_customer, 0)
        current_time += data.get_distance(prev_customer, 0)
        
        # Check depot time window
        depot_data = data.get_customer_data(0)
        if current_time > depot_data['due_date']:
            feasible = False
            
        # Check capacity constraint (200 per vehicle)
        if demand > 200:
            feasible = False
            
        return distance, demand, feasible
    
    def __repr__(self):
        return f"Solution(vehicles={self.num_vehicles}, distance={self.total_distance:.2f}, feasible={self.feasible})"
