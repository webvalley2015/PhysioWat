"""
Created on Wed Jul  8 10:52:05 2015

@author: roberta
"""
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import windowing as wnd
import dtwscript as dts

def modified_extract_features(data_s1, data_s2, windows, labels, timestamp):
    '''
    STEP e LEN in seconds
    :param pha_processed: the phasic np matrix with 4 columns
    :param WINSTEP: window step
    :param WINLEN: window length
    '''
    dtw_values = []
    for i in range(len(windows)):
        t_start, t_end = windows[i]
        win_s1= data_s1[(timestamp >= t_start) & (timestamp < t_end),3]
        win_s2= data_s2[(timestamp >= t_start)&(timestamp < t_end),3]
        # estrai porzione dei dati
        #porzione_M = ...
        #porzione_F = ...
        #normalizzazione delle porzioni
        win_s1= (win_s1- np.mean(win_s1)) / np.std(win_s1)
        win_s2= (win_s2- np.mean(win_s2)) / np.std(win_s2)
        dtw_curr= dts.dtw(win_s1, win_s2)
        lab = labels[i]
        dtw_values.append([dtw_curr, lab])
        #attaccare in qualche modo le labels
        
    return dtw_values #(gia' con le labels)


os.chdir('/home/roberta/Work/file/data/GSR/preprocessed/F')

WINLEN = 10
WINSTEP = 5

filelist = os.listdir(os.getcwd())

experiments = []
for filename in filelist:
    experiments.append(filename[0:3])
    
experiments = np.unique(experiments)

labels_header = 'timestamp, driver, phasic, tonic, labels'
statistic = np.zeros(5)
for EXP in experiments:
    data_male = pd.read_csv(EXP+'_M.csv', sep=',')
    data_female = pd.read_csv(EXP+'_F.csv', sep=',')

    if data_male.shape[1] > data_female.shape[1]:  
        l = data_female.shape[1]
        data_male = data_male[:l,:]
    else :
        l = data_male.shape[1]
        data_female = data_female[:l,:]

	SAMP_F = 1.0 / (data_male[1,0] - data_male[0,0])
	timestamp = np.arange(0, l/SAMP_F, 1.0/SAMP_F)
    
    windows, labels = wnd.get_windows_no_mix(timestamp, data_female[:,-1], WINLEN, WINSTEP)
    
	#extrazione porzione da entrambi i file
	dtw_measures = []
    for i in range(len(l)):
        dtw_measures.append(modified_extract_features(data_male, data_female, windows, labels, timestamp))
    print dtw_measures
#salvare dtw_measures su file di testo
