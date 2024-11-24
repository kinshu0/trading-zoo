import requests
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime
import heapq
from bases import event, Order, tradeRecord

class OrderBook:
    '''
    Order book for a single security
    is essentially two heaps (max heap of buy orders, min heap of sell orders)
    each game tick, users will add the orders to the order book and the orders will be matched with records showing which are fulfilled being returned to the caller
    '''
    def __init__(self):
        self.buyHeap = [] # max heap of buy orders
        self.sellHeap = [] # min heap of sell orders
        self.market_order = None  # Track the current market maker order
    
    def __str__(self) -> str:
        """
        Returns a string representation of the order book in format:
        <security id>  Bid: <price>(<amount>), .....
        Ask: <price>(<amount>), ...
        """
        # Get security name from any order (market maker or first order in heaps)
        security_id = ""
        if self.market_order:
            security_id = self.market_order.security
        elif self.buyHeap:
            security_id = self.buyHeap[0][1].security
        elif self.sellHeap:
            security_id = self.sellHeap[0][1].security
            
        # Format bids (buy orders) - need to negate prices as they're stored negatively
        bids = [f"{-price:.2f}({order.quantity})" for price, order in sorted(self.buyHeap)]
        bid_str = "Bid: " + ", ".join(bids) if bids else "Bid: -"
        
        # Format asks (sell orders)
        asks = [f"{price:.2f}({order.quantity})" for price, order in sorted(self.sellHeap)]
        ask_str = "Ask: " + ", ".join(asks) if asks else "Ask: -"
        
        return f"{security_id}  {bid_str}\n{ask_str}"
    
    def update_market_maker_order(self, security: str, current_price: float, timestamp: int):
        """
        Updates the market maker's sell order with the new price
        """
        # Remove old market maker order if it exists
        if self.market_order is not None:
            self.sellHeap = [(p, o) for p, o in self.sellHeap 
                            if o.id != "MARKET_MAKER"]
            heapq.heapify(self.sellHeap)
        
        # Create and add new market maker order
        self.market_order = Order.create_market_sell_order(security, current_price, timestamp)
        heapq.heappush(self.sellHeap, (self.market_order.price, self.market_order))
    
    def addOrder(self, order: Order):
        '''
        add an order to the order book from the agent
        '''
        if order.isBuy:
            heapq.heappush(self.buyHeap, (-order.price, order))
        else:
            heapq.heappush(self.sellHeap, (order.price, order))
    
    
    def fullfillOrders(self, tick: int):
        '''
        fullfills the orders from the orderbook, returns a list of trade records
        '''
        records= []
        
        # loop through the orderbook, fulfilling orders as much as possible
        while self.buyHeap and self.sellHeap and self.sellHeap[0][0] <= (-self.buyHeap[0][0]):
            subtractAmt = min(self.buyHeap[0][1].quantity, self.sellHeap[0][1].quantity)
            
            # create record of the transaction
            currRecord = tradeRecord(seller=self.sellHeap[0][1].id,
                                     buyer=self.buyHeap[0][1].id,
                                     security=self.sellHeap[0][1].security,
                                     price=self.sellHeap[0][0],
                                     quantity=subtractAmt,
                                     timestamp=tick)
            records.append(currRecord)
            
            
            # update the amount of the order
            self.buyHeap[0][1].quantity -= subtractAmt
            self.sellHeap[0][1].quantity -= subtractAmt
            
            # if the entire order has been fulfilled, remove it from the heap
            if self.buyHeap[0][1].quantity == 0:
                heapq.heappop(self.buyHeap)
            if self.sellHeap[0][1].quantity == 0:
                heapq.heappop(self.sellHeap)
    
    
                
        return records


class GameOrderBook:
    '''
    class that has all the order books for each of the securities
    each different security has its own  order book - maintains the heap invariant
    '''
    
    def __init__(self, securities: List[str]) -> None:
        self.orderBooks : Dict[str, OrderBook] = {security: OrderBook() for security in securities} # key = security name, value = order book
    
    def update_market_maker_orders(self, security_prices: Dict[str, float], timestamp: int) -> None:
        """
        Updates market maker orders for all securities with current prices
        
        Parameters:
            security_prices: Dictionary mapping security names to their current prices
            timestamp: Current game tick
        """
        for security, price in security_prices.items():
            self.orderBooks[security].update_market_maker_order(security, price, timestamp)
    
    def addOrder(self, orders: List[Order]) -> None:
        '''
        adds all the orders from the agents to their respective order books
        '''
        for order in orders:
            self.orderBooks[order.security].addOrder(order)
    
    def fullfillOrders(self, tick: int) -> Dict[str, List[tradeRecord]]:
        '''
        fullfills all the orders from the order books for all the securities
        '''
        records = {}
        
        for security, orderBook in self.orderBooks.items():
            records[security] = orderBook.fullfillOrders(tick)
        
        return records


