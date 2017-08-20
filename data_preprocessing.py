# 2017/07/25

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, Imputer, LabelEncoder, OneHotEncoder
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.utils.data as data

class DataPreProcessing():
    def __init__(self):
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.X = None
        self.y = None
        
    def collectData(self):
        pass
    
    def importDataset1(self, csv_file, X_start_index=0, X_end_index=-1, y_index=-1):
        self.dataset = pd.read_csv(csv_file)
        self.X = self.dataset.iloc[:, X_start_index:X_end_index].values
        self.y = self.dataset.iloc[:, y_index].values
    
    def importDataset2(self, csv_file, lst_columns, y_index):
        self.dataset = pd.read_csv(csv_file)
        self.X = self.dataset.iloc[:, lst_columns].values
        self.y = self.dataset.iloc[:, y_index].values
        
    def importDataset3(self, csv_file, list_of_columns):
        dataset = pd.read_csv(csv_file)
        self.X = dataset.iloc[:, list_of_columns].values
        
    def importDataset4(self):            
        self.movies = pd.read_csv('ml-1m/movies.dat', sep = '::', header = None, engine = 'python', encoding = 'latin-1')
        self.users = pd.read_csv('ml-1m/users.dat', sep = '::', header = None, engine = 'python', encoding = 'latin-1')
        self.ratings = pd.read_csv('ml-1m/ratings.dat', sep = '::', header = None, engine = 'python', encoding = 'latin-1')
        
    def fillInMissingData(self, filler='NaN', strategy='mean', axis=0, index_start_fill=1, index_end_fill=3, **kwargs):
        imputer = Imputer(missing_values=filler, strategy=strategy, axis=axis, **kwargs)
        imputer = imputer.fit(self.X[:, index_start_fill:index_end_fill])
        self.X[:, index_start_fill: index_end_fill] = imputer.transform(self.X[:, index_start_fill:index_end_fill])
    
    def encodeCategoricalDataForIndependentVar(self, column_to_encode=0):
        self.labelencoder_X = LabelEncoder()
        self.X[:, column_to_encode] = self.labelencoder_X.fit_transform(self.X[:, column_to_encode])
        self.onehotencoder = OneHotEncoder(categorical_features=[column_to_encode])
        self.X = self.onehotencoder.fit_transform(self.X).toarray()
    
    def encodeCategoricalDataForDependentVar(self):
        labelencoder_y = LabelEncoder()
        self.y = labelencoder_y.fit_transform(self.y)
        
    def encodeCategoricalData(self):
        labelencoder_X_1 = LabelEncoder()
        self.X[:, 1] = labelencoder_X_1.fit_transform(self.X[:, 1])
        labelencoder_X_2 = LabelEncoder()
        self.X[:, 2] = labelencoder_X_2.fit_transform(self.X[:, 2])
        self.onehotencoder = OneHotEncoder(categorical_features = [1])
        self.X = self.onehotencoder.fit_transform(self.X).toarray()
        self.X = self.X[:, 1:]
    
    def avoidTheDummyVariableTrap(self, start_index=1):
        self.X = self.X[:, start_index:]
        
    def splitIntoTrainingAndTestSets(self, **kwargs):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, **kwargs) 
        
    def scaleFeatures1(self):
        self.sc_X = StandardScaler()
        self.X_train = self.sc_X.fit_transform(self.X_train)
        self.X_test = self.sc_X.transform(self.X_test)
        self.sc_y = StandardScaler()
        self.y_train = self.sc_y.fit_transform(self.y_train)

    def scaleFeatures2(self):
        self.sc = StandardScaler()
        self.X_train = self.sc.fit_transform(self.X_train)
        self.X_test = self.sc.transform(self.X_test)
        
    def scaleFeatures3(self):
        self.sc_X = StandardScaler()
        self.sc_y = StandardScaler()
        self.X = self.sc_X.fit_transform(self.X)
        self.y = self.sc_y.fit_transform(self.y)
        
    def prepareTrainingAndTestSets(self):
        self.training_set = pd.read_csv('ml-100k/u1.base', delimiter = '\t')
        self.training_set = np.array(self.training_set, dtype = 'int')
        self.test_set = pd.read_csv('ml-100k/u1.test', delimiter = '\t')
        self.test_set = np.array(self.test_set, dtype = 'int')
        
        # Getting the number of users and movies
        self.nb_users = int(max(max(self.training_set[:,0]), max(self.test_set[:,0])))
        self.nb_movies = int(max(max(self.training_set[:,1]), max(self.test_set[:,1])))
    
    def convertData(self):
        #override
        # Converting the data into an array with users in lines and movies in columns
        self.new_data = []
        for id_users in range(1, self.nb_users + 1):
            id_movies = data[:,1][data[:,0] == id_users]
            id_ratings = data[:,2][data[:,0] == id_users]
            ratings = np.zeros(self.nb_movies)
            ratings[id_movies - 1] = id_ratings
            self.new_data.append(list(ratings))
        self.training_set = torch.convert(self.training_set)
        self.test_set = torch.convert(self.test_set)
    
    def convertIntoTensors(self):
        # Converting the data into Torch tensors
        self.training_set = torch.FloatTensor(self.training_set)
        self.test_set = torch.FloatTensor(self.test_set)