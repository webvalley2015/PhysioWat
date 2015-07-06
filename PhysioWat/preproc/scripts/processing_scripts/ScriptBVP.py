"""
Created on Tue Jun 30 17:56:22 2015

@author: flavio & Andrea
"""
'''
function for extract IBI from BVP
'''

import numpy as np
# import matplotlib.pyplot as plt
import filters as ourFilters
import IBI
import windowing
import tools

def loadBVP(filename):
    '''
    DEBUG ONLY. This will be done by the server
    reads the data of a BVP from a file (full path and name in filename) like Emaptica_E4 ones
    '''
    a = np.genfromtxt(filename, delimiter=',', skip_header = 1)
    return a

#Simulate users app
if __name__ == '__main__':
    #user insertion, the path is substituted with database source
    # path = '/home/flavio/Work/PhysioWat/robaNoGit/data/SUB100/SUB100/Empatica_E4/'
    fileName = './data/BVP.csv'
    SAMP_F = 64

    #load data from the file
    rawdata = loadBVP(fileName)
    
    #filter the signal
    #the user selects the parameters, with default suggested
    filterType = 'butter'
    F_PASS = 2
    F_STOP = 6
    ILOSS = 0.1
    IATT = 40
    filtered_signal = ourFilters.filterSignal(rawdata[:,1], SAMP_F, passFr = F_PASS, stopFr = F_STOP, LOSS = ILOSS, ATTENUATION = IATT, filterType = filterType)

    #compact timestamp, signal and labels for the next processes
    total_signal = np.column_stack((rawdata[:,0], filtered_signal, rawdata[:,2]))
    
    #extraction peaks from the signal
    #the user selects the parameters, with default suggested
    delta = 1
    peaks = IBI.getPeaksIBI(total_signal,SAMP_F, delta)
    #calculation of the IBI
    #the user selects the parameters, with default suggested
    minFr = 40
    maxFr = 200
    ibi = IBI.max2interval(peaks, minFr, maxFr)

    tools.array_labels_to_csv(ibi, np.array(["timestamp", "IBI", "lables"]), "./output/preproc_"+fileName[7:-4]+".csv")


    #-----FEATURES EXTRACTION-----
    timestamp = ibi[:,0]
    timed_vals = ibi[:,[0,1]]
    lbls = ibi[:,2]
    winds, lbls = windowing.get_windows_contiguos(timestamp, lbls, 100, 50)

    feat, lbls = IBI.extract_IBI_features(timed_vals, winds, lbls)

    feat_col=np.array(['RRmean', 'RRSTD', 'pNN50', 'pNN25', 'pNN10', 'RMSSD', 'SDSD'])

    tools.array_labels_to_csv(feat, feat_col, "./output/feat_"+fileName[7:-4]+".csv")