# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 17:10:50 2015

@author: andrea
"""

#import libraries
import pandas as pd
import os

# from PhysioWat.preproc.scripts.processing_scripts import feat_script as f
import feat_script as fs

labels = {}
localdir = {}
data1 = None
data3 = None

names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Decision Tree",
         "Random Forest", "AdaBoost", "Naive Bayes", "LDA", "QDA"]


def load_config(lab=None, loc_dir=None):
    global labels
    global localdir
    
    if lab is None:
        #define costants
        labels = {'still':0,
                  'arm':1,
                  'walk':2,
                  'run':3
              }
    else:
        labels = lab

    if loc_dir is None:
        localdir = '/home/andrea/Work/data/27_06_Analisys/extracted/'
    else:
        localdir = loc_dir


def load_data():
    global data1
    global data3
    
    data1 = pd.DataFrame.from_csv(path=os.path.join(localdir, 'gr1'))
    data3 = pd.DataFrame.from_csv(path=os.path.join(localdir, 'gr3'))
    

def test_KNN():
    # test knn alg
    return fs.bestfit_KNN(data1, 'KNN', 1) # FIXME 3rd parameter

def test_RFC():
    return fs.bestfit_RFC(data1, 'RFC', 1) # FIXME 3rd parameter

def main():
    """
    exec all the tests
    """
    laod_config()
    load_data()
    clf, result = test_KNN()



if __name__ == "__main__":
    pass







################ FIXME

    
    
#     #try withrh the iris dataset

#     #f.feat_barplot(data1)
#     #f.feat_barplot(data2)
#     #f.feat_barplot(data3)

             
#     for i,a in enumerate(names):
#         print a + '\t' + str(i)

#     #y_true, y_pred = f.tryjustone(data1, data2, 3)         
#     #y_true, y_pred = f.tryjustone(data1, data3, 3)
#     #y_true, y_pred = f.tryjustone(data2, data3, 3)
#     #y_true, y_pred = f.tryjustone(data2, data1, 3)
#     #y_true, y_pred = f.tryjustone(data3, data2, 3)
#     #y_true, y_pred = f.tryjustone(data3, data1, 3)

#     # ancora in fase d'implementazione (multiple)
#     #y_true, y_pred = f.trythemall(data1, data2)
#     #y_true, y_pred = f.trythemall(data1, data3)
#     #y_true, y_pred = f.trythemall(data2, data3)
#     #y_true, y_pred = f.trythemall(data2, data1)
#     #y_true, y_pred = f.trythemall(data3, data2)
#     #y_true, y_pred = f.trythemall(data3, data1)


# def to_be_fixed():
#     for first in [data1, data2, data3]:
#         for second in [data1, data2, data3]:
#             if (first[0] != second[0]):
#                 y_true, y_pred = f.tryjustone(first, second, 3)
#                 metrics, conf_matrix = f.get_report(y_true, y_pred)
#                 for keys,values in metrics.items():
#                     print  keys, '\t' , round(values,2)


#     #fitting the model

#     clf = f.bestfit(data1, alg=1, feat='ACC') #that is the linearSVM
#     #testing it
 
 
