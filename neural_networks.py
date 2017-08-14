# 2017/07/29

from data_preprocessing import DataPreProcessing
from data_postprocessing import DataPostProcessing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class NN(DataPreProcessing, DataPostProcessing):
    def __init__(self):
        super(NN, self).__init__()
    
    def compileNN(self, **kwargs):
        pass


import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import cross_val_score

class ANN(NN):
    def __init__(self):
        super(ANN, self).__init__()
        
    def build(self):
        self.classifier = self.actuallyBuild()
    
    def actuallyBuild(self):
        classifier = Sequential()
        classifier.add(Dense(units = 6, kernel_initializer = 'uniform', activation = 'relu', input_dim = 11))
        classifier.add(Dense(units = 6, kernel_initializer = 'uniform', activation = 'relu'))
        classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))
        classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
        return classifier
        
    def fitToTrainingSet(self, **kwargs):
        self.classifier.fit(self.X_train, self.y_train, **kwargs)
        
    def predictResults(self):
        self.y_pred = self.classifier.predict(self.X_test)
        self.y_pred = (self.y_pred > 0.5)

    def makeNewPrediction(self, lst_feature_values):
        new_prediction = self.classifier.predict(self.sc.transform(np.array([lst_feature_values])))
        self.new_prediction = new_prediction > 0.5
        
    def evaluate(self):
        # override when inherit this class
        classifier = KerasClassifier(build_fn = self.actuallyBuild, batch_size = 10, epochs = 100)
        accuracies = cross_val_score(estimator = classifier, X = self.X_train, y = self.y_train, cv = 10, n_jobs = -1)
        self.mean = accuracies.mean()
        self.variance = accuracies.std()
        
    def improve(self):
        # override when inherit this class
        #drop out regularization to reduce overfitting if needed
        classifier = KerasClassifier(build_fn = self.actuallyBuild)
        parameters = {'batch_size': [25, 32],
                      'epochs': [100, 500],
                      'optimizer': ['adam', 'rmsprop']}
        grid_search = GridSearchCV(estimator = classifier,
                                   param_grid = parameters,
                                   scoring = 'accuracy',
                                   cv = 10)
        grid_search = grid_search.fit(self.X_train, self.y_train)
        self.best_parameters = grid_search.best_params_
        self.best_accuracy = grid_search.best_score_


from keras.models import Sequential
from keras.layers import Conv2D #Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
from keras.preprocessing import image

class CNN(ANN):

    def __init__(self):
        super(CNN, self).__init__()
        
    def build(self):
        # override when inherit
        # Initialising the CNN
        self.classifier = Sequential()
        
        # Step 1 - Convolution
        self.classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu')) #Conv2D
        
        # Step 2 - Pooling
        self.classifier.add(MaxPooling2D(pool_size = (2, 2)))
        
        # Adding a second convolutional layer
        self.classifier.add(Conv2D(32, (3, 3), activation = 'relu')) #Conv2D
        self.classifier.add(MaxPooling2D(pool_size = (2, 2)))
        
        # Step 3 - Flattening
        self.classifier.add(Flatten())
        
        # Step 4 - Full connection
        self.classifier.add(Dense(units = 128, activation = 'relu'))
        self.classifier.add(Dense(units = 1, activation = 'sigmoid'))
    
    def compileNN(self, **kwargs):
        self.classifier.compile(**kwargs)
        
    def fitToImages(self):
        # overrride when inherit
        train_datagen = ImageDataGenerator(rescale = 1./255,
                                           shear_range = 0.2,
                                           zoom_range = 0.2,
                                           horizontal_flip = True)
        
        test_datagen = ImageDataGenerator(rescale = 1./255)
        
        self.training_set = train_datagen.flow_from_directory('dataset/training_set',
                                                         target_size = (64, 64),
                                                         batch_size = 32,
                                                         class_mode = 'binary')
        
        self.test_set = test_datagen.flow_from_directory('dataset/test_set',
                                                    target_size = (64, 64),
                                                    batch_size = 32,
                                                    class_mode = 'binary')
        
        self.classifier.fit_generator(self.training_set,
                                 samples_per_epoch = 8000,
                                 nb_epoch = 25,
                                 validation_data = self.test_set,
                                 nb_val_samples = 2000)
        
    def makeNewPrediction(self):
        # overrride when inherit
        test_image = image.load_img('dataset/single_prediction/cat_or_dog_1.jpg', target_size = (64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = self.classifier.predict(test_image)
        #what is this line for
        #self.training_set.class_indices
        if result[0][0] == 1:
            self.prediction = 'dog'
        else:
            self.prediction = 'cat'


import math        
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM   
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler   
     
class RNN(NN):
        
    def __init__(self):
        super(RNN, self).__init__()
    
    def importTrainingSet(self):
        self.training_set = pd.read_csv('Google_Stock_Price_Train.csv')
        self.training_set = self.training_set.iloc[:,1:2].values

    def scaleFeatures(self):
        self.sc = MinMaxScaler()
        self.training_set = self.sc.fit_transform(self.training_set)

    def getInputsAndOutputs(self):
        # override when inherit
        self.X_train = self.training_set[0:1257]
        self.y_train = self.training_set[1:1258]

    def reshape(self):
        #override when inherit
        self.X_train = np.reshape(self.X_train, (1257, 1, 1))
        
    def build(self):
        #override when inherit
        # Initialising the RNN
        self.regressor = Sequential()
        
        # Adding the input layer and the LSTM layer
        self.regressor.add(LSTM(units = 4, activation = 'sigmoid', input_shape = (None, 1)))
        
        # Adding the output layer
        self.regressor.add(Dense(units = 1))
    
    def compileNN(self, **kwargs):
        self.regressor.compile(**kwargs)
        
    def fitToTrainingSet(self, **kwargs):
        self.regressor.fit(self.X_train, self.y_train, **kwargs)
        
    def makePredictions(self):
        # Getting the real stock price of 2017
        test_set = pd.read_csv('Google_Stock_Price_Test.csv')
        self.real_stock_price = test_set.iloc[:,1:2].values
        
        # Getting the predicted stock price of 2017
        inputs = self.real_stock_price
        inputs = self.sc.transform(inputs)
        inputs = np.reshape(inputs, (20, 1, 1))
        self.predicted_stock_price = self.regressor.predict(inputs)
        self.predicted_stock_price = self.sc.inverse_transform(self.predicted_stock_price)

    def visualizeResults(self):
        plt.plot(self.real_stock_price, color = 'red', label = 'Real Google Stock Price')
        plt.plot(self.predicted_stock_price, color = 'blue', label = 'Predicted Google Stock Price')
        plt.title('Google Stock Price Prediction')
        plt.xlabel('Time')
        plt.ylabel('Google Stock Price')
        plt.legend()
        plt.show()
        
    def evaluate(self):
        self.rmse = math.sqrt(mean_squared_error(self.real_stock_price, self.predicted_stock_price))
