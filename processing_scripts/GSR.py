'''
Functions for GSR only
'''
from __future__ import division
import numpy as np
import scipy.signal as spy
from tools import peakdet, gen_bateman
from filters import smoothGaussian
from scipy.interpolate import interp1d
import pandas as pd
import matplotlib.pyplot as plt


def estimate_drivers(t_gsr, gsr, T1, T2, MX, DELTA_PEAK, FS=None):
    """
    TIME_DRV, DRV, PH_DRV, TN_DRV = estimate_drivers(TIME_GSR, GSR, T1, T2, MX, DELTA_PEAK):

    Estimates the various driving components of a GSR signal.
    The IRF is a bateman function defined by the gen_bateman function.
    T1, T2, MX and DELTA_PEAK are modificable parameters (optimal 0.75, 2, 1, 0.02)
    """
    if FS==None:
        FS = 1/( t_gsr[1] - t_gsr[0])

    #======================
    # step 1: DECONVOLUTION
    #======================

    # generating bateman function and tailored gsr
    bateman, t_bat, gsr_in = gen_bateman(MX, T1, T2, FS, gsr)
    L =len(bateman[0:np.argmax(bateman)])
    # deconvolution
    driver, residuals=spy.deconvolve(gsr_in, bateman)
    driver = driver * FS
    # gaussian smoothing (s=200 ms)
    degree = int(np.ceil(0.2*FS))
    driver=smoothGaussian(driver, degree)

    # generating times
    t_driver = np.arange(-L/FS, -L/FS+len(driver)/FS, 1/FS) + t_gsr[0]

    driver = driver[L*2:]
    t_driver = t_driver[L*2:]

    #======================
    # step 2: IDENTIFICATION OF INTER IMPULSE SECTIONS
    #======================
    # peak detection
    # we will use "our" peakdet algorithm
#    DELTA_PEAK = np.median(abs(np.diff(driver, n=2)))
    max_driv, min_driv_temp = peakdet(driver, DELTA_PEAK)

    DELTA_MIN = DELTA_PEAK/4
    max_driv_temp, min_driv = peakdet(driver, DELTA_MIN)

    # check alternance algorithm based on mean>0
    maxmin=np.zeros(len(driver))
    maxmin[(max_driv[:,0]).astype(np.uint32)] =  1
    maxmin[(min_driv[:,0]).astype(np.uint32)] = -1

    '''
                OLD CODE
    index=2
    prev=1
    markers= np.zeros(len(driver))
    while (index<len(maxmin)):
        if maxmin[index]==-1:
            portion = maxmin[prev+1: index-1]
            if np.mean(portion)<=0: # there is not a maximum between two mins
                markers[prev] = markers[prev] + 1
                markers[index] = markers[index] - 1
            prev=index
        index +=1

    start = np.arange(len(markers))[markers==1]
    end = np.arange(len(markers))[markers==-1]

    # create array of interimpulse indexes
    inter_impulse_indexes = np.array([0])
    for i in range(len(start)):
        inter_impulse_indexes = np.r_[inter_impulse_indexes, range(start[i], end[i]+1)]
    inter_impulse_indexes = np.r_[inter_impulse_indexes, len(markers)-1]
    '''
    inter_impulse_indexes, min_idx=get_interpolation_indexes(max_driv, driver, n=5)

    inter_impulse = driver[inter_impulse_indexes.astype(np.uint16)]
    t_inter_impulse = t_driver[inter_impulse_indexes.astype(np.uint16)]

    #======================
    # ESTIMATION OF THE TONIC DRIVER
    #======================
    # interpolation with time grid 10s
    t_inter_impulse_10 = np.arange(t_driver[0], t_driver[-1], 5)

    # estimating values on the time-grid
    inter_impulse_10=np.array([driver[0]])

    for index in range(1, len(t_inter_impulse_10)-1):
        ind_start = np.argmin(abs(t_inter_impulse - t_inter_impulse_10[index-1]))
        ind_end = np.argmin(abs(t_inter_impulse - t_inter_impulse_10[index+1]))

        if ind_end>ind_start:
            value=np.mean(inter_impulse[ind_start:ind_end])
        else:
            value=inter_impulse[ind_start]
        inter_impulse_10 = np.r_[inter_impulse_10, value]

    inter_impulse_10 = np.r_[inter_impulse_10, np.mean(inter_impulse[ind_end:])]

    t_inter_impulse_10  = np.r_[t_inter_impulse_10 , t_driver[-1]]
    inter_impulse_10 = np.r_[inter_impulse_10, driver[-1]]


    f = interp1d(t_inter_impulse_10, inter_impulse_10, kind='cubic')

    tonic_driver = f(t_driver)

    phasic_driver = driver - tonic_driver

    return t_driver, driver, phasic_driver, tonic_driver

