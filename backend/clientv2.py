import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List
import json
from model import Order

from agentsv2 import agents

load_dotenv()

@dataclass
class security_description:
    security_name : str
    quantity : int

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
    orderbook: dict
    positions: dict
    performance: dict
    trade_history: list
    tick: int

class TradingClient:
    def __init__(self, team_name: str, starting_balance: int):
        """
        Initialize a trading client for an animal team
        
        Args:
            team_name: Name of the animal team (e.g., 'penguins', 'monkeys', etc.)
            starting_balance: Starting balance of team
        """
        self.team_name = team_name.lower()
        
        # Get the appropriate team agents from the agents dictionary
        team_agents = agents[self.team_name]
        self.analyst = team_agents["analyst"]
        self.trader = team_agents["trader"]
        self.pr = team_agents["pr"]
        
        self.portfolio: List[security_description] = []
        self.balance_available = starting_balance
        self.daily_summary = None
        
    def get_quote(self, market_info: dict[str, MarketInfo], current_tick: int) -> List[Order]:
        """
        Generate quotes based on market information for multiple items
        
        Args:
            market_info: Dictionary mapping item names to their MarketInfo
            current_tick: Current tick number (1-15)
        
        Returns:
            List of Order objects with the recommended trades
        """
        # Format market data into the expected JSON structure
        market_data = {
            "tick": current_tick,
            "orderbook": {},
            "team_positions": {
                "asset_holdings": {item: 0 for item in market_info.keys()},  # Update with actual holdings
                "cash_balance": self.balance_available
            },
            "team_performance": {
                "total_pnl": 0,  # Update with actual PnL
                "daily_pnl": 0
            },
            "trade_history": []
        }
        
        # Add news at tick 1
        if current_tick == 1:
            market_data["news"] = "\n".join(f"{item}: {info.story}" for item, info in market_info.items())
        
        # Update orderbook and trade history from market info
        for item, info in market_info.items():
            market_data["orderbook"][item] = info.orderbook
            market_data["trade_history"].extend(info.trade_history)
        
        # test_msg = 'hello how are you'

        # Get analysis from analyst agent
        analysis_result = self.analyst.initiate_chat(
            self.trader,
            message=json.dumps(market_data),
            # message=test_msg,
            max_turns=1
        )
        
        # Parse analyst's JSON response
        analyst_response = json.loads(analysis_result.chat_history[1]['content'])
        
        # Get trader's response with order details
        trader_response = json.loads(analysis_result.chat_history[-1]['content'])
        
        # Generate PR summary
        pr_data = {
            "market_data": market_data,
            "analysis": analyst_response,
            "orders": trader_response
        }
        pr_result = self.pr.initiate_chat(
            message=json.dumps(pr_data),
            max_turns=1
        )
        
        # Store daily summary if it's the last tick
        if current_tick == 15:
            self.daily_summary = json.loads(pr_result.chat_history[1]['content'])["daily_summary"]
        
        # Convert trader's response into Order objects
        orders = []
        for order in trader_response["orders"]:
            orders.append(Order(
                security=order["asset"],
                price=float(order["price"]),
                quantity=int(order["quantity"]),
                isBuy=(order["side"].upper() == "BUY"),
                timestamp=current_tick
            ))
        
        return orders

    def get_name(self) -> str:
        """Return the team name"""
        return self.team_name
    
    def get_daily_summary(self) -> dict:
        """Return the PR agent's daily summary"""
        return self.daily_summary if self.daily_summary else {
            "headline": f"No summary available for {self.team_name}",
            "key_moves": [],
            "strategy_explanation": "",
            "performance_narrative": ""
        }


