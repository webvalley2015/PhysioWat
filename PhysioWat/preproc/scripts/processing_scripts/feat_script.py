# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 17:10:50 2015

@author: andrea (Atlas1)

     ,___,
     (O.o)
     /),,)
      " "
     WHAT?

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.lda import LDA
from sklearn.qda import QDA
from sklearn.metrics import *

# names is the list containig the names of the possible 
# algorithms, check the consistency with the classifiers dictionary 
names = ["Nearest Neighbors", "Support Vector Machine", "RBF SVM\t", "Decision Tree",
             "Random Forest", "AdaBoost\t", "LDA\t", "QDA\t"]

#classifiers is the pd.dictionary of the possible algorithms.
# use as " classifiers[alg](set_parameters) " once you have them
classifiers = {
        'KNN': lambda nn: KNeighborsClassifier(n_neighbors=nn),
        'SVM': lambda kernel, C, degree : SVC(kernel=kernel, C=C, degree=deg),
        'DCT': lambda max_f: DecisionTreeClassifier(max_features=max_f),
        'RFC': lambda n_est, max_f: RandomForestClassifier(n_estimators=n_est, 
                                                           max_features=max_f),
        'ADA': lambda n_est, l_rate: AdaBoostClassifier(n_estimators = n_est, 
                                                        learning_rate=l_rate),
        'LDA': lambda solver: LDA(solver=solver),
        'QDA': lambda : QDA()
        }
        

classifiersDefaultParameters = {
        'KNN': KNeighborsClassifier(),
        'SVM': SVC(kernel='linear'),
        'DCT': DecisionTreeClassifier(),
        'RFC': RandomForestClassifier(),
        'ADA': AdaBoostClassifier(),
        'LDA': LDA(),
        'QDA': QDA()
        }
    

def feat_boxplot(x):
    '''
    This function makes a big BOX-WHISKER plot with all the 
    features passed in input, one bar for each class
    
    Params:
        x (pandas.DataFrame)        
            dataset of extracted features (optional: just 
            pass the features you want to plot)
            
    Return:
        None
        (on the screen) the subplot with the barplots
            
    FIXME:
        this function will be modified to return a matrix 
        ready to be plotted with js libraries
    
    '''
    plt.style.use('ggplot')
    data = pd.DataFrame()
    for i in range(len(x.columns)-1):   #for each feature in your dataframe X
        data0 = x.query('label == '+str(0)).iloc[:,i]   #calc the boxplot for 
                                                        #this class
        data1 = x.query('label == '+str(1)).iloc[:,i]   # and for this one
        data2 = x.query('label == '+str(2)).iloc[:,i]   # ...
        data3 = x.query('label == '+str(3)).iloc[:,i]
        data = [data0, data1, data2, data3]
        plt.subplot(5,10, i+1)                          #it will be deleted
        plt.boxplot(data)
        plt.title(x.columns[i])
    plt.show()
    # return as you want      #not done yet
    
def crossvalidate_1df_SVM(data, alg, k):
    '''
    This function use a k-fold crossvalidation to predict labels from the
    input database
      
    Params:
        data (pandas.DataFrame)        
            dataset of extracted features (with labels as last column)
        alg (string)
            string of three upcase characters to identify the algorithm.
            To have the list see the classifiers dictionary
        k (int)
            the k parameters for the k-fold cross validation.
            Usually 5 or 10 in most analisys
            
    Return:
        sol (np.array)
            array of the true labels (that is y_true)
        predicted_labels (np.array)
            array of the predicted labels (that is y_pred)
        (on the screen) the accuracy mean for each k-fold, because of the
            predict function
        
    Notes: just use to copy lines
    
    '''
    sol = data.label  #standard way to divide the feature DF from the target
    sol = np.array(sol)    
    data = data[data.columns[:-1]].as_matrix()
    
    #test_sol = test_data.label
    #test_in_data = test_data[test_data.columns[:-1]]

    #perform K-FOLD validation
    #set the K parameters, usually 5 or 10
    acc = np.zeros([k,1])
    kf = cross_validation.KFold(data.shape[0],k), shuffle=True)

    for train_index, test_index in kf:
        X_train, X_test = data[train_index], data[test_index]
        y_train, y_test = sol[train_index], sol[test_index]      
        predicted_labels = f.predict(f.get_selected_clf(X_train, y_train, alg), X_test, y_test )
        
    return sol, predicted_labels

   
