# 2017/08/06

from trader import RNNTrader

class WebApp(RNNTrader):
    
    def __init__(self):
        super(RNNTrader, self).__init__()
        
    def run(self):
        model = self.locateMostRecentModel(self, date_object):
        loaded_model = loadModel(model)
        #gather real time data
        #make predictions on data
        #make recommendations or generate commentary
        
        #later
        #research more bots
        #how to generate visuals - cartoon egret, blue (gradient?) triangle background
        #sendNofications - maybe through text or Messenger
        #graph <--veryyyy unsure about, prob not, should at least have historical predictions on webapp
            #predictions/self.date/_graph_
    
    def makeRecommendation(self):
        #
        
    def generateCommentary(self):
        commentary = ''
        #if change is 10 percent or more,
        #    commentary += self.generateSignificantMovementCommentary + '\n'
        
        funny_commentary = [
            'I want food. FEED ME',
            'I demand you feed me',
            'How many times do I have to tell you? MOAR FOOD',
            'SQUAAAAAAAAAWK',
            'Eeeeeeeegret',
            'Look at my plummage *puffs out chest*',
            'WEEEEE I can fly *flap flap*'
            'Hmmm what else do birds do?'
            'Am I amazing or am I really amazing?',
            "Tell me I\'m pretty",
            'Hodl hodl hodl~ Or did I mean hold?',
            'Zzzzz so sleepy...'
        ]
        #how choose random item in list and add it commentary with \n
        
        commentary += self.generateActualPrediction() #or makeRealTimePrediction
        
        
    def generateSignificantMovementCommentary(self):
        positive_20 = [
            'This is gonna be wild!',
            'Ooooooh do I foresee a favorable spike?'
        ]
        positive_10 = [
            'Mmmmm this is quite tasty',
            'I am enjoying this'
        ]
        negative_20 = [
            'Brace for impact!',
            'I feel a great panic approaching'
        ]
        negative_10 = [
            'This is not very pretty. And I like pretty',
            'Move the other way please'
        ]
        #if else statements to choose between them

    def generateActualPrediction(self):
        #return current_price, predicted_price, percent_change each on new lines
    
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