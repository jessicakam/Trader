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
from sklearn.externals import joblib

class ETHTrader(RNN):
    
    TRADER_TYPE = 'eth'
    DATE_FORMAT = '%Y/%m/%d'
    MODEL_FOLDER = 'models'
    MODEL_NAME = 'ETHTrader.hd5'
    SCALER_FOLDER = 'scaler'
    SCALER_NAME = 'ETHTrader_sc.save'
    
    def __init__(self, **kwargs):
        super(ETHTrader, self).__init__()
        self.today = datetime.utcnow()
        self.yesterday = self.today - timedelta(days=1)
        self.start_date = self.yesterday.strftime(ETHTrader.DATE_FORMAT)
        self.end_date = self.yesterday.strftime(ETHTrader.DATE_FORMAT)
        if kwargs.get('date'):           
            self.start_date = kwargs.get('date')
            self.end_date = kwargs.get('date')
        if kwargs.get('start_date') and kwargs.get('end_date'):
            self.start_date = kwargs.get('start_date')
            self.end_date = kwargs.get('end_date')
        self.already_trained = kwargs.get('already_trained')
                
    def run(self):
        self.generateListDates()
        for date in self.lst_dates:
            self.date = date
            print('Running trader for {0}'.format(self.date))
            if self.already_trained:
                self.loadModel()
                self.deleteOld(ETHTrader.MODEL_FOLDER, ETHTrader.MODEL_NAME)
            self.importTrainingSet()
            self.scaleFeatures()
            self.getInputsAndOutputs()
            self.reshape()
            if not self.already_trained:
                self.build()
                self.compileNN()
            self.fitToTrainingSet()
            # maybe later unindent these three at the end
            self.makePredictions()
            self.visualizeResults()
            self.evaluate()
            self.saveModel()
        
    def generateFilePath(self, folder, date, filename):
        return os.path.join(folder, ETHTrader.TRADER_TYPE, date, filename)
    
    def generateListDates(self):
        start = self.start_date
        end = self.end_date
        self.lst_dates = []
        while start <= end:
            self.lst_dates.append(start)
            start_obj = self.dateStringToObject(start) + timedelta(days=1)
            start = self.dateObjectToString(start_obj)
            
    def dateStringToObject(self, date_string):
        return datetime.strptime(date_string, ETHTrader.DATE_FORMAT)
        
    def dateObjectToString(self, date_object):
        return date_object.strftime(ETHTrader.DATE_FORMAT)
    
    def importTrainingSet(self):
        print('Importing training set')
        self.file_to_import = self.generateFilePath('data', self.date, 'gdax.csv')
        self.training_set = pd.read_csv(self.file_to_import)
        self.training_set = self.training_set.iloc[:,3:4].values
        self.num_observations = len(self.training_set)

    def scaleFeatures(self):
        print('Scaling features')
        self.sc = MinMaxScaler()
        self.training_set = self.sc.fit_transform(self.training_set)
        if self.already_trained:
            self.deleteOld(ETHTrader.SCALER_FOLDER, ETHTrader.SCALER_NAME)
        # save new scaler
        self.makeFolders(ETHTrader.SCALER_FOLDER)
        scaler_filename = self.generateFilePath(ETHTrader.SCALER_FOLDER, self.date, ETHTrader.SCALER_NAME)
        joblib.dump(self.sc, scaler_filename)

    def getInputsAndOutputs(self):
        print('Getting inputs and outputs')
        self.X_train = self.training_set[0:self.num_observations-1]
        self.y_train = self.training_set[1:self.num_observations]

    def reshape(self):
        print('Reshaping')
        self.X_train = np.reshape(self.X_train, (len(self.X_train), 1, 1)) #(observations, timestamp, num_features)
        
    def build(self):
        print('Building...')
        # Initialising the RNN
        self.regressor = Sequential()
        
        # Adding the input layer and the LSTM layer
        self.regressor.add(LSTM(units = 4, activation = 'sigmoid', input_shape = (None, 1))) #input_shape = (time steps, num_features)
        
        # Adding the output layer
        self.regressor.add(Dense(units = 1))
    
    def compileNN(self):
        self.regressor.compile(optimizer='adam', loss='mean_squared_error')
        
    def fitToTrainingSet(self):
        print('Fitting to training set')
        self.regressor.fit(self.X_train, self.y_train, batch_size = 32, epochs = 200)
        self.already_trained = True
        
    def makePredictions(self):
        print('Making predictions')
        self.next_day = self.dateObjectToString(self.dateStringToObject(self.date) + timedelta(days=1))
        next_days_data = self.generateFilePath('data', self.next_day, 'gdax.csv')
        # Getting the real prices for the next day
        test_set = pd.read_csv(next_days_data)
        self.real_price = test_set.iloc[:,3:4].values
        
        # Getting the predicted prices for the next day
        inputs = self.real_price
        inputs = self.sc.transform(inputs)
        inputs = np.reshape(inputs, (len(self.real_price), 1, 1))
        self.predicted_price = self.regressor.predict(inputs)
        self.predicted_price = self.sc.inverse_transform(self.predicted_price)

    def visualizeResults(self):
        print('Visualizing results')
        desired_dates_to_visualize = ['2016/05/25', '2016/05/26', '2017/08/01', '2017/08/15'] #
        if self.date in desired_dates_to_visualize: #
            plt.plot(self.real_price, color = 'red', label = 'Real ETH Price')
            plt.plot(self.predicted_price, color = 'blue', label = 'Predicted ETH Price')
            plt.title('ETH Price Prediction' + ' ' + self.next_day)
            plt.xlabel('Time')
            plt.ylabel('ETH Price')
            plt.legend()
            plt.show()
        
    def evaluate(self):
        print('Evaluating')
        self.rmse = math.sqrt(mean_squared_error(self.real_price, self.predicted_price))
    
    def makeFolders(self, initial_folder):
        year, month, day = self.date.split('/')
        folders = [ETHTrader.TRADER_TYPE, year, month, day]
        if not os.path.exists(initial_folder):
            os.makedirs(initial_folder)
        path_so_far = initial_folder
        for folder in folders:
            path_so_far = os.path.join(path_so_far, folder)
            if not os.path.exists(path_so_far):
                os.makedirs(path_so_far)
    
    def saveModel(self):
        model_name = self.generateFilePath(ETHTrader.MODEL_FOLDER, self.date, ETHTrader.MODEL_NAME)
        self.makeFolders(ETHTrader.MODEL_FOLDER)
        self.regressor.save(model_name)
        del self.regressor
        
    def loadModel(self):
        print('Loading model...')
        prev_day = self.dateStringToObject(self.date) - timedelta(days=1)
        model_name = self.locateMostRecent(ETHTrader.MODEL_FOLDER, prev_day, ETHTrader.MODEL_NAME)
        self.regressor = load_model(model_name)
    
    def deleteOld(self, folder, filename):
        print('Deleting old...')
        most_recent = self.locateMostRecent(folder, self.dateStringToObject(self.date), filename)
        os.remove(most_recent)
        
    def locateMostRecent(self, folder, date_object, filename):
        found = False
        while not found:    
            most_recent = self.generateFilePath(folder, self.dateObjectToString(date_object), filename)
            if os.path.isfile(most_recent):
                found = True
            else:
                date_object = date_object - timedelta(days=1)
        print('Located: {0}'.format(most_recent))
        return most_recent

