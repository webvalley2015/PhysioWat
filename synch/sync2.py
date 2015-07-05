import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import csv 
'''
correlation between GSR_F/EKG_F and GSR_M/EKG_M features extracted by pre-processing team
'''

def cut(df,df2):                                    #cutting array features to have two datasets of features with the same number of rows
    f1 = np.genfromtxt(df, delimiter=',')
    f2 = np.genfromtxt(df2,delimiter=',') 
    if len(f1) > len(f2):  
        l = len(f2)
        f1 = f1[:l,:]
    else :
        l = len(f1)
        f2 = f2[:l,:]
    return f1, f2
        
        
def correlate_features(df, df2):                                      #correlate of the features for sync
	features=[]
	df, df2 = cut(df,df2)
	for i in range(4):                                                   
		features.append(spearmanr(df[:, i], df2[:, i]))
	print np.array(features)
	return features 
                              

if __name__=="__main__":
    cross_result = correlate_features(df,df2)
    print cross_result
	
