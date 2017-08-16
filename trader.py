"""
Name: Jessica Kam
Date: 2017/07/01
"""
from neural_networks import RNN

import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM   
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler

class RNNTrader(RNN):
    
    def __init__(self):
        super(RNNTrader, self).__init__()
    
    def importTrainingSet(self):
        print('Importing training set')
        self.training_set = pd.read_csv('data/eth/2017/08/01/gdax.csv')
        self.training_set = self.training_set.iloc[:,3:4].values #1:2

    #def scaleFeatures(self):
    #    self.sc = MinMaxScaler()
    #    self.training_set = self.sc.fit_transform(self.training_set)

    def getInputsAndOutputs(self):
        print('Getting inputs and outputs')
        self.X_train = self.training_set[0:23] #0:1257, files lines = 1259
        self.y_train = self.training_set[1:23+1] #1:1258

    def reshape(self):
        print('Reshaping...')
        self.X_train = np.reshape(self.X_train, (23, 1, 1)) #(observations, timestamp, num_features)
        
    def build(self):
        print('Building...')
        # Initialising the RNN
        self.regressor = Sequential()
        print('self.regressor: {0}'.format(self.regressor))
        
        # Adding the input layer and the LSTM layer
        self.regressor.add(LSTM(units = 4, activation = 'sigmoid', input_shape = (None, 1))) #input_shape = (time steps, num_features)
        
        # Adding the output layer
        self.regressor.add(Dense(units = 1))
        
        #Compile
        #self.regressor.compile(optimizer='adam', loss='mean_squared_error')
    
    #def compileNN(self): #, **kwargs):
    #    self.regressor.compile(optimizer='adam', loss='mean_squared_error')
        
    #def fitToTrainingSet(self): #, **kwargs):
    #    self.regressor.fit(self.X_train, self.y_train, batch_size = 32, epochs = 200) #**kwargs)
        
    def makePredictions(self):
        """
        # Getting the real stock price of 2017
        test_set = pd.read_csv('Google_Stock_Price_Test.csv')
        self.real_stock_price = test_set.iloc[:,1:2].values
        
        # Getting the predicted stock price of 2017
        inputs = self.real_stock_price
        inputs = self.sc.transform(inputs)
        inputs = np.reshape(inputs, (20, 1, 1))
        self.predicted_stock_price = self.regressor.predict(inputs)
        self.predicted_stock_price = self.sc.inverse_transform(self.predicted_stock_price)
        """
        print('Making predictions...')
        # Getting the real stock price of 2017
        test_set = pd.read_csv('data/eth/2017/08/02/gdax.csv')
        self.real_price = test_set.iloc[:,3:4].values
        
        # Getting the predicted stock price of 2017
        inputs = self.real_price
        inputs = self.sc.transform(inputs)
        inputs = np.reshape(inputs, (23, 1, 1))
        self.predicted_price = self.regressor.predict(inputs)
        self.predicted_price = self.sc.inverse_transform(self.predicted_price)

    def visualizeResults(self):
        print('Visualizing results')
        plt.plot(self.real_price, color = 'red', label = 'Real ETH Price')
        plt.plot(self.predicted_price, color = 'blue', label = 'Predicted ETH Price')
        plt.title('ETH Price Prediction')
        plt.xlabel('Time')
        plt.ylabel('ETH Price')
        plt.legend()
        plt.show()
        
    def evaluate(self):
        print('Evaluating')
        self.rmse = math.sqrt(mean_squared_error(self.real_price, self.predicted_price))
    
    """
    
    def __init__(self, **kwargs):
        super(Trader, self).__init__()
        
    #def determineRecommendation(self):
    #nah prob just act is better
        
    def updateWebApp(self):
        #not sure
        #plot
        

    def saveKerasModel(self):
        model.save(filepath)
        
    def loadKerasModel(self):
        #keras.models.load_model(filepath) to reinstantiate your model. load_model

    #not good for keras        
    def pickleModel(self):
        #not sure
        filename = 'finalized_model.sav'
        pickle.dump(model, open(filename, 'wb'))
    
    def exportWithJoblib(self):
        # save the model to disk
        filename = 'finalized_model.sav'
        joblib.dump(model, filename)
        
    def importWithJoblib(self):
        loaded_model = joblib.load(filename)
        result = loaded_model.score(X_test, Y_test)
        print(result)
    
    def importModel(self):
        # load the model from disk
        loaded_model = pickle.load(open(filename, 'rb'))
        result = loaded_model.score(X_test, Y_test)
        print(result)
            
    """