def processPSR(pha, t, DELTA):
    """
    pha, maxmin, peaks = processPSR(pha, t, DELTA)

    Process the entire phasic signal iSn order to extract the informations for the subsequently index extraction.
    """
    #==================
    # peak related indexes
    x=np.arange(len(pha))
    max_pha, min_pha = peakdet(pha, DELTA, x)

    # TODO: select max > DELTA

    if len(max_pha)==0 or len(min_pha)==0 :
        print('no peaks found processPSR')
        return pd.DataFrame()

    vector_maxmin = np.zeros(len(pha))
    vector_maxmin[max_pha[:,0].astype(int)] = 1

    vector_maxmin[min_pha[:,0].astype(int)] = -1

    # extract pks durations
    vector_peaks = np.zeros(len(t))
    vector_peaks[pha > DELTA] = 1
    vector_peaks = np.diff(vector_peaks)
    vector_peaks = np.r_[0, vector_peaks]

    pha_processed = pd.DataFrame(np.c_[pha, vector_maxmin, vector_peaks], index = t, columns = ['pha', 'maxmin', 'peaks'])
    return pha_processed

def PSRindexes(pha_processed, plot = False):
    """
    FEATURES = GSRindexes(PHA_PROCESSED)

    Returns a dict of labeled features.
    """
    if len(pha_processed.peaks) == 0: # no peaks
        print('no peaks found PSR indexes')
        return dict()

    pha = np.array(pha_processed.pha)
    maxmin = np.array(pha_processed.maxmin)
    peaks = np.array(pha_processed.peaks)
    t = np.array(pha_processed.index)

    t_max = t[maxmin == 1]
    pha_max = pha[maxmin == 1]

    t_start = t[peaks == 1]

    pha_start = pha[peaks == 1]

    t_end = t[peaks == -1]
#    t_end = np.r_[t_end, t[-1]]

    if plot:
        # plotting
        t_min = t[maxmin == -1]
        #  pha_min = pha[maxmin == -1]

