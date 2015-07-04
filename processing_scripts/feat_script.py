# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 17:10:50 2015

@author: andrea
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn import datasets, svm, metrics
from sklearn import cross_validation
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA
from sklearn.metrics import *
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

WINLEN = 100
WINSTEP = 50

cols = ["AccX","AccY","AccZ", "GyrX","GyrY","GyrZ", "MagX","MagY","MagZ"]

colnames = ['Acc.std.Norm', 'Mag.std.Norm', 'Mag.Mean.Z', 'Mag.Mean.X', 'Mag.Mean.Y', 'Acc.std.Y', 'Acc.std.X', 'Acc.std.Z', 'Acc.Max.X', 'label', 'Gyr.Min.Z', 'Gyr.Min.Y', 'Gyr.Min.X', 'Mag.Min.Norm', 'Acc.Min.Norm', 'Gyr.Min.Norm', 'Mag.Mean.Norm', 'Acc.Mean.X', 'Acc.Mean.Y', 'Acc.Mean.Z', 'Gyr.Max.Norm', 'Mag.Max.Norm', 'Acc.Max.Norm', 'Gyr.Mean.Norm', 'Acc.Max.Y', 'Acc.Max.Z', 'Gyr.Mean.Z', 'Gyr.Mean.Y', 'Gyr.Mean.X', 'Mag.Max.Z', 'Mag.Max.X', 'Mag.Max.Y', 'Acc.Mean.Norm', 'Acc.Min.Z', 'Acc.Min.X', 'Acc.Min.Y', 'Gyr.std.Norm', 'Mag.Min.X', 'Mag.Min.Y', 'Mag.Min.Z', 'Mag.std.Z', 'Mag.std.Y', 'Mag.std.X', 'Gyr.std.X', 'Gyr.std.Y', 'Gyr.std.Z', 'Gyr.Max.Y', 'Gyr.Max.X', 'Gyr.Max.Z']

names = ["Nearest Neighbors", "Linear SVM\t", "RBF SVM\t", "Decision Tree",
             "Random Forest", "AdaBoost\t", "LDA\t", "QDA\t"]

classifiers = {
        'KNN': lambda nn: KNeighborsClassifier(n_neighbors=nn),
        'SVL': lambda C: SVC(kernel="linear", C=C),
        'SVM': lambda kernel, C, degree : SVC(kernel=kernel, C=C, degree=deg),
        'DCT': lambda max_f: DecisionTreeClassifier(max_features=max_f),
        'RFC': lambda n_est, max_f: RandomForestClassifier(n_estimators=n_est, max_features=max_f),
        'ADA': lambda n_est, l_rate: AdaBoostClassifier(n_estimators = n_est, learning_rate=l_rate),
        'LDA': lambda solver: LDA(solver=solver),
        'QDA': lambda : QDA()
        }

