from flask import Flask, Response 
from client import TradingClient
from model import GameOrderBook
from dataclasses import dataclass
from security import security_manager 
from bases import security_description, security_details, event, MarketInfo, full_portfolio
import random

app = Flask(__name__)

game_started = False
current_tick = 0
event_timeline = []
news_feed = []
securities_descriptions = []
completed_transactions = []
pending_transactions = []

clients = dict()

def create_event_timeline():
    # have a timeline generated
    return [event(tick_start = 0, event_description = "event0", security_affected="FISH", event_severity=-1),
            event(tick_start = 25, event_description = "event1", security_affected="ICE", event_severity=3),
            # ...
            ]

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
            ]

    event_timeline = create_event_timeline()

    securities_descriptions = [
        security_description(name = "ICE",
         story = "The sun's rays grow stronger each day, and whispers spread through the market of a great heat wave approaching. The cloud shepherds have been seen guiding their flocks far to the north, leaving the southern markets exposed to the sun's fierce embrace.",
         price = 1
         ),


        security_description(name = "FISH",
         story = "A mysterious current has shifted in the deep waters, bringing schools of silver-scaled visitors to unusual waters. The wise seals speak of a great migration that happens once every blue moon, but the local fishing fleets seem oddly quiet about their recent catches.",
         price = 1
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

@app.route("/pending_transactions")
def get_pending_transactions():
    return pending_transactions

@app.route("/tick")
def tick():
    global game_started, current_tick, clients, event_timeline, news_feed, securities_descriptions, quotes, securities_sequences, completed_transactions, pending_transactions

    if not game_started:
        return ("Game has not started", 403)

    current_market_info = dict()

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
        order = client.get_quote(market_info = current_market_info, current_tick=current_tick, balance=client.balance_available, portfolio=client.portfolio)
        quotes.addOrder([o for o in order if o.id != "NONE"])

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

    for security in securities_descriptions:
        for security_seq_obj in securities_sequences:
            if security_seq_obj.name == security.name:
                severity = 0
                for event in event_timeline:
                    if event.tick_start == current_tick and event.security_affected == security.name:
                        severity = event.event_severity
                
                security.price = security_seq_obj.generateNextPrice(severity)

    for event in event_timeline:
        if event.tick_start == current_tick:
            news_feed.append(event.event_description)


    return f"{current_tick}"

@app.route("/")
def root():
    return "OK"
