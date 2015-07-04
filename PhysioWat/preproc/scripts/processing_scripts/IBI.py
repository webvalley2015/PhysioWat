from __future__ import division
import numpy as np
import tools as ourTools

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


def extract_IBI_features(data, windows, labels):
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
        #print startt
        endt = windows[tindex][1]
        #print endt
        this_win = values[(times >= startt)&(times < endt)]
        if this_win.size == 0:
            res_labels.pop(tindex)
        result.append(calculateHRVindexes(this_win))
    return np.nan_to_num(result), res_labels


def getPeaksIBI(signal, SAMP_F, peakDelta):
    '''
    get the peaks for the ibi calculation
    return: an nparrays (N,2), containing the time (in s) in the first column and the height of the peak in the second column
    signal: signal in which search the peaks
    peakDelta: minimum peak height
    SAMP_F: the sampling frequency of signal
    '''
    t = np.arange(0, len(signal)/float(SAMP_F), 1.0/SAMP_F)
    maxp, minp = ourTools.peakdet(signal, peakDelta, t)
    '''print 'maxp:'
    print maxp
    plt.plot(t, signal)
    plt.plot(maxp[:,0], maxp[:,1], 'o')
    plt.show()'''
    return maxp

def max2interval(peaks, minrate=40, maxrate=200):
    """
    Returns intervals from timesMax, after filtering possible artefacts based on rate range (rates in min^(-1))
    if two peaks are nearer than minrate or further than maxrate, the algorithm try to recognize if there's a false true or a peak missing
    return: an nparray (N,2) containing the time in the first column and the ibi in the second
    peaks: an nparray (N,) containing the time of the peaks in the first column
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

    tprev=peaks[0]
    tfalse=tprev

    for i in range(1, len(peaks)):
        tact=peaks[i]

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
    #the result contains a 2D array with the times and the ibi
    return np.column_stack(( np.array(timeRR), np.array(RR)))


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
