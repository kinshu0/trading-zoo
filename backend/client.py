import os
from dotenv import load_dotenv
load_dotenv()
from dataclasses import dataclass
from typing import List
from bases import security_details, MarketInfo, Order
import random

from autogen import ConversableAgent
from dataclasses import dataclass
from typing import Dict, List
import time
import uuid

config_list = [
    {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "api_key": os.environ.get("NEBIUS_API_KEY"),
        'base_url':"https://api.studio.nebius.ai/v1/"
    },
    # {
    #     "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-fast",
    #     "api_key": os.environ.get("NEBIUS_API_KEY"),
    #     'base_url':"https://api.studio.nebius.ai/v1/"
    # },
    # {
    #     "model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
    #     "api_key": os.environ.get("NEBIUS_API_KEY"),
    #     'base_url':"https://api.studio.nebius.ai/v1/"
    # },
]

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
            name=f"Base guy",
            system_message=f"You are a {team_name}, make the best commodity choices. Your answer should only be the name of the commodity.",
            llm_config={"config_list": config_list},
        )

        self.portfolio : List[security_details] = [] 
        self.balance_available = starting_balance
        self.valuation_history = []
    
    def get_portfolio_valuation(self):
        return sum([sec.price * sec.quantity for sec in self.portfolio]) + self.balance_available
        
    #def get_quote(self, market_info: dict[str, MarketInfo], current_tick : int, balance, portfolio) -> List[Order]:
    def get_quote(self, securities : list, portolio_securities : list, quotes, current_tick : int, current_balance : int) -> List[Order]:
        """
        Generate quotes based on market information for multiple items
        
        Args:
            market_info: Dictionary mapping item names to their MarketInfo
        
        Returns:
            List of Order objects with the recommended trades
        """
        # Format market info for analyst

        random.shuffle(securities)
        random.shuffle(portolio_securities)
        # print(securities)
        # print(portolio_securities)
        # print(current_tick)
        type_order = random.choice(['BUY', 'SELL'])

        if not portolio_securities or type_order == 'BUY':
            req = f"Choose your preferred commodity to buy as the animal you are. You can only choose from the following items: {', '.join(securities)}"
        elif type_order == 'SELL':
            req = f"Choose your preferred commodity to sell as the animal you are. You can only choose from the following items: {', '.join(portolio_securities)}"
        
        # First get analysis from analyst agent
        analysis_result = self.analyst.initiate_chat(
            self.analyst,
            message=req,
            max_turns=1
        )

        res = analysis_result.chat_history[2]['content'].upper()

        orders = []

        if (res not in securities and type_order == 'BUY') or (res not in portolio_securities and type_order == 'SELL') or (quotes.orderBooks[res].sellHeap[0][0] > current_balance):
            orders.append(Order(
                id='NONE',
                security=res,
                price=0,
                quantity=1,
                isBuy=True,
                timestamp=current_tick
            ))
        elif not portolio_securities or type_order == 'BUY':
            orders.append(Order(
                id=self.team_name,
                security=res,
                price=quotes.orderBooks[res].sellHeap[0][0],
                quantity=1,
                isBuy=True,
                timestamp=current_tick
            ))
        elif type_order == 'SELL':
            orders.append(Order(
                id=self.team_name,
                security=res,
                price=quotes.orderBooks[res].buyHeap[0][0],
                quantity=1,
                isBuy=False,
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

# test()