def exFeat(l_curr, lab):
    mean = l_curr.mean()
    std = l_curr.std()
    mi = l_curr.min()
    ma = l_curr.max()
    feat = {
    'Acc.Mean.X': mean.AccX, 
    'Acc.Mean.Y': mean.AccY,
    'Acc.Mean.Z': mean.AccZ,
    'Acc.Mean.Norm': mean.AccNorm,
    'Gyr.Mean.X': mean.GyrX, 
    'Gyr.Mean.Y': mean.GyrY,
    'Gyr.Mean.Z': mean.GyrZ,
    'Gyr.Mean.Norm': mean.GyrNorm,
    'Mag.Mean.X': mean.MagX, 
    'Mag.Mean.Y': mean.MagY,
    'Mag.Mean.Z': mean.MagZ,
    'Mag.Mean.Norm': mean.MagNorm,
    'Acc.Max.X': ma.AccX, 
    'Acc.Max.Y': ma.AccY,
    'Acc.Max.Z': ma.AccZ,
    'Acc.Max.Norm': ma.AccNorm,
    'Gyr.Max.X': ma.GyrX, 
    'Gyr.Max.Y': ma.GyrY,
    'Gyr.Max.Z': ma.GyrZ,
    'Gyr.Max.Norm': ma.GyrNorm,
    'Mag.Max.X': ma.MagX, 
    'Mag.Max.Y': ma.MagY,
    'Mag.Max.Z': ma.MagZ,
    'Mag.Max.Norm': ma.MagNorm,
    'Acc.Min.X': mi.AccX, 
    'Acc.Min.Y': mi.AccY,
    'Acc.Min.Z': mi.AccZ,
    'Acc.Min.Norm': mi.AccNorm,
    'Gyr.Min.X': mi.GyrX, 
    'Gyr.Min.Y': mi.GyrY,
    'Gyr.Min.Z': mi.GyrZ,
    'Gyr.Min.Norm': mi.GyrNorm,
    'Mag.Min.X': mi.MagX, 
    'Mag.Min.Y': mi.MagY,
    'Mag.Min.Z': mi.MagZ,
    'Mag.Min.Norm': mi.MagNorm,
    'Acc.std.X': std.AccX, 
    'Acc.std.Y': std.AccY,
    'Acc.std.Z': std.AccZ,
    'Acc.std.Norm': std.AccNorm,
    'Gyr.std.X': std.GyrX, 
    'Gyr.std.Y': std.GyrY,
    'Gyr.std.Z': std.GyrZ,
    'Gyr.std.Norm': std.GyrNorm,
    'Mag.std.X': std.MagX, 
    'Mag.std.Y': std.MagY,
    'Mag.std.Z': std.MagZ,
    'Mag.std.Norm': std.MagNorm,
    'label': lab
    }
    
    '''
     ,___,
     (O.o)
     /),,)
      " "
     WHAT?
    ''' 
    #print feat.keys()
    return feat

def windowAnalize (nparr, lab):

    df = pd.DataFrame(nparr, columns = cols)
    AccNorm = np.sqrt(df.AccX**2 + df.AccY**2 + df.AccZ**2)
    GyrNorm = np.sqrt(df.GyrX**2 + df.GyrY**2 + df.GyrZ**2)
    MagNorm = np.sqrt(df.MagX**2 + df.MagY**2 + df.MagZ**2)
    df = pd.concat([df, AccNorm, GyrNorm, MagNorm], axis=1)
    df.columns = ["AccX","AccY","AccZ", "GyrX","GyrY","GyrZ", "MagX","MagY","MagZ","AccNorm","GyrNorm","MagNorm"]
    print(df)
    t_start = df.index[0]
    t_end = t_start + WINLEN
    
    res = pd.DataFrame(columns=colnames)
    while (t_end < df.shape[0]-1):
        df_curr = df.query(str(t_start)+'<=index<'+str(t_end))
        v = exFeat(df_curr, lab)
        newrow = pd.DataFrame(v, index=[t_start])
        res = res.append(newrow)
        #update values
        t_start = t_start + WINSTEP
        t_end = t_start + WINLEN

    return res
    
def raw_plot(data):
    plt.style.use('ggplot')
    plt.figure()
    plt.plot(data[:,list((0,1,2))])
    plt.plot(data[:,list((3,4,5))])
    plt.plot(data[:,list((6,7,8))])
    plt.show()

    #to revise it!!
def feat_barplot(x):
    plt.style.use('ggplot')
    data = pd.DataFrame()
    for i in range(len(x.columns)-1):
        data0 = x.query('label == '+str(0)).iloc[:,i]
        data1 = x.query('label == '+str(1)).iloc[:,i]
        data2 = x.query('label == '+str(2)).iloc[:,i]
        data3 = x.query('label == '+str(3)).iloc[:,i]
        data = [data0, data1, data2, data3]
        plt.subplot(5,10, i+1)
        plt.boxplot(data)
        plt.title(x.columns[i])
    plt.show()
    
