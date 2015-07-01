'''
Filters
'''
from scipy.signal import gaussian, convolve, filtfilt, filter_design
import numpy as np

def smoothGaussian(X,sigma=5):
    """
    SIGNAL_OUT = smoothGaussian(SIGNAL_IN,SIGMA=5):

    Gaussian smooting by convolution with a gaussian window with sigma=SIGMA
    """
    window = gaussian(sigma * 10+1, sigma)
    smoothed = convolve(X, window, 'same')

    return smoothed


def ButterworthFilter (SIGNAL, F_PASS, F_STOP, F_SAMP, LOSS=0.1, ATTENUATION=40):
    '''
    Applies the ButterWorth filter to a signal
    return: the signal filtered
    SIGNAL: the signal to filter
    F_PASS: pass frequency, last frequency kept. Must be smaller than F_STOP for a low_pass filter
    F_STOP: stop frequency, first frequency removed. Must be between F_PASS and 0.5*smp_fr
    F_SAMP: smp_fr (sampling frequency)
    LOSS: index of the max variation of the kept frequency (in [0,1])
    ATTENUATION: index of the max variation of the removed frequency from 0
    '''
    nyq = 0.5 * F_SAMP
    wp = np.array(F_PASS)/nyq
    ws = np.array(F_STOP)/nyq
    b, a = filter_design.iirdesign(wp, ws, LOSS, ATTENUATION, ftype='butter')
    filtered_signal = filtfilt(b, a, SIGNAL)
    return filtered_signal


def filterSignal (SIGNAL ,smp_fr, passFr = 2, stopFr = 6, filterType = 'butter'):
    '''
    return a filtered signal with the algorithm 'butter' and the frequencies passed
    SIGNAL: the signal you want to filter
    smp_fr: the sampling frequency of the signal
    passFr: (default 2) the pass frequency of the filter
    stopFr: (default 6) the stop frequency of the filter
    filterType: (default 'butter') type of the filter
    '''
    if filterType == 'butter':
        filtered_signal = ButterworthFilter(SIGNAL, passFr, stopFr, smp_fr)
    #Add here the other filters
    else:
        #Default filter
        filtered_signal = ButterworthFilter(SIGNAL, passFr, stopFr, smp_fr)
    return filtered_signal