def create_sample_data():
    """Create sample market data for 3 ticks"""
    
    # Sample securities
    securities = ["BANANA", "FISH", "COCONUT"]
    
    # Sample news stories (only for tick 1)
    news_stories = {
        "BANANA": "The jungle monkeys discovered a hidden valley of golden bananas, but storm clouds gather overhead.",
        "FISH": "Arctic waters are teeming with silver fish, yet whispers of warm currents spread among the penguins.",
        "COCONUT": "Fox traders report increased coconut hoarding by squirrels, market tensions rise."
    }
    
    # Sample orderbook template
    def create_orderbook(base_price, tick_modifier):
        return {
            "bids": [
                {"price": base_price - 0.5 + tick_modifier, "quantity": 100, "team": "penguins"},
                {"price": base_price - 1.0 + tick_modifier, "quantity": 150, "team": "monkeys"},
                {"price": base_price - 1.5 + tick_modifier, "quantity": 200, "team": "foxes"}
            ],
            "asks": [
                {"price": base_price + 0.5 + tick_modifier, "quantity": 120, "team": "foxes"},
                {"price": base_price + 1.0 + tick_modifier, "quantity": 180, "team": "penguins"},
                {"price": base_price + 1.5 + tick_modifier, "quantity": 160, "team": "monkeys"}
            ]
        }
    
    # Base prices for each security
    base_prices = {
        "BANANA": 10.0,
        "FISH": 15.0,
        "COCONUT": 12.0
    }
    
    # Sample trade history template
    def create_trades(tick, base_price):
        return [
            {
                "tick": tick,
                "buyer": "penguins",
                "seller": "monkeys",
                "price": base_price + 0.2,
                "quantity": 50
            },
            {
                "tick": tick,
                "buyer": "foxes",
                "seller": "penguins",
                "price": base_price - 0.1,
                "quantity": 30
            }
        ]
    
    # Create sample data for each tick
    sample_data = {}
    for tick in range(1, 4):  # 3 ticks
        tick_data = {}
        for security in securities:
            tick_modifier = (tick - 1) * 0.2  # Small price movement each tick
            
            market_info = MarketInfo(
                story=news_stories[security] if tick == 1 else "",
                orderbook=create_orderbook(base_prices[security], tick_modifier),
                positions={"holdings": 100, "cash": 10000},
                performance={"total_pnl": 500 * tick, "daily_pnl": 100 * tick},
                trade_history=create_trades(tick, base_prices[security]),
                tick=tick
            )
            tick_data[security] = market_info
        sample_data[tick] = tick_data
    
    return sample_data

def test_trading_client():
    """Test the TradingClient with sample data"""
    
    # Create sample data
    sample_data = create_sample_data()
    
    # Create instances for each team
    clients = {
        team: TradingClient(team, starting_balance=100000)
        for team in ["penguins", "foxes", "monkeys"]
    }
    
    # Run simulation for 3 ticks
    results = {team: [] for team in clients.keys()}
    
    print("Starting trading simulation test...")
    print("=" * 50)
    
    for tick in range(1, 4):
        print(f"\nProcessing tick {tick}")
        print("-" * 30)
        
        for team_name, client in clients.items():
            print(f"\nTeam {team_name.upper()} processing...")
            
            # Get quotes from client
            try:
                orders = client.get_quote(sample_data[tick], tick)
                results[team_name].extend(orders)
                
                # Print orders
                print(f"Generated {len(orders)} orders:")
                for order in orders:
                    print(f"  {order.security}: {'BUY' if order.isBuy else 'SELL'} "
                          f"{order.quantity} @ {order.price}")
                
                # Print PR summary if it's the last tick
                if tick == 3:
                    summary = client.get_daily_summary()
                    print(f"\nDaily Summary for {team_name.upper()}:")
                    print(f"Headline: {summary['headline']}")
                    print("Key Moves:")
                    for move in summary['key_moves']:
                        print(f"  - {move}")
                    
            except Exception as e:
                print(f"Error processing team {team_name}: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Simulation test complete!")
    
    return results

if __name__ == "__main__":
    # Run the test
    results = test_trading_client()
    
    # Print final statistics
    print("\nFinal Order Statistics:")
    for team, orders in results.items():
        buy_orders = len([o for o in orders if o.isBuy])
        sell_orders = len([o for o in orders if not o.isBuy])
        print(f"\n{team.upper()}:")
        print(f"  Total Orders: {len(orders)}")
        print(f"  Buy Orders:  {buy_orders}")
        print(f"  Sell Orders: {sell_orders}")