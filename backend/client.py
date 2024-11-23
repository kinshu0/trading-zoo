import os
from dotenv import load_dotenv
load_dotenv()
from dataclasses import dataclass
from typing import List

from autogen import ConversableAgent
from dataclasses import dataclass
from typing import Dict, List
import time
import uuid
from model import Order

@dataclass
class security_description:
    security_name : str
    quantity : int
    price : int

config_list = [
    {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
        "api_key": os.environ.get("NEBIUS_API_KEY"),
        'base_url':"https://api.studio.nebius.ai/v1/"
    },
    {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "api_key": os.environ.get("NEBIUS_API_KEY"),
        'base_url':"https://api.studio.nebius.ai/v1/"
    }
]

@dataclass
class MarketInfo:
    story: str
    orderbook: str

# Analyst agent that solves riddles and analyzes market information
analyst = ConversableAgent(
    name="Wise Owl Analyst",
    system_message="""You are a wise owl market analyst in a whimsical trading game. 
    Your job is to decipher the hidden meanings in story riddles and analyze the orderbook 
    to make trading recommendations for your animal team.

    For each item, you should:
    1. Decode the story riddle to understand its impact on supply and demand
    2. Analyze the orderbook patterns
    3. Make a clever trading recommendation
    
    Format your response as: ITEM: ACTION|PRICE|QUANTITY
    Include a brief explanation of how you decoded the riddle!
    
    Return 'TERMINATE' when your analysis is complete.""",
    llm_config={"config_list": config_list},
)

# Trader agent that converts analysis into orders with strict formatting
trader = ConversableAgent(
    name="Deal-Making Agent",
    system_message="""You are a trading agent that converts analysis into order formats.
    You must respond EXACTLY in this format with no other text:
    ITEM: ACTION|PRICE|QUANTITY
    
    For multiple items, put each order on a new line:
    ICE: BUY|50|100
    FISH: SELL|30|200
    
    Only valid actions are BUY or SELL.
    Price must be a number.
    Quantity must be a whole number.
    Return 'TERMINATE' when complete.""",
    llm_config={"config_list": config_list},
)

class TradingClient:
    def __init__(self, team_name: str, starting_balance : int):
        """
        Initialize a trading client for an animal team
        
        Args:
            team_name: Name of the animal team (e.g., 'penguins', 'monkeys', etc.)
            starting_balance: Starting balance of team
        """
        self.team_name = team_name
        self.analyst = analyst
        self.trader = trader
        self.portfolio : List[security_description] = [] 
        self.balance_available = starting_balance
    
    def get_portfolio_valuation(self):
        return sum([sec.price * sec.quantity for sec in self.portfolio]) + self.balance_available
        
    def get_quote(self, market_info: dict[str, MarketInfo], current_tick : int) -> List[Order]:
        """
        Generate quotes based on market information for multiple items
        
        Args:
            market_info: Dictionary mapping item names to their MarketInfo
        
        Returns:
            List of Order objects with the recommended trades
        """
        # Format market info for analyst
        analysis_request = f"\nYou are advising Team {self.team_name}!\n"
        for item, info in market_info.items():
            analysis_request += f"\nItem: {item}\n"
            analysis_request += f"Story Riddle: {info.story}\n"
            analysis_request += f"Current State of Orderbook\n: {info.orderbook}\n"
        
        # First get analysis from analyst agent
        analysis_result = self.analyst.initiate_chat(
            self.trader,
            message=analysis_request,
            max_turns=1
        )
        
        # Get the last message from analyst
        analyst_response = analysis_result.chat_history[1]['content']
        
        # Now have trader respond to the analyst's message
        trader_response = analysis_result.chat_history[-1]['content']
        
        # Parse multiple orders from trader's response
        orders = []
        for order_line in trader_response.strip().split('\n'):
            if order_line and not order_line.upper() == 'TERMINATE':
                item, details = order_line.split(": ")
                action, price, quantity = details.split("|")
                
                orders.append(Order(
                    #id=f"{self.team_name}-{uuid.uuid4()}",
                    id=f"{self.team_name}",
                    security=item,
                    price=float(price),
                    quantity=int(quantity),
                    isBuy=(action.upper() == "BUY"),
                    timestamp=current_tick
                ))
        
        return orders

    def get_name(self):
        return self.team_name

def test():
    tc = TradingClient('penguins')

    market_info = {
        "ICE": MarketInfo(
            story="The sun's rays grow stronger each day, and whispers spread through the market of a great heat wave approaching. The cloud shepherds have been seen guiding their flocks far to the north, leaving the southern markets exposed to the sun's fierce embrace.",
            orderbook="Bid: 50(100), 48(200)\nAsk: 52(80), 54(150)"
        ),
        "FISH": MarketInfo(
            story="A mysterious current has shifted in the deep waters, bringing schools of silver-scaled visitors to unusual waters. The wise seals speak of a great migration that happens once every blue moon, but the local fishing fleets seem oddly quiet about their recent catches.",
            orderbook="Bid: 30(300), 29(500)\nAsk: 31(200), 32(400)"
        )
    }

    orders = tc.get_quote(market_info)
    for order in orders:
        print(order)
