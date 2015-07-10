'''
Manage data from inertial sensors
Accelerometer, Gyroscope, Magnetometer
'''
from __future__ import division
import numpy as np
from tools import selectCol

def convert_units(data, coeff = 1):
    '''
    :param data: accelerometer, gyroscope OR magnetometer data as a numpy.array with x, y, z indexes. Do not
                 pass more than 1 sensor data at a time!! np.array
    :param coeff: coefficient to multiply to convert the units
    :param prefix: "acc", "gyr" or "mag" (accelerometer, gyroscope or magnetoscope
    :return: the converted data
    '''
    #TODO SCEGLI DEVICE
    data*=coeff
    return data

def power_fmax(spec,freq,fmin,fmax):
    #returns power in band
    psd_band=spec[np.where((freq > fmin) & (freq<=fmax))]
    print len(psd_band)
    freq_band=freq[np.where((freq > fmin) & (freq<=fmax))]
    powerinband = np.sum(psd_band)/len(psd_band)
    try:
        fmax=freq_band[np.argmax(psd_band)]
    except ValueError as e:
        print "FFT fmax: ", e.message
        fmax=0
        pass
    return powerinband, fmax

def extract_features_acc(data_acc, t, col_acc, windows):
    '''
    Extract features for acceleration
    :param data_acc: data where to extract feats, as a np.array
    :param t: timestamp
    :param col_acc: labels
    :param WINLEN: window length
    :param WINSTEP: window step
    :param fsamp: sampling rate (Hz)
    :return: feats as np 2d array and the relative labels (np 1d array)
    '''
    fsamp=int(round(1/(t[1]-t[0])))

    col_mod=['acc_mod','acc_mod_plan']
    col_all=np.r_[col_acc, np.array(col_mod)]

    data_acc=np.column_stack((data_acc, np.sqrt(data_acc[:, 0]**2+data_acc[:,1]**2+data_acc[:,2]**2)))
    data_acc=np.column_stack((data_acc, np.sqrt(data_acc[:, 0]**2+data_acc[:,2]**2)))
    # data_acc_more, col_all=get_differences(data_acc, col_all)
    #===================================
    samples, labels=windowing_and_extraction(data_acc, t, fsamp, windows, col_all)
    return samples, labels

def extract_features_gyr(data, t, col_gyr, windows):
    '''
    Extract features for gyroscope
    :param data: data where to extract feats, as a np.array
    :param t: timestamp
    :param col_gyr: labels
    :param WINLEN: window length
    :param WINSTEP: window step
    :param fsamp: sampling rate (Hz)
    :return: feats as np 2d array and the relative labels (np 1d array)
    '''
    # data_more, col_gyr=get_differences(data, col_gyr)
    fsamp=int(round(1/(t[1]-t[0])))
    #===================================
    samples, labels=windowing_and_extraction(data, t, fsamp,windows, col_gyr)
    return samples, labels

def extract_features_mag(data, t, col_mag, windows):
    '''
    Extract features for magnetometer
    :param data: data where to extract feats, as a np.array
    :param t: timestamp
    :param col_mag: labels
    :param WINLEN: window length
    :param WINSTEP: window step
    :param fsamp: sampling rate (Hz)
    :return: feats as np array and the relative labels
    '''
    # data_more, col_mag=get_differences(data, col_mag)
    fsamp=int(round(1/(t[1]-t[0])))
    #===================================
    samples, labels=windowing_and_extraction(data, t, fsamp, windows, col_mag)
    return samples, labels

#Deprecated
def get_differences(data, col_all, n=[1,2,5,10]):
    #===================================
    # calculate the difference of vectors
    result=np.array(data)
    col_ret=np.array(col_all)
    for n_diff in n:
        suffix='_d'+str(n_diff)
        #TODO NON SO SE SIA CORRETTO
        subj=np.array(data)
        subj=np.vstack([subj, subj[-n_diff:,:]])
        diff=np.diff(subj, n=n_diff, axis=0)
        for col in col_all:
            col_ret=np.append(col_ret, col+suffix)
        result=np.column_stack([result, diff])
    return result, col_ret

