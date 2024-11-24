from flask import Flask, Response
from client import TradingClient
from model import GameOrderBook
from dataclasses import dataclass
from security import security_manager 
from bases import security_description, security_details, event, MarketInfo, full_portfolio
import random
from flask_cors import CORS
from model import Order
import json
from human import HumanClient
import time
human_state = {
    'orders': []
}


app = Flask(__name__)
CORS(app, 
     resources={r"/*": {
         "origins": ["http://localhost:3000"],
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"],
         "supports_credentials": True  # Add this line
     }})
game_started = False
current_tick = 0
event_timeline = []
news_feed = []
securities_descriptions = []
completed_transactions = []
pending_transactions = []
lastEvents = []

clients = dict()

def create_event_timeline():
    # have a timeline generated
    events = [
        ("A massive ice storm hits the northern regions, increasing ice production", 2, ["ICE"]),
        # ("Devastating fish disease outbreak decimates populations", -1, ["FISH"]), 
        ("Monkeys discover revolutionary banana harvesting technique", 2, ["BANANA"]),
        ("Category 5 tropical storm ravages pineapple farms", -1, ["PINEAPPLE"]),
        # ("Minor shift in penguin migration affects fishing", -1, ["FISH", "ICE"]),
        ("Breakthrough preservation technology for tropical fruits", 2, ["BANANA", "PINEAPPLE"]),
        # ("Coastal erosion impacts pebble quality", -1, ["PEBBLES"]),
        ("Major volcanic eruption creates rare pebble deposits", 2, ["PEBBLES"]), 
        ("Warming oceans disrupt fish breeding", -1, ["FISH"]),
        ("Record cold temperatures boost ice production", 2, ["ICE"]),
        # ("Short-term banana worker strike", -1, ["BANANA"]),
        ("New pebble enhancement process shows promise", 1, ["PEBBLES"]),
        ("Massive fish school migration discovery", 3, ["FISH"]),
        # ("Severe drought threatens fruit harvests", -1, ["BANANA", "PINEAPPLE"]),
        ("Revolutionary ice harvesting method unveiled", 3, ["ICE"]),
        ("Arctic blast creates ideal ice conditions", 2, ["ICE"]),
        ("Toxic algae bloom threatens fish stocks", -1, ["FISH"]),
        ("Genetic breakthrough improves banana yield", 2, ["BANANA"]),
        # ("Pest infestation damages pineapple crops", -1, ["PINEAPPLE"]),
        # ("Changing ocean currents impact marine life", -1, ["FISH", "ICE"]),
        ("AI-powered fruit ripening system developed", 3, ["BANANA", "PINEAPPLE"]),
        ("Construction boom depletes pebble supplies", -1, ["PEBBLES"]),
        ("Ancient premium pebble deposit discovered", 2, ["PEBBLES"]),
        ("Overfishing crisis in key regions", -1, ["FISH"]),
        ("New ice storage technology extends shelf life", 1, ["ICE"]),
        ("Disease affects banana plantation yields", -1, ["BANANA"]),
        ("International demand for premium pebbles soars", 2, ["PEBBLES"]),
        ("Sustainable fishing practices boost populations", 1, ["FISH"]),
        ("Extended dry season impacts fruit production", -2, ["BANANA", "PINEAPPLE"]),
        ("Polar vortex creates ice surplus", 2, ["ICE"])
    ]
    
    return events

@app.route("/register/<string:name>")
def register_client(name):
    global game_started, clients

    if not game_started:
        clients[name] = TradingClient(name = name, starting_balance = 100)

        return name
    else:
        return ("Game has already started, unable to register new clients.", 403)

@app.route("/clients")
def get_clients():
    return {client.team_name : full_portfolio(portfolio=client.portfolio, balance=client.balance_available) for client in clients}

@app.route("/client/<string:name>")
def get_client_by_name(name):
    return clients[name].get_name()

@app.route("/securities")
def get_securities():
    return {sec.name : sec.price for sec in securities_descriptions}

@app.route("/start")
def start():
    global game_started, event_timeline, quotes, securities_sequences, securities_descriptions, clients

    clients = [
            TradingClient(team_name = "penguins", starting_balance = 100),
            TradingClient(team_name = "foxes", starting_balance = 100),
            TradingClient(team_name = "monkeys", starting_balance = 100),
            TradingClient(team_name = "iguanas", starting_balance = 100),
            HumanClient(team_name = "Hooman", starting_balance = 100, state=human_state)
            ]


    event_timeline = create_event_timeline()

    securities_descriptions = [
        security_description(name = "ICE",
         story = "ice commodity",
         price = 3
         ),
        security_description(name = "FISH",
         story = "fish commodity",
         price = 3
         ),
        security_description(name = "BANANA",
         story = "banana commodity",
         price = 3
         ),
        security_description(name = "PEBBLE",
         story = "pebble commodity",
         price = 3
         ),
        security_description(name = "PINEAPPLES",
         story = "pineapple commodity",
         price = 3
         )

    ]

    securities_sequences = []

    for security in securities_descriptions:
        securities_sequences.append(security_manager(name = security.name, volatility=random.choice(["calm", "medium", "volatile"]), start=security.price))

    quotes = GameOrderBook(securities = [security.name for security in securities_descriptions])

    game_started = True

    return "Game started!"

