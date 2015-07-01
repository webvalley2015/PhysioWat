# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 17:56:22 2015

@author: flavio & Andrea
"""
'''
function for BVP only
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import filters as ourFilters
import tools as ourTools

def getIBI (signal, SAMP_F):
    '''
    this function calculates the IBI on a BVP filtered graph
    return: a pd DataFrame containing the inter-beat interval (in s) indexed with time
    signal: the filtered BVP signal
    SAMP_F: the sampling frequency of the data
    '''
    # estimating peaks and IBI
    t = np.arange(0, len(signal)/float(SAMP_F), 1.0/SAMP_F)
    maxp, minp = ourTools.peakdet(signal, 1, t)

    IBI, tIBI = ourTools.max2interval(maxp[:,0], 40, 180)
    #ibi contains the Inter-Beat interval between two beats, indexed with the time of the beats
    ibi = pd.DataFrame(IBI, index = tIBI, columns=['IBI'])
    return ibi


def analyzeBVP(filename, SAMP_F, filterType = 'butter'):
    '''
    this function get the BVP from a file and returns a IBI. The filters paramateres are passed
    return: the IBI (in s) extracted from the BVP in filename
    filename: the full name of the file that contains the BVP
    SAMP_F: the sapling frequency of the data
    '''
    #load data from the file
    datanp = np.genfromtxt(path+fileName, delimiter=';', skip_header = 1)[:,1]
    #filter the signal
    #filterSignal (SIGNAL ,smp_fr, passFr = 2, stopFr = 6, filterType = 'butter'):
    filtered_signal = ourFilters.filterSignal(datanp, SAMPLING_FREQ, filterType = filterType)
    return getIBI(filtered_signal, SAMP_F)


#Simulate server
if __name__ == '__main__':
    path = '/home/flavio/Work/PhysioWat/robaNoGit/data/SUB100/SUB100/Empatica_E4/'
    fileName = 'BVP.csv'
    SAMPLING_FREQ = 64

    ibi = analyzeBVP(path+fileName, SAMPLING_FREQ)
    plt.plot(ibi.index, ibi.IBI)
    plt.show()

