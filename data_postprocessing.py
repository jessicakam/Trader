# 2017/08/01

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score

class DataPostProcessing():
    
    def predictResults(self):
        self.y_pred = self.classifier.predict(self.X_test)
        
    def makeConfusionMatrix(self):
        self.cm = confusion_matrix(self.y_test, self.y_pred)

    def applyKFoldCrossValidation(self, **kwargs):
        self.accuracies = cross_val_score(**kwargs)
        self.mean = self.accuracies.mean()
        self.std = self.accuracies.std()