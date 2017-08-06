"""
Name: Jessica Kam
Date: 2017/07/01
"""
import gdax, time
from datetime import datetime

class Trader(RNN):
    
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








