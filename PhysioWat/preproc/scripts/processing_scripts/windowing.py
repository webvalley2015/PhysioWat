'''
Functions for windowing
'''
import numpy as np

def get_windows_contiguos(time, labels, WINLEN, WINSTEP):
    '''
    Get windows dividing regardless the label. If a window contains more labels, it will not have a label
    :param labels: np.array of labels
    :param WINLEN: window length in time!
    :param WINSTEP: window step in time!
    :return: Windows as a list of [start, end], np.array of labels
    '''
    starts=np.arange(time[0], time[-1]-WINLEN, WINSTEP)
    ends=starts+WINLEN
    windows=[]
    labs=np.array([])
    for i in range(len(starts)):
        windows.append([starts[i], ends[i]])
        portion=labels[(time>=starts[i]) & (time<ends[i])]
        mean=portion.mean()
        if mean==int(mean):
            labs=np.r_[labs, mean]
        else:
            labs=np.r_[labs, np.nan]
    return windows, labs

def get_windows_no_mix(time, labels, WINLEN, WINSTEP):
    '''
    calculates the windows, restarting from beginning for every new label
    return: (windows, labels). windows is a list of [start, end], label is a list of int
    labels: array of labels (int)
    '''
    windows=[]
    labs=np.array([])
    parts, mini_labels = get_windows_full_label(time, labels)
    for start, end in parts:
        t_partial=time[(time>=start) & (time<end)]
        partial=labels[(time>=start) & (time<end)]
        starts=np.arange(t_partial[0], t_partial[-1]-WINLEN, WINSTEP)
        ends=starts+WINLEN
        for i in range(len(starts)):
            windows.append([starts[i], ends[i]])
            labs=np.r_[labs, partial[0]]
    return windows, labs


def get_windows_full_label(time, labels):
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
            wl.append([time[i],0])
            rl.append(labels[i])
    wl[-1][1]= time[-1]+1
    return wl, np.array(rl)

def generate_dummy_windows(time, WINLEN, WINSTEP):
    '''
    Dummy windows for debugging
    :param L: length
    :param WINLEN: window length
    :param WINSTEP: window step
    :return: list of couples [start, end]
    '''
    ws=[]
    for start in np.arange(time[0],time[-1]-WINLEN, WINSTEP):
        ws.append([start, start+WINLEN])
    return ws