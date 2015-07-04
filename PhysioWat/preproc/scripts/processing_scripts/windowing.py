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
    calculates the windows, restarting from beginning for every new label
    return: (windows, labels). windows is a list of [start, end], label is a list of int
    labels: array of labels (int)
    '''
    windows=[]
    labs=np.array([])
    parts, mini_labels = get_windows_full_label(labels)
    for start, end in parts:
        partial=labels[start:end]
        starts=np.arange(0, len(partial)-WINLEN, WINSTEP)
        ends=starts+WINLEN
        for i in range(len(starts)):
            windows.append([start+starts[i], start+ends[i]])
            labs=np.r_[labs, partial[0]]
    return windows, labs


def get_windows_full_label(labels):
    '''
    Window = Label length
    :param labels: np.array of labels
    :return: windows as list of [start, end]
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

def generate_dummy_windows(L, WINLEN, WINSTEP):
    '''
    Dummy windows for debugging
    :param L: length
    :param WINLEN: window length
    :param WINSTEP: window step
    :return: list of couples [start, end]
    '''
    ws=[]
    for start in range(0,L-WINLEN, WINSTEP):
        ws.append([start, start+WINLEN])
    return ws