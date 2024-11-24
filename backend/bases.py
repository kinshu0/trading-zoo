from dataclasses import dataclass, field
from typing import List

@dataclass
class security_description:
    name : str
    story : str
    price : int

@dataclass
class security_details:
    security_name : str
    quantity : int
    price : int

@dataclass
class full_portfolio:
    portfolio : List[security_details]
    balance : int

@dataclass
class MarketInfo:
    story: str
    orderbook: str

@dataclass
class event:
    tick_start : int
    event_description : str
    security_affected : str
    event_severity : int

@dataclass(order=True)
class Order:
    id: str = field(compare=False) # who is making the order
    security: str = field(compare=False) # the security the order is for
    price: float = field(compare=False) # quote price (buy or sell)
    quantity: int = field(compare=False)  # quantity of the order
    isBuy: bool = field(compare=False) # true if buy order, false if sell order
    timestamp: int = field(compare=True) # int of the tick the order was made

    @classmethod
    def create_market_sell_order(cls, security: str, price: float, timestamp: int):
        """Creates a market maker sell order"""
        return cls(
            id="MARKET_MAKER",
            security=security,
            price=price * 1.00,  # 5% premium for market maker orders
            quantity=1000,  # Large quantity available
            isBuy=False,
            timestamp=timestamp
        )

@dataclass
class tradeRecord:
    seller: str # who is selling
    buyer: str # who is buying
    security: str # the security the trade is for
    price: float # price at which the trade was made
    quantity: int # quantity of the trade
    timestamp: int # int of the tick the trade was made

@dataclass
class MarketEvent:
    """Represents a market event that impacts security prices"""
    name: str
    time: int
    severity: float  # -3 to +3
    affected_volatilities: List[str]
    
    def __str__(self):
        direction = "positive" if self.severity > 0 else "negative"
        return f"{self.name} ({direction} impact)"