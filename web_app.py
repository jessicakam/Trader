# 2017/08/06

from trader import RNNTrader

class WebApp(RNNTrader):
    #
    def makeRecommendation(self):
        #The price is currently ___. I predict it will be ___ in an hour. You may want to consider buy/sell if you can
        # ... It's probably best to just hold
        #Ooooo I foresee a good spike coming up. Go in
        #Oooo I foresee a good dip coming up. 
        #Squakk
        #Eeeeeeeegret
    
    def logRecommendation(self):
        recommendation = self.makeRecommendation()
        self.makeFolders('logs')
        self.generateLogName(self)
        #open log file and write to it
        
    def makeRealTimeHourlyPredictions(self):
        print('Making predictions...')
        # Getting the real prices for a day
        test_set = pd.read_csv(self.file_to_import) #'data/eth/2017/08/01/gdax.csv')
        self.real_price = test_set.iloc[:,3:4].values
        
        # Getting the predicted prices for the day
        inputs = self.real_price
        inputs = self.sc.transform(inputs)
        inputs = np.reshape(inputs, (len(self.real_price), 1, 1)) #24, 1, 1
        self.predicted_price = self.regressor.predict(inputs)
        self.predicted_price = self.sc.inverse_transform(self.predicted_price)
    
    
    



    #able to train newer ones with more info like top 50 bids etc
    def collectRealTimeData(self):
        #not sure if should support
        #prob need websocket integration
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
        
        public_client.get_product_24hr_stats('ETH-USD')         #  high, last, low, open, vol, vol_30day
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