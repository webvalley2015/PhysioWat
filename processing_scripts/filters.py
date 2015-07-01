'''
Filters
'''
from scipy.signal import gaussian, convolve, filtfilt
#DEBUG ONLY
from scipy.signal import freqz
import matplotlib.pyplot as plt
import numpy as np

def smoothGaussian(X,sigma=5):
    """
    SIGNAL_OUT = smoothGaussian(SIGNAL_IN,SIGMA=5):

    Gaussian smooting by convolution with a gaussian window with sigma=SIGMA
    """
    window = gaussian(sigma * 10+1, sigma)
    smoothed = convolve(X, window, 'same')

    return smoothed

#DEBUG ONLY
def mfreqz(b,a, wp, ws):
    '''
    :param b: filter parameter
    :param a: filter parameter
    :param wp: RELATIVE pass frequency
    :param ws: RELATIVE stop frequency
    :return:
    '''
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

def iir_coefficients(F_PASS, F_STOP, F_SAMP, LOSS=0.1, ATTENUATION=40, ftype = 'butter', plot=False):
    '''
    F_PASS: pass frequency, last frequency kept. Must be smaller than F_STOP for a low_pass filter
    F_STOP: stop frequency, first frequency removed. Must be between F_PASS and 0.5*smp_fr
    F_SAMP: smp_fr (sampling frequency)
    LOSS: index of the max variation of the kept frequency (in [0,1])
    ATTENUATION: index of the max variation of the removed frequency from 0
    '''
    from scipy.signal import filter_design as fd
    nyq = 0.5 * F_SAMP
    wp = np.array(F_PASS)/nyq
    ws = np.array(F_STOP)/nyq
    b, a = fd.iirdesign(wp, ws, LOSS, ATTENUATION, ftype=ftype)
    if plot:
        mfreqz(b,a, wp, ws)
    return(b, a)

def filterSignal (SIGNAL ,smp_fr, passFr = 2, stopFr = 6):
    '''
    return a filtered signal with the algorithm 'butter' and the frequencies passed
    SIGNAL: the signal you want to filter
    smp_fr: the sampling frequency of the signal
    passFr: (default 2) the pass frequency of the filter
    stopFr: (default 6) the stop frequency of the filter
    '''
    b, a = iir_coefficients(passFr, stopFr, smp_fr, plot = False)
    filtered_signal = filtfilt(b, a, SIGNAL)
    return filtered_signal
