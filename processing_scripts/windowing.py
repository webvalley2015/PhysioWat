'''
Functions for windowing
'''
import numpy as np
import pandas as pd

def get_windows_contiguos(labels, WINLEN, WINSTEP):
    pass

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
    return (windows, windows_labels)

def get_windows_full_label(labels, WINLEN, WINSTEP):
    pass