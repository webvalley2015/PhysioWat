# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 17:56:22 2015

@author: flavio & Andrea
"""
'''
function for extract IBI from BVP
'''

import numpy as np
import matplotlib.pyplot as plt
import filters as ourFilters
import tools as ourTools


def analyzeBVP(filename, SAMP_F, filterType = 'butter'):
    '''
    this function get the BVP from a file and returns a IBI. The filters paramateres are passed
    return: the IBI (in s) extracted from the BVP in filename
    filename: the full name of the file that contains the BVP
    SAMP_F: the sapling frequency of the data
    filterType: (default 'butter') the type of the filter to use
    '''
    #load data from the file
    rawdata = np.genfromtxt(filename, delimiter=';', skip_header = 1)[:,1]
    #filter the signal
    #filterSignal (SIGNAL ,smp_fr, passFr = 2, stopFr = 6, filterType = 'butter'):
    filtered_signal = ourFilters.filterSignal(rawdata, SAMPLING_FREQ, filterType = filterType)
    return ourTools.getIBI(filtered_signal, SAMP_F, 1)


#Simulate server
if __name__ == '__main__':
    path = '/home/flavio/Work/PhysioWat/robaNoGit/data/SUB100/SUB100/Empatica_E4/'
    fileName = 'BVP.csv'
    SAMPLING_FREQ = 64

    ibi = analyzeBVP(path+fileName, SAMPLING_FREQ)
    print ibi
    plt.plot(ibi.index, ibi.IBI)
    plt.show()

