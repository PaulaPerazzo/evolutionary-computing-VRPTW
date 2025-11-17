"""
VRPTW Data Loader Module
Loads and manages data from r101.csv for the Vehicle Routing Problem with Time Windows
"""
import pandas as pd
import numpy as np
from typing import Tuple, Dict


class VRPTWData:
    """Class to load and manage VRPTW data from CSV file"""
    
    def __init__(self, filepath: str):
        """
        Initialize VRPTW data loader
        
        Args:
            filepath: Path to the CSV file containing VRPTW data
        """
        self.filepath = filepath
        self.customers_df = None
        self.depot = None
        self.customers = None
        self.distance_matrix = None
        self.load_data()
        
    def load_data(self):
        """Load data from CSV file"""
        self.customers_df = pd.read_csv(self.filepath)
        
        # Depot is customer 0
        self.depot = self.customers_df[self.customers_df['NUMBER'] == 0].iloc[0]
        
        # Customers are all except depot (NUMBER > 0)
        self.customers = self.customers_df[self.customers_df['NUMBER'] > 0]
        
        # Calculate distance matrix
        self.distance_matrix = self._calculate_distance_matrix()
        
    def _calculate_distance_matrix(self) -> np.ndarray:
        """
        Calculate Euclidean distance matrix between all locations
        
        Returns:
            Distance matrix as numpy array
        """
        # Extract coordinates as numpy arrays for vectorized operations
        coords = self.customers_df[['XCOORD', 'YCOORD']].values
        n = len(coords)
        
        # Vectorized distance calculation
        # Expand dimensions for broadcasting
        coords_i = coords[:, np.newaxis, :]  # Shape: (n, 1, 2)
        coords_j = coords[np.newaxis, :, :]  # Shape: (1, n, 2)
        
        # Calculate squared differences and sum
        diff_squared = np.sum((coords_i - coords_j) ** 2, axis=2)
        
        # Take square root to get Euclidean distance
        distance_matrix = np.sqrt(diff_squared)
                    
        return distance_matrix
    
    def get_customer_data(self, customer_id: int) -> Dict:
        """
        Get data for a specific customer
        
        Args:
            customer_id: Customer number
            
        Returns:
            Dictionary with customer data
        """
        customer = self.customers_df[self.customers_df['NUMBER'] == customer_id].iloc[0]
        return {
            'number': int(customer['NUMBER']),
            'x': customer['XCOORD'],
            'y': customer['YCOORD'],
            'demand': customer['DEMAND'],
            'ready_time': customer['READY_TIME'],
            'due_date': customer['DUE_DATE'],
            'service_time': customer['SERVICE_TIME']
        }
    
    def get_distance(self, from_customer: int, to_customer: int) -> float:
        """
        Get distance between two customers
        
        Args:
            from_customer: Starting customer number
            to_customer: Ending customer number
            
        Returns:
            Distance between customers
        """
        return self.distance_matrix[from_customer, to_customer]
    
    def get_num_customers(self) -> int:
        """Get number of customers (excluding depot)"""
        return len(self.customers)
    
    def get_customer_ids(self) -> list:
        """Get list of customer IDs (excluding depot)"""
        return self.customers['NUMBER'].tolist()
