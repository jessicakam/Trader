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

FEATURES for trader:
mean
variance
std?
moving volume?
box and whisker chart thing
moving avg/exponential moving avg/infinite impulse response


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

"""