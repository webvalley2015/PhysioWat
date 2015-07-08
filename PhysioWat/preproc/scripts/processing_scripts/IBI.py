from __future__ import division
import numpy as np
from tools import peakdet, get_row_for_col, selectCol as selcol

#####################################
## NOTE
# PSD estimation: AR method
# INTERPOLATION: cubic spline
# ! ! !
# RR in milliseconds!
#####################################

def calculateHRVindexes(RR):
    '''
    funzione per calcolare le features di una finestra di IBI
    RR: frammento di IBI (in s) come array (N,)
    return: array numpy di numeri (le features) ed eventualmente un array di labels
    '''
    TDindexes, TDlabels=calculateTDindexes(RR*1000) # TD indexes
    
    Indexes=np.hstack((TDindexes))
    return Indexes


def extract_IBI_features(data, cols, windows, labels):
    '''
    exetract the features  from an IBI with passed windows
    return: np.array containing the features of each window, the new labels (removes the ones corresponding to empty windows)
    data: the data from which extract the features, passed as a numpy array (N,2) with time and values in the two columns
    windows: numpy array containing the start and the end point (in time) of every windows
    labels: np.array containing the labels
    cols: the column labels
    '''
    result = []
    res_labels = labels
    times = selcol(data, cols, "TIME")
    values = selcol(data, cols, "IBI")
    for tindex in xrange(len(windows)):
        startt = windows[tindex][0]
        endt = windows[tindex][1]
        this_win = values[(times >= startt)&(times < endt)]
        if this_win.size == 0:
            res_labels.pop(tindex)
        result.append(calculateHRVindexes(this_win))
    return np.nan_to_num(result), res_labels


def getPeaksIBI(signal, cols, peakDelta, s_type):
    '''
    get the peaks for the ibi calculation
    return: an nparrays (N,3), containing in order the time (in s), the height of the peak and the lables and the column names
    signal: signal as np.array (N,3) in which search the peaks (columns: timestamp, signal, labels)
    peakDelta: minimum peak height
    SAMP_F: the sampling frequency of signal
    cols: the column labels
    s_type=signal type: BVP or GSR
    '''
    timed_lbls = selcol(signal, cols, ["TIME", "LAB"])
    t = selcol(signal, cols,  "TIME")
    signal_vals = selcol(signal ,cols, s_type)
    maxp, minp = peakdet(signal_vals, peakDelta, t)
    new_lbls = get_row_for_col(timed_lbls, maxp[:,0])[:,1]
    cols_out=["TIME", "PEAK", "LAB"]
    return np.column_stack((maxp, new_lbls)), cols_out

def max2interval(peaks, cols,  minrate=40, maxrate=200):
    """
    Returns intervals from timesMax, after filtering possible artefacts based on rate range (rates in min^(-1))
    if two peaks are nearer than minrate or further than maxrate, the algorithm try to recognize if there's a false true or a peak missing
    return: an nparray (N,3) containing in order the time, the ibi and the label
    peaks: an nparray (N,3) containing in order the timestamp, the height and the label of each peak
    minrate: represents the minimum(in min^(-1)) bpm to detect
    maxrate: represents the maximum(in min^(-1)) bpm to detect
    """
    maxRR=60/minrate
    minRR=60/maxrate

    RR=[]
    timeRR=[]

    # algoritmo alternativo
    # beat artifacts correction
    ##inizializzazioni
    timed_lbls = selcol(peaks, cols, ["TIME", "LAB"])
    peaks_time = selcol(peaks, cols, "TIME")
    
    tprev=peaks_time[0]
    tfalse=tprev

    for i in range(1, len(peaks_time)):
        tact=peaks_time[i]

        RRcurr=tact-tprev
        if (RRcurr<minRR): # troppo breve: falso picco?
            tfalse=tact  #aspetto (non aggiorno tact) e salvo il falso campione

        elif RRcurr>maxRR: # troppo lungo ho perso un picco?
            RRcurr=tact-tfalse # provo con l'ultimo falso picco se esiste
            tprev=tact # dopo ripartiro' da questo picco

        if RRcurr>minRR and RRcurr<maxRR: # tutto OK
            RR.append(RRcurr) #aggiungo valore RR
            timeRR.append(tact) #aggiungo istante temporale
            tfalse=tact #aggiorno falso picco
            tprev=tact #aggiorno tprev
    #calculates the labels foreach time in timeRR
    try:
        labelRR = get_row_for_col(timed_lbls, timeRR)[:,1]
    except IndexError as e:
        print "NO LABELS: ", e.message
        labelRR=np.array([])
        pass
    #the result contains a 2D array with the times and the ibi
    return np.column_stack((timeRR, RR, labelRR)), ["TIME", "IBI", "LAB"]


def calculateTDindexes(RR):
    #calculates Time domain indexes
    RRmean=np.mean(RR)
    RRSTD= np.std(RR)            
    
    RRDiffs=np.diff(RR) 
        
    RRDiffs50 = [x for x in np.abs(RRDiffs) if x>50]
    pNN50=100.0*len(RRDiffs50)/len(RRDiffs)
    RRDiffs25 = [x for x in np.abs(RRDiffs) if x>25]
    pNN25=100.0*len(RRDiffs25)/len(RRDiffs)
    RRDiffs10 = [x for x in np.abs(RRDiffs) if x>10]
    pNN10=100.0*len(RRDiffs10)/len(RRDiffs)
    
    RMSSD = np.sqrt(sum(RRDiffs**2)/(len(RRDiffs)-1))
    SDSD = np.std(RRDiffs)

    labels= np.array(['RRmean', 'RRSTD', 'pNN50', 'pNN25', 'pNN10', 'RMSSD', 'SDSD'], dtype='S10')
    
    return [RRmean, RRSTD, pNN50, pNN25, pNN10, RMSSD,  SDSD], labels
