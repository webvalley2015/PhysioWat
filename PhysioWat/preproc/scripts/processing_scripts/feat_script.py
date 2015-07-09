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
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.lda import LDA
from sklearn.qda import QDA
from sklearn.metrics import *
from scipy import stats
import time
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

# names is the list containig the names of the possible 
# algorithms, check the consistency with the classifiers dictionary 
names = ["Nearest Neighbors", "Support Vector Machine", "RBF SVM\t", "Decision Tree",
             "Random Forest", "AdaBoost\t", "LDA\t", "QDA\t"]

#classifiers is the pd.dictionary of the possible algorithms.
# use as " classifiers[alg](set_parameters) " once you have them
classifiers = {
        'KNN': lambda nn: KNeighborsClassifier(n_neighbors=nn),
        'SVM': lambda kernel, C : SVC(kernel=kernel, C=C),
        'DCT': lambda max_f: DecisionTreeClassifier(max_features=max_f),
        'RFC': lambda n_est, max_f: RandomForestClassifier(n_estimators=n_est, 
                                                           max_features=max_f),
        'ADA': lambda n_est, l_rate: AdaBoostClassifier(n_estimators = n_est, 
                                                        learning_rate=l_rate),
        'LDA': lambda solver: LDA(solver),
        #'QDA': lambda : QDA()
        }
        

classifiersDefaultParameters = {
        'KNN': KNeighborsClassifier(),
        'SVM': SVC(kernel='linear'),
        'DCT': DecisionTreeClassifier(),
        'RFC': RandomForestClassifier(),
        'ADA': AdaBoostClassifier(),
        'LDA': LDA(),
        #'QDA': QDA()
        }
    
iterations = 5 #20 TRY
cv_val = 5

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
    #    plt.style.use('ggplot')
    #    step = 30
    #    end =  x.shape[1]
    #    data = pd.DataFrame()
    #    #ttest = np.zeros(end)
    #    for k in range(0, end, step):
    #        for i in range(k, k+step):   #for each feature in your dataframe X
    #            if i >= end :
    #                break
    #            data0 = x.query('LAB == '+str(0)).iloc[:,i]   #calc the boxplot for 
    #                                                            #this class
    #            data1 = x.query('LAB == '+str(1)).iloc[:,i] 
    #            data = [data0, data1]
    #            #ttest[i] = stats.ttest_ind(data0,data1)
    #            plt.subplot(5,6, (i%step)+1)                          #it will be deleted
    #            plt.boxplot(data)
    #            plt.axis('off')
    #            plt.title(x.columns[i], fontsize=5)
    #        plt.savefig('./figs/fig'+str(nam)+'XXX'+str(k)+'.png')
    
    end =  x.shape[1]
    datas = []
    labels = np.unique(x['LAB'])
    #ttest = np.zeros(end)
    for i in range(0, end):
        data = []
        for lab in labels:
            temp_serie = x.query('LAB == '+str(lab)).iloc[:,i]
            data.append(get_box_vals(temp_serie))
        datas.append(data)
        plt.subplot(3,4, i+1)
        plt.boxplot(data)
        plt.title(x.columns[i])#, fontsize=5)
    #    plt.subplot(23, 12)                          #it will be deleted
    #    plt.boxplot(datas)
    #    plt.axis('off')
    #    plt.title(x.columns[i], fontsize=5)
    #    plt.savefig('./figs/fig'+str(nam)+'XXX'+str(k)+'.png')    
    plt.savefig('boxw_best10.png')
    return datas

def get_box_vals(serie):
    '''
    This function calculates the five values for a box-plot of a pandas Series
    
    Params:
        serie (pandas.Series)
            Series of all the values of a feature of one label
        
    Return:
        boxvals (python list)
            array containing the five values for box-plot: min, 1° quartile, median, 3° quartile, max
    '''
    median = np.median(serie)
    minimum = np.min(serie)
    maximum = np.max(serie)
    quartile1 = np.percentile(serie, 25)
    quartile3 = np.percentile(serie, 75)
    return [minimum, quartile1, median, quartile3, maximum]

  
def quick_crossvalidate(data, alg):
  
    clf = classifiersDefaultParameters[alg]
    mean_local, err_local = iterate_crossvalidation(clf, data, 'ACC')
    
    lab = data.LAB
    data = data[data.columns[:-1]]
    

    return clf.fit(data, lab), mean_local, err_local
    
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

