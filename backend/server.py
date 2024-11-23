from flask import Flask, request, jsonify
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
import threading

app = Flask(__name__)

# Data Models
@dataclass
class Asset:
    name: str
    total_quantity: int
    current_price: float

@dataclass
class Trade:
    buyer: str
    seller: str
    asset: str
    quantity: int
    price: float
    timestamp: datetime

@dataclass
class Quote:
    asset: str
    bid: float
    ask: float
    party: str
    quantity: int

# Global state with thread-safe locks
class TradingState:
    def __init__(self):
        self.lock = threading.Lock()
        self.assets = {
            "ICE": Asset("ICE", 1000, 10.0),
            "BANANA": Asset("BANANA", 1000, 5.0),
            "FISH": Asset("FISH", 1000, 8.0)
        }
        self.order_book: Dict[str, List[Quote]] = {
            "ICE": [],
            "BANANA": [],
            "FISH": []
        }

state = TradingState()

@app.route('/quote', methods=['POST'])
def submit_quote():
    data = request.json
    agent_name = data.get('agent_name')
    asset = data.get('asset')
    bid = data.get('bid')
    ask = data.get('ask')
    quantity = data.get('quantity', 1)

    if not asset or (bid is None and ask is None):
        return jsonify({"error": "Invalid quote parameters"}), 400

    with state.lock:
        if asset not in state.order_book:
            return jsonify({"error": "Invalid asset"}), 400
        
        quote = Quote(
            asset=asset,
            bid=bid,
            ask=ask,
            party=agent_name,
            quantity=quantity
        )
        state.order_book[asset].append(quote)
        
    return jsonify({
        "message": f"Quote submitted for {asset}: bid={bid}, ask={ask}, quantity={quantity}"
    })

@app.route('/match_trades', methods=['POST'])
def match_trades():
    trades = []
    with state.lock:
        for asset in state.order_book:
            quotes = state.order_book[asset]
            for i, buy_quote in enumerate(quotes):
                if buy_quote.bid is None:
                    continue
                for j, sell_quote in enumerate(quotes):
                    if i != j and sell_quote.ask is not None and buy_quote.bid >= sell_quote.ask:
                        trade = Trade(
                            buyer=buy_quote.party,
                            seller=sell_quote.party,
                            asset=asset,
                            quantity=min(buy_quote.quantity, sell_quote.quantity),
                            price=(buy_quote.bid + sell_quote.ask) / 2,
                            timestamp=datetime.now()
                        )
                        trades.append(trade)
                        # Update asset price
                        state.assets[asset].current_price = trade.price
        
        # Clear matched orders
        for asset in state.order_book:
            state.order_book[asset] = []

    return jsonify({
        "trades": [
            {
                "buyer": t.buyer,
                "seller": t.seller,
                "asset": t.asset,
                "quantity": t.quantity,
                "price": t.price,
                "timestamp": t.timestamp.isoformat()
            }
            for t in trades
        ]
    })

@app.route('/market_data', methods=['GET'])
def get_market_data():
    with state.lock:
        return jsonify({
            "assets": {
                name: {
                    "name": asset.name,
                    "total_quantity": asset.total_quantity,
                    "current_price": asset.current_price
                }
                for name, asset in state.assets.items()
            },
            "order_book": {
                asset: [
                    {
                        "bid": q.bid,
                        "ask": q.ask,
                        "party": q.party,
                        "quantity": q.quantity
                    }
                    for q in quotes
                ]
                for asset, quotes in state.order_book.items()
            }
        })

if __name__ == '__main__':
    app.run(port=5000)