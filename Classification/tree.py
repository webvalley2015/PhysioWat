#!/usr/bin/python

import numpy as np # for np arrays and np output file
import matplotlib.pyplot as plt # for understanding the data- testing
from sklearn import tree # for decision tree

# data from processing team- data_mean & data_var are extracted features, we may add more
data_mean = np.load('data_mean.npy') 
data_var = np.load('data_var.npy')

# for plotting
nClass = len(data_mean) # get the length of the array of extracted features
labels = [] # initialize the array of labels (will be 0s or 1s)
nFeatures = [] # initialize a temporary array of features

for i in range(nClass): # for the number of features
	nFeatures.append(len(data_mean[i])) # add the length of the feature data to the nFeatures

N = min(nFeatures) # N is the minimum length of the feature data
nTrain = N / 5 # divide the minimum length of the feature data by five, BUT WHY

#initialize training and testing data arrays
data_rnd = []
dataTrain = [0,0,0,0,0,0]
labelsTrain = [0]
dataTest = [0,0,0,0,0,0]
labelsTest = [0]

for i in range(nClass):
	# randomly select training and testing sub-datasets
	idx = np.arange(N) # idx is an array 0 to the minimum length of data points minus 1
	np.random.seed(13) # use a random seed for improved randomness
	np.random.shuffle(idx) # shuffle the array idx

	tmp = np.hstack([data_mean[i][0:N,:], data_var[i][0:N,:]]) # combine the var and mean arrays column-wise
	data_rnd.append(tmp[idx]) 

	labels.append(np.ones((N)) * (i+1))

	dataTrain = np.vstack([dataTrain, data_rnd[i][0:nTrain,:]])
	#labelsTrain = np.vstack([labelsTrain, labels[i][0:nTrain]])
	labelsTrain = np.append(labelsTrain, labels[i][0:nTrain])
	
	dataTest = np.vstack([dataTest, data_rnd[i][nTrain+1:-1,:]])
	#labelsTest = np.vstack([labelsTest, labels[i][nTrain+1:-1]])
	labelsTest = np.append(labelsTest, labels[i][nTrain+1:-1])

dataTrain = dataTrain[1:-1,:]
labelsTrain = labelsTrain[1:-1]
dataTest = dataTest[1:-1,:]
labelsTest = labelsTest[1:-1]

# create figure and plot data
fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax1.plot(dataTrain)
ax2 = fig.add_subplot(2,1,2)
ax2.plot(labelsTrain)

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax1.plot(dataTest)
ax2 = fig.add_subplot(2,1,2)
ax2.plot(labelsTest)

# Train
clf = tree.DecisionTreeClassifier()
clf = clf.fit(dataTrain, labelsTrain) # fit the data using training data & labels
labelsPredict = clf.predict(dataTest) # try to predict the labels
score = clf.score(dataTest, labelsTest) # find the accuracy score
print 'Classification Accuracy %f' % score # print out the accuracy score

# Displaying the data, will be deleted later
plt.figure()
plt.plot(range(len(labelsTest)), labelsTest, range(len(labelsPredict)), labelsPredict)

plt.show()

