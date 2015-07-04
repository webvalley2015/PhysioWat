import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import csv 
'''
correlation between GSR_F and GSR_M features extracted by pre-processing team
'''

def cut(df,df2):                                    #cutting array features to have two datasets of features with the same number of rows
    f1 = np.genfromtxt(df, delimiter=",")
    f2 = np.genfromtxt(df2,delimiter=",")
    print " f1 è lungo= {0} f2 lungo {1} ".format(len(f1),len(f2)) 
    if len(f1) > len(f2):
        l = len(f2)
        f1 = f1[:l,:]
    else :
        l = len(f1)
        f2 = f2[:l,:]
    return f1, f2
        
        
def correlate_features(df, df2):                                      #correlate of the features for synch
	features=[]
	df, df2 = cut(df,df2)
	for i in range(4):                                                   
		features.append(spearmanr(df[:, i], df2[:, i]))
	print features
	return features 
                              

if __name__=="__main__":
    cross_result = correlate_features("GSR__F.txt","GSR__m.txt")
    print cross_result
	
