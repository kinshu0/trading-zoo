import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

class TradingClient:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url

    def submit_quote(
        self,
        agent_name: str,
        asset: str,
        bid: Optional[float] = None,
        ask: Optional[float] = None,
        quantity: int = 1
    ) -> Dict[str, Any]:
        """Submit a quote to the trading server"""
        response = requests.post(
            f"{self.base_url}/quote",
            json={
                "agent_name": agent_name,
                "asset": asset,
                "bid": bid,
                "ask": ask,
                "quantity": quantity
            }
        )
        response.raise_for_status()
        return response.json()

    def match_trades(self) -> Dict[str, Any]:
        """Trigger trade matching on the server"""
        response = requests.post(f"{self.base_url}/match_trades")
        response.raise_for_status()
        return response.json()

    def get_market_data(self) -> Dict[str, Any]:
        """Get current market data"""
        response = requests.get(f"{self.base_url}/market_data")
        response.raise_for_status()
        return response.json()