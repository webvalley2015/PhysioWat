'''
Manage data from inertial sensors
Accelerometer, Gyroscope, Magnetometer
'''
from __future__ import division
import numpy as np
import pandas as pd

def convert_units(data, labels, coeff = 1):
    '''
    :param data: accelerometer, gyroscope OR magnetometer data as a pandas.DataFrame with x, y, z indexes. Do not
                 pass more than 1 sensor data at a time!!
    :param coeff: coefficient to multiply to convert the units
    :param prefix: "acc", "gyr" or "mag" (accelerometer, gyroscope or magnetoscope
    :return: the converted data
    '''
    data[labels]*=coeff
    return data

def power_fmax(spec,freq,fmin,fmax):
    #returns power in band
    psd_band=spec[np.where((freq > fmin) & (freq<=fmax))]
    freq_band=freq[np.where((freq > fmin) & (freq<=fmax))]
    powerinband = np.sum(psd_band)/len(psd_band)
    fmax=freq_band[np.argmax(psd_band)]
    return powerinband, fmax

def extract_features_acc(data, WINLEN = 30, WINSTEP = 15, fsamp=100, col_acc=['accx','accy','accz']):
    '''
    PASS COL_ACC IN ORDER X, Y, Z
    :param data: data where to extract feats
    :param WINLEN: window length
    :param WINSTEP: window step
    :param fsamp: sampling rate (Hz)
    :param col_acc: labels (x, y, z in order!)
    :return: feats
    '''
    col_mod=['acc_mod','acc_mod_plan']
    col_all=col_acc+col_mod

    x=col_acc[0]
    y=col_acc[1]
    z=col_acc[2]

    data['acc_mod'] = np.sqrt(data[x]**2+data[y]**2+data[z]**2)
    data['acc_mod_plan']= np.sqrt(data[x]**2+data[z]**2)

    data=get_differences(data, col_all)

    #===================================
    samples, labels=windowing_and_extraction(data, fsamp, WINLEN, WINSTEP)
    samples2=pd.DataFrame(samples, columns=labels)
    return samples2

def extract_features_gyr(data, WINLEN = 30, WINSTEP = 15, fsamp=100, col_gyr=['gyrx','gyry','gyrz']):
    data=get_differences(data, col_gyr)
    #===================================
    samples, labels=windowing_and_extraction(data, fsamp, WINLEN, WINSTEP)
    samples2=pd.DataFrame(samples, columns=labels)
    return samples2

def extract_features_mag(data, WINLEN = 30, WINSTEP = 15, fsamp=100, col_mag=['magx','magy','magz']):
    data=get_differences(data, col_mag)

    #===================================
    samples, labels=windowing_and_extraction(data, fsamp, WINLEN, WINSTEP)
    samples2=pd.DataFrame(samples, columns=labels)
    return samples2


def get_differences(data, col_all, n=[1,2,5,10]):
    #===================================
    # calculate the difference of vectors
    for n_diff in n:
        suffix='_d'+str(n_diff)

        diff=pd.DataFrame(np.diff(data[col_all], n=n_diff, axis=0), columns=data[col_all].columns+suffix)

        data=data.join(diff)
    return data

def windowing_and_extraction(data, fsamp, WINSTEP, WINLEN):
    samples = []

    t_start=data.timestamp.iloc[0]
    t_max=data.timestamp.iloc[-1]
    #
    t_end=t_start+WINLEN

    bands=np.linspace(0.1,25,11)
    # ciclo sulla sessione - finestratura
    while(t_end<=t_max):
        feat=np.array([])
        labels=np.array([])

        ind_start=np.argmin(abs(data.timestamp-t_start))
        ind_end=np.argmin(abs(data.timestamp-t_end))

        #windowing
        data_win = data.ix[ind_start:ind_end,3:data.shape[1]]

        #max - mean
        feat=np.hstack([feat, np.max(data_win)-np.mean(data_win)])
        labels=np.hstack([labels, data.ix[ind_start:ind_end,3:data.shape[1]].columns+'_-_max_mean'])

        #min - mean
        feat=np.hstack([feat, np.min(data_win)-np.mean(data_win)])
        labels=np.hstack([labels, data.ix[ind_start:ind_end,3:data.shape[1]].columns+'_-_min_mean'])

        #max - min
        feat=np.hstack([feat, np.max(data_win)-np.min(data_win)])
        labels=np.hstack([labels, data.ix[ind_start:ind_end,3:data.shape[1]].columns+'_-_max_min'])

        #std
        feat=np.hstack([feat, np.std(data_win)])
        labels=np.hstack([labels, data.ix[ind_start:ind_end,3:data.shape[1]].columns+'_-_sd'])

        #integral
        feat=np.hstack([feat, np.sum(data_win-np.mean(data_win))])
        labels=np.hstack([labels, data.ix[ind_start:ind_end,3:data.shape[1]].columns+'_-_integral'])

        #mean tipo diff
        col_diff=data.ix[:,14:].columns
        feat=np.hstack([feat, np.mean(data_win[col_diff])])
        labels=np.hstack([labels, data.ix[ind_start:ind_end,col_diff].columns+'_-_mean_diff'])

        #mean(abs) tipo diff
        col_diff=data.ix[:,14:].columns
        feat=np.hstack([feat, np.mean(np.abs(data_win[col_diff]))])
        labels=np.hstack([labels, data.ix[ind_start:ind_end,col_diff].columns+'_-_mean_abs'])

        # FD features
        for ind_col in range(data_win.shape[1]):
            curr_col=data_win.ix[:,ind_col]
            prefix=curr_col.name
            curr_col_array=np.array(curr_col)
            psd=abs(np.fft.fft(curr_col_array))
            fqs=np.arange(0, fsamp, fsamp/len(psd))

            for j in range(0, len(bands)-1):
                pw,fmx = power_fmax(psd, fqs, bands[j], bands[j+1])
                feat=np.hstack([feat, pw, fmx])
                labels=np.hstack([labels, prefix+'_-_power_'+str(bands[j])+'-'+str(bands[j+1]), prefix+'_-_fmax_'+str(bands[j])+'-'+str(bands[j+1])])

        samples.append(feat)
        t_start=t_start+WINSTEP
        t_end=t_start+WINLEN
    return samples, labels
