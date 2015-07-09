import numpy as np
from numpy import array, zeros, argmin, inf
import matplotlib.pyplot as plt
import csv 
import mlpy
from numpy.linalg import norm
import matplotlib.pyplot as plt
import matplotlib.cm as cm
'''
script of DTW between signals no stimuli

''' 

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

def dtw(x,y, labels):
    #x=np.genfromtxt(x, delimiter=',',skip_header=True)                             #DTW correlate between two signals to calculate the distance
    #y=np.genfromtxt(y, delimiter=',',skip_header=True)
    #x = downsampling(x)
    #y = downsampling(y)
    #x= x[:,3]
    #y= y[:,3]
    #x= (x- np.mean(x)) / np.std(x)
    #y= (y- np.mean(y)) / np.std(y)
    #plt.plot(x)
    #plt.plot(y)
    if labels > 0: 
        dist, cost, path = mlpy.dtw_std(x, y, dist_only=False)
        dist = dist / len(x)
    print np.array(dist)
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    plot1 = plt.imshow(cost.T, origin='lower', cmap=cm.gray, interpolation='nearest')
    plot2 = plt.plot(path[0], path[1], 'w')
    xlim = ax.set_xlim((-0.5, cost.shape[0]-0.5))
    ylim = ax.set_ylim((-0.5, cost.shape[1]-0.5))
    plt.show()
    return dist, labels

if __name__=="__main__":
    a= dtw(x,y)
    print a
	
