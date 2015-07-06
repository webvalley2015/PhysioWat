'''
function for extract IBI from EKG
'''

import numpy as np
import filters as ourFilters
import tools as ourTools
import IBI
import windowing

def loadEKG(filename):
    '''
    DEBUG ONLY. This will be done by the server
    reads the data of a EKG from a file (full path and name in filename) like Nicola's ones
    '''
    a = np.genfromtxt(filename, delimiter=',', skip_header = 8)
    return a


#Simulate user app
if __name__ == '__main__':
    #user insertion, the path is substituted with database source
    # path = "/home/flavio/Work/PhysioWat/robaNoGit/data/Nicolasdata/"
    fileName = "./data/EKG_F01_M.csv"
    SAMP_F = 256
    
    #load data from the file
    rawdata = loadEKG(fileName)
    #SAMP_F = int(round(1/(rawdata[1,0]-rawdata[0,0]))) se i dati di Nicola non avessero il timestamp buggato
    
    #downsampling
    #the user selects the parameters, with default suggested
    new_f = SAMP_F
    downsampled_data = ourTools.downsampling(rawdata, SAMP_F, new_f)
    
    #filter
    #the user selects the parameters, with default suggested
    filterType = None
    F_PASS = 0
    F_STOP = 0
    ILOSS = 0
    IATT = 0
    filtered_signal = ourFilters.filterSignal(downsampled_data[:,1], SAMP_F, passFr = F_PASS, stopFr = F_STOP, LOSS = ILOSS, ATTENUATION = IATT, filterType = filterType)
    
    #compact timestamp, signal and labels for the next processes
    #DEBUG ONLY, create a new ideal timestamp
    temp_ts = np.arange(0, rawdata.shape[0]/SAMP_F, 1.0/SAMP_F)

    total_signal = np.column_stack((temp_ts, filtered_signal, downsampled_data[:,2]))

    
    #extraction peaks from the signal
    #the user selects the parameters, with default suggested
    delta = 0.2
    peaks = IBI.getPeaksIBI(total_signal,SAMP_F, delta)
    
    #calculation of the IBI
    #the user selects the parameters, with default suggested
    minFr = 40
    maxFr = 200
    ibi = IBI.max2interval(peaks, minFr, maxFr)

    ourTools.array_labels_to_csv(ibi, np.array(["timestamp", "IBI", "labels"]), "./output/preproc_"+fileName[7:-4]+".csv")

    #-----FEATURES EXTRACTION-----

    lbls = np.array([0 for i in ibi[:,0]])
    winds, lbls = windowing.get_windows_contiguos(ibi[:,0], lbls, 100, 50)

    feat, lbls = IBI.extract_IBI_features(ibi, winds, lbls)
    feat_col=np.array(['RRmean', 'RRSTD', 'pNN50', 'pNN25', 'pNN10', 'RMSSD', 'SDSD'])

    ourTools.array_labels_to_csv(feat, feat_col, "./output/feat_"+fileName[7:-4]+".csv")
