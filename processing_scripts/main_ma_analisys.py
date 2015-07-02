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


y_true, y_pred = f.tryjustone(data1, data2, 3)
f.get_report(y_true, y_pred)
#y_true, y_pred = f.tryjustone(data1, data3, 3)
#y_true, y_pred = f.tryjustone(data2, data3, 3)
#y_true, y_pred = f.tryjustone(data2, data1, 3)
#y_true, y_pred = f.tryjustone(data3, data2, 3)
#y_true, y_pred = f.tryjustone(data3, data1, 3)

# ancora in fase d'implementazione (multiple)
#y_true, y_pred = f.trythemall(data1, data2)
#y_true, y_pred = f.trythemall(data1, data3)
#y_true, y_pred = f.trythemall(data2, data3)
#y_true, y_pred = f.trythemall(data2, data1)
#y_true, y_pred = f.trythemall(data3, data2)
#y_true, y_pred = f.trythemall(data3, data1)