def cvSVC(raw_df, sol): #very old, do not use!
    x = raw_df
    y = sol
    #x_train, x_test, y_train, y_test = cross_validation.train_test_split(x,y, test_size=0.4)
    Clist = [ 10**i for i in range(-5,8) ]
    accuracy = np.zeros(3)#.reshape((1,-1))
    for par in Clist:
        clf = svm.LinearSVC(C=par)
        #clf = clf.fit(x_train, y_train)
        scores = cross_validation.cross_val_score(clf, x, y, cv=5)
        print(scores)
        vec = np.array([par, scores.mean(), scores.std()*2])
        #print vec
        accuracy = np.concatenate((accuracy, vec))
        
    accuracy = accuracy.reshape((-1,3))
    accuracy = accuracy[1:,:]
    plt.figure()
    plt.plot(accuracy[:,0],accuracy[:,1])
    plt.xscale('log')
    plt.show()    
    return accuracy
    
def crossvalidate_1df_SVM(data, method):
    sol = data.label
    data = data[data.columns[:-1]]
    data = data.as_matrix()
    sol = np.array(sol)
    #test_sol = test_data.label
    #test_in_data = test_data[test_data.columns[:-1]]

    #k-fold validation
    k = 10;
    acc = np.zeros([k,1])
    kf= cross_validation.KFold(data.shape[0],k)#, shuffle=True)
    index = 0;
    for train_index, test_index in kf:
        X_train, X_test = data[train_index], data[test_index]
        y_train, y_test = sol[train_index], sol[test_index]
        #clf= DecisionTreeClassifier()
        #clf_fitted = clf.fit(X_train, y_train)
        #print clf_fitted.score(X_test, y_test)
        #clf= svm.LinearSVC(C=5)
        #clf_fitted = clf.fit(X_train, y_train)
        print predict(get_selected_clf(X_train, y_train), X_test, y_test )
        acc[index] = clf_fitted.score(X_test, y_test)
        index+=1
        
    print(np.mean(acc))
    
def tryjustone(in_data, te_data, which):
    te_tar = te_data.label
    in_tar = in_data.label
    te_data = te_data[te_data.columns[:-1]]
    in_data = in_data[in_data.columns[:-1]]

    # cv_scores = cross_validation.cross_val_score(RandomForestClassifier(), in_data, in_tar)
    y_pred = predict(get_selected_clf(in_data, in_tar, which), te_data, te_tar )
    return te_tar.values , y_pred
    
def get_selected_clf(X, Y, which):
    clf = classifiers[which]
    clf=clf.fit(X, Y)
    return  clf

def predict(clf, testX, testY):
    labels_predict = clf.predict(testX)
    score = clf.score(testX, testY)
    print "Accuracy %.5f" % (score)
    return labels_predict

def trythemall(in_data, te_data):
    te_tar = te_data.label
    in_tar = in_data.label
    te_data = te_data[te_data.columns[:-1]]
    in_data = in_data[in_data.columns[:-1]]
        
        
    print 'List of accuracies...'
    for name, clf in zip(names, classifiers.items):
        #ax = plt.subplot(len(datasets), len(classifiers) + 1, i)
        clf.fit(in_data, in_tar)
        #labels_predict = clf.predict(te_data)
        score = clf.score(te_data, te_tar)
        print "Accuracy for\t " + name +"\t  %.5f" %(score)
        
