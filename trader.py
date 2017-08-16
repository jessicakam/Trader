"""
Name: Jessica Kam
Date: 2017/07/01
"""
from neural_networks import RNN
from datetime import datetime, timedelta
import os

import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler

class RNNTrader(RNN):
    
    DATE_FORMAT = '%Y/%m/%d'
    
    def __init__(self, **kwargs):
        super(RNNTrader, self).__init__()
        self.internal_log = 'internal_log.txt'
        self.today = datetime.utcnow()
        yesterday = self.today - timedelta(days=1)
        self.start_date = yesterday.strftime(RNNTrader.DATE_FORMAT)
        self.end_date = yesterday.strftime(RNNTrader.DATE_FORMAT)
        if kwargs.get('date'):           
            self.start_date = kwargs.get('date')
            self.end_date = kwargs.get('date')
        if kwargs.get('start_date') and kwargs.get('end_date'):
            self.start_date = kwargs.get('start_date')
            self.end_date = kwargs.get('end_date')
        self.already_trained = kwargs.get('already_trained')
    
    def log(self, msg):
        with open(self.internal_log, 'a') as f:
            f.write('{0}: '.format(self.dateObjectToString(self.today)) + msg + '\n')
            
    def run(self):
        self.generateListDates()
        for date in self.lst_dates:
            self.date = date
            self.log('Running trader for {0}'.format(self.date))
            if self.already_trained:
                self.loadModel()
                self.deleteOldModel()
            self.findFileToImport()
            self.importTrainingSet()
            self.scaleFeatures()
            self.getInputsAndOutputs()
            self.reshape()
            if not self.already_trained:
                self.build()
                self.compileNN()
            self.fitToTrainingSet()
            #maybe later unindent these three at the end
            self.makePredictions()
            self.visualizeResults()
            self.evaluate()
            self.saveModel()

    def findFileToImport(self):
        self.file_to_import = os.path.join('data',
                                           'eth',
                                           self.date,
                                           'gdax.csv')
            
    def generateListDates(self):
        start = self.start_date
        end = self.end_date
        self.lst_dates = []
        while start <= end:
            self.lst_dates.append(start)
            start_obj = self.dateStringToObject(start) + timedelta(days=1)
            start = self.dateObjectToString(start_obj)
            
    def dateStringToObject(self, date_string):
        return datetime.strptime(date_string, RNNTrader.DATE_FORMAT)
        
    def dateObjectToString(self, date_object):
        return date_object.strftime(RNNTrader.DATE_FORMAT)
    
    def importTrainingSet(self):
        self.log('Importing training set')
        self.training_set = pd.read_csv(self.file_to_import) #'data/eth/2017/08/01/gdax.csv')
        self.training_set = self.training_set.iloc[:,3:4].values #1:2
        self.num_observations = len(self.training_set)

    def getInputsAndOutputs(self):
        self.log('Getting inputs and outputs')
        self.X_train = self.training_set[0:self.num_observations-1] #0:23 #0:1257, files lines = 1259
        self.y_train = self.training_set[1:self.num_observations] #1:24 #1:1258

    def reshape(self):
        self.log('Reshaping')
        self.X_train = np.reshape(self.X_train, (len(self.X_train), 1, 1)) #23, 1, 1 #(observations, timestamp, num_features)
        
    def build(self):
        self.log('Building...')
        # Initialising the RNN
        self.regressor = Sequential()
        
        # Adding the input layer and the LSTM layer
        self.regressor.add(LSTM(units = 4, activation = 'sigmoid', input_shape = (None, 1))) #input_shape = (time steps, num_features)
        
        # Adding the output layer
        self.regressor.add(Dense(units = 1))
    
    def compileNN(self):
        self.regressor.compile(optimizer='adam', loss='mean_squared_error')
        
    def fitToTrainingSet(self):
        self.log('Fitting to training set')
        self.regressor.fit(self.X_train, self.y_train, batch_size = 32, epochs = 200)
        self.already_trained = True ##
        
    def makePredictions(self):
        self.log('Making predictions')
        # Getting the real prices for a day
        test_set = pd.read_csv(self.file_to_import) #'data/eth/2017/08/01/gdax.csv')
        self.real_price = test_set.iloc[:,3:4].values
        
        # Getting the predicted prices for the day
        inputs = self.real_price
        inputs = self.sc.transform(inputs)
        inputs = np.reshape(inputs, (len(self.real_price), 1, 1)) #24, 1, 1
        self.predicted_price = self.regressor.predict(inputs)
        self.predicted_price = self.sc.inverse_transform(self.predicted_price)

    def visualizeResults(self):
        self.log('Visualizing results')
        #desired_dates_to_visualize = ['2016/05/25', '2017/01/01', '2017/06/01', '2017/08/15'] #
        #if self.date in desired_dates_to_visualize: #
        plt.plot(self.real_price, color = 'red', label = 'Real ETH Price')
        plt.plot(self.predicted_price, color = 'blue', label = 'Predicted ETH Price')
        plt.title('ETH Price Prediction' + ' ' + self.date)
        plt.xlabel('Time')
        plt.ylabel('ETH Price')
        plt.legend()
        plt.show()
    
    def evaluate(self):
        self.log('Evaluating')
        self.rmse = math.sqrt(mean_squared_error(self.real_price, self.predicted_price))
        
    def generateModelName(self, date):
        return os.path.join('model', date, 'RNNTrader_refactored.hd5') #
    
    def makeFolders(self, initial_folder):
        year, month, day = self.date.split('/')
        folders = [year, month, day] #model
        if not os.path.exists(initial_folder):
            os.makedirs(initial_folder)
        path_so_far = initial_folder
        for folder in folders:
            path_so_far = os.path.join(path_so_far, folder)
            if not os.path.exists(path_so_far):
                os.makedirs(path_so_far)
    
    def saveModel(self):
        model_name = self.generateModelName(self.date)
        self.makeFolders('model')
        self.regressor.save(model_name)
        del self.regressor
        
    def loadModel(self):
        self.log('Loading model...')
        prev_day = self.dateStringToObject(self.date) - timedelta(days=1)
        model_name = self.locateMostRecentModel(prev_day)
        self.regressor = load_model(model_name)
        
    def deleteOldModel(self):
        self.log('Deleting old model...')
        prev_day = self.dateStringToObject(self.date) - timedelta(days=1)
        model_name = self.locateMostRecentModel(prev_day)
        os.remove(model_name)
        
    def locateMostRecentModel(self, date_object):
        model_found = False #
        while not model_found:    
            model_name = self.generateModelName(self.dateObjectToString(date_object))
            if os.path.isfile(model_name):
                model_found = True #
            else:
                date_object = date_object - timedelta(days=1)
        self.log('Found: {0}'.format(model_name))
        return model_name

