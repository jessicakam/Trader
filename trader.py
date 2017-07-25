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
import gdax, time
public_client = gdax.PublicClient()

public_client.get_products()    #list of dictionaries and like conversions btw LTC, EUR, USD, BTC, GBP, ETH
                                #ones interested in: LTC-BTC, ETH-BTC, LTC-USD, BTC-USD, ETH-USD

# Get the order book at the default level.
public_client.get_product_order_book('ETH-USD')
# Get the order book at a specific level.
public_client.get_product_order_book('ETH-USD', level=1) #  Only the best bid and ask
public_client.get_product_order_book('ETH-USD', level=2) #  Top 50 bids and asks (aggregated)
public_client.get_product_order_book('ETH-USD', level=3) #  Full order book (non aggregated)

# Get the product ticker for a specific product.
public_client.get_product_ticker(product_id='ETH-USD')   #  Basic info about last trade 

# Get the product trades for a specific product.
public_client.get_product_trades(product_id='ETH-USD')   #  Get latest trades

public_client.get_product_historic_rates('ETH-USD')
# To include other parameters, see function docstring:
public_client.get_product_historic_rates('ETH-USD', granularity=3000)   # 200 candles max, in  in ISO 8601 format, internationally acepted one 
#public_client.get_product_historic_rates('ETH-USD', start, end, granularity=3000)
#ISO time example: 2017-07-01T19:26:10+00:00
public_client.get_product_historic_rates('ETH-USD', start='2017-07-01T19:26:10+00:00', end='2017-07-01T19:33:10+00:00', granularity=60)
#time, low, high, open, close, volume
#Desired timeslice in seconds
#start, end in ISO 860
#but output in epoch

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


# Paramters are optional
wsClient = gdax.WebsocketClient(url="wss://ws-feed.gdax.com", products="BTC-USD")
# Do other stuff...
wsClient.close()

#subscribe to multiple products
wsClient = gdax.WebsocketClient(url="wss://ws-feed.gdax.com", 
                                products=["BTC-USD", "ETH-USD"])


#three methods to overwrite before init so can react to streaming
#onOpen - called once, immediately before the socket connection is made, this is where you want to add inital parameters.
#onMessage - called once for every message that arrives and accepts one argument that contains the message of dict type.
#onClose - called once after the websocket has been closed
class myWebsocketClient(gdax.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["LTC-USD"]
        self.message_count = 0
        print("Lets count the messages!")
    def on_message(self, msg):
        self.message_count += 1
        if 'price' in msg and 'type' in msg:
            print ("Message type:", msg["type"], 
                   "\t@ {}.3f".format(float(msg["price"])))
    def on_close(self):
        print("-- Goodbye! --")

wsClient = myWebsocketClient()
wsClient.start()
print(wsClient.url, wsClient.products)
while (wsClient.message_count < 500):
    print ("\nmessage_count =", "{} \n".format(wsClient.message_count))
    time.sleep(1)
wsClient.close()


"""
##NOT WORKING
# OrderBook subscribes to a websocket and keeps a real-time record of the orderbook for the product_id input. 
order_book = gdax.OrderBook(product_id='BTC-USD')
order_book.start()
time.sleep(10)
order_book.close()

"""


##For print time out for myself, maybe for quer
from datetime import datetime
from dateutil import tz

# METHOD 1: Hardcode zones:
#from_zone = tz.gettz('UTC')
#to_zone = tz.gettz('America/Los_Angeles')

# METHOD 2: Auto-detect zones:
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

utc_time = datetime.utcnow()

# Tell the datetime object that it's in UTC time zone since 
utc_time = utc_time.replace(tzinfo=from_zone)

# Convert time zone
local_time = utc_time.astimezone(to_zone)


##ANOVA
##pandas moving_avg
##tf
##nltk