def quick_fat(in_data, te_data, alg): # stand for quick Fit And Test
    '''
    This function use to fit on a dataset and test
    on one another. Just a quick prediction
      
    Params:
        in_data (pandas.DataFrame)        
            dataset of extracted features (with labels as last column).
            Used to fit the model
        te_data (pandas.DataFrame)        
            dataset of extracted features (with labels as last column).
            Used to test the model
        alg (string)
            string of three upcase characters to identify the algorithm.
            To have the list see the classifiers dictionary
            
    Return:
        te_tar.values (np.array)
            array of the true labels (that is y_true)
        y_pred (np.array)
            array of the predicted labels
        (on the screen) the accuracy mean for each k-fold, because of the
            predict function
        
    Notes: it does not perform cross-validation
    
    '''
    te_tar = te_data.label #standard way to divide the feat_DF from the target
    in_tar = in_data.label
    te_data = te_data[te_data.columns[:-1]]
    in_data = in_data[in_data.columns[:-1]]

    y_pred = f.predict(f.get_selected_clf(in_data, in_tar, alg), te_data, te_tar )
    return te_tar.values , y_pred
    
def get_selected_clf(X, Y, alg):
    '''
    This function fits the classificator (clf) on a given algorithm
      
    Params:
        X (np.array - a matrix)        
            dataset of extracted features (no labels as last column).
            Used to fit the model
        Y (np.array)        
            array of true labels
        alg (string)
            string of three upcase characters to identify the algorithm.
            To have the list see the classifiers dictionary
            
    Return:
        clf (classificators' object)
            the classificator fitted on the given dataframe
            
    FIXME: the clf requires a list of obj to perform, not a dictionary
    
    '''
    clf = classifiersDefaultParameters[alg]
    clf=clf.fit(X, Y)
    return  clf

def predict(clf, testX, testY):
    '''
    This function predicts the labels of a given dataframe and test
    it to obtain a quick accuracy print
      
    Params:
        clf (classificators' object)
            the classificator fitted on the given dataframe
        testX (np.array - a matrix)        
            dataset of extracted features (no labels as last column).
            Used to predict the labels
        testY (np.array)        
            array of true labels
            
    Return:
        te_tar.values (np.array)
            array of the true labels (that is y_true)
        y_pred (np.array)
            array of the predicted labels
        (on the screen) the accuracy of the prediction
        
    Notes: if 'print' is deleted, testY is not necessary
    
    '''
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
       
    if   alg == 'KNN': pos, val = bestfit_KNN(fe_data, alg, feat)
    elif alg == 'SVM': pos, val = bestfit_SVM(fe_data, alg, feat)
    elif alg == 'DCT': pos, val = bestfit_DCT(fe_data, alg, feat)
    elif alg == 'RFC': pos, val = bestfit_RFC(fe_data, alg, feat)
    elif alg == 'ADA': pos, val = bestfit_ADA(fe_data, alg, feat)
    elif alg == 'LDA': pos, val = bestfit_LDA(fe_data, alg, feat)
    elif alg == 'QDA': pos, val = bestfit_QDA(fe_data, alg, feat)
        
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
            scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=10, n_jobs=1)
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


