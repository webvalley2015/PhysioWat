#!/usr/bin/python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

fs = 50.0;
dT = 1.0/fs;

data_mean = np.load('data_mean.npy')
data_var = np.load('data_var.npy')

nClass = len(data_mean)

labels = []
nFeatures = []

for i in range(nClass):
	
	# labels for the different activities	
	# labels.append(np.ones((len(data_mean[i]),1)) * (i+1))
	
	nFeatures.append(len(data_mean[i]))
	
# end for i

N = min(nFeatures)

nTrain = N / 5

data_rnd = []
dataTrain = [0, 0, 0, 0, 0, 0]
labelsTrain = [0]
dataTest = [0, 0, 0, 0, 0, 0]
labelsTest = [0]

for i in range(nClass):
	
	idx = np.arange(N)
	np.random.seed(13)
	np.random.shuffle(idx)

	tmp = np.hstack([data_mean[i][0:N,:], data_var[i][0:N,:]])
	data_rnd.append(tmp[idx])

	labels.append(np.ones((N)) * (i+1))

	dataTrain = np.vstack([dataTrain, data_rnd[i][0:nTrain,:]])
	#labelsTrain = np.vstack([labelsTrain, labels[i][0:nTrain]])
	labelsTrain = np.append(labelsTrain, labels[i][0:nTrain])
	
	dataTest = np.vstack([dataTest, data_rnd[i][nTrain+1:-1,:]])
	#labelsTest = np.vstack([labelsTest, labels[i][nTrain+1:-1]])
	labelsTest = np.append(labelsTest, labels[i][nTrain+1:-1])
	
# end for i

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

clf = RandomForestClassifier(n_jobs=2)

# Train
clf = clf.fit(dataTrain, labelsTrain)

labelsPredict = clf.predict(dataTest)

score = clf.score(dataTest, labelsTest)

print 'Classification Accuracy %f' % score

plt.figure()
plt.plot(range(len(labelsTest)), labelsTest, range(len(labelsPredict)), labelsPredict)

plt.show()

