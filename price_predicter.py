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
        self.date = datetime.today()
        self.public_client = gdax.PublicClient()
        
        self.positive_10 = [
            'This is gonna be wild!',
            'Ooooooh do I foresee a favorable spike?'
        ]
        self.positive_5 = [
            'Mmmmm this is quite tasty',
            'I am enjoying this'
        ]
        self.negative_5 = [
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
        model = self.locateMostRecent(ETHTrader.MODEL_FOLDER, self.today, ETHTrader.MODEL_NAME)
        self.regressor = load_model(model)
        self.gatherRealTimeData()
        self.makeAPrediction()
        self.makeRecommendation()
        self.recordPrediction()
    
    def gatherRealTimeData(self):
        print('Gathering real time data')
        order_book = self.public_client.get_product_order_book('ETH-USD', level=1)
        self.current_ask = float(order_book['asks'][0][0])
        self.current_bid = float(order_book['bids'][0][0])
        self._current_price = round((self.current_ask + self.current_bid) / 2, 2)
        self.current_price = np.array([self._current_price])
        print('Current Price: {0}'.format(self._current_price))
            
    def makeAPrediction(self):
        print('Predicting a single price')
        scaler_filename = self.locateMostRecent(ETHTrader.SCALER_FOLDER, self.date, ETHTrader.SCALER_NAME)
        self.sc = joblib.load(scaler_filename) 
        self.current_price = self.sc.transform(self.current_price.reshape(-1, 1))
        self.current_price = np.reshape(self.current_price, (1, 1, 1))
        self.predicted_price = self.regressor.predict(self.current_price)
        self.predicted_price = self.sc.inverse_transform(self.predicted_price)
        self._predicted_price = round(self.predicted_price[0][0] / 100 * 100, 2)
        print('Predicted Price: {0}'.format(self._predicted_price))
        
    def makeRecommendation(self):
        self.commentary = ''
        self.change = round(self._predicted_price - self._current_price, 2)
        self.percent_change = round(self.change / self._current_price * 100, 2)
        if self.percent_change >= 5 or self.percent_change <= -5:
            self.commentary += self.generateSignificantMovementCommentary()
        else:
            self.commentary += self.selectRandomlyFromList(self.general_funny_commentary) + ' '
        self.commentary += self.includeActualPrediction() + '\n'
        
    def generateSignificantMovementCommentary(self):
        if self.percent_change >= 10:
            return self.selectRandomlyFromList(self.positive_10)
        elif self.percent_change >= 5:
            return self.selectRandomlyFromList(self.positive_5)
        elif self.percent_change <= -10:
            return self.selectRandomlyFromList(self.negative_10)
        else:
            return self.selectRandomlyFromList(self.negative_5)
        
    def selectRandomlyFromList(self, lst):
        return random.choice(lst) + '\n'
        
    def includeActualPrediction(self):
        return '(Current Price: {0}, \n Predicted Price: {1}, \n Predicted Change: {2}($), {3}%) \n'.format(self._current_price, self._predicted_price, self.change, self.percent_change)
    
    def recordPrediction(self):
        self.date = self.dateObjectToString(self.date)
        self.makeFolders(PricePredicter.PREDICTION_FOLDER)
        prediction_file = self.generateFilePath(PricePredicter.PREDICTION_FOLDER, self.date, PricePredicter.PREDICTION_FILENAME)
        with open(prediction_file, 'a') as f:
            f.write(self.commentary)
        # also write to a file for messages
        with open(PricePredicter.PREDICTION_FILENAME, 'w') as f:
            f.write(self.commentary)

if __name__ == '__main__':    
    predicter = PricePredicter()
    predicter.run()
