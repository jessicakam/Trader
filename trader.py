"""
Name: Jessica Kam
Date: 2017/07/01

import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

api_url = 'https://api.gdax.com/'
auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

# Get accounts
r = requests.get(api_url + 'accounts', auth=auth)
print r.json()

"""
import gdax
public_client = gdax.PublicClient()

public_client.get_products()

# Get the order book at the default level.
public_client.get_product_order_book('BTC-USD')
# Get the order book at a specific level.
public_client.get_product_order_book('BTC-USD', level=1) #  Only the best bid and ask
public_client.get_product_order_book('BTC-USD', level=2) #  Top 50 bids and asks (aggregated)
public_client.get_product_order_book('BTC-USD', level=3) #  Full order book (non aggregated)

# Get the product ticker for a specific product.
public_client.get_product_ticker(product_id='ETH-USD')   #  Basic info about last trade 

# Get the product trades for a specific product.
public_client.get_product_trades(product_id='ETH-USD')   #  Get latest trades

public_client.get_product_historic_rates('ETH-USD')
# To include other parameters, see function docstring:
public_client.get_product_historic_rates('ETH-USD', granularity=3000)   # 200 candles max, in  in ISO 8601 format
#public_client.get_product_historic_rates('ETH-USD', start, end, granularity=3000)

public_client.get_product_24hr_stats('ETH-USD')         #  high, last, low, open, vol, vol_30day

public_client.get_currencies()

public_client.get_time()                                #  epoch (Unix like time) : iso

request = public_client.get_fills(limit=100)

##try box and whisker plots instead of candles

#Websocket client
# Paramters are optional
wsClient = gdax.WebsocketClient(url="wss://ws-feed.gdax.com", products="BTC-USD")
# Do other stuff...
wsClient.close()

#wss://ws-feed.gdax.com     #websocket feed




