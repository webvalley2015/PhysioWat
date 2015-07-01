# -*- coding: utf-8 -*-
"""
Created on Wed Jul 1 15:42:22 2015

@author: flavio
"""
'''
function for extract IBI from EKG
'''

import numpy as np
import matplotlib.pyplot as plt
#import filters as ourFilters
import tools as ourTools


def analyzeEKG(filename, SAMP_F):
    '''
    this function get the EKG from a file and returns a IBI
    return: the IBI (in s) extracted from the EKG in filename
    filename: the full name of the file that contains the EKG
    SAMP_F: the sapling frequency of the data
    '''
    #load data from the file
    rawdata = np.genfromtxt(filename, delimiter=',', skip_header = 8)[:,1]
    #downsampling
        #funzione per il downsampling
    return ourTools.getIBI(rawdata, SAMP_F, 0.2)


#Simulate server
if __name__ == '__main__':
    path = "/home/flavio/Work/PhysioWat/robaNoGit/data/Nicola's_data/"
    fileName = "EKG_F01_F.txt"

    SAMPLING_FREQ = 256
    
    ibi = analyzeEKG(path+fileName, SAMPLING_FREQ)
    print ibi
    plt.plot(ibi.index, ibi.IBI)
    plt.show()