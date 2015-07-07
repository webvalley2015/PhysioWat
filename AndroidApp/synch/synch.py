import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

db= ("GSR_F01_F.txt")
d= np.genfromtxt(db, delimiter= ",")    #array of data
db2= ("GSR_F01_M.txt")
d2= np.genfromtxt(db2, delimiter= ",")


def downsampling(d):                   #downsampling of the data
    t= d[:,0]
    f_samp= 256
    f_new= 10
    n_samp= f_samp/f_new
    indexes= np.arange(len(d))
    keep= (indexes%n_samp == 0)
    gsr= np.array(d[keep])
    t_gsr= t[keep]
    return gsr, t_gsr

d_dw, t_d_dw=downsampling(d)
d2_dw, t_d2_dw=downsampling(d2)

print d_dw, d2_dw                        #print of downsampling


def compute_windows(d_length, wlen=100, wstep=50):                      
    return range(0, d_length-wlen, wstep)  

def extract_features(d, wlen, wstep):                                #extract features from windows           
    windows_list = compute_windows(len(d), wlen, wstep)
    features_activity = []                                       
    for wstart in windows_list:                                 
	    wend=wstart+wlen                                        
	    d_portion=d[wstart : wend, :]                 
	    features_portion = get_features_row(d_portion)       
	    features_activity.append(features_portion)

    return np.array(features_activity)


def get_features_row(d_portion):
    features=[]                                                     
    idx = 1                        
    axis=d_portion[:,idx]                                    
    features.append(np.mean(axis))
    features.append(np.std(axis))
    features.append(np.min(axis))
    features.append(np.max(axis))
    features.append(np.max(axis)-np.min(axis))
    features.append(np.sqrt(np.mean(axis**2)))
    return features                             
		
          
def correlate_features(d, d2):                                      #correlate of the features for synch
	features=[]
	f1 = extract_features(d, 100, 50)
	f2 = extract_features(d2, 100, 50)
	for i in range(4):                                                   
		features.append(spearmanr(f1[:, i], f2[:, i]))
	print features
	return features 
               
cross_result = correlate_features(d,d2)                
	
	


