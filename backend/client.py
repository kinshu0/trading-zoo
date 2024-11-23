import os
from dotenv import load_dotenv
load_dotenv()

from autogen import ConversableAgent

from model import Order

config_list = [
    {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "api_key": os.environ.get("NEBIUS_API_KEY"),
        'base_url':"https://api.studio.nebius.ai/v1/"
    },
    {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
        "api_key": os.environ.get("NEBIUS_API_KEY"),
        'base_url':"https://api.studio.nebius.ai/v1/"
    }
]

from dataclasses import dataclass
from typing import Dict, List
import time
import uuid

@dataclass
class MarketInfo:
    news: str
    orderbook: str


agent = ConversableAgent(
    "chatbot",
    llm_config={"config_list": config_list},
    code_execution_config=False,  # Turn off code execution, by default it is off.
    function_map=None,  # No registered functions, by default it is None.
    human_input_mode="NEVER",  # Never ask for human input.
)

# Analyst agent that processes market information
analyst = ConversableAgent(
    name="Analyst",
    system_message="""You are a market analyst AI. Analyze the provided news and orderbook information to make trading recommendations.
    For each security, determine:
    1. Sentiment (bullish/bearish) based on news
    2. Price pressure based on orderbook
    3. Recommended action (buy/sell) and price
    Format your response as: SECURITY: ACTION|PRICE|QUANTITY
    Return 'TERMINATE' when analysis is complete.""",
    llm_config={"config_list": config_list},
)

# Trader agent that converts analysis into orders
trader = ConversableAgent(
    name="Trader",
    system_message="""You are a trading AI that converts analysis into order objects.
    Parse the analyst's recommendation and create appropriate orders.
    Format: SECURITY: ACTION|PRICE|QUANTITY
    Return 'TERMINATE' when orders are generated.""",
    llm_config={"config_list": config_list},
)

class TradingClient:
    def __init__(self, name: str):
        self.name = name
        self.analyst = analyst
        self.trader = trader
        
    def get_quote(self, market_info: dict[str, MarketInfo]) -> Order:
        """
        Generate a quote based on market information for multiple assets
        
        Args:
            market_info: Dictionary mapping security names to their MarketInfo
        
        Returns:
            Order object with the recommended trade
        """
        # Format market info for analyst
        analysis_request = ""
        for security, info in market_info.items():
            analysis_request += f"\nSecurity: {security}\n"
            analysis_request += f"News: {info.news}\n"
            analysis_request += f"Orderbook: {info.orderbook}\n"
        
        # Get analysis from analyst agent
        analysis_result = self.analyst.initiate_chat(
            self.trader,
            message=analysis_request
        )
        
        # Extract the last message from analyst (ignoring intermediate chat)
        analysis = [msg for msg in analysis_result if msg.get("role") == "assistant"][-1]["content"]
        
        # Have trader convert analysis to order
        order_result = self.trader.initiate_chat(
            self.analyst,
            message=f"Convert the following analysis to an order for {self.name}:\n{analysis}"
        )
        
        # Parse trader's response into Order object
        order_msg = [msg for msg in order_result if msg.get("role") == "assistant"][-1]["content"]
        security, details = order_msg.split(": ")
        action, price, quantity = details.split("|")
        
        return Order(
            id=f"{self.name}-{uuid.uuid4()}",
            security=security,
            price=float(price),
            quantity=int(quantity),
            isBuy=(action.lower() == "buy"),
            timestamp=int(time.time())
        )

    def get_name(self):
        return self.name
    

def test():

    tc = TradingClient('mammoth')

    market_info = {
        "BTC": MarketInfo(
            news="Bitcoin adoption increasing among institutional investors. Major bank announces crypto custody service.",
            orderbook="Bid: 50000(5), 49800(10)\nAsk: 50200(3), 50400(8)"
        ),
        "ETH": MarketInfo(
            news="Ethereum network congestion leading to high gas fees. New Layer 2 solution announced.",
            orderbook="Bid: 2800(15), 2780(25)\nAsk: 2820(10), 2840(20)"
        )
    }

    order = tc.get_quote(market_info)
    print(order)


test()