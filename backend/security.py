from typing import Optional, Dict, List, Any
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
import random


class security:
    '''
    class that encapsulates the actions of a security, with ability to generate the next price
    '''
    def __init__(self, name: str, volatility: str):
        '''
        volatility can be "calm", "medium", "volatile", this affects how dramatic the price changes are
        '''
        self.name = name
        self.volatility = volatility
        self.volatility_levels = {
            "calm": 0.02,      # Increased from previous values
            "medium": 0.04,    # Increased from previous values
            "volatile": 0.08   # Increased from previous values
        }
        self.drift = 0.0002   # Slightly increased upward bias
        self.prices = [1.0]   # Starting price
        
    def generateNextPrice(self):
        '''
        generates the next price of the security
        '''
        volatility_factor = self.volatility_levels[self.volatility]
        # Modified to create more variability
        price_change = (random.uniform(-0.8, 1) * volatility_factor) + self.drift
        new_price = self.prices[-1] * (1 + price_change)
        self.prices.append(max(0.01, new_price))
    

def test_securities(num_iterations: int = 100):
    """
    Creates and plots securities with different volatility levels
    """
    securities = [
        security("Calm Stock", "calm"),
        security("Medium Stock", "medium"),
        security("Volatile Stock", "volatile")
    ]
    
    # Generate prices for each security
    for _ in range(num_iterations):
        for sec in securities:
            sec.generateNextPrice()
    
    # Plot the results
    plt.figure(figsize=(12, 6))
    for sec in securities:
        plt.plot(sec.prices, label=f"{sec.name} ({sec.volatility})")
    
    plt.title("Security Price Movements by Volatility")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage:
if __name__ == "__main__":
    test_securities()