def my_predict(clf, testX, testY):
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
    #score = clf.score(testX, testY)
    #print "Accuracy %.5f" % (score)
    return labels_predict



def deep_alg_fat(in_data, te_data): #stays for Deep Algorithms Fit & Test
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
    te_tar = te_data.LAB
    in_tar = in_data.LAB
    te_data = te_data[te_data.columns[:-1]]
    in_data = in_data[in_data.columns[:-1]]
        
        
    #print 'List of accuracies...'
    for name, clf in zip(names, classifiers.items):
        #ax = plt.subplot(len(datasets), len(classifiers) + 1, i)
        clf.fit(in_data, in_tar)
        #labels_predict = clf.predict(te_data)
        score = clf.score(te_data, te_tar)
        #print "Accuracy for\t " + name +"\t  %.5f" %(score)
        
        
        
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
        'ACC': accuracy_score(y_true, y_pred),
        'F1M': f1_score(y_true, y_pred, average='macro'),
        'F1m': f1_score(y_true, y_pred, average='micro'),
        'F1W': f1_score(y_true, y_pred, average='weighted'),
        'WHM': fbeta_score(y_true, y_pred, average='weighted', beta=1),
        #'Hamming loss': hamming_loss(y_true, y_pred),
        #'Jaccard distance': jaccard_similarity_score(y_true, y_pred),
        'PRM': precision_score(y_true, y_pred, average='macro'),
        'PRm': precision_score(y_true, y_pred, average='micro'), 
        'PRW': precision_score(y_true, y_pred, average='weighted'),
        'REM': recall_score(y_true, y_pred, average='macro'),
        'REm': recall_score(y_true, y_pred, average='micro'), 
        'REW': recall_score(y_true, y_pred, average='weighted'), 
    }
    conf_mat = confusion_matrix(y_true, y_pred)

    #X = np.arange(len(report))
    #plt.bar(X, report.values(), align='center', width=0.5)
    #plt.xticks(X, report.keys(), rotation=90)
    #ymax = max(report.values()) + 1
    #plt.ylim(0, ymax)
    #plt.draw()  
    
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
    print 'Starting... bestAlg()'
    the_metric = 0
    the_mat = np.zeros((len(classifiers), 3))
    for i, a in enumerate(classifiers.keys()):
        print i, a
        loc_clf, loc_metric, loc_error = bestfit(fe_data, a, metric, fromalg=True)
        the_mat[i, :] = np.array([i, loc_metric, loc_error])
        if loc_metric > the_metric:
            the_metric = loc_metric
            the_clf = loc_clf
            the_error = loc_error
        print loc_metric, loc_clf
 
    #    in_tar = fe_data.LAB
    #    in_data = fe_data[fe_data.columns[:-1]]
    #    
    #    big_iterations = iterations*2 #100 TRY
    #    mean_sum = 0.
    #    std_sum = 0.
    #    for i in range(big_iterations):
    #        fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
    #        in_tar = fe_data.LAB
    #        in_data = fe_data[fe_data.columns[:-1]]
    #        scores = cross_validation.cross_val_score(the_clf, in_data, in_tar, cv=cv_val, n_jobs=1)
    #        mean_sum += scores.mean()
    #        std_sum  += scores.std()
    #    quick_res = np.array([(mean_sum/big_iterations), (std_sum/big_iterations)])
    return the_clf, the_mat
    