#        pha_end = pha[peaks == -1]
#        pha_end = np.r_[pha_end, pha[-1]]

        plt.plot(t, pha, 'o-b')
        plt.vlines(t_max, min(pha), max(pha), 'r', linewidth = 1.5)
        plt.vlines(t_min, min(pha), max(pha), 'b', linewidth = 1.5)
        plt.vlines(t_start, min(pha), max(pha), 'g')
        plt.vlines(t_end, min(pha), max(pha), 'c')
        #    plt.hlines(DELTA, min(t), max(t), 'k', linewidth = 0.8)
        plt.xlabel('Time [s]')
        plt.grid()
        plt.show()

    # simple features
    features = {'pha_max' : np.max(pha), 'pha_min' : np.min(pha), 'pha_mean' : np.mean(pha), 'pha_std' : np.std(pha), 'pha_auc' : np.sum(pha)/len(pha)}
    # n peaks
    features.update({'n_peak': len(t_max)})

    if len(t_max) == 0:
        features.update({'pks_max' : np.nan, 'pks_min' : np.nan, 'pks_mean' : np.nan})
        features.update({'dur_min' : np.nan, 'dur_max' : np.nan, 'dur_mean' : np.nan})
        features.update({'slp_max' : np.nan, 'slp_min' : np.nan, 'slp_mean' : np.nan})
    else:
        # pks amplitudes
        features.update({'pks_max' : np.max(pha_max), 'pks_min' : np.min(pha_max), 'pks_mean' : np.mean(pha_max)})

        # durations
        i, j = 0, 0
        durations = []
        while i<len(t_start) and j<len(t_end):
            curr_t_start = t_start[i]
            curr_t_end = t_end[j]
            while curr_t_end < curr_t_start and j<len(t_end) - 1:
                j = j + 1
                curr_t_end = t_end[j]

            if curr_t_end > curr_t_start:
                durations.append(curr_t_end - curr_t_start)
            i += 1
            j += 1

        if len(durations) == 0:
            durations = [0]

        features.update({'dur_min' : np.min(durations), 'dur_max' : np.max(durations), 'dur_mean' : np.mean(durations)})

        # slopes
        i, j = 0, 0
        slopes = []
        while i<len(t_start) and j<len(t_max):
            curr_t_start = t_start[i]
            curr_t_max = t_max[j]
            while curr_t_max < curr_t_start and j<len(t_max) - 1:
                j = j + 1
                curr_t_max = t_max[j]

            if curr_t_max > curr_t_start: #missiing max
                curr_pha_start = pha_start[i]
                curr_pha_max = pha_max[j]
                curr_slope = np.sqrt((curr_t_max - curr_t_start)**2 + (curr_pha_max - curr_pha_start)**2)

                slopes.append(curr_slope)
            i += 1
            j += 1

        if len(slopes) == 0:
            slopes=[0]

        features.update({'slp_max' : np.max(slopes), 'slp_min' : np.min(slopes), 'slp_mean' : np.mean(slopes)})

        #compute latency
        latency = t_max[0] - t[0]
        features.update({'latency' : latency})
    return features

def get_interpolation_indexes(maxs, driver, n=3):
    '''
    :param maxs: List of local maximums (peaks)
    :param driver: the function
    :param n: The number of steps (forward or backward)
    :return:The indexes for the interpolation
    '''
    indexes=[]
    L=driver.shape[0]
    for i in range(maxs.shape[0]):
        idx=maxs[i,0]
        start=idx-n
        end=idx+n
        if start<0:
            start=0
        if end>L:
            end=L
        if idx!= start and idx!=end:
            indexes.append((start+np.argmin(driver[start:idx]), idx+np.argmin(driver[idx:end])))

    prev=0
    result=np.array([0])
    for start, end in indexes:
        if prev!=start:
            result=np.r_[result,np.arange(prev, start+1)]
        prev=end
    return result, indexes

def extract_features(pha, WINSTEP=10, WINLEN=80):
    '''
    STEP e LEN in seconds
    :param pha: the phasic dataset
    :param WINSTEP: window step
    :param WINLEN: window length
    :return: features as pandas dataframe
    '''
    feats_all=pd.DataFrame()
    for start in range(0,len(pha.index)-WINLEN, WINSTEP):
        t_start=pha.index[start]
        t_end=t_start+WINLEN/4
        window=pha[t_start:t_end]
        winfeat=pd.DataFrame(PSRindexes(window), index=[t_start])
        feats_all=feats_all.append(winfeat)
    return feats_all

def remove_spikes(data, FSAMP, TH=0.1):
    '''
    Removes annoying spikes
    :param data: data set (no t)
    :param FSAMP: sampling frequency
    :param TH: Threshold
    :return: data, timestamps
    '''
    t = np.arange(len(data)) * 1/FSAMP
    spikes = abs(np.diff(data, FSAMP))
    spikes = smoothGaussian(spikes, round(FSAMP/2))
    indexes_spikes = np.array(np.where(spikes<=TH))[0]
    data_in = data[indexes_spikes]
    t_in = t[indexes_spikes]
    f = interp1d(t_in, data_in)
    t_out = np.arange(t_in[0], t_in[-1], 1/FSAMP)
    data_out = f(t_out)

    return t_out, data_out