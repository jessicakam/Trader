"""
Name: Jessica Kam
Date: 2017/07/24

OTHER NOTES TO INCOPORATE LATER, try and find some more common ones to add to templates
#for readme: adapted from material in Udemy ML A-Z and DL A-Z course, along with Berkeley's DataX course and other sources
#future: Coursera course, DS100, pdfs, papers, TF+scikitlearn+keras libraries

PREPROCESSING:
mean subtraction
	X -= np.mean(X, axis=0)
normalization **recommended
	mean subtraction then divide by standard deviation
	normalizing
PLA + whitening

CROSS VALIDATION
-select between best lambda to minimize loss

for sentiment analysis,
-bag of words adn multinomial Naive Bayes model

FEATURES for trader: <- prob in csv file
mean
variance
std?
volume?
box and whisker chart thing
moving avg/exponential moving avg/infinite impulse response
market price
open, close?
median of open bids and asks
volume in comparison to market size



***look at API again for what CAN get
***want max account value or potential account value after commissions
######
baby steps to end goal as of 7/24:
-write script to get sample data OR find source online
-create templates for different possible models that can be used
-train those models, evaluate based on accuracy, etc on training and test set
-store and pickle them
-find way to integrate with live data from command line ###pretty much MVP
###able to show William at this point
###also see notebook of other notes from earlier this month
ideas from this point:
cronjob/tab to automate pulling data and running scripts? #how long take train though
-find way to put online indeally as a web app, maybe from github where can plot and host
-what to do about server (school servers) or home machine or AWS which are prob necessary
-websocket?
-gurobi help?
 

####################

**clean up embarassing Github repos

MIXED algorithms:
AdaBoost - bunch of "weak" class -> more powerful

func for NN:
-cross entropy (good for classification)
-MSE (good for regression)


for classifiers:
-use score attributes for accuracy?
something like score(X_train, y_train)

diff ways to compute distances:
euclidean
manhattan
minkowski?

##add notes from TODO:
-ML/DL course
-ipython and pdfs from DataX
-see if also TF and Keras model map like the useful scipy one

-see if able to use existing data sources like one on Kaggle or if should write own script
-make trade tests using api
-try dual boot again, else just stick with virtual box
-try gdax setup again?



"""




