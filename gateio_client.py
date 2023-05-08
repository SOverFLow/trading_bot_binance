import hmac
import hashlib
import requests
import time
from config import API_KEY, API_SECRET


BASE_URL = 'https://api.gateio.ws/api/v4'

def get_signature(timestamp, method, url, query_string=None, body=None):
    signature_string = f"{timestamp}\n{method}\n{url}\n"
    if query_string:
        signature_string += f"{query_string}\n"
    else:
        signature_string += "\n"
    if body:
        signature_string += f"{body}"

    signature = hmac.new(
        API_SECRET.encode(),
        signature_string.encode(),
        hashlib.sha512
    ).hexdigest()

    return signature

def get_headers(timestamp, signature):
    return {
        "KEY": API_KEY,
        "Timestamp": str(timestamp),
        "SIGN": signature,
        "Content-Type": "application/json"
    }



def get_server_time():
    method = "GET"
    url = f"{BASE_URL}/spot/accounts"

    local_timestamp = int(time.time() * 1000)
    signature = get_signature(local_timestamp, method, url)
    headers = get_headers(local_timestamp, signature)

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")

    server_timestamp = int(response.headers['Date']) // 1000000
    time_offset = server_timestamp - local_timestamp

    return time_offset





def get_historical_klines(symbol, interval):
    method = "GET"
    url = f"{BASE_URL}/spot/candlesticks"
    query_string = f"currency_pair={symbol}&interval={interval}"

    timestamp = get_server_time()
    signature = get_signature(timestamp, method, url, query_string)

    headers = get_headers(timestamp, signature)
    response = requests.get(url, headers=headers, params=query_string)

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")

    return response.json()

def execute_trade(symbol, side, amount):
    method = "POST"
    url = f"{BASE_URL}/spot/orders"
    body = {
        "currency_pair": symbol,
        "side": side,
        "type": "market",
        "amount": str(amount)
    }

    timestamp = get_server_time()
    signature = get_signature(timestamp, method, url, body=str(body))

    headers = get_headers(timestamp, signature)
    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")

    return response.json()