def get_report(y_true, y_pred):
    report = {
        #'Accuracy (n)': accuracy_score(y_true, y_pred, normalize=False),
        'Accuracy (%)': accuracy_score(y_true, y_pred),
        'Zero-One Classification loss': zero_one_loss(y_true, y_pred),
        #'Zero-One Classification loss': zero_one_loss(y_true, y_pred, normalize=False)
        #what is y_score?!? to compute average_precision_score
        'F-measure (macro)': f1_score(y_true, y_pred, average='macro'),
        'F-measure (micro)': f1_score(y_true, y_pred, average='micro'),
        'F-measure (weighted)': f1_score(y_true, y_pred, average='weighted'),
        #the beta-value is unknown!!! fix it
        'WeHarmMean prec&recall': fbeta_score(y_true, y_pred, average='weighted', beta=1),
        'Hamming loss': hamming_loss(y_true, y_pred),
        #hinge loss is missing! ( i get 6 classes in decision_function instead of 4)
        'Jaccard distance': jaccard_similarity_score(y_true, y_pred),
        'Precision score (macro)': precision_score(y_true, y_pred, average='macro'),
        'Precision score (micro)': precision_score(y_true, y_pred, average='micro'), 
        'Precision score (weighted)': precision_score(y_true, y_pred, average='weighted'),
        'Recall score (macro)': recall_score(y_true, y_pred, average='macro'),
        'Recall score (micro)': recall_score(y_true, y_pred, average='micro'), 
        'Recall score (weighted)': recall_score(y_true, y_pred, average='weighted'), 
    }
    conf_mat = confusion_matrix(y_true, y_pred)

    X = np.arange(len(report))
    plt.bar(X, report.values(), align='center', width=0.5)
    plt.xticks(X, report.keys(), rotation=90)
    ymax = max(report.values()) + 1
    plt.ylim(0, ymax)
    plt.show()    
    
    return report, conf_mat
    
def bestfit(fe_data, alg, feat):
    #in_tar = in_data.label
    #in_data = in_data[in_data.columns[:-1]]
#classifiers = {
#        'SVM': lambda kernel, C, degree : SVC(kernel=kernel, C=C, degree=deg),
#        'RFC': lambda n_est, max_f: RandomForestClassifier(n_estimators=n_est, max_features=max_f),
#        'ADA': lambda n_est, l_rate: AdaBoostClassifier(n_estimators = n_est, learning_rate=l_rate)
#        }
#        
    if alg == 'KNN': pos, val = bestfit_KNN(fe_data, alg, feat)
        elif alg == 'SVL': pos, val = bestfit_SVL(fe_data, alg, feat)
            elif alg == 'SVM': pos, val = bestfit_SVM(fe_data, alg, feat)
                elif alg == 'DCT': pos, val = bestfit_DCT(fe_data, alg, feat)
                    elif alg == 'RFC': pos, val = bestfit_RFC(fe_data, alg, feat)
                        elif alg == 'ADA': pos, val = bestfit_ADA(fe_data, alg, feat)
                            elif alg == 'LDA': pos, val = bestfit_LDA(fe_data, alg, feat)
                                elif alg == 'QDA': pos, val = bestfit_QDA(fe_data, alg, feat):
    return pos, val

def bestfit_KNN(fe_data, alg, feat):
    accuracy = np.zeros(0)
    NNlist = [1, 3, 5, 7, 9, 11]
    iterations = 20
    for nn in NNlist:
        clf = classifiers[alg](n_neighbors=nn)
        mean_vec = 0.
        for i in range(iterations):
            fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
            in_tar = fe_data.label
            in_data = fe_data[fe_data.columns[:-1]]
            scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=10, n_jobs=-1)
            #print scores
            in_vec = np.array([C, scores.mean(), scores.std()*2])
            mean_vec += in_vec[1]
        accuracy = np.append(accuracy, (mean_vec/iterations))
    #plot the accuracy
    plt.figure()
    plt.plot(NNlist,accuracy)
    #plt.xscale('log')
    plt.show()    
    return accuracy.argmax(), accuracy.max()


