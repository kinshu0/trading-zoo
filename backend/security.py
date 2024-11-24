from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
import random
from bases import MarketEvent

def generate_random_event() -> MarketEvent:
    """Generates a random market event"""
    events = [
        ("Tech Breakthrough", 0.5, 3.0, ["volatile", "medium"]),
        ("Market Crash", -2.0, -3.0, ["calm", "medium", "volatile"]),
        ("Regulatory Changes", -1.0, 1.0, ["medium", "volatile"]),
        ("Natural Disaster", -2.0, -1.0, ["calm", "medium"]),
        ("Political Upheaval", -1.5, 1.5, ["volatile"]),
        ("Economic Report", -1.0, 1.0, ["calm", "medium"]),
    ]
    
    name, sev_min, sev_max, affected = random.choice(events)
    return MarketEvent(
        name=name,
        time=0,  # Will be set when event occurs
        severity=random.uniform(sev_min, sev_max),
        affected_volatilities=affected
    )

class security_manager:
    '''
    class that encapsulates the actions of a security, with ability to generate the next price
    '''
    def __init__(self, name: str, volatility: str, start : int):
        '''
        volatility can be "calm", "medium", "volatile", this affects how dramatic the price changes are
        Calmer stocks have higher drift and more resistance to events
        '''
        self.name = name
        self.volatility = volatility
        self.volatility_levels = {
            "calm": 0.01,      
            "medium": 0.08,    
            "volatile": 0.15   
        }
        self.drift_levels = {
            "calm": 0.005,     
            "medium": 0.0005,  
            "volatile": 0.0    # Changed from negative to neutral drift
        }
        self.event_susceptibility = {
            "calm": 0.2,      
            "medium": 1.0,    
            "volatile": 2.5   
        }
        self.prices = [start]
        self.initial_price = 1.0  # Store initial price for mean reversion
        
    def generateNextPrice(self, severityFactor: float = 0.0):
        '''
        generates the next price of the security
        '''
        volatility_factor = self.volatility_levels[self.volatility]
        drift = self.drift_levels[self.volatility]
        current_price = self.prices[-1]
        
        # Modified random movement based on volatility type
        if self.volatility == "volatile":
            # Add mean reversion for volatile stocks when price is too low
            if current_price < self.initial_price * 0.5:
                # Strong upward bias when price is very low
                recovery_drift = 0.002 * (self.initial_price / current_price)
                price_change = (random.uniform(-0.8, 1.5) * volatility_factor) + recovery_drift
            else:
                # Normal volatile behavior
                price_change = (random.uniform(-1.0, 1.0) * volatility_factor) + drift
        elif self.volatility == "medium":
            price_change = (random.uniform(-0.8, 1) * volatility_factor) + drift
        else:  # calm
            price_change = (random.uniform(-0.3, 0.4) * volatility_factor) + drift
        
        # Calculate base price after normal movement
        new_price = current_price * (1 + price_change)
        
        # Add news impact as a direct price jump, scaled by event susceptibility
        if severityFactor != 0:
            event_scale = self.event_susceptibility[self.volatility]
            jump_magnitude = (severityFactor / 3) * (current_price * 0.8) * event_scale
            new_price += jump_magnitude
        
        # Ensure price doesn't get too close to zero

        actual_new_price = max(0.1, new_price)
        self.prices.append(actual_new_price)

        return actual_new_price
    

def test_securities(num_iterations: int = 100, event_probability: float = 0.03):
    """
    Creates and plots securities with different volatility levels and random events
    
    Parameters:
        num_iterations: Number of time steps to simulate
        event_probability: Probability of an event occurring at each time step
    """
    securities = [
        security_manager("Calm Stock", "calm"),
        security_manager("Medium Stock", "medium"),
        security_manager("Volatile Stock", "volatile")
    ]
    
    # Track events for plotting
    events: List[MarketEvent] = []
    
    # Generate prices for each security
    for t in range(num_iterations):
        # Randomly generate events
        if random.random() < event_probability:
            event = generate_random_event()
            event.time = t
            events.append(event)
            
            # Apply event effects to relevant securities
            for sec in securities:
                if sec.volatility in event.affected_volatilities:
                    sec.generateNextPrice(event.severity)
                else:
                    sec.generateNextPrice()
        else:
            # Normal price generation
            for sec in securities:
                sec.generateNextPrice()
    
    # Plot the results
    plt.figure(figsize=(15, 8))
    
    # Plot security prices
    for sec in securities:
        plt.plot(sec.prices, label=f"{sec.name} ({sec.volatility})")
    
    # Add event markers
    for event in events:
        plt.axvline(x=event.time, color='gray', linestyle='--', alpha=0.5)
        # Add event label
        plt.text(event.time, plt.ylim()[1], str(event), 
                rotation=90, verticalalignment='bottom')
    
    plt.title("Security Price Movements with Market Events")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    
    # Adjust layout to prevent text cutoff
    plt.tight_layout()
    plt.show()

# Example usage:
if __name__ == "__main__":
    test_securities(num_iterations=200)  # Increased iterations to see more events





