'''
Functions for GSR only
'''
from __future__ import division

import numpy as np
import scipy.signal as spy
from tools import peakdet, gen_bateman, selectCol
from filters import smoothGaussian
from scipy.interpolate import interp1d
# import matplotlib.pyplot as plt

def estimate_drivers(t_gsr, gsr, labs, T1=0.75, T2=2, MX=1, DELTA_PEAK=0.02, k_near=5, grid_size=5, s=0.2):
    """
    TIME_DRV, DRV, PH_DRV, TN_DRV, LABS = estimate_drivers(TIME_GSR, GSR, LABS, T1, T2, MX, DELTA_PEAK):

    Estimates the various driving components of a GSR signal.
    The IRF is a bateman function defined by the gen_bateman function.
    T1, T2, MX and DELTA_PEAK are modificable parameters (optimal 0.75, 2, 1, 0.02)
    k_near and grid_size are optional parameters, relative to the process
    s= t in seconds of gaussian smoothing
    """
    FS = int(round(1/( t_gsr[1] - t_gsr[0])))

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
    degree = int(np.ceil(s*FS))
    driver=smoothGaussian(driver, degree)

    # generating times
    t_driver = np.arange(-L/FS, -L/FS+len(driver)/FS, 1/FS) + t_gsr[0]

    driver = driver[L*2:]
    t_driver = t_driver[L*2:]

    mask=(t_gsr>=t_driver[0])&(t_gsr<=t_driver[-1])
    labs=labs[mask]

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
    inter_impulse_indexes, min_idx=get_interpolation_indexes(max_driv, driver, n=k_near)

    inter_impulse = driver[inter_impulse_indexes.astype(np.uint16)]
    t_inter_impulse = t_driver[inter_impulse_indexes.astype(np.uint16)]

    #======================
    # ESTIMATION OF THE TONIC DRIVER
    #======================
    # interpolation with time grid 10s
    t_inter_impulse_grid = np.arange(t_driver[0], t_driver[-1], grid_size)

    # estimating values on the time-grid
    inter_impulse_10=np.array([driver[0]])

    ind_end=0
    for index in range(1, len(t_inter_impulse_grid)-1):
        ind_start = np.argmin(abs(t_inter_impulse - t_inter_impulse_grid[index-1]))
        ind_end = np.argmin(abs(t_inter_impulse - t_inter_impulse_grid[index+1]))

        if ind_end>ind_start:
            value=np.mean(inter_impulse[ind_start:ind_end])
        else:
            value=inter_impulse[ind_start]
        inter_impulse_10 = np.r_[inter_impulse_10, value]

    inter_impulse_10 = np.r_[inter_impulse_10, np.mean(inter_impulse[ind_end:])]

    t_inter_impulse_grid  = np.r_[t_inter_impulse_grid , t_driver[-1]]
    inter_impulse_10 = np.r_[inter_impulse_10, driver[-1]]


    f = interp1d(t_inter_impulse_grid, inter_impulse_10, kind='cubic')

    tonic_driver = f(t_driver)

    phasic_driver = driver - tonic_driver

    return t_driver, driver, phasic_driver, tonic_driver, labs

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
        return dict()

    vector_maxmin = np.zeros(len(pha))
    vector_maxmin[max_pha[:,0].astype(int)] = 1

    vector_maxmin[min_pha[:,0].astype(int)] = -1

    # extract pks durations
    vector_peaks = np.zeros(len(t))
    vector_peaks[pha > DELTA] = 1
    vector_peaks = np.diff(vector_peaks)
    vector_peaks = np.r_[0, vector_peaks]

    return pha, vector_maxmin, vector_peaks, t

def PSRindexes(pha, maxmin, peaks, t):
    """
    FEATURES = GSRindexes(PHA_PROCESSED)

    Returns a dict of labeled features.
    """
    if len(peaks) == 0: # no peaks
        print('no peaks found PSR indexes')
        return dict()

    t_max = t[maxmin == 1]
    pha_max = pha[maxmin == 1]

    t_start = t[peaks == 1]

    pha_start = pha[peaks == 1]

    t_end = t[peaks == -1]
#    t_end = np.r_[t_end, t[-1]]

    # simple features
    features = {'pha_max' : np.max(pha), 'pha_min' : np.min(pha), 'pha_mean' : np.mean(pha), 'pha_std' : np.std(pha), 'pha_auc' : np.sum(pha)/len(pha)}
    # n peaks
    features.update({'n_peak': len(t_max)})

    if len(t_max) == 0:
        features.update({'pks_max' : np.nan, 'pks_min' : np.nan, 'pks_mean' : np.nan})
        features.update({'dur_min' : np.nan, 'dur_max' : np.nan, 'dur_mean' : np.nan})
        features.update({'slp_max' : np.nan, 'slp_min' : np.nan, 'slp_mean' : np.nan})
        features.update({"latency" : np.nan})
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

def extract_features(pha, t, DELTA, windows):
    '''
    STEP e LEN in seconds
    :param pha_processed: the phasic np matrix with 4 columns
    :param WINSTEP: window step
    :param WINLEN: window length
    :return: features as np array
    '''
    pha, maxmin, peaks, t=processPSR(pha, t, DELTA)
    feats_all=dict()
    for t_start, t_end in windows:
        window=(t>=t_start) & (t<t_end)
        winfeat=PSRindexes(pha[window], maxmin[window], peaks[window], t[window])
        for key, value in winfeat.items():
            if key in feats_all:
                feats_all.update({key: np.hstack((feats_all[key], value))})
            else:
                feats_all.update({key: np.array([value])})
    return feats_all

def remove_spikes(data, FSAMP, TH=0.005):
    t = np.arange(len(data)) * 1/FSAMP
    spikes = abs(np.diff(data))
    spikes = smoothGaussian(spikes, FSAMP)
    spikes = (spikes - np.min(spikes))/(np.max(spikes) - np.min(spikes))
    indexes_spikes = np.array(np.where(spikes<=TH))[0]
    data_in = data[indexes_spikes]
    t_in = t[indexes_spikes]
    f = interp1d(t_in, data_in)
    t_out = np.arange(t_in[0], t_in[-1], 1/FSAMP)
    data_out = f(t_out)
    return t_out, data_out

def preproc(data, cols, T1=0.75, T2=2, MX=1, DELTA_PEAK=0.02, k_near=5, grid_size=5, s=0.2):
    gsr=selectCol(data, cols, "GSR")
    t_gsr=selectCol(data, cols, "TIME")
    print "T_GSR", t_gsr.shape
    try:
        labs=selectCol(data, cols, "LAB")
    except IndexError as e:
        print "NO LAB:", e.message
        labs=np.zeros(data.shape[0])

    output_cols=["TIME", "DRV", "PHA", "TNC", "LAB"]
    TIME_DRV, DRV, PH_DRV, TN_DRV, labs = estimate_drivers(t_gsr, gsr, labs, T1, T2, MX, DELTA_PEAK, k_near, grid_size, s)
    print "T_DRV", TN_DRV.shape
    print "LAB", labs.shape
    result=np.column_stack((TIME_DRV, DRV, PH_DRV, TN_DRV, labs))
    return result, output_cols