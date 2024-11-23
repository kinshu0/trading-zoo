import requests
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import heapq

@dataclass
class event:
    tick_start : int
    event_description : str

@dataclass
class Order:
    id: str # who is making the order
    security: str # the security the order is for
    price: float # quote price (buy or sell)
    quantity: int # quantity of the order
    isBuy: bool # true if buy order, false if sell order
    timestamp: int # int of the tick the order was made

@dataclass
class tradeRecord:
    seller: str # who is selling
    buyer: str # who is buying
    security: str # the security the trade is for
    price: float # price at which the trade was made
    quantity: int # quantity of the trade
    timestamp: int # int of the tick the trade was made
    

class OrderBook:
    '''
    Order book for a single security
    is essentially two heaps (max heap of buy orders, min heap of sell orders)
    each game tick, users will add the orders to the order book and the orders will be matched with records showing which are fulfilled being returned to the caller
    '''
    def __init__(self):
        self.buyHeap = [] # max heap of buy orders
        self.sellHeap = [] # min heap of sell orders
    
    
    def addOrder(self, order: Order):
        '''
        add an order to the order book from the agent
        '''
        if order.isBuy:
            heapq.heappush(self.buyHeap, (-order.price, order))
        else:
            heapq.heappush(self.sellHeap, (order.price, order))
    
    
    def fullfillOrders(self, order: Order, tick: int):
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


