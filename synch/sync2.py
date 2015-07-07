import numpy as np
from numpy import array, zeros, argmin, inf
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import csv 
import mlpy
from numpy.linalg import norm
import matplotlib.pyplot as plt
import matplotlib.cm as cm
'''
correlation between GSR_F/EKG_F and GSR_M/EKG_M features extracted by pre-processing team
'''

def cut(df,df2):                                    #cutting array features to have two datasets of features with the same number of rows
    f1 = np.genfromtxt(df, delimiter=',')
    f2 = np.genfromtxt(df2,delimiter=',') 
    if len(f1) > len(f2):  
        l = len(f2)
        f1 = f1[:l,:]
    else :
        l = len(f1)
        f2 = f2[:l,:]
    return f1, f2
        
        
def correlate_features(df, df2):                                      #correlate of the features for sync
    features=[]
    df, df2 = cut(df,df2)
    for i in range(4):                                                   
	    features.append(spearmanr(df[:, i], df2[:, i]))
    print np.array(features)
    plt.plot(np.array(features))
    plt.show()
    return features

def downsampling(d):                   #downsampling of the data
    t= d[:,0]
    f_samp= 256
    f_new= 1
    n_samp= f_samp/f_new
    indexes= np.arange(len(d))
    keep= (indexes%n_samp == 0)
    gsr= np.array(d[keep])
    t_gsr= t[keep]
    return gsr 

def dtw(x,y):
    x=np.genfromtxt(x, delimiter=',')                             #DTW correlate between two signals to calculate the distance
    y=np.genfromtxt(y, delimiter=',')
    x = downsampling(x)
    y = downsampling(y)
    x= x[:,1]
    y= y[:,1]
    x= (x- np.mean(x)) / np.std(x)
    y= (y- np.mean(y)) / np.std(y)
    plt.plot(x)
    plt.plot(y)
    plt.show()
    dist, cost, path = mlpy.dtw_std(x, y, dist_only=False)
    print np.array(dist)
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    plot1 = plt.imshow(cost.T, origin='lower', cmap=cm.gray, interpolation='nearest')
    plot2 = plt.plot(path[0], path[1], 'w')
    xlim = ax.set_xlim((-0.5, cost.shape[0]-0.5))
    ylim = ax.set_ylim((-0.5, cost.shape[1]-0.5))
    plt.show()
    return dist

                              

if __name__=="__main__":
    cross_result = correlate_features(df, df2)
    a= dtw(x,y)
    print cross_result, a
	