def bestfit_SVC(fe_data, alg, feat):
    Klist = ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']
    iterations = 5 #20
    for i in range(len(Klist)):
        kernel = Klist[i]
        if kernel in ['linear', 'rbf', 'poly', 'sigmoid', 'precomputed']:
            accuracy = np.zeros(0)
            Clist = [ 10**i for i in range(-5,8) ]
            for C in Clist:
                #clf = classifiers[alg](kernel=kernel, C=C) 
                clf = SVC(kernel=kernel, C=C)                
                mean_vec = 0.
                for i in range(iterations):
                    fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
                    in_tar = fe_data.label
                    in_data = fe_data[fe_data.columns[:-1]]
                    scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=10, n_jobs=1)
                    #print scores
                    in_vec = np.array([C, scores.mean(), scores.std()*2])
                    mean_vec += in_vec[1]
                accuracy = np.append(accuracy, (mean_vec/iterations))
            #plot the accuracy
            plt.figure()
            plt.plot(Clist,accuracy)
            plt.title(kernel)
            plt.show()
        elif kernel == 'poly':
            Clist = [ 10**i for i in range(-5,8) ]
            Dlist = [2,3]
            accuracy = np.zeros((len(Clist), len(Dlist)))
            for C in Clist:
                for deg in Dlist:
                    #clf = classifiers[alg](kernel=kernel, C=C, degree=deg)            
                    clf = SVC(kernel=kernel, C=C, degree=deg)                    
                    mean_vec = 0.
                    for i in range(iterations):
                        fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
                        in_tar = fe_data.label
                        in_data = fe_data[fe_data.columns[:-1]]
                        scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=5, n_jobs=1)
                        #print scores
                        in_vec = np.array([C, scores.mean(), scores.std()*2])
                        mean_vec += in_vec[1]
                    accuracy_local = mean_vec/iterations
                    accuracy[Clist.index(C), Dlist.index(deg)] = accuracy_local
            #plot the accuracy
            plt.figure()
            plt.imshow(accuracy)
            plt.title(kernel)
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
            scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=10, n_jobs=1)
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
        scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=10, n_jobs=1)
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
    
#!!! solver
def bestfit_LDA(fe_data, alg, feat):
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
            scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=10, n_jobs=1)
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
    NElist = [i*50 for i in range(1,201)]
    LRlist = [i*0.25 for i in range(2,9) ]
    accuracy = np.zeros((len(NElist), len(LRlist)))
    iterations = 20
    for n_est in NElist:
        for l_rate in LRlist:
            clf = classifiers[alg](n_estimators = n_est, learning_rate=l_rate)
            #clf = AdaBoostClassifier(n_estimators = n_est, learning_rate=l_rate)
            mean_vec = 0.
            for i in range(iterations):
                fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
                in_tar = fe_data.label
                in_data = fe_data[fe_data.columns[:-1]]
                scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=5, n_jobs=1)
                #print scores
                in_vec = np.array([C, scores.mean(), scores.std()*2])
                mean_vec += in_vec[1]
            accuracy_local = mean_vec/iterations
            accuracy[NElist.index(n_est), LRlist.index(l_rate)] = accuracy_local
    #plot the accuracy
    plt.figure()
    plt.imshow(accuracy)
    plt.show()    
    return accuracy.argmax(), accuracy.max()
    
    
def bestfit_RFC(fe_data, alg, feat):
    NElist = [i*25 for i in range(1,20)]
    MFlist = [1, 1., 'sqrt', 'log2', None]
    accuracy = np.zeros((len(NElist), len(MFlist)))
    iterations = 10# 20
    for n_est in NElist:
        for max_f in MFlist:
            #clf = classifiers[alg](n_estimators = n_est, max_features=max_f)
            #print(max_f)
            clf = RandomForestClassifier(n_estimators=n_est, max_features=max_f)            
            mean_vec = 0.
            for i in range(iterations):
                fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
                in_tar = fe_data.label
                in_data = fe_data[fe_data.columns[:-1]]
                scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=5, n_jobs=1)
                #print scores
                in_vec = np.array([C, scores.mean(), scores.std()*2])
                mean_vec += in_vec[1]
            accuracy_local = mean_vec/iterations
            accuracy[NElist.index(n_est), MFlist.index(max_f)] = accuracy_local
    #plot the accuracy
    plt.figure()
    plt.imshow(accuracy)
    plt.show()    
    return accuracy.argmax(), accuracy.max()