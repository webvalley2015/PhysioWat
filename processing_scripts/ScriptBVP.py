# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 17:56:22 2015

@author: flavio & Andrea
"""
'''
function for BVP only
'''
from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import filters as ourFilters
import tools as t

if __name__ == '__main__':
    
    
    path = '/home/andrea/Work/data/Physio/data/SUB100/SUB100/Empatica E4/'
    fileName = 'BVP.csv'
    SAMPLING_FREQ = 64


    data = pd.DataFrame.from_csv(path+fileName, sep=';')
    #plt.plot(data.index, data.BVP)
    datanp= data.as_matrix().reshape(data.shape[0])

    t = np.arange(0, len(datanp)/SAMPLING_FREQ, 1/SAMPLING_FREQ)  
    ppg_filtered = ourFilters.filterSignal(datanp, SAMPLING_FREQ)

    #plt.plot(data.index, ppg_filtered)
    #plt.show()

    
    # estimating peaks and IBI
    maxp, minp = pkd.peakdet(-ppg_filtered, 100, t)
    
    #plt.plot(t_orig, -ppg_filtered)
    #plt.plot(maxp[:,0], maxp[:,1], 'o')
    
    IBI, tIBI = pkd.max2interval(maxp[:,0], 40, 180)
    ibi = pd.DataFrame(IBI, index = tIBI, columns=['IBI'])
    
    #plt.figure(2)
    #ax1 = plt.subplot(211)
    #plt.plot(t_orig, -ppg_filtered)
    #plt.plot(maxp[:,0], maxp[:,1], '^r')
    #plt.vlines(tIBI, np.min(-ppg_filtered), np.max(-ppg_filtered), 'lightgray')
    
    #plt.grid()
    #plt.subplot(212, sharex=ax1)
    #plt.plot(ibi.index, ibi.IBI, 'o')
    #plt.vlines(tIBI, np.min(ibi.IBI), np.max(ibi.IBI), 'lightgray')
    #plt.grid()
    #plt.show()
    
    plt.figure(3)
    plt.plot(t_orig, B.Temp)
    plt.grid()
    plt.show()
