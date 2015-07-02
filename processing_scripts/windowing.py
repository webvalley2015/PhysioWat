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
    pass

def get_windows_full_label(labels, WINLEN, WINSTEP):
    pass