"""
Created on Wed Jul  8 10:52:05 2015

@author: roberta
"""
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
#import myUtilities.windowing as wnd
import windowing as wnd
import dtwscript as dts
import mlpy

def modified_extract_features(data_male, data_female, windows, labels, timestamp):
    '''
    STEP e LEN in seconds
    :param pha_processed: the phasic np matrix with 4 columns
    :param WINSTEP: window step
    :param WINLEN: window length
    '''
    dtw_values = []
    for i in range(len(windows)):
        t_start, t_end = windows[i]
        win_s1= data_male[np.where((timestamp >= t_start) & (timestamp < t_end))[0]]
        win_s2= data_female[np.where((timestamp >= t_start) &  (timestamp < t_end))[0]]
        #normalizzazione delle porzioni
        #tn_male = np.array(data_male.tonic)
        #tn_female = np.array(data_female.tonic)
    
        #tn_male = mynorm_maxmin(tn_male)
        #tn_female = mynorm_maxmin(tn_female)
        win_s1= (win_s1- np.mean(win_s1)) / np.std(win_s1)
        win_s2= (win_s2- np.mean(win_s2)) / np.std(win_s2)
            
        dtw_curr= mlpy.dtw_std(win_s1, win_s2)
        dtw_curr = dtw_curr/ len(win_s1)
        lab = labels[i]
        dtw_values.append([dtw_curr, lab])
        #attaccare in qualche modo le labels
        
    return dtw_values #(gia' con le labels)

#def downsampling(data, FS_NEW, switch=True, t_col=0):
#    '''
#    Downsamples the signals (too much data is long to extract!)
#    :param data: The data to downsample
#    :param FS_NEW: The new frequency
#    :param switch: False = Do not downsample
#    :return: The downsampled data
#    '''
#    if not switch:
#        return data
#
#    FSAMP=int(round(1/(data[1,t_col]-data[0,t_col])))
#    if FSAMP <= FS_NEW or FSAMP % FS_NEW != 0:
#        raise ValueError("FS_NEW should be lower than FSAMP and one of its divisors #illy")
#    N_SAMP = FSAMP / FS_NEW
#
#    indexes = np.arange(len(data))
#    keep = (indexes % N_SAMP == 0)
#
#    result = np.array(data[keep, :])
#    return result


def mynorm(x):
    return((x - np.mean(x)) / np.std(x))
    
def mynorm_maxmin(x):
    return((x - np.min(x)) / (np.max(x)- np.min(x)))
    
os.chdir('/home/roberta/Work/file/data/GSR/preprocessed/F/')

WINLEN = 10
WINSTEP = 5

filelist = os.listdir(os.getcwd())

experiments = []
for filename in filelist:
    experiments.append(filename[0:3])
    
experiments = np.unique(experiments)

labels_header = 'timestamp, driver, phasic, tonic, labels'

N_SAMP = 8
dtw_measures = []
for EXP in experiments:
data_male = pd.read_csv(EXP+'_M.csv', sep=',')
data_female = pd.read_csv(EXP+'_F.csv', sep=',')

if data_male.shape[0] > data_female.shape[0]:  
    l = data_female.shape[0]
    data_male = data_male.iloc[:l,:]
else:
    l = data_male.shape[0]
    data_female = data_female.iloc[:l,:]

tn_male = np.array(data_male.tonic)
tn_female = np.array(data_female.tonic)

tn_male = mynorm_maxmin(tn_male)
tn_female = mynorm_maxmin(tn_female)

indexes = np.arange(len(tn_male))
keep = (indexes % N_SAMP == 0)

tn_male = np.array(tn_male[keep])
tn_female = np.array(tn_female[keep])

SAMP_F = 1.0 / (data_male.iloc[1,0] - data_male.iloc[0,0])
timestamp = np.arange(0, l/SAMP_F, 1.0/SAMP_F)
    
labs = np.array(data_female.iloc[:,-1])    
    
windows, labels = wnd.get_windows_no_mix(timestamp, labs, WINLEN, WINSTEP)
    
#extrazione porzione da entrambi i file
	
#    n_col = data_male.shape[1]
#    for i in range(1, n_col - 1):
#dtw_curr = dtw_curr/ len(tn_male)
dtw_curr = modified_extract_features(tn_male, tn_female, windows, labels, timestamp)
#dtw_curr= mlpy.dtw_std(tn_male, tn_female)
#dtw_curr = dtw_curr/ len(tn_male)
#dtw_measures.append(dtw_curr)
np.savetxt(EXP+'_dtw_wind.csv', res_exp, delimiter=',')

res_exp = np.vstack([dtw_curr])
np.savetxt('F_dtw_all_signal.csv', res_exp, delimiter=',')

#print dtw_measures
#salvare dtw_measures su file di testo
