# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 17:56:22 2015

@author: flavio
"""
'''
function for BVP only
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import myUtilities.filters as filters

def mfreqz(b,a, wp, ws):
    '''
    :param b: filter parameter
    :param a: filter parameter
    :param wp: RELATIVE pass frequency
    :param ws: RELATIVE stop frequency
    :return:
    '''
    w,h = signal.freqz(b,a)
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
    filters.iir_coefficients(F_PASS, F_STOP, F_SAMP, LOSS=0.1, ATTENUATION=40, ftype = 'butter', plot=False)
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

def getFilterParam (smp_fr, passFr = 2, stopFr = 6):
    b,a = iir_coefficients(passFr, stopFr, smp_fr, plot = False)
    return (b,a)

def iir_filter(SIGNAL, B, A):
    from scipy.signal import filtfilt
    sig=filtfilt(B, A, SIGNAL)
    return(sig)

path = #add the path
fileName = #add the filename

SAMPLING_FREQ = #add the sampling frequency

data = pd.DataFrame.from_csv(path+fileName, sep=';')
plt.plot(data.index, data.BVP)
datanp= data.as_matrix().reshape(data.shape[0])

bPar, aPar = getFilterParam(SAMPLING_FREQ)
filtered_signal = iir_filter(datanp, bPar, aPar)

plt.plot(data.index, filtered_signal)
plt.show()
