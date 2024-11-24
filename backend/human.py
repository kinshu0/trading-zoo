from typing import Dict, List
from model import Order

from client import security_details

class HumanClient:
    def __init__(self, team_name: str, starting_balance : int, state):
        self.team_name = 'hooman'

        self.portfolio : List[security_details] = [] 
        self.balance_available = starting_balance
        self.state = state
        self.valuation_history = []
    
    def get_portfolio_valuation(self):
        return sum([sec.price * sec.quantity for sec in self.portfolio]) + self.balance_available
        
    def get_quote(self, securities : list, portolio_securities : list, quotes, current_tick : int, current_balance : int) -> List[Order]:
        return self.state['orders']

    def get_name(self):
        return self.team_name