@app.route("/valuation/<name>")
def get_valuation(name):
    global clients

    if not clients:
        return ("Not found", 404)
    
    for client in clients:
        if client.team_name == name:
            return f"{client.get_portfolio_valuation()}"

@app.route("/completed_transactions")
def get_completed_transcations():
    return completed_transactions

@app.route("/valuation_history")
def get_valuation_history():
    return {client.team_name : client.valuation_history for client in clients}

@app.route("/pending_transactions")
def get_pending_transactions():
    return pending_transactions

@app.route("/isEvent")
def is_event():
    return lastEvents

@app.route("/tick")
def tick():
    global game_started, current_tick, clients, event_timeline, news_feed, securities_descriptions, quotes, securities_sequences, completed_transactions, pending_transactions, lastEvents

    if not game_started:
        return ("Game has not started", 403)
    
    if current_tick == 0:
        current_tick = 1
        return "1"
    time.sleep(5)


    # Add sleep to slow down ticks  # 5 second delay between ticks

    current_market_info = dict()

    print(securities_descriptions)

    quotes.update_market_maker_orders(security_prices = {security.name : security.price for security in securities_descriptions}, timestamp=current_tick)

    #print('-' * 200, 'START')

    for security in securities_descriptions:

        current_market_info[security.name] = MarketInfo(story = security.story,
                                                   orderbook = quotes.orderBooks[security.name].__str__())

        #print(security.name, quotes.orderBooks[security.name].__str__())

    #for cc in clients:
        #print(cc.team_name, cc.portfolio, cc.balance_available)

    #print('-' * 200)


    for client in clients:
        #order = client.get_quote(market_info = current_market_info, current_tick=current_tick, balance=client.balance_available, portfolio=client.portfolio)
        order = client.get_quote(
        securities=[sec.name for sec in securities_descriptions], 
        portolio_securities=[sec.security_name for sec in client.portfolio if sec.quantity > 0],
        quotes=quotes,
        current_tick=current_tick,
        current_balance=client.balance_available)

        quotes.addOrder([o for o in order if o.id != "NONE"])

    human_state['orders'] = []

    resolved = quotes.fullfillOrders(tick = current_tick)

    for r in resolved.values():
        completed_transactions += r

    pending_transactions = []

    for book in quotes.orderBooks.values():
        for i in book.buyHeap:
            if i[1].id != "MARKET_MAKER":
                pending_transactions.append(i[1])

        for i in book.sellHeap:
            if i[1].id != "MARKET_MAKER":
                pending_transactions.append(i[1])


    print('COMPLETED TRANSACTIONS:', completed_transactions)
    print('PENDING TRANSACTIONS', pending_transactions)

    #for security in securities_descriptions:
        #print(security.name, quotes.orderBooks[security.name].__str__())
    #print(resolved)

    #print('-' * 200, 'END')

    for resolved_security in resolved:
        for record in resolved[resolved_security]:
            for client in clients:
                if client.team_name == record.seller:
                    client.balance_available += record.quantity * record.price
                    for held_security in client.portfolio:
                        if held_security.security_name == resolved_security:
                            held_security.quantity -= record.quantity

                elif client.team_name == record.buyer:
                    client.balance_available -= record.quantity * record.price
                    resolved_b = False
                    for held_security in client.portfolio:
                        if held_security.security_name == resolved_security:
                            held_security.quantity += record.quantity
                            resolved_b = True

                    if not resolved_b:
                        client.portfolio.append(security_details(security_name=resolved_security, quantity=record.quantity, price=record.price))
                            

    current_tick += 1
    
    severity = 0

    affected = []
    sev = 0
    event_desc = ""

    if (random.random() < 0.3 and len(event_timeline) > 0):  # 1/5 chance
        random_event_index = random.randint(0, len(event_timeline)-1)
        event_desc, sev, affected = event_timeline.pop(random_event_index)
        severity = sev
        lastEvents.append(event_desc)

    for security in securities_descriptions:
        for security_seq_obj in securities_sequences:
            if security_seq_obj.name == security.name:
                
                if security.name in affected:
                    security.price = security_seq_obj.generateNextPrice(severity)
                else:
                    security.price = security_seq_obj.generateNextPrice(0)

                for client in clients:
                    for detail in client.portfolio:
                        if detail.security_name == security.name:
                            detail.price = security.price

    for client in clients:
        client.valuation_history.append(client.get_portfolio_valuation())

    return f"{current_tick}"

'''
sample call: http://127.0.0.1:5000/add_order/hooman/ICE/1.0/100/True
'''

@app.route("/add_order/<string:team_name>/<string:security>/<float:price>/<int:quantity>/<string:isBuy>")
def add_order(team_name, security, price, quantity, isBuy):
    isBuy = True if isBuy == "True" else False
    o = Order(
        id=team_name,
        security=security,
        price=price,
        quantity=quantity,
        isBuy=isBuy,
        timestamp=current_tick
    )

    human_state['orders'].append(o)

    return "OK"

@app.route("/")
def root():
    return "OK"


app.run(port=5000)