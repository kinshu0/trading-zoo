import os
from dotenv import load_dotenv
load_dotenv()
from dataclasses import dataclass
from typing import List
from bases import security_details, MarketInfo, Order

from autogen import ConversableAgent
from dataclasses import dataclass
from typing import Dict, List
import time
import uuid

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

BASE_PROMPT = """You are participating in a whimsical asset trading simulation with the following mechanics:
- Each trading day consists of exactly 15 ticks
- News events are only provided at tick 1 of each day
- You receive orderbook, positions, performance, and trade history data each tick
- The ultimate goal is to maximize trading profits while maintaining team character"""

PENGUIN_IDENTITY = """You are part of the Penguin Trading Group, known for your methodical, conservative approach to trading. 
Like your Antarctic nature, you prefer steady, calculated moves over risky ventures. Your team values stability and thorough 
analysis, taking pride in your ability to weather market storms through careful position management. You communicate in a 
formal, precise manner, often using ice and weather-related metaphors."""

FOX_IDENTITY = """You are a member of the Fox Trading Collective, characterized by your clever and opportunistic trading style. 
Your team excels at spotting market inefficiencies and executing swift, precise trades. Like your vulpine nature, you are 
adaptable and quick to react to changing market conditions. You communicate with wit and cunning, often using predator-prey 
metaphors and demonstrating strategic thinking."""

MONKEY_IDENTITY = """You are part of the Monkey Trading Squad, known for your highly active and social trading approach. 
Your team thrives on market energy and momentum, often engaging in rapid trading when opportunities arise. Like your primate 
nature, you're curious and quick to explore new strategies, though sometimes prone to exciting swings. You communicate 
energetically, using tree and jungle metaphors, and maintain a playful yet intelligent tone."""

ANALYST_ROLE = """As the team's Analyst, your role is to process news and market data into actionable recommendations.

For each analysis cycle, you should:
1. Process news content for market impact (tick 1 only)
2. Analyze orderbook patterns and trade history
3. Consider team positions and performance
4. Generate trading recommendations

Rules to adhere to:
1. You can't buy more than your balance allows
2. You can't sell more than your current position
"""

TRADER_ROLE = """As the team's Trader, your role is to execute trading recommendations from the Analyst into order formats.
You must respond EXACTLY in this format with no other text:
ITEM: ACTION|PRICE|QUANTITY

For multiple items, put each order on a new line:
ICE: BUY|50|100
FISH: SELL|30|200

Only valid actions are BUY or SELL.
Price must be a number.
Quantity must be a whole number.
Return 'TERMINATE' when complete."""


agents = {
    "penguins": {
        "analyst": BASE_PROMPT + "\n" + PENGUIN_IDENTITY + "\n" + ANALYST_ROLE,
        "trader": TRADER_ROLE
    },
    "foxes": {
        "analyst": BASE_PROMPT + "\n" + FOX_IDENTITY + "\n" + ANALYST_ROLE,
        "trader": TRADER_ROLE
    },
    "monkeys": {
        "analyst": BASE_PROMPT + "\n" + MONKEY_IDENTITY + "\n" + ANALYST_ROLE,
        "trader": TRADER_ROLE
    }
}

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

        self.analyst = ConversableAgent(
            name=f"{team_name} Analyst",
            system_message=agents[team_name]["analyst"],
            llm_config={"config_list": config_list},
        )
        self.trader = ConversableAgent(
            name=f"{team_name} Trader",
            system_message=agents[team_name]["trader"],
            llm_config={"config_list": config_list},
        )

        # self.analyst = analyst
        # self.trader = trader
        self.portfolio : List[security_details] = [] 
        self.balance_available = starting_balance
    
    def get_portfolio_valuation(self):
        return sum([sec.price * sec.quantity for sec in self.portfolio]) + self.balance_available
        
    def get_quote(self, market_info: dict[str, MarketInfo], current_tick : int, balance, portfolio) -> List[Order]:
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
            analysis_request += f"Current free balance: {balance}\n"
            analysis_request += f"Current portfolio: {str(portfolio)}\n"
        
        # First get analysis from analyst agent
        analysis_result = self.trader.initiate_chat(
            self.analyst,
            message=analysis_request,
            max_turns=1
        )

        analyst_response = analysis_result.chat_history[1]['content']

        trader_result = self.analyst.initiate_chat(
            self.trader,
            message=analyst_response,
            max_turns=1
        )

        trader_response = trader_result.chat_history[1]['content']

        # analysis_result = self.analyst.initiate_chat(
        #     self.trader,
        #     message=analysis_request,
        #     max_turns=1
        # )
        
        # # Get the last message from analyst
        # analyst_response = analysis_result.chat_history[1]['content']
        
        # # Now have trader respond to the analyst's message
        # trader_response = analysis_result.chat_history[-1]['content']
        
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
    tc = TradingClient('penguins', starting_balance=100)

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

    orders = tc.get_quote(market_info, current_tick=1, portfolio=[], balance=100)
    for order in orders:
        print(order)


test()