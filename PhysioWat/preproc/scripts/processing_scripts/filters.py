'''
Filters
'''
from scipy.signal import gaussian, convolve, filtfilt, filter_design, freqz
import numpy as np
# import matplotlib.pyplot as plt
from scipy.signal import filter_design as fd

def smoothGaussian(X,sigma=5, switch=True):
    """
    SIGNAL_OUT = smoothGaussian(SIGNAL_IN,SIGMA=5):

    Gaussian smooting by convolution with a gaussian window with sigma=SIGMA
    """
    if not switch:
        return X
    window = gaussian(sigma * 10+1, sigma)
    smoothed = convolve(X, window, 'same')

    return smoothed

def filtfiltFilter (SIGNAL, F_PASS, F_STOP, F_SAMP, LOSS, ATTENUATION, ftype = 'butter'):
    '''
    Applies the selected filter to a signal (all the types has the same parameter)
    return: the signal filtered
    SIGNAL: the signal to filter
    F_PASS: pass frequency, last frequency kept
    F_STOP: stop frequency, first frequency removed
    F_SAMP: smp_fr (sampling frequency)
    LOSS: index of the max variation of the kept frequency (in [0,1])
    ATTENUATION: index of the max variation of the removed frequency from 0 (higher ATTENUATION implies lower variation)
    ftype: (default 'butter') is the type of filter. Should be "butter", "cheby1", "cheby2", "ellip"
    notes:  F_PASS, F_STOP < smp_fr / 2
            F_PASS < F_STOP for a lowpass filter
            F_PASS > F_STOP for a highpass filter
    '''
    nyq = 0.5 * F_SAMP
    wp = np.array(F_PASS)/nyq
    ws = np.array(F_STOP)/nyq
    b, a = filter_design.iirdesign(wp, ws, LOSS, ATTENUATION, ftype = ftype)
    plot = False    
    if plot:
        mfreqz(b,a, wp, ws)
    filtered_signal = filtfilt(b, a, SIGNAL)
    return filtered_signal


def filterSignal (SIGNAL ,smp_fr, passFr, stopFr, LOSS=0.1, ATTENUATION=40, filterType = None):
    '''
    return a filtered signal with the algorithm selected (filterType) and the frequencies passed
    SIGNAL: the signal you want to filter
    smp_fr: the sampling frequency of the signal
    passFr: the pass frequency of the filter
    stopFr: the stop frequency of the filter
    LOSS: the maximum LOSS for the filter (default = 0.1)
    ATTENUATION: the minimum 'movement' for the filter (default = 40)
    filterType: (default 'None') type of the filter. None or invalid value implies no filtering
    '''

    filters=["butter", "cheby1", "cheby2", "ellip"]
    if filterType in filters:
        filtered_signal = filtfiltFilter(SIGNAL, passFr, stopFr, smp_fr, LOSS, ATTENUATION, ftype=filterType)
    else:
        filtered_signal = SIGNAL
    return filtered_signal

#Plot frequency and phase response
def mfreqz(b,a, wp, ws):
    w,h = freqz(b,a)
    h_dB = 20 * np.log10 (abs(h))
    ax1 = plt.subplot(211)
    plt.plot(w/max(w),h_dB)
    plt.vlines(wp, np.min(h_dB), np.max(h_dB), 'g', linewidth = 2)
    plt.vlines(ws, np.min(h_dB), np.max(h_dB), 'r', linewidth = 2)
    plt.ylim(np.min(h_dB), np.max(h_dB))
    plt.ylabel('Magnitude (db)')
    plt.xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    plt.title(r'Frequency response; order A: '+str(len(a))+' order B: '+str(len(b)))
    plt.subplot(212, sharex = ax1)
    h_Phase = np.unwrap(np.arctan2(np.imag(h),np.real(h)))
    plt.plot(w/max(w),h_Phase)
    plt.vlines(wp, np.min(h_Phase), np.max(h_Phase), 'g', linewidth = 2)
    plt.vlines(ws, np.min(h_Phase), np.max(h_Phase), 'r', linewidth = 2)
    plt.ylabel('Phase (radians)')
    plt.xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    plt.title(r'Phase response')
    plt.subplots_adjust(hspace=0.5)

'''
def iir_coefficients(F_PASS, F_STOP, F_SAMP, LOSS=0.1, ATTENUATION=40, ftype = 'butter', plot=False):
    nyq = 0.5 * F_SAMP
    wp = np.array(F_PASS)/nyq
    ws = np.array(F_STOP)/nyq
    b, a = fd.iirdesign(wp, ws, LOSS, ATTENUATION, ftype=ftype)
    if plot:
        mfreqz(b,a, wp, ws)
    return b, a'''