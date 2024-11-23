from flask import Flask, Response 
from client import TradingClient, MarketInfo
from model import event, GameOrderBook
from dataclasses import dataclass
from security import security as security_seq
import random

app = Flask(__name__)

game_started = False
current_tick = 0
event_timeline = []
news_feed = []
securities_descriptions = []

@dataclass
class security_description:
    name : str
    story : str
    price : int

clients = dict()

def create_event_timeline():
    # have a timeline generated
    return [event(tick_start = 0, event_description = "event0", security_affected="None", event_severity=0),
            event(tick_start = 25, event_description = "event1", security_affected="None", event_severity=0),
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
    return list(clients.keys())

@app.route("/client/<string:name>")
def get_client_by_name(name):
    return clients[name].get_name()

@app.route("/start")
def start():
    global game_started, event_timeline, quotes, securities_sequences, securities_descriptions, clients

    clients = [
            TradingClient(team_name = "penguins", starting_balance = 100),
            TradingClient(team_name = "foxes", starting_balance = 100),
            TradingClient(team_name = "mammoths", starting_balance = 100),
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
        securities_sequences.append(security_seq(name = security.name, volatility=random.choice(["calm", "medium", "volatile"]), start=security.price))

    quotes = GameOrderBook(securities = [security.name for security in securities_descriptions])

    game_started = True

    return "Game started!"

@app.route("/tick")
def tick():
    global game_started, current_tick, clients, event_timeline, news_feed, securities_descriptions, quotes, securities_sequences

    if not game_started:
        return ("Game has not started", 403)

    current_market_info = dict()

    security_name_and_price = dict()

    for security in securities_descriptions:
        security_name_and_price[security.name] = security.price

    quotes.update_market_maker_orders(security_prices = security_name_and_price, timestamp=current_tick)

    print('-' * 100)

    for security in securities_descriptions:

        current_market_info[security.name] = MarketInfo(story = security.story,
                                                   orderbook = quotes.orderBooks[security.name].__str__())

        print(security.name, quotes.orderBooks[security.name].__str__())

    for cc in clients:
        print(cc.team_name, cc.portfolio)

    print('-' * 100)

    for event in event_timeline:
        if event.tick_start == current_tick:
            news_feed.append(event.event_description)

    for client in clients:
        order = client.get_quote(market_info = current_market_info, current_tick=current_tick)
        quotes.addOrder(order)

    resolved = quotes.fullfillOrders(tick = current_tick)

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
                    for held_security in client.portfolio:
                        if held_security.security_name == resolved_security:
                            held_security.quantity += record.quantity

    current_tick += 1

    for security in securities_descriptions:
        #             orderbook="Bid: 30(300), 29(500)\nAsk: 31(200), 32(400)"

        for security_seq_obj in securities_sequences:
            if security_seq_obj.name == security.name:
                security.price = security_seq_obj.generateNextPrice()


    return f"{current_tick}"

@app.route("/")
def root():
    return "OK"
