from flask import Flask, Response 
from client import trading_client, MarketInfo
from model import event, GameOrderBook

app = Flask(__name__)

game_started = False
current_tick = 0
event_timeline = []
news_feed = []
securities = []


clients = dict()

def create_event_timeline():
    # have a timeline generated
    return [event(tick_start = 0, event_description = "event0"),
            event(tick_start = 25, event_description = "event1"),
            # ...
            ]

@app.route("/register/<string:name>")
def register_client(name):
    global game_started, clients

    if not game_started:
        clients[name] = trading_client(name = name, starting_balance = 100)

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
    global game_started, event_timeline, quotes, securities_stories

    clients = [
            trading_client(name = "penguins", starting_balance = 100),
            trading_client(name = "foxes", starting_balance = 100),
            trading_client(name = "mammoths", starting_balance = 100),
            ]

    event_timeline = create_event_timeline()

    securities = ["ice", "fish"]

    securities_stories = {
            "ice" : "The sun's rays grow stronger each day, and whispers spread through the market of a great heat wave approaching. The cloud shepherds have been seen guiding their flocks far to the north, leaving the southern markets exposed to the sun's fierce embrace.",

            "fish" : "A mysterious current has shifted in the deep waters, bringing schools of silver-scaled visitors to unusual waters. The wise seals speak of a great migration that happens once every blue moon, but the local fishing fleets seem oddly quiet about their recent catches."

            }

    quotes = GameOrderBook(securities = securities)

    game_started = True

    return "Game started!"

@app.route("/tick")
def tick():
    global game_started, current_tick, clients, event_timeline, news_feed, securities, quotes, securities_stories

    current_market_info = dict() #= MarketInfo(story = "", 
                        #             orderbook)

    for security in securities:
        #             orderbook="Bid: 30(300), 29(500)\nAsk: 31(200), 32(400)"

        current_market_info[security] = MarketInfo(story = securities_stories[security],
                                                   orderbook = ""
                                                   )

    if not game_started:
        return ("Game has not started", 403)

    for event in event_timeline:
        if event.tick_start == current_tick:
            news_feed.append(event.event_description)

    for client in clients:
        quotes.addOrder(clients[client].get_quote(market_info = current_market_info))

    resolved = quotes.fullfillOrders(tick = current_tick)

    for resolved_security in resolved:
        for record in resolved[security]:
            for client in clients:
                if client.name == record.seller:
                    client.balance_available += record.quantity * record.price
                    for held_security in client.portfolio:
                        if held_security.security_name == resolved_security:
                            held_security.quantity -= record.quantity

                elif client.name == record.buyer:
                    client.balance_available -= record.quantity * record.price
                    for held_security in client.portfolio:
                        if held_security.security_name == resolved_security:
                            held_security.quantity += record.quantity

    current_tick += 1

    return f"{current_tick}"

@app.route("/")
def root():
    return "OK"
