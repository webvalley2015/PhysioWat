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
        #'SVM': lambda kernel, C, deg=0 : SVC(kernel=kernel, C=C, degree=deg),
        'DCT': lambda max_f: DecisionTreeClassifier(max_features=max_f),
        'RFC': lambda n_est, max_f: RandomForestClassifier(n_estimators=n_est, 
                                                           max_features=max_f),
        'ADA': lambda n_est, l_rate: AdaBoostClassifier(n_estimators = n_est, 
                                                        learning_rate=l_rate),
        'LDA': lambda solver: LDA(solver),
        'QDA': lambda : QDA()
        }
        

classifiersDefaultParameters = {
        'KNN': KNeighborsClassifier(),
        #'SVM': SVC(kernel='linear'),
        'DCT': DecisionTreeClassifier(),
        'RFC': RandomForestClassifier(),
        'ADA': AdaBoostClassifier(),
        #'LDA': LDA(),
        'QDA': QDA()
        }
    
iterations = 5 #20 TRY

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
    This function use a k-fold crossvalidation to predict labels on the
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
        
    FIXME:
        the kf command doesn't seem valid but it seems all to work fine
    
    '''
    sol = data.label  #standard way to divide the feature DF from the target
    sol = np.array(sol)    
    data = data[data.columns[:-1]].as_matrix()
    
    #test_sol = test_data.label
    #test_in_data = test_data[test_data.columns[:-1]]

    #perform K-FOLD validation
    #set the K parameters, usually 5 or 10
    acc = np.zeros([k,1])
    kf = cross_validation.KFold(data.shape[0],k)# right here

    for train_index, test_index in kf:
        X_train, X_test = data[train_index], data[test_index]
        y_train, y_test = sol[train_index], sol[test_index]      
        predicted_labels = f.predict(f.get_selected_clf(X_train, y_train, alg), X_test, y_test )
        
    return sol, predicted_labels

   
def quick_fat(in_data, te_data, alg): # stand for quick Fit And Test
    '''
    This function fit on a dataset and test
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



def deep_alg_fat(in_data, te_data): #stans for Deep Algorithms Fit & Test
    '''
    Have to work on it.
    It perform a test on all the algorithms, but just only
    with the def parameters.
    Need to change it
      
    Params:
        in_data (pandas.DataFrame)        
            dataframe of extracted features (with labels as last column).
            Used to fit the model
        te_data (pandas.DataFrame)        
            datafram of extracted features (with labels as last column).
            Used to test the model
            
    Return:
        metricsDF (pd.Dataframe)
            dataframe of metrics, rows as metrics and cols as diff algorithms
        
    FIXME
        need to work on it. At the moment it doesn't work
    
    '''
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
    '''
    This function calculates the most common metrics for a classification
    and put them in a dictionary
      
    Params:
        y_true (np.array)
            array of the true labels of the features
        y_pred (np.array)
            array of the predicted labels
            
    Return:
        report (pd.Dict)
            dictionary containing all the features and their value
        conf_mat (np.array)
            matrix containing the dispersion matrix.
            Cols are real classes, rows the predicted ones
        
    Notes: if 'print' is deleted, testY is not necessary
    '''
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
    
def bestAlg(fe_data, metric):
    '''
    Given the dataframe of the extracted features and the metric to
    maximize it returns the clf ready to be used for the classification
    trying all the algotithms
    
    -- Disclaimer --
    It is very slow to execute
      
    Params:
        fe_data (pd.DataFrame)
            the feature dataframe to fit your data
        metric (string)
            string of three upcase characters to identify the metric.
            To have the list see the metrics dictionary

    Return:
        clf (classificators' object)
            the classificator fit on the given dataframe
            
    FIXME : misses the metrics option. Now it's just accuracy (and not global)


    '''
   
    the_metric = 0
    metric = 0 #just for debugging
    for a in classifiers.keys():
        loc_clf, loc_metric = bestfit(fe_data, a, metric)
        if loc_metric > the_metric:
            the_metric = loc_metric
            the_clf = loc_clf
        print the_clf, the_metric        
    in_tar = fe_data.label
    in_data = fe_data[fe_data.columns[:-1]]
    
    return the_clf.fit(in_data, in_tar)
    
