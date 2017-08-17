# 2017/08/06

from trader import RNNTrader
from datetime import datetime
import gdax

class WebApp(RNNTrader):
    
    def __init__(self):
        super(RNNTrader, self).__init__()
        today = datetime.utcnow()
        self.public_client = gdax.PublicClient()
        
        self.positive_20 = [
            'This is gonna be wild!',
            'Ooooooh do I foresee a favorable spike?'
        ]
        self.positive_10 = [
            'Mmmmm this is quite tasty',
            'I am enjoying this'
        ]
        self.negative_20 = [
            'Brace for impact!',
            'I feel a great panic approaching'
        ]
        self.negative_10 = [
            'This is not very pretty. And I like pretty',
            'Move the other way please'
        ]
        
        self.general_funny_commentary = [
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
        
    def run(self):
        ##TODO - prob remove logging
        
        # every hour
        model = self.locateMostRecentModel(self, date_object):
        self.regressor = loadModel(model)
        self.gatherRealTimeData()
        self.makeAPrediction()
        self.generateCommentary()
        #self.log(self.commentary)
        self.logPrediction()
        
        #make recommendations or generate commentary
        
        #later
        #research more bots
        #how to generate visuals - cartoon egret, blue (gradient?) triangle background
        #sendNofications - maybe through text or Messenger
        #graph <--veryyyy unsure about, prob not, should at least have historical predictions on webapp
            #predictions/self.date/_graph_
    
    def gatherRealTimeData(self):
        order_book = public_client.get_product_order_book('ETH-USD', level=1)
        self.current_price = [float(order_book['asks'][0][0])] #correct data type?
            
    def makeAPrediction(self):
        self.log('Predicting a single price')
        # Getting the real prices for a day
        #test_set = pd.read_csv(self.file_to_import) #'data/eth/2017/08/01/gdax.csv')
        #self.real_price = test_set.iloc[:,3:4].values
        
        # Getting the predicted prices for the day
        #inputs = self.real_price
        #inputs = self.sc.transform(inputs)
        
        #self.real_time_price = self.sc.transform(self.real_time_price)
        self.current_price = np.reshape(self.current_price, (1, 1, 1)) #24, 1, 1
        self.predicted_price = self.regressor.predict(self.current_price) #prediction work without transform???
        #self.predicted_price = self.sc.inverse_transform(self.predicted_price)
            
    def makeRecommendation(self):
        self.commentary = ''
        self.change = (self.predicted_price - self.current_price) / self.current_price
        if self.change >= 1.1 or self.change <= 0.9:
            self.commentary += self.generateSignificantMovementCommentary() + '\n'
        #how choose random item in list and add it commentary with \n
        self.commentary += self.selectRandomlyFromList(self.general_funny_commentary) + '\n'
        self.commentary += self.includeActualPrediction() + '\n'
        
    def generateSignificantMovementCommentary(self):
        if self.change >= 1.2:
            return self.selectRandomlyFromList(self.positive_20)
        elif self.change >= 1.1:
            return self.selectRandomlyFromList(self.positive_10)
        elif self.change <= 0.8:
            return self.selectRandomlyFromList(self.negative_20)
        else:
            return self.selectRandomlyFromList(self.negative_10)
        
    def selectRandomlyFromList(self, lst):
        return
        

    def includeActualPrediction(self):
        return 'current price: {0}'.format(self.current_price) + '\n' + \
                'predicted price: {0}'.format(self.predicted_price) + '\n' + \
                'percent change: {0}'.format(self.change)
    
    def generateLogFileName(self):
        return os.path.join('logs', 'eth', self.dateObjectToString(today), 'prediction_log.txt') #            
    
    def logPrediction(self):
        self.makeFolders('logs')
        log_file = self.generateLogFileName()
        with open(log_file, 'a') as f:
            f.write(self.commentary)
        