def windowing_and_extraction(data, t, fsamp, windows, col):
    samples = []
    columns=np.array([])

    bands=np.linspace(0.1,25,11)
    # ciclo sulla sessione - finestratura
    for t_start, t_end in windows:
        feat=np.array([])
        columns=np.array([])
        mask=(t>=t_start)&(t<t_end)

        #windowing
        data_win = data[mask,:]
        fmean=np.mean(data_win, axis=0)

        #max - mean
        feat=np.hstack([feat, np.max(data_win, axis=0)-fmean])
        columns=np.hstack([columns, concat_string(col, "_-_max_mean")])
        #print feat.shape, columns.shape
        #min - mean
        feat=np.hstack([feat, np.min(data_win, axis=0)-fmean])
        columns=np.hstack([columns,concat_string(col, '_-_min_mean')])
        #print feat.shape, columns.shape

        #max - min
        feat=np.hstack([feat, np.max(data_win, axis=0)-np.min(data_win, axis=0)])
        columns=np.hstack([columns, concat_string(col, '_-_max_min')])
        #print feat.shape, columns.shape

        #std
        feat=np.hstack([feat, np.std(data_win, axis=0)])
        columns=np.hstack([columns, concat_string(col, '_-_sd')])
        #print feat.shape, columns.shape

        #integral
        feat=np.hstack([feat, np.sum(data_win-fmean.reshape(1,fmean.shape[0]), axis=0)])
        columns=np.hstack([columns, concat_string(col, '_-_integral')])
        #print feat.shape, columns.shape

        # #mean tipo diff
        # feat=np.hstack([feat, np.mean(data_win[:,-ndiff:], axis=0)])
        # columns=np.hstack([columns, concat_string(col[-ndiff:], '_-_mean_diff')])
        # #print feat.shape, columns.shape
        #
        # #mean(abs) tipo diff
        # feat=np.hstack([feat, np.mean(np.abs(data_win[:,-ndiff:]), axis=0)])
        # columns=np.hstack([columns, concat_string(col[-ndiff:], '_-_mean_abs')])
        # #print feat.shape, columns.shape

        # FD features
        for ind_col in range(data_win.shape[1]):
            curr_col=data_win[:,ind_col]
            prefix=col[ind_col]
            curr_col_array=np.array(curr_col)
            psd=abs(np.fft.fft(curr_col_array))
            fqs=np.arange(0, fsamp, fsamp/len(psd))

            for j in range(0, len(bands)-1):
                pw,fmx = power_fmax(psd, fqs, bands[j], bands[j+1])
                feat=np.hstack([feat, pw, fmx])
                columns=np.hstack([columns, prefix+'_-_power_'+str(bands[j])+'-'+str(bands[j+1]), prefix+'_-_fmax_'+str(bands[j])+'-'+str(bands[j+1])])
                #print feat.shape, columns.shape
        samples.append(feat)
    samples_array=np.array(samples)
    return samples_array, columns

def concat_string(array, str):
    result=[]
    for element in array:
        result.append(element+str)
    return np.array(result)

def preproc(data, cols, coeffAcc=1, coeffGyr=1, coeffMag=1):
    '''
    :param data: the data
    :param cols: the olumns in input
    :param coeff: the conversion rate
    :param data_type: ACC, GYR or MAG
    :return: aray and columns
    '''
    col_acc=["ACCX", "ACCY", "ACCZ"]
    col_gyr=["GYRX", "GYRY", "GYRZ"]
    col_mag=["MAGX", "MAGY", "MAGZ"]
    time=selectCol(data, cols, "TIME")
    try:
        data_acc=selectCol(data, cols, col_acc)
        present_acc=True
    except IndexError as e:
        print "NO ACC:", e.message
        present_acc=False
    try:
        data_gyr=selectCol(data, cols, col_gyr)
        present_gyr=True
    except IndexError as e:
        print "NO GYR:", e.message
        present_gyr=False
    try:
        data_mag=selectCol(data, cols, col_mag)
        present_mag=True
    except IndexError as e:
        print "NO MAG:", e.message
        present_mag=False

    try:
        labs=selectCol(data, cols, "LAB")
    except IndexError as e:
        print "NO LAB:", e.message
        print cols
        labs=np.zeros(data.shape[0])
        pass

    result=time
    columns=["TIME"]
    if present_acc:
        data_acc=convert_units(data_acc, coeffAcc)
        result=np.column_stack((result,data_acc))
        columns += col_acc
    if present_gyr:
        data_gyr=convert_units(data_gyr, coeffGyr)
        result=np.column_stack((result,data_gyr))
        columns += col_gyr
    if present_mag:
        data_mag=convert_units(data_mag, coeffMag)
        result=np.column_stack((result,data_mag))
        columns += col_mag
    result=np.column_stack((result, labs))
    columns += ["LAB"]
    return result, columns