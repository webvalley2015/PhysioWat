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

def loadBVP(filename):
    '''
    DEBUG ONLY. This will be done by the server
    reads the data of a BVP from a file (full path and name in filename) like Emaptica_E4 ones
    '''
    return np.genfromtxt(filename, delimiter=';', skip_header = 1)[:,1]

#Simulate users app
if __name__ == '__main__':
    #user insertion, the path is substituted with database source
    path = '/home/flavio/Work/PhysioWat/robaNoGit/data/SUB100/SUB100/Empatica_E4/'
    fileName = 'BVP.csv'
    SAMP_F = 64

    #load data from the file
    rawdata = loadBVP(path + fileName)
    
    #filter the signal
    #the user selects the parameters, with default suggested
    filterType = 'butter'
    F_PASS = 2
    F_STOP = 6
    ILOSS = 0.1
    IATT = 40
    filtered_signal = ourFilters.filterSignal(rawdata, SAMP_F, passFr = F_PASS, stopFr = F_STOP, LOSS = ILOSS, ATTENUATION = IATT, filterType = filterType)
    
    #get the IBI from the filtered signal
    #the user selects the parameters, with default suggested
    delta = 1
    minFr = 40
    maxFr = 200
    ibi = ourTools.getIBI(filtered_signal, SAMP_F, delta, minFr, maxFr)
    
    #DEBUG output
    print ibi
    plt.plot(ibi.index, ibi.IBI)
    plt.show()

