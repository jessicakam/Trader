# 2017/08/06

from trader import ETHTrader
from datetime import datetime, timedelta
import gdax
import os
import random
import numpy as np
from sklearn.preprocessing import MinMaxScaler  
from sklearn.externals import joblib
from keras.models import load_model

class PricePredicter(ETHTrader):
    
    PREDICTION_FOLDER = 'predictions'
    PREDICTION_FILENAME = 'predictions.txt'
    
    def __init__(self):
        super(PricePredicter, self).__init__()
        #self.today = datetime.utcnow()
        #self.date = self.dateObjectToString(self.today)
        #print("self.date: {0}".format(self.date))
        self.date = datetime.today() #.strftime(ETHTrader.DATE_FORMAT)
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
            'GAHHHH! Brace for impact!',
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
        #print('today: {0}'.format(self.dateObjectToString(self.today)))
        model = self.locateMostRecent(ETHTrader.MODEL_FOLDER, self.today, ETHTrader.MODEL_NAME) #self.today
        self.regressor = load_model(model)
        #self.regressor = self.loadModel(model)
        #self.loadModel()
        self.gatherRealTimeData()
        self.makeAPrediction()
        self.makeRecommendation()
        #self.generateCommentary()
        #self.log(self.commentary)
        self.recordPrediction()
        
        #make recommendations or generate commentary
        
        #later
        #research more bots
        #how to generate visuals - cartoon egret, blue (gradient?) triangle background
        #sendNofications - maybe through text or Messenger
        #graph <--veryyyy unsure about, prob not, should at least have historical predictions on webapp
            #predictions/self.date/_graph_
    
    def gatherRealTimeData(self):
        print('Gathering real time data')
        order_book = self.public_client.get_product_order_book('ETH-USD', level=1)
        self.current_ask = float(order_book['asks'][0][0]) #correct data type?
        self.current_bid = float(order_book['bids'][0][0])
        self._current_price = round((self.current_ask + self.current_bid) / 2, 2)
        self.current_price = np.array([self._current_price])
        print('Current Price: {0}'.format(self._current_price))
            
    def makeAPrediction(self):
        print('Predicting a single price')
        # Getting the real prices for a day
        #test_set = pd.read_csv(self.file_to_import) #'data/eth/2017/08/01/gdax.csv')
        #self.real_price = test_set.iloc[:,3:4].values
        
        # Getting the predicted prices for the day
        #inputs = self.real_price
        #inputs = self.sc.transform(inputs)
        
        #from sklearn.externals import joblib
        #scaler_filename = "scaler.save"
        #joblib.dump(scaler, scaler_filename) 
        
        # And now to load...
        scaler_filename = self.locateMostRecent(ETHTrader.SCALER_FOLDER, self.date, ETHTrader.SCALER_NAME) #'scaler/eth/2017/08/15/sc.save'
        self.sc = joblib.load(scaler_filename) 
        
        #self.sc = MinMaxScaler()
        #scaled = self.sc.fit_transform(np.array([self.current_ask, self.current_bid]).reshape(-1,1))
        #print('scaled: {0}'.format(scaled))
        
        self.current_price = self.sc.transform(self.current_price.reshape(-1, 1)) ##
        self.current_price = np.reshape(self.current_price, (1, 1, 1)) #24, 1, 1
        self.predicted_price = self.regressor.predict(self.current_price) #prediction work without transform???
        self.predicted_price = self.sc.inverse_transform(self.predicted_price)
        self._predicted_price = round(self.predicted_price[0][0] / 100 * 100, 2)
        print('predicted price: {0}'.format(self._predicted_price)) 
        
        
        """
        test_set = pd.read_csv('Google_Stock_Price_Test.csv')
        self.real_stock_price = test_set.iloc[:,1:2].values
        
        # Getting the predicted stock price of 2017
        inputs = self.real_stock_price
        inputs = self.sc.transform(inputs)
        inputs = np.reshape(inputs, (20, 1, 1))
        self.predicted_stock_price = self.regressor.predict(inputs)
        self.predicted_stock_price = self.sc.inverse_transform(self.predicted_stock_price)
        
        """
        
    def makeRecommendation(self):
        self.commentary = ''
        self.change = round(self._predicted_price - self._current_price, 2)
        self.percent_change = round(self.change / self._current_price * 100, 2)
        if self.percent_change >= 10 or self.percent_change <= -10:
            self.commentary += self.generateSignificantMovementCommentary()
        #how choose random item in list and add it commentary with \n
        self.commentary += self.selectRandomlyFromList(self.general_funny_commentary)
        self.commentary += self.includeActualPrediction() + '\n'
        
    def generateSignificantMovementCommentary(self):
        if self.percent_change >= 20:
            return self.selectRandomlyFromList(self.positive_20)
        elif self.percent_change >= 10:
            return self.selectRandomlyFromList(self.positive_10)
        elif self.percent_change <= -20:
            return self.selectRandomlyFromList(self.negative_20)
        else:
            return self.selectRandomlyFromList(self.negative_10)
        
    def selectRandomlyFromList(self, lst):
        return random.choice(lst) + '\n'
        
    def includeActualPrediction(self):
        return '(Current Price: {0} \n Predicted Price: {1} \n Predicted Change: {2}($), {3}%) \n'.format(self._current_price, self._predicted_price, self.change, self.percent_change)
    
    #def generateLogFileName(self):
    #    return os.path.join('logs', 'eth', self.dateObjectToString(self.today), 'predictions.txt') #            
    
    def recordPrediction(self):
        self.date = self.dateObjectToString(self.date)
        self.makeFolders(PricePredicter.PREDICTION_FOLDER)
        prediction_file = self.generateFilePath(PricePredicter.PREDICTION_FOLDER, self.date, PricePredicter.PREDICTION_FILENAME) #self.generateLogFileName()
        with open(prediction_file, 'a') as f:
            f.write(self.commentary)
        # also write to a file for messages
        with open(PricePredicter.PREDICTION_FILENAME, 'w') as f:
            f.write(self.commentary)

if __name__ == '__main__':
    """
    opt_parser = OptionParser()
    today = datetime.utcnow()
    opt_parser.add_option('-d',
                         '--date',
                         dest='date',
                         help='Specific date (YYYY/mm/dd) to run trader on, default to yesterday (PST)')
    opt_parser.add_option('-s',
                          '--start_date',
                          dest='start_date',
                          help='Start date if want to run on more than one day')
    opt_parser.add_option('-e',
                          '--end_date',
                          dest='end_date',
                          help='End date if want to run on more than one day')
    opt_parser.add_option('-t',
                          '--train',
                          action='store_false',
                          dest='already_trained',
                          help='Use this option if initial model does not exist')
    opt_parser.add_option('-r',
                          '--retrain',
                          action='store_true',
                          dest='already_trained',
                          help='Use this option if want to retrain an existing model with new data')
    (options, args) = opt_parser.parse_args()

    trader = RNNTrader(date=options.date,
                       start_date=options.start_date,
                       end_date=options.end_date,
                       already_trained=options.already_trained)
    trader.run()
    """
    
    predicter = PricePredicter()
    predicter.run()
