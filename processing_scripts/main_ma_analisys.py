# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 17:10:50 2015

@author: andrea
"""

#import libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import feat_script as f

#define costants
labels = {'still':0,
        'arm':1,
        'walk':2,
        'run':3
        }

#import, preprocessing and windowing (with feat extraction)
localdir = '/home/andrea/Work/data/27_06_Analisys/extracted/'
data1 = pd.DataFrame.from_csv(path=localdir + 'gr1')
data2 = pd.DataFrame.from_csv(path=localdir + 'gr2')
data3 = pd.DataFrame.from_csv(path=localdir + 'gr3')

f.feat_barplot(data1)
f.feat_barplot(data2)
f.feat_barplot(data3)

names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Decision Tree",
             "Random Forest", "AdaBoost", "Naive Bayes", "LDA", "QDA"]
             
i = 0
for a in names:
    print a + '\t' + str(i)
    i += 1

#print f.cvDCT(in_data, sol)
#print f.cvSVC(in_data, sol)