def bestfit(fe_data, alg, metric, fromalg=False):
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
       
    print 'Starting... best_fit on ', alg   
    if   alg == 'KNN': clf, loc_metric, loc_error, loc_mat = bestfit_KNN(fe_data, alg, metric)
    elif alg == 'SVM': clf, loc_metric, loc_error, loc_mat = bestfit_SVM(fe_data, alg, metric)
    elif alg == 'DCT': clf, loc_metric, loc_error, loc_mat = bestfit_DCT(fe_data, alg, metric)
    elif alg == 'RFC': clf, loc_metric, loc_error, loc_mat = bestfit_RFC(fe_data, alg, metric)
    elif alg == 'ADA': clf, loc_metric, loc_error, loc_mat = bestfit_ADA(fe_data, alg, metric)
    elif alg == 'LDA': clf, loc_metric, loc_error, loc_mat = bestfit_LDA(fe_data, alg, metric)
    elif alg == 'QDA': clf, loc_metric, loc_error, loc_mat = bestfit_QDA(fe_data, alg, metric)
        
        
    in_tar = fe_data.LAB
    in_data = fe_data[fe_data.columns[:-1]]
    
    if fromalg == True:
        return clf.fit(in_data, in_tar), loc_metric, loc_error
    else:
        return clf.fit(in_data, in_tar), loc_metric, loc_error, loc_mat




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
    NNlist = [1, 3, 5, 7, 9, 11]  #TRY
    my_met = np.zeros((len(NNlist), 3))
    mean_max = 0
    
    for i, nn in enumerate(NNlist):
        clf = classifiers[alg](nn)
        mean_local, err_local = iterate_crossvalidation(clf, fe_data, metric)
        if mean_local > mean_max:
                mean_max = mean_local
                max_pos = i
            
        my_met[NNlist.index(nn), :] = np.array([nn, mean_local, err_local])
        
        
    #plot the my_met
    #plt.figure()
    #plt.plot(my_met[:,0], my_met[:,1])
    #plt.xscale('log') #just if a parameter is exponentially growing
    #plt.show()

    bestnn = NNlist[my_met[:,1].argmax()]
    clf = classifiers[alg](bestnn)
    
    return clf, my_met[max_pos,1], my_met[max_pos,2], my_met
    
    
def bestfit_SVM(fe_data, alg, metric):
    Klist = ['linear', 'rbf', 'sigmoid'] #TRY
    bestC = 0.
    mean_max = 0
    Clist = [ 10**i for i in range(-3,6) ]# TRY
    my_met = np.matrix([0,0,0,0])
    for k, kernel in enumerate(Klist):
        for i, C in enumerate(Clist):
            print kernel, C
            clf = classifiers[alg](kernel, C)          
            mean_local, err_local = iterate_crossvalidation(clf, fe_data, metric)
            if mean_local > mean_max:
                mean_max = mean_local
                max_pos = k*len(Clist)+i
            in_vec = np.array([C, mean_local, err_local, k])
            my_met = np.vstack((my_met, in_vec))
        #plot the my_met
        #plt.figure()
        #plt.plot(my_met[:,0], my_met[:,1])
        #plt.xscale('log') #just if a parameter is exponentially growing
        #plt.show()
    
    my_met = my_met[1:,:]
    bestkernel = Klist[int(my_met[my_met[:,1].argmax(),3])]
    bestC = int(my_met[my_met[:,1].argmax(),0])
        
    clf = classifiers[alg](bestkernel, bestC)
    print 'reached end'
    #return clf, my_met[max_pos,1], my_met[max_pos,2], my_met
    return clf, my_met[int(mean_max),1].max(), my_met[max_pos,2], my_met
    

def bestfit_DCT(fe_data, alg, metric):
    MFlist = [1, None, 'log2', 'sqrt'] #TRY
    my_met = np.zeros((len(MFlist), 3))
    mean_max = 0    
    for k, max_f in enumerate(MFlist):
        clf = classifiers[alg](max_f)
        mean_local, err_local = iterate_crossvalidation(clf, fe_data, metric)
        if mean_local > mean_max:
                mean_max = mean_local
                max_pos = k            
        my_met[MFlist.index(max_f), :] = np.array([k, mean_local, err_local])
        
    #plot the my_met
    #plt.figure()
    #plt.plot(my_met[:,0], my_met[:,1])
    #plt.xscale('log') #just if a parameter is exponentially growing
    #plt.show() 

    bestmax_f = MFlist[my_met[:,1].argmax()]
    clf = classifiers[alg](bestmax_f)
    return clf, my_met[max_pos,1], my_met[max_pos,2], my_met
    
def bestfit_QDA(fe_data, alg, metric):  #ok
    my_met = np.matrix([[0,0,0]])
    #just default parameters
    clf = classifiers[alg]()
    mean_local, err_local = iterate_crossvalidation(clf, fe_data, metric)
    my_met = np.array([0, mean_local, err_local])

    #plot the my_met
    #plt.figure()
    #plt.plot(my_met[:,0], my_met[:,1])
    #plt.xscale('log') #just if a parameter is exponentially growing
    #plt.draw()  
    #print  my_met[:,1].max()
    return clf, my_met[1], my_met[2], my_met
    
    
