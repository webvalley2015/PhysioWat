'''
Functions for EMG only
'''
from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

import myUtilities.sk_tools as sk
import myUtilities.filters as flt
import myUtilities.peak_detection as pkd
import myUtilities.ABP_utilities as abp
import myUtilities.windowing as wnd
import myUtilities.IBI_features as hrv

def remove_spikes_EMG(emg, trg):
    import myUtilities.filters as flt
    
    def maxmin(x):
        return((x - np.min(x))/(np.max(x) - np.min(x)))
        
    trg = trg - trg[0]
    trg[trg<0] = 0
    trg = maxmin(trg)
    trg[trg<0.01]=0
    trg = abs(np.diff(trg))
    TH=0.002
    trg_expanded = flt.smoothGaussian(trg, 12)
    trg_to_remove = np.where(trg_expanded > TH)[0] + 12
    trg_to_remove = trg_to_remove[trg_to_remove<len(emg)]
    #trg_expanded = (trg_expanded - np.min(trg_expanded)) / (np.max(trg_expanded) - np.min(trg_expanded))
    emg[trg_to_remove]= np.mean(emg)
    return(emg)

def EMGindexes(emg):
    """
    FEATURES = EMGindexes(emg)

    Returns a dict of labeled features.
    """
    # simple features
    features = {'emg_max': np.max(emg), 'emg_min' : np.min(emg), 'emg_mean' : np.mean(emg), 'emg_std' : np.std(emg), 'emg_auc' : np.sum(emg)/len(emg), 'emg_range' : (np.max(emg) - np.min(emg))}
    return features

def extract_EMG_features(data, windows, labels):
    '''
    exetract the features  from an IBI with passed windows
    return: np.array containing the features of each window, the new labels (removes the ones corresponding to empty windows)
    data: the data from which extract the features, passed as a numpy array (N,2) with time and values in the two columns
    windows: numpy array containing the start and the end point (in time) of every windows
    labels: np.array containing the labels
    '''
    result = []
    res_labels = labels
    times = data[:,0]
    values = data[:,1]
    for tindex in xrange(len(windows)):
        startt = windows[tindex][0]
        endt = windows[tindex][1]
        this_win = values[(times >= startt)&(times < endt)]
        if this_win.size == 0:
            res_labels.pop(tindex)
        result.append(EMGindexes(this_win))
    return result, res_labels