import time
import pandas as pd
from gateio_client import get_historical_klines, execute_trade

symbol = "FLOKI_USDT"
interval = "15m"
trade_size = 0.001
short_window = 40
long_window = 100

def main():
    in_position = False

    while True:
        print("Fetching historical klines data...")
        data = pd.DataFrame(get_historical_klines(symbol, interval))
        #data.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        data.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'additional_column']

        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
        data.set_index('timestamp', inplace=True)
        data['close'] = data['close'].astype(float)

        data['short_mavg'] = data['close'].rolling(window=short_window).mean()
        data['long_mavg'] = data['close'].rolling(window=long_window).mean()

        last_row = data.iloc[-1]
        previous_row = data.iloc[-2]

        #if not in_position and last_row['short_mavg'] > last_row['long_mavg'] and previous_row['short_mavg'] <= previous_row['long_mavg']:
        print("Buying...")
        execute_trade(symbol, "buy", trade_size)
        in_position = True
        break
        #elif in_position and last_row['short_mavg'] < last_row['long_mavg'] and previous_row['short_mavg'] >= previous_row['long_mavg']:
            #print("Selling...")
            #execute_trade(symbol, "sell", trade_size)
            #in_position = False

        time.sleep(10) 

if __name__ == '__main__':
    main()