def bestfit_LDA(fe_data, alg, metric):
    SRlist = ['svd', 'lsqr']#, 'eigen']
    my_met = np.zeros((len(SRlist), 3))
    mean_max = 0
    
    for k, solver in enumerate(SRlist):
        clf = classifiers[alg](solver)
        mean_local, err_local = iterate_crossvalidation(clf, fe_data, metric)
        if mean_local > mean_max:
                mean_max = mean_local
                max_pos = k
        my_met[SRlist.index(solver), :] = np.array([k, mean_local, err_local])

    #plot the my_met
    #X = np.arange(len(SRlist)+1)
    #plt.plot(X, my_met[:,1])
    #plt.xticks(X, SRlist, rotation=90)
    #plt.draw()      
    #plt.figure()
    #plt.plot(my_met[:,0], my_met[:,1])
    #plt.xscale('log') #just if a parameter is exponentially growing
    ##plt.show()

    # print  my_met
    bestsolver = SRlist[my_met[:,1].argmax()]
    clf = classifiers[alg](bestsolver)
    
    return clf, my_met[max_pos,1], my_met[max_pos,2], my_met
    
#watch out... this is a particular matrix... 65s for 75cvs
def bestfit_ADA(fe_data, alg, metric):
    NElist = [i*50 for i in range(1, 201)]# TRY
    LRlist = [i*0.25 for i in range(2,8)] # TRY
    my_met = np.zeros((len(NElist), len(LRlist)))
    err_met = np.zeros((len(NElist), len(LRlist)))
    #j, tstop = 0, 0
    for n_est in NElist:
        for l_rate in LRlist:
            clf = classifiers[alg](n_est, l_rate)
            mean_local, err_local = iterate_crossvalidation(clf, fe_data, metric)
            my_met[NElist.index(n_est), LRlist.index(l_rate)] = mean_local
            err_met[NElist.index(n_est), LRlist.index(l_rate)] = err_local
    #plot the my_met
    #plt.figure()
    #plt.imshow(my_met)
    #plt.draw()  
    #print '{}'.format(tstop /float(i))
    bestn_est, bestl_rate = np.unravel_index(my_met.argmax(), (len(NElist), len(LRlist)))
    #print my_met.max()
    #print NElist[bestl_rate]
    #print LRlist[bestn_est]
    clf = classifiers[alg](NElist[bestn_est], LRlist[bestl_rate])
    return clf, my_met[bestn_est, bestl_rate], err_met[bestn_est, bestl_rate], my_met#, err_met
    
#watch out... this is a particular matrix    6m for 300cvs
def bestfit_RFC(fe_data, alg, metric):
    NElist = [i*25 for i in range(1,20,10)]# TRY
    MFlist = [1,  None, 'log2','sqrt' ] #TRY
    my_met = np.zeros((len(NElist), len(MFlist)))
    err_met = np.zeros((len(NElist), len(MFlist)))
    for n_est in NElist:
        for max_f in MFlist:
            clf = classifiers[alg](n_est, max_f)           
            mean_local, err_local = iterate_crossvalidation(clf, fe_data, metric)
            my_met[NElist.index(n_est), MFlist.index(max_f)] = mean_local
            err_met[NElist.index(n_est), MFlist.index(max_f)] = err_local
    #plot the my_met
    #plt.figure()
    #plt.imshow(my_met)
    #plt.draw()  
    
    bestn_est, bestmax_f = np.unravel_index(my_met.argmax(), (len(NElist), len(MFlist)))
    clf = classifiers[alg](NElist[bestn_est], MFlist[bestmax_f])
    return clf, my_met[bestn_est, bestmax_f], err_met[bestn_est, bestmax_f], my_met#, err_met
    