def bestfit_SVL(fe_data, alg, feat):
    accuracy = np.zeros(0)
    Clist = [ 10**i for i in range(-5,8) ]
    iterations = 20
    for C in Clist:
        clf = classifiers[alg](C=C)
        mean_vec = 0.
        for i in range(iterations):
            fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
            in_tar = fe_data.label
            in_data = fe_data[fe_data.columns[:-1]]
            scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=10, n_jobs=-1)
            #print scores
            in_vec = np.array([C, scores.mean(), scores.std()*2])
            mean_vec += in_vec[1]
        accuracy = np.append(accuracy, (mean_vec/iterations))
    #plot the accuracy
    plt.figure()
    plt.plot(Clist,accuracy)
    plt.xscale('log')
    plt.show()    
    return accuracy.argmax(), accuracy.max()
    

def bestfit_DCT(fe_data, alg, feat):
    accuracy = np.zeros(0)
    MFlist = [1, 1., 'sqrt', 'log2', None]
    iterations = 20
    for max_f in MFlist:
        clf = classifiers[alg](max_features=max_f)
        mean_vec = 0.
        for i in range(iterations):
            fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
            in_tar = fe_data.label
            in_data = fe_data[fe_data.columns[:-1]]
            scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=10, n_jobs=-1)
            #print scores
            in_vec = np.array([C, scores.mean(), scores.std()*2])
            mean_vec += in_vec[1]
        accuracy = np.append(accuracy, (mean_vec/iterations))
    #plot the accuracy
    plt.figure()
    plt.plot(MFlist,accuracy)
    #plt.xscale('log')
    plt.show()    
    return accuracy.argmax(), accuracy.max()
    
def bestfit_QDA(fe_data, alg, feat):
    accuracy = np.zeros(0)
    #just default parameters
    iterations = 20
    for i in range(iterations):
        fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
        in_tar = fe_data.label
        in_data = fe_data[fe_data.columns[:-1]]
        scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=10, n_jobs=-1)
        #print scores
        in_vec = np.array([C, scores.mean(), scores.std()*2])
        mean_vec += in_vec[1]
    accuracy = float(mean_vec)/iterations
    #plot the accuracy
    plt.figure()
    plt.plot(accuracy)
    #plt.xscale('log')
    plt.show()    
    return 0, accuracy.max()
    
def bestfit_KNN(fe_data, alg, feat):
    accuracy = np.zeros(0)
    SRlist = ['svd', 'lsqr', 'eigen']
    iterations = 20
    for solver in SRlist:
        clf = classifiers[alg](solver=solver)
        mean_vec = 0.
        for i in range(iterations):
            fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
            in_tar = fe_data.label
            in_data = fe_data[fe_data.columns[:-1]]
            scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=10, n_jobs=-1)
            #print scores
            in_vec = np.array([C, scores.mean(), scores.std()*2])
            mean_vec += in_vec[1]
        accuracy = np.append(accuracy, (mean_vec/iterations))
    #plot the accuracy
    plt.figure()
    plt.plot(SRlist,accuracy)
    #plt.xscale('log')
    plt.show()    
    return accuracy.argmax(), accuracy.max()
    
def bestfit_ADA(fe_data, alg, feat):
    accuracy = np.zeros(0)
    NElist = [i*50 for i in range(0,201)]
    LRlist = [i*0.25 for i in range(2,9) ]
    iterations = 5# 20
    for n_est in NElist:
        for l_rate in LRlist:
            clf = classifiers[alg](n_estimators = n_est, learning_rate=l_rate)
            mean_vec = 0.
            for i in range(iterations):
                fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
                in_tar = fe_data.label
                in_data = fe_data[fe_data.columns[:-1]]
                scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=10, n_jobs=-1)
                #print scores
                in_vec = np.array([C, scores.mean(), scores.std()*2])
                mean_vec += in_vec[1]
            accuracy_local = mean_vec/iterations
            _ = pd.Series([n_est, l_rate, accuracy])
            accuracy = accuracy.append(_)
    #plot the accuracy
    plt.figure()
    CS = plt.contour(X, Y, Z)
    plt.clabel(CS, inline=1, fontsize=10)
    plt.title('Simplest default with labels')
    plt.show()    
    return accuracy.argmax(), accuracy.max()