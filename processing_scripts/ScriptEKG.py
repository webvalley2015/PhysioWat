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
import filters as ourFilters
import tools as ourTools

def loadEKG(filename):
    '''
    DEBUG ONLY. This will be done by the server
    reads the data of a EKG from a file (full path and name in filename) like Nicola's ones
    '''
    return np.genfromtxt(filename, delimiter=',', skip_header = 8)[:,1]


#Simulate user app
if __name__ == '__main__':
    #user insertion, the path is substituted with database source
    path = "/home/flavio/Work/PhysioWat/robaNoGit/data/Nicola's_data/"
    fileName = "EKG_F01_F.txt"
    SAMP_F = 256
    
    #load data from the file
    rawdata = loadEKG(path + fileName)
    
    #downsampling
    #the user selects the parameters, with default suggested
    downsampling_ratio = 1
    new_f = SAMP_F / float(downsampling_ratio)
    downsampled_data = ourTools.downsampling(rawdata, SAMP_F, new_f)
    
    #filter
    #the user selects the parameters, with default suggested
    filterType = None
    F_PASS = 0
    F_STOP = 0
    ILOSS = 0
    IATT = 0
    filtered_signal = ourFilters.filterSignal(downsampled_data, SAMP_F, passFr = F_PASS, stopFr = F_STOP, LOSS = ILOSS, ATTENUATION = IATT, filterType = filterType)
    
    #extraction of IBI from preprocessed signal
    #the user selects the parameters, with default suggested
    delta = 0.2
    ibi = ourTools.getIBI(rawdata, SAMP_F, delta)
    
    #DEBUG output
    print ibi
    plt.plot(ibi.index, ibi.IBI)
    plt.show()