def iterate_crossvalidation(clf, fe_data, metric):
    metric_list = {
        'ACC': 'accuracy',
        'F1M': 'f1_macro',
        'F1m': 'f1_micro',
        'F1W': 'f1_weighted',
        #'WHM': known bug not implemented
        'PRM': 'precision_macro',
        'PRm': 'precision_micro',
        'PRW': 'precision_weighted',
        'REM': 'recall_macro',
        'REm': 'recall_micro',
        'REW': 'recall_weighted'
    }
    mean_sum = 0.
    std_sum = 0.
    for i in range(iterations):
        print 'it_cv ',i, '   '
        fe_data = fe_data.iloc[np.random.permutation(len(fe_data))]
        in_tar = fe_data.LAB
        in_data = fe_data[fe_data.columns[:-1]]

        scores = cross_validation.cross_val_score(clf, in_data, in_tar, cv=cv_val, scoring=metric_list[metric])
        mean_sum += scores.mean()
        std_sum  += scores.std()
    mean_local = mean_sum/iterations
    err_local  = std_sum/iterations
    return mean_local, err_local

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
        
    Notes: it does perform cross-validation
    
    '''
    te_tar = te_data.LAB #standard way to divide the feat_DF from the target
    in_tar = in_data.LAB
    te_data = te_data[te_data.columns[:-1]]
    in_data = in_data[in_data.columns[:-1]]

    y_pred = my_predict(get_selected_clf(in_data, in_tar, alg), te_data, te_tar )
    return te_tar.values , y_pred
    


def normalize(df):
    lab = df.LAB
    df = df[df.columns[:-1]]
    #df = df[df.columns[:3]]
    df_norm = (df - df.mean(axis=0)) / df.std(axis=0)
    df_norm = pd.concat((df, lab), axis=1)
    df_norm = df_norm.dropna(how='any')
    return df_norm

def split(df, how_much):    #need to be float between 0 and 1
    colnames = df.columns

    b = df.LAB
    a = df[df.columns[:-1]]
    a_train, a_test, b_train, b_test = train_test_split(a, b, test_size=how_much, random_state=42)
    
    a_train = pd.DataFrame(a_train)
    b_train = pd.DataFrame(b_train)
    train = pd.concat((a_train, b_train), axis=1)
    train.columns = colnames
    
    a_test = pd.DataFrame(a_test)
    b_test = pd.DataFrame(b_test)
    test = pd.concat((a_test, b_test), axis=1)
    test.columns = colnames
    
    return train, test
   
def cut_feature(df, k):
    label = df.LAB
    df = df[df.columns[:-1]]
    pippo = SelectKBest(f_classif, k=k).fit(df, label)
    return np.append(pippo.get_support(), True)
   

def getfeatnumber(df_in, df_te, k):
    #return the dfin e dfte of len "best k feat"
    sel_cut = cut_feature(df_in, k)
    train_data = df_in.ix[:,sel_cut]
    test_data = df_te.ix[:,sel_cut]
    return train_data, test_data, list(train_data.columns)

def bestfeatn(input_data, intest_data):
    #space = np.linspace(0, input_data.shape[1], num=deepk).astype(np.int64)
    space = [1,2,3,4,5,10,15,20,25,50,75,100,150,200,500,1000,2000,5000,10000]
    my_met = np.zeros((len(space),2))
    best_feat_num = [0,0]
    end = input_data.shape[1]   
    listoflists=[]
    for k, i in enumerate(space):
        if i >= end :
            break
        print 'Begin extraction of ', i , ' best features'
        sel_cut = cut_feature(input_data, i)
        train_data = input_data.ix[:,sel_cut]
        test_data = intest_data.ix[:,sel_cut]
        listoflists.append((list(train_data.columns)))
        
        #feat_boxplot(train_data, str(i))
        y_true, y_pred = quick_fat(train_data, test_data, 'RFC')
        #clf = bestfit(train_data, 'RFC', 1)
        #y_true = test_data.LAB
        #y_pred = my_predict(clf, test_data, y_true )
        print y_true
        print y_pred
        dic_metric, conf_mat = get_report(y_true, y_pred)
        #print conf_mat
        my_met[k,:] = (i, dic_metric['ACC']) #to improve here better
        if dic_metric['ACC'] > best_feat_num[1]:
            best_feat_num[1] = dic_metric['ACC']
            best_feat_num[0] = i
            
    best_feat_num = best_feat_num[0]
    sel_cut = cut_feature(input_data, best_feat_num)
    train_data = input_data.ix[:,sel_cut]
    test_data = intest_data.ix[:,sel_cut] 
    
    my_met = my_met[:k,:]

    return  train_data, test_data, my_met, listoflists
        
        

def pers_crossvalidation1(data, alg, par):
    clf = classifiers[alg](par1)
    mean_local, err_local = iterate_crossvalidation(clf, data, 'ACC')
    
    lab = data.LAB
    data = data[data.columns[:-1]]
    return clf.fit(data, lab), mean_local, err_local

    
def pers_crossvalidation2(data, alg, par1, par2):
    clf = classifiers[alg](par1, par2)
    mean_local, err_local = iterate_crossvalidation(clf, data, 'ACC')
    
    lab = data.LAB
    data = data[data.columns[:-1]]
    return clf.fit(data, lab), mean_local, err_local  


def import_bojan():
    localdir = '/home/andrea/Work/data/BojanAnalisys/'
    features = pd.read_table(filepath_or_buffer=localdir + 'features.txt', sep='\n', header=None)#, index_col=None, sep=',')
    colnames = pd.Series(features[0])

    xtest  = pd.read_csv(localdir+'X_test.txt', names=colnames, header=None, delim_whitespace=True)
    xtrain = pd.read_csv(localdir+'X_train.txt', names=colnames, header=None, delim_whitespace=True)
    ytest  = pd.read_csv(localdir+'y_test.txt', header=None,delim_whitespace=True)
    ytest.columns = ['LAB']
    ytrain = pd.read_csv(localdir+'y_train.txt', header=None, delim_whitespace=True)
    ytrain.columns = ['LAB']
    test = pd.concat((xtest,ytest), axis=1)
    train = pd.concat((xtrain,ytrain), axis=1)
    
def import_claire():
    print 'Starting main...'  
    #to import the dataset (extracted feature)
    localdir = '/home/andrea/Work/data/Physio/physio/PhysioWat/PhysioWat/preproc/scripts/processing_scripts/output/'
    #input_data = pd.DataFrame.from_csv(path=localdir + 'feat_claire_labeled.csv', index_col=None, sep=',')
    input_data = pd.DataFrame.from_csv(path=localdir + 'feat_claire_10labels.csv', index_col=None, sep=',')
    
    #to normalize the data (optional)
    norm_data = normalize(input_data)
            
    #feature selection
    train_data, test_data = split(norm_data, 0.)
    
    clf, metric = bestAlg(train_data, 'ACC')
    dic_metric, conf_mat = test_learning(clf, test_data)
    
    train_data, test_data, my_met, listoflistsofbest = bestfeatn(train_data, test_data)
    feat_boxplot(norm_data[listoflistsofbest[5]])
    #train_data, test_data, listofbest = getfeatnumber( train_data, test_data, 10)
    clf, metric = bestAlg(train_data, 'ACC')
    dic_metric, conf_mat = test_learning(clf, test_data)
    
    #plot of feature selection
    #plt.figure()
    #plt.plot(range(len(res_mat)),res_mat[:,1])
    
    #search the best alg with the best classifier    
    #print dic_metric
    #print conf_mat
    
def test_learning(clf, test_data):
    y_true = test_data.LAB
    te_data = test_data[test_data.columns[:-1]]
    y_pred = my_predict(clf, te_data, y_true )
    return get_report(y_true, y_pred)
   
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    # from matplotlib.backends.backend_pdf import PdfPages

    print 'Starting main...'  
    #to import the dataset (extracted feature)
    localdir = '/home/andrea/Work/data/Physio/physio/PhysioWat/PhysioWat/preproc/scripts/processing_scripts/output/'
    train_data = pd.DataFrame.from_csv(path=localdir + 'feat_train.csv', index_col=None, sep=',')
    test_data = pd.DataFrame.from_csv(path=localdir + 'feat_test.csv', index_col=None, sep=',')
    
    #to normalize the data (optional)
    print 'Starting norm...'      
    train_data = normalize(train_data)
    test_data = normalize(test_data)
                
    print 'Starting Asis...'  
    clf, metric = bestAlg(train_data, 'ACC')
    metric.tofile('alg_report_asis')
    print 'Starting test asis...'  
    dic_metric, conf_mat = test_learning(clf, test_data)
    dic_metric.tofile('dic_report_asis')
    conf_mat.tofile('conf_mat_asis')
    
    #feature selectionata = 
    #train_data, test_dsplit(norm_data, 0.)   
    print 'Starting feature selection...'  
    train_data, test_data, my_met, listoflistsofbest = bestfeatn(train_data, test_data)
    my_met.tofile('feat_sel_quickreport')
    listoflistsofbest.tofile('list_of_best_feat')
    feat_boxplot(norm_data[listoflistsofbest[5]])

    print 'Starting train and test f_selected...'    
    clf, metric = bestAlg(train_data, 'ACC')
    metric.tofile('alg_report_fsel')
    dic_metric, conf_mat = test_learning(clf, test_data)
    dic_metric.tofile('dic_report_fsel')
    conf_mat.tofile('conf_mat_fsel')
    print '...ending main'