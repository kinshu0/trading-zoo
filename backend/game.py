from flask import Flask, Response 
from client import trading_client
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
        clients[name] = trading_client(name)

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
    global game_started, event_timeline

    event_timeline = create_event_timeline()

    securities = ["Banana", "Coconut"]

    game_started = True

    return "Game started!"

@app.route("/tick")
def tick():
    global game_started, current_tick, clients, event_timeline, news_feed, securities

    if not game_started:
        return ("Game has not started", 403)

    quotes = GameOrderBook(securities = securities)

    for event in event_timeline:
        if event.tick_start == current_tick:
            news_feed.append(event.event_description)

    for client in clients:
        quotes.addOrder(clients[client].get_quote())

    resolved = fullfillOrders(tick = current_tick)

    # process resolved

    current_tick += 1

    return f"{current_tick}"

@app.route("/")
def root():
    return "OK"
