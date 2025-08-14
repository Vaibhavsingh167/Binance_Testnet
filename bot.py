from binance.client import Client
import time
import threading
from datetime import datetime 
import os

API_Key = os.environ.get("BINANCE_API_KEY")
Secret_Key = os.environ.get("BINANCE_SECRET_KEY")
client = Client(API_Key, Secret_Key,testnet=True)

symbol = 'BTCUSDT'
buy_price_threshold  = 118000   # buy when price <= 118,000
sell_price_threshold = 118100   # sell when price >= 118,800
trade_quantity       = 0.001




bot_running = False
in_position = False
price_history = []  # [(timestamp, price)]
trade_history = []  # [(timestamp, price, 'BUY'/'SELL')]

def get_current_price():
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def log_price(price):
    timestamp = datetime.now().strftime("%H:%M:%S")
    price_history.append((timestamp, price))
    if len(price_history) > 50:  # keep last 50 points
        price_history.pop(0)

def log_trade(price, trade_type):
    timestamp = datetime.now().strftime("%H:%M:%S")
    trade_history.append((timestamp, price, trade_type))

def place_buy_order(quantity):
    order = client.order_market_buy(symbol=symbol, quantity=quantity)
    print(f"Buy Order Placed: {order}")
    log_trade(get_current_price(), "BUY")
    return order

def place_sell_order(quantity):
    order = client.order_market_sell(symbol=symbol, quantity=quantity)
    print(f"Sell Order Placed: {order}")
    log_trade(get_current_price(), "SELL")
    return order

def trading_loop():
    global bot_running, in_position
    while bot_running:
        try:
            current_price = get_current_price()
            log_price(current_price)
            print(f"Current Price: {current_price}")

            if not in_position and current_price <= buy_price_threshold:
                place_buy_order(trade_quantity)
                in_position = True

            elif in_position and current_price >= sell_price_threshold:
                place_sell_order(trade_quantity)
                in_position = False

        except Exception as e:
            print("Error in bot:", e)
        time.sleep(30)

def start_bot():
    global bot_running
    if not bot_running:
        bot_running = True
        threading.Thread(target=trading_loop, daemon=True).start()

def stop_bot():
    global bot_running
    bot_running = False