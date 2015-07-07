'''
Filters
'''
from scipy.signal import gaussian, convolve, filtfilt, filter_design, freqz
import numpy as np
from IBI import getPeaksIBI
#DEBUG ONLY
# import matplotlib.pyplot as plt

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

def matched_filter(signal, SAMP_F, t_start_good_ecg, t_end_good_ecg, peak_bef = 0.35, peak_aft = 1):
    '''
    return the signal filtered with a match algorithm
    signal: np.array (N,3) containing the EKG
    SAMP_F: sampling frequency of signal
    t_start_good_ecg: time start for the good EKGs
    t_end_good_ecg: time end for the good EKGs
    peak_bef: (default 0.35) the lenght of each beat before the peak (in s)
    peak_aft: (default 1) the lenght of each beat after the peak (in s)
    '''
    peak_len = peak_bef + peak_aft
    timestamp = signal[:,0]
    ecg = signal[:,1]
    #take good_ekg from signal, so it can be passed to getPeaksIBI
    good_ecg = signal[(timestamp >= t_start_good_ecg)&(timestamp < t_end_good_ecg),:]
    maxp = getPeaksIBI(good_ecg, SAMP_F, 0.25)
    templates = np.zeros(peak_len*SAMP_F)
    for i in maxp[:,0]:
        tmp = ecg[(timestamp >= (i - peak_bef))&(timestamp < (i + peak_aft))]
        tmp = (tmp - np.min(tmp))/(np.max(tmp) - np.min(tmp))
        templates = np.vstack((templates, tmp))
    templates = templates[:, 1:]
    #for gr in templates:
    #    plt.plot(gr) 
    #plt.show()
    ecg_template = np.mean(templates, axis = 0)
    #plt.plot(ecg_template)
    #plt.show()
    ecg_template = ecg_template - ecg_template[0]
    ecg_template = ecg_template[::-1]
    ecg_matched = np.convolve(ecg, ecg_template, mode = 'same')
    return ecg_matched


#DEBUG ONLY
#Plot frequency and phase response
# def mfreqz(b,a, wp, ws):
#     w,h = freqz(b,a)
#     h_dB = 20 * np.log10 (abs(h))
#     ax1 = plt.subplot(211)
#     plt.plot(w/max(w),h_dB)
#     plt.vlines(wp, np.min(h_dB), np.max(h_dB), 'g', linewidth = 2)
#     plt.vlines(ws, np.min(h_dB), np.max(h_dB), 'r', linewidth = 2)
#     plt.ylim(np.min(h_dB), np.max(h_dB))
#     plt.ylabel('Magnitude (db)')
#     plt.xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
#     plt.title(r'Frequency response; order A: '+str(len(a))+' order B: '+str(len(b)))
#     plt.subplot(212, sharex = ax1)
#     h_Phase = np.unwrap(np.arctan2(np.imag(h),np.real(h)))
#     plt.plot(w/max(w),h_Phase)
#     plt.vlines(wp, np.min(h_Phase), np.max(h_Phase), 'g', linewidth = 2)
#     plt.vlines(ws, np.min(h_Phase), np.max(h_Phase), 'r', linewidth = 2)
#     plt.ylabel('Phase (radians)')
#     plt.xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
#     plt.title(r'Phase response')
#     plt.subplots_adjust(hspace=0.5)