def bestfit(fe_data, alg, metric):
    '''
    If you have some parameters to fit this is the right function.
    Given the dataframe of the extracted features, the algs and the metric to
    maximize it returns the clf ready to be used for the classification.
    
    -- Disclaimer --
    it just calls the right subfunction to proceed
      
    Params:
        fe_data (pd.DataFrame)
            the feature dataframe to fit your data
        alg (string)
            string of three upcase characters to identify the algorithm.
            To have the list see the classifiers dictionary
        metric (string)
            string of three upcase characters to identify the metric.
            To have the list see the metrics dictionary

    Return:
        clf (classificators' object)
            the classificator fit on the given dataframe
            
    FIXME : misses the metrics option. Now it's just accuracy (and not global)


    '''
       
    if   alg == 'KNN': clf, loc_metric = bestfit_KNN(fe_data, alg, metric)
    elif alg == 'SVM': clf, loc_metric = bestfit_SVM(fe_data, alg, metric)
    elif alg == 'DCT': clf, loc_metric = bestfit_DCT(fe_data, alg, metric)
    elif alg == 'RFC': clf, loc_metric = bestfit_RFC(fe_data, alg, metric)
    elif alg == 'ADA': clf, loc_metric = bestfit_ADA(fe_data, alg, metric)
    elif alg == 'LDA': clf, loc_metric = bestfit_LDA(fe_data, alg, metric)
    elif alg == 'QDA': clf, loc_metric = bestfit_QDA(fe_data, alg, metric)
        
        
    in_tar = fe_data.label
    in_data = fe_data[fe_data.columns[:-1]]
    
    return clf.fit(in_data, in_tar), loc_metric




'''
    --------------------------------------------------------------------
    - Now begins the sequence of subfunctions.                           -
    - They all work in the same way and all return the same parameters -
    - So this is the general description for them                      -
    --------------------------------------------------------------------
      
    Params:
        fe_data (pd.DataFrame)
            the feature dataframe to fit your data
        alg (string)
            string of three upcase characters to identify the algorithm.
            To have the list see the classifiers dictionary
        metric (string)
            string of three upcase characters to identify the metric.
            To have the list see the metrics dictionary

    Return:
        clf (classificators' object - not fit)
            the classificator ready to be fit on the given dataframe
        metric (float)
            the max value of the metric
'''




def bestfit_KNN(fe_data, alg, metric):  # ok
    my_met = np.matrix([[0,0,0]])
    NNlist = [1, 3, 5] #, 7, 9, 11]  TRY
    
    for nn in NNlist:
        clf = classifiers[alg](nn)
        mean_sum = 0.
        std_sum = 0.
        for i in range(iterations):
            fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
            in_tar = fe_data.label
            in_data = fe_data[fe_data.columns[:-1]]
            scores = cross_validation.cross_val_score(clf, in_data, in_tar, 
                                                      cv=10, n_jobs=1)
            #in this variables are saved the value of mean and error
            mean_sum += scores.mean()
            std_sum  += scores.std()
        in_vec = np.array([nn, (mean_sum/iterations), (std_sum/iterations)])
        my_met = np.vstack((my_met, in_vec))
        
        
    #plot the my_met
    plt.figure()
    plt.plot(my_met[:,0], my_met[:,1])
    #plt.xscale('log') #just if a parameter is exponentially growing
    plt.show()

    bestnn = NNlist[my_met[:,1].argmax()]
    clf = classifiers[alg](bestnn)
    return clf, my_met[:,1].max()
    
    
def bestfit_SVM(fe_data, alg, metric):
    Klist = ['linear', 'rbf', 'sigmoid', 'precomputed', 'poly']
    #can switch the order, but poly should be the last element
    bestC = bestdeg = bestMet = 0.
    bestkernel = bestmy_met = besterr_met = 0
    for i in range(len(Klist)):
        my_met = np.matrix([[0,0,0]])
        kernel = Klist[i]
        if kernel in ['linear', 'rbf']: #, 'sigmoid', 'precomputed']: TRY
            my_met = np.zeros(0)
            Clist = [ 10**i for i in range(-2,2)]#range(-5,8) ] TRY
            for C in Clist:
                clf = classifiers[alg](kernel, C)          
                mean_sum = 0.
                std_sum = 0.
                for i in range(iterations):
                    fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
                    in_tar = fe_data.label
                    in_data = fe_data[fe_data.columns[:-1]]
                    scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=10, n_jobs=1)
                    #in this variables are saved the value of mean and error
                    mean_sum += scores.mean()
                    std_sum  += scores.std()
                in_vec = np.array([C, (mean_sum/iterations), (std_sum/iterations)])
                my_met = np.vstack((my_met, in_vec))
            #plot the my_met
            plt.figure()
            plt.plot(my_met[:,0], my_met[:,1])
            plt.xscale('log') #just if a parameter is exponentially growing
            plt.show()
            if ( my_met[:,1].max() > bestMet ):
                bestMet = my_met[:,1].max()
                bestC = Clist[my_met[:,1].argmax()]
                bestkernel = kernel
                bestmy_met = my_met.copy()
                besterr_met = err_met.copy()
        elif kernel == 'poly':
            Clist = [ 10**i for i in range(-2,2)]#range(-5,8) ] TRY
            Dlist = [2,3]
            #watch out... this is a particular matrix
            q_met = np.zeros((len(Clist), len(Dlist)))
            err_met = np.zeros((len(Clist), len(Dlist)))
            for C in Clist:
                for deg in Dlist:
                    clf = classifiers[alg](kernel, C, deg)             
                    mean_sum = 0.
                    std_sum = 0.
                    for i in range(iterations):
                        fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
                        in_tar = fe_data.label
                        in_data = fe_data[fe_data.columns[:-1]]
                        scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=5, n_jobs=1)
                        
                        mean_sum += scores.mean()
                        std_sum  += scores.std()
                    mean_local = mean_sum/iterations
                    err_local  = std_sum/iterations
                    q_met[Clist.index(C), Dlist.index(deg)] = mean_local
                    err_met[Clist.index(C), Dlist.index(deg)] = err_local
            #plot the q_met
            plt.figure()
            plt.imshow(q_met)
            plt.title(kernel)
            plt.show()
            if (q_met.max() > bestMet ):
                bestMet = q_met.max()
                bestC, bestdeg = np.unravel_index(q_met.argmax(), (len(Clist), len(Dlist)))
                bestkernel = kernel
                bestmy_met = q_met.copy()
                besterr_met = err_met.copy()
          

    clf = classifiers[alg](kernel, bestC, bestdeg)
    return clf, max(my_met[:,1].max(), q_met.max())
    

def bestfit_DCT(fe_data, alg, metric):
    my_met = np.matrix([[0,0,0]])
    MFlist = [1, 1., 'sqrt']#, 'log2', None] TRY
    for max_f in MFlist:
        clf = classifiers[alg](max_f)
        mean_sum = 0.
        std_sum = 0.
        for i in range(iterations):
            fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
            in_tar = fe_data.label
            in_data = fe_data[fe_data.columns[:-1]]
            scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=10, n_jobs=1)
            #print scores
            #in this variables are saved the value of mean and error
            mean_sum += scores.mean()
            std_sum  += scores.std()
        in_vec = np.array([max_f, (mean_sum/iterations), (std_sum/iterations)])
        my_met = np.vstack((my_met, in_vec))
        
    #plot the my_met
    plt.figure()
    plt.plot(my_met[:,0], my_met[:,1])
    #plt.xscale('log') #just if a parameter is exponentially growing
    plt.show() 

    bestmax_f = MFlist[my_met[:,1].argmax()]
    clf = classifiers[alg](bestmax_f)
    return clf, my_met[:,1].max()
    
def bestfit_QDA(fe_data, alg, metric):  #ok
    my_met = np.matrix([[0,0,0]])
    #just default parameters
    clf = classifiers[alg]()
    mean_sum = 0.
    std_sum = 0.
    for i in range(iterations):
        fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
        in_tar = fe_data.label
        in_data = fe_data[fe_data.columns[:-1]]
        scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=10, n_jobs=1)
        #print scores
        #in this variables are saved the value of mean and error
        mean_sum += scores.mean()
        std_sum  += scores.std()
    in_vec = np.array([1, (mean_sum/iterations), (std_sum/iterations)])
    my_met = np.vstack((my_met, in_vec))

    #plot the my_met
    plt.figure()
    plt.plot(my_met[:,0], my_met[:,1])
    #plt.xscale('log') #just if a parameter is exponentially growing
    plt.show()    
    #print  my_met[:,1].max()
    return clf, my_met[:,1].max()
    
    
