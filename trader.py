"""
Name: Jessica Kam
Date: 2017/07/01
"""
import gdax, time
from datetime import datetime

class Trader(RNN):
    """
        rnn = nn.RNN()
        instance = 'rnn'
        
        rnn.importTrainingSet()
        
        rnn.scaleFeatures()
        
        rnn.getInputsAndOutputs()
        self.assertTrue(rnn.X_train.any(), instance + '.X_train should be set.')
        self.assertTrue(rnn.y_train.any(), instance + '.y_train should be set.')
        
        X_before = rnn.X_train
        rnn.reshape()
        X_after = rnn.X_train
        self.assertTrue((X_before.shape[0] != X_after[0]) or (X_before.shape[1] != X_before.shape[1]), instance + '.X_train should change after reshaping')
        
        rnn.build()
        self.assertTrue(rnn.regressor, instance + '.regressor should be set.')
        
        rnn.compileNN(optimizer='adam', loss='mean_squared_error')
        
        rnn.fitToTrainingSet(batch_size = 32, epochs = 200)
        
        rnn.makePredictions()
        self.assertTrue(rnn.real_stock_price.any(), instance + '.real_stock_price should be set.')
        self.assertTrue(rnn.predicted_stock_price.any(), instance + '.predicted_stock_price should be set.')
        
        rnn.visualizeResults()
        
        rnn.evaluate()
        self.assertTrue(rnn.rmse, instance + '.rsme should be set')
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
            

    
class RNNTrader(Trader, RNN):
    pass
    
    
class PolyRegTrader(Trader, PolyReg):
    pass     








