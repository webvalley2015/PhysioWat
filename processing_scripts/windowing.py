'''
Functions for windowing
'''
import numpy as np

def get_windows_contiguos(labels, WINLEN, WINSTEP):
    '''
    Get windows dividing regardless the label. If a window contains more labels, it will not have a label
    :param labels: np.array of labels
    :param WINLEN: window length
    :param WINSTEP: window step
    :return: Windows as a list of [start, end], np.array of labels
    '''
    starts=np.arange(0, len(labels)-WINLEN, WINSTEP)
    ends=starts+WINLEN
    windows=[]
    labs=np.array([])
    for i in range(len(starts)):
        windows.append([starts[i], ends[i]])
        portion=labels[starts[i]:ends[i]]
        mean=portion.mean()
        if mean==int(mean):
            labs=np.r_[labs, mean]
        else:
            labs=np.r_[labs, np.nan]
    return windows, labs

def get_windows_no_mix(labels, WINLEN, WINSTEP):
    '''
    calculates the windows avoiding unlabeled windows
    return: (windows, labels). windows is a list of [start, end], label is a list of int
    labels: array of labels (int)
    '''
    windows = []
    windows_labels = []
    length = len(labels)
    i = 0
    while i < length:
        set_win_labels = labels[i:i+WINLEN]
        if np.unique(set_win_labels).shape[0] == 1:
            win_label = set_win_labels[0]
            windows.append([i,i+WINLEN])
            windows_labels.append(win_label)
        i += WINSTEP
    return windows, np.array(windows_labels)

def get_windows_full_label(labels):
    '''
    returns the windows created by putting in the same windows all the near points with same label
    '''
    wl= [[0,0]]
    rl= [labels[0]]
    for i in range(1, len(labels)):
        if labels[i] != labels[i-1]:
    	    wl[-1][1]= i
            wl.append([i,0])
            rl.append(labels[i])
    wl[-1][1]= len(labels)
    return wl, np.array(rl)