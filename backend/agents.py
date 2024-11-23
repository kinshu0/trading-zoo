import autogen
import os
from dotenv import load_dotenv

load_dotenv()

from typing import Dict, List

# Configuration for the agents
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

# Assistant configurations
assistant_config = {
    "config_list": config_list,
    "seed": 42,
    "temperature": 0.7,
}

def create_agents():
    """Create and return all trading agents"""
    
    # Create the agent configurations
    penguin_analyst_config = {
        "name": "penguin_analyst",
        "system_message": """You are an analyst for the Penguin trading team. You specialize in analyzing market conditions
        for ice and cold-weather related assets. You have a strong preference for ice and believe in its long-term value.
        Your role is to analyze news and market conditions and advise your trader. You can request market data using the
        trading_client.get_market_data() function."""
    }

    penguin_trader_config = {
        "name": "penguin_trader",
        "system_message": """You are a trader for the Penguin trading team. You execute trades based on your analyst's
        recommendations and market conditions. You can submit quotes using the trading_client.submit_quote() function
        with your name ('penguin_trader') as the agent_name."""
    }

    monkey_analyst_config = {
        "name": "monkey_analyst",
        "system_message": """You are an analyst for the Monkey trading team. You specialize in analyzing market conditions
        for fruit-based assets, especially bananas. You have a strong preference for bananas and believe in their value.
        Your role is to analyze news and market conditions and advise your trader. You can request market data using the
        trading_client.get_market_data() function."""
    }

    monkey_trader_config = {
        "name": "monkey_trader",
        "system_message": """You are a trader for the Monkey trading team. You execute trades based on your analyst's
        recommendations and market conditions. You can submit quotes using the trading_client.submit_quote() function
        with your name ('monkey_trader') as the agent_name."""
    }

    fox_analyst_config = {
        "name": "fox_analyst",
        "system_message": """You are an analyst for the Fox trading team. You specialize in analyzing market conditions
        for all types of assets with a focus on arbitrage opportunities. You're particularly interested in fish.
        Your role is to analyze news and market conditions and advise your trader. You can request market data using the
        trading_client.get_market_data() function."""
    }

    fox_trader_config = {
        "name": "fox_trader",
        "system_message": """You are a trader for the Fox trading team. You execute trades based on your analyst's
        recommendations and market conditions. You can submit quotes using the trading_client.submit_quote() function
        with your name ('fox_trader') as the agent_name."""
    }

    # Create the agents
    agents = {
        "penguin_analyst": autogen.AssistantAgent(**penguin_analyst_config),
        "penguin_trader": autogen.AssistantAgent(**penguin_trader_config),
        "monkey_analyst": autogen.AssistantAgent(**monkey_analyst_config),
        "monkey_trader": autogen.AssistantAgent(**monkey_trader_config),
        "fox_analyst": autogen.AssistantAgent(**fox_analyst_config),
        "fox_trader": autogen.AssistantAgent(**fox_trader_config),
    }

    # Create a human proxy agent for orchestration
    agents["user_proxy"] = autogen.UserProxyAgent(
        name="user_proxy",
        system_message="You are coordinating the trading simulation.",
        human_input_mode="NEVER"
    )

    return agents