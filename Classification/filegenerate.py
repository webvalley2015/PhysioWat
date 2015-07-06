#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import pickle
import scipy.integrate
from sklearn import ensemble

def newfunc(wh, start, end):
    duration = start - end
    max = np.amax(wh) * abs(duration)
    min = np.amin(wh) * abs(duration)
    steps = abs(duration / len(wh))
    axis = np.arange(start, end, steps)
    while len(wh) != len(axis):
        if len(wh) > len(axis): 
            #print 'add'
            axis = np.append(axis, (axis[len(axis)-1] + steps))
        elif len(wh) < len(axis): 
            #print 'remove'
            axis = np.delete(axis, (len(axis) - 1))
        #print str(len(wh)) + ' ' +  str(len(axis))
        
    totar = 0
    for val in range(len(wh)):
        wh[val] = abs(wh[val])
    if max < 0 and min < 0:
        va = min - max
        tarea = scipy.integrate.simps(wh, axis)
        tarea = min + tarea
        totar = abs(va) - tarea
    elif max > 0 and min < 0:
        va = max - min
        tarea = scipy.integrate.simps(wh, axis)
        totar = abs(va) -  tarea
    elif max > 0 and min > 0:
        va = max - min
        tarea = scipy.integrate.simps(wh, axis)
        tarea = tarea - min
        totar = abs(va) - tarea
    return totar

if True:
    fs = 50.0;
    dT = 1.0 / fs;
    
    filenames = ['claire_ASD.txt', 'standing.txt']
    labels = ['ASD', 'control']

    N = len(filenames)
    WINDOW_SIZE = 100
    STEP = 100

    data_all = []
    data_mean = []
    data_var = []
    data_combined = [0,0,0]
    data_mean_combined = [0,0,0]
    data_var_combined = [0,0,0]

    for i in range(N):
        data_all.append(np.loadtxt(filenames[i], delimiter=',', usecols=(2, 3, 4)))
        data_combined = np.vstack([data_combined, data_all[i]])

	
        [row, col] = data_all[i].shape
	
        _mean = np.zeros((len(range(0, row, STEP)), col))
        _var = np.zeros((len(range(0, row, STEP)), col))
	
        for i_col in range(col):
		
            ind = 0
		
            for i_row in range(0, row, STEP):
	
                # compute mean of window elements
                _var[ind, i_col] = newfunc(data_all[i][i_row:i_row + WINDOW_SIZE-1, i_col], i_row, i_row + WINDOW_SIZE-1)
                _mean[ind, i_col] = np.mean(data_all[i][i_row:i_row + WINDOW_SIZE-1, i_col])
            # end for i_row
		
        # end for i_col
		
        data_mean.append(_mean)
        data_mean_combined = np.vstack([data_mean_combined, data_mean[i]])
	
        data_var.append(_var)
        data_var_combined = np.vstack([data_var_combined, data_var[i]])
    # end for i

    np.save('data_mean', data_mean)
    np.save('data_var', data_var)

    data_combined = data_combined[1:-1,:]
    data_mean_combined = data_mean_combined[1:-1,:]
    data_var_combined = data_var_combined[1:-1,:]

    plt.figure()
    plt.plot(data_combined)

    plt.figure()
    plt.plot(data_mean_combined)

    plt.figure()
    plt.plot(data_var_combined)
    

