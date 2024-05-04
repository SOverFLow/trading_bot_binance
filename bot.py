import os
import time
import pandas as pd
from binance.client import Client

# Binance API credentials
api_key = '==========='
api_secret = '============='

# Create Binance API client
client = Client(api_key, api_secret)

# Trading parameters
symbol = 'GALAUSDT'
interval = Client.KLINE_INTERVAL_15MINUTE
trade_size = 0.001

# Moving average parameters
short_window = 40
long_window = 100

def get_historical_klines(symbol, interval):
    klines = client.get_klines(symbol=symbol, interval=interval)
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])

    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.set_index('timestamp', inplace=True)
    data['close'] = data['close'].astype(float)

    return data

def get_moving_average(data, window):
    return data['close'].rolling(window=window).mean()

def execute_trade(signal):
    if signal == 'BUY':
        print("Buying...")
        client.create_order(symbol=symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=trade_size)
    elif signal == 'SELL':
        print("Selling...")
        client.create_order(symbol=symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_MARKET, quantity=trade_size)

def main():
    in_position = False

    while True:
        print("\n\nFetching historical klines data...\n\n")
        data = get_historical_klines(symbol, interval)

        data['short_mavg'] = get_moving_average(data, short_window)
        data['long_mavg'] = get_moving_average(data, long_window)


        print(data)

        last_row = data.iloc[-1]
        previous_row = data.iloc[-2]

        #if not in_position and last_row['short_mavg'] > last_row['long_mavg'] and previous_row['short_mavg'] <= previous_row['long_mavg']:
        execute_trade('BUY')
        break 
            #in_position = True
        #elif in_position and last_row['short_mavg'] < last_row['long_mavg'] and previous_row['short_mavg'] >= previous_row['long_mavg']:
            #execute_trade('SELL')
            #in_position = False
            #break

        time.sleep(10)

if __name__ == '__main__':
    main()