def bestfit_LDA(fe_data, alg, metric):
    my_met = np.matrix([[0,0,0]])
    SRlist = ['svd', 'lsqr', 'eigen']
    for solver in SRlist:
        clf = classifiers[alg](solver)
        mean_sum = 0.
        std_sum = 0.
        for i in range(iterations):
            fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
            in_tar = fe_data.label
            in_data = fe_data[fe_data.columns[:-1]]
            scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=10, n_jobs=1)
            #print scores
            #in this variables are saved the value of mean and error
            mean_sum += scores.mean()
            std_sum  += scores.std()
        in_vec = np.array([solver, (mean_sum/iterations), (std_sum/iterations)])
        my_met = np.vstack((my_met, in_vec))

    #plot the my_met
    X = np.arange(len(SRlist)+1)
    plt.plot(X, my_met[:,1])
    plt.xticks(X, SRlist, rotation=90)
    plt.show()        
    #plt.figure()
    #plt.plot(my_met[:,0], my_met[:,1])
    #plt.xscale('log') #just if a parameter is exponentially growing
    #plt.show()

    bestsolver = SRlist[my_met[:,1].argmax()]
    clf = classifiers[alg](bestsolver)
    print  my_met[:,1].max()
    return clf, my_met[:,1].max()
    
#watch out... this is a particular matrix... 65s for 75cvs
def bestfit_ADA(fe_data, alg, metric):
    NElist = [i*50 for i in range(1,5)]#201)] TRY
    LRlist = [i*0.25 for i in range(2,5)]#9) ] TRY
    my_met = np.zeros((len(NElist), len(LRlist)))
    err_met = np.zeros((len(NElist), len(LRlist)))
    for n_est in NElist:
        for l_rate in LRlist:
            clf = classifiers[alg](n_est, l_rate)
            mean_sum = 0.
            std_sum = 0.
            for i in range(iterations):
                fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
                in_tar = fe_data.label
                in_data = fe_data[fe_data.columns[:-1]]
                scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=5, n_jobs=1)
                mean_sum += scores.mean()
                std_sum  += scores.std()
            mean_local = mean_sum/iterations
            err_local  = std_sum/iterations
            my_met[NElist.index(n_est), LRlist.index(l_rate)] = mean_local
            err_met[NElist.index(n_est), LRlist.index(l_rate)] = err_local
    #plot the my_met
    plt.figure()
    plt.imshow(my_met)
    plt.show()    
    
    bestn_est, bestl_rate = np.unravel_index(my_met.argmax(), (len(NElist), len(LRlist)))
    clf = classifiers[alg](bestn_est, bestl_rate)
    return clf, my_met.max()
    
#watch out... this is a particular matrix    6m for 300cvs
def bestfit_RFC(fe_data, alg, metric):
    NElist = [i*25 for i in range(1,5)]#20)] TRY
    MFlist = [1, 1., 'sqrt']#, 'log2', None] TRY
    my_met = np.zeros((len(NElist), len(MFlist)))
    err_met = np.zeros((len(NElist), len(MFlist)))
    for n_est in NElist:
        for max_f in MFlist:
            clf = classifiers[alg](n_est, max_f)           
            mean_sum = 0.
            std_sum = 0.
            for i in range(iterations):
                fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
                in_tar = fe_data.label
                in_data = fe_data[fe_data.columns[:-1]]
                scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=5, n_jobs=1)
                mean_sum += scores.mean()
                std_sum  += scores.std()
            mean_local = mean_sum/iterations
            err_local  = std_sum/iterations
            my_met[NElist.index(n_est), MFlist.index(max_f)] = mean_local
            err_met[NElist.index(n_est), MFlist.index(max_f)] = err_local
    #plot the my_met
    plt.figure()
    plt.imshow(my_met)
    plt.show()    
    
    bestn_est, bestmax_f = np.unravel_index(my_met.argmax(), (len(NElist), len(MFlist)))
    clf = classifiers[alg](bestn_est, bestmax_f)
    return clf, my_met.max()