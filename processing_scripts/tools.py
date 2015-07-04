from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd
from pandas import DataFrame

def peakdet(v, delta, x = None, startMax = True):
    '''
    Functions for detecting peaks in EKG/GSR
    v: function in which search the peaks
    delta: minimum peak height
    x: (default None) the "timeline"
    startMax: (default True)
    '''

    maxtab = []
    mintab = []

    if x is None:
        x = np.arange(len(v))

    v = np.asarray(v)

    mn, mx = np.Inf, -np.Inf
    mnpos, mxpos = np.NaN, np.NaN

    lookformax = startMax

    for i in np.arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return np.array(maxtab), np.array(mintab)

def gen_bateman(mx, T1, T2, fsamp=4, gsr = None):
    """
    BATEMAN, T_BATEMAN [, GSR_WITH_BAT] = BATEMAN, T_BATEMAN = gen_bateman(max, T1, T2, fsamp=4 [, gsr = None])
    Generates the bateman function:
    bateman = A * (exp(-t/T1) - exp(-t/T2))

    If gsr is given it return also the gsr tailored with the bateman function to be deconvolved.
    """
    # TODO: fix bateman (start) and duration

    t_bat=np.arange(1.000/fsamp, 100, 1.000/fsamp)
    g=-1
    bateman=g*(np.exp(-t_bat/T1)-np.exp(-t_bat/T2))
#    d_bateman=g*(-1/(T1)*np.exp(-t_bat/T1)-(-1/T2)*np.exp(-t_bat/T2))
    bateman=mx*bateman/np.max(bateman)
    bateman=bateman[t_bat<20]
#    bateman[0]=np.nan
    bateman=bateman[1:]

    t_bat = t_bat[t_bat<20]
    t_bat = t_bat[1:]

    if  gsr is not None:
        bateman_first_half=bateman[0:np.argmax(bateman)]*gsr[0]/bateman[np.argmax(bateman)]
        bateman_second_half=bateman[np.argmax(bateman):]*gsr[-1]/bateman[np.argmax(bateman)]
        gsr_in=np.r_[bateman_first_half, gsr, bateman_second_half]
        return bateman, t_bat, gsr_in
    else:
        return bateman, t_bat

#Deprecated
def plotter(filename):
    '''
    :param filename: file to plot
    :return: nothing, just plot
    '''
    data = load_file(filename)
    plt.figure()
    plt.plot(data[:,0], data[:,1])
    plt.xlabel("Time")
    plt.ylabel("GSR (nS)")
    plt.show()

def load_file(filename, header=1, sep=";"):
    '''
    Load data from file
    :param filename: name of the file where data is stored
    :return: data as np.array
    '''
    data = np.genfromtxt(filename, delimiter=sep, skip_header=header)
    data[:,0]-=data[0,0]
    return data

def max2interval(timesMax, minrate=40, maxrate=200):
    """
    intervals, time_intervals = max2interval(timesMax, minrate=40,maxrate=270):
    
    Returns intervals from max_times, after filtering possible artefacts based on rate range (rates in min^(-1))
    if two peaks are nearer than minrate or further than maxrate, the algorithm try to recognize if there's a false true or a peak missing
    minrate and maxrate are in min^(-1), and represents the minimum and the maximum bpm to detect
    """
    maxRR=60/minrate
    minRR=60/maxrate

    RR=[]
    timeRR=[]

    # algoritmo alternativo
    # beat artifacts correction
    ##inizializzazioni

    tprev=timesMax[0]
    tfalse=tprev

    for i in range(1, len(timesMax)):
        tact=timesMax[i]

        RRcurr=tact-tprev
        if (RRcurr<minRR): # troppo breve: falso picco?
            tfalse=tact  #aspetto (non aggiorno tact) e salvo il falso campione

        elif RRcurr>maxRR: # troppo lungo ho perso un picco?
            RRcurr=tact-tfalse # provo con l'ultimo falso picco se esiste
            tprev=tact # dopo ripartiro' da questo picco

        if RRcurr>minRR and RRcurr<maxRR: # tutto OK
            RR.append(RRcurr) #aggiungo valore RR
            timeRR.append(tact) #aggiungo istante temporale
            tfalse=tact #aggiorno falso picco
            tprev=tact #aggiorno tprev
    return np.array(RR),  np.array(timeRR)


def prepare_json_to_plot(series, labels):
    '''
    Saves a json file in order to pass it to the layout team
    :param series: list of series
    :param labels: list of labels
    :return: nothing
    '''
    if len(series)==len(labels):
        li=[]
        for i in range(len(series)):
            li.append({ "name" : labels[i],
                    "data" : series[i].tolist()
                    })
        json_string=json.dumps({"series":li})
        file=open("graph.json", "w")
        file.write(json_string)
        file.close()

def load_file_pd(filename, sep=";", names=None):
    '''
    Load data from file
    :param filename: name of the file where data is stored
    :return: data as pandas.DataFrame
    '''
    data = pd.read_csv(filename, sep=sep, names=names)
    return data

def downsampling(data, FSAMP, FS_NEW, switch=True):
    '''
    Downsamples the signals (too much data is long to extract!)
    :param data: The data to downsample
    :param FSAMP: The strating frequency
    :param FS_NEW: The new frequency
    :param off: Do not downsample
    :return: The downsampled data
    '''
    if FSAMP <= FS_NEW or FSAMP%FS_NEW!=0 or not switch:
        return data
    N_SAMP = FSAMP/FS_NEW

    indexes = np.arange(len(data))
    keep = (indexes%N_SAMP == 0)

    result = np.array(data[keep,:])
    return result

def getIBI (signal, SAMP_F, peakDelta, minFr = 40, maxFr = 200):
    '''
    this function calculates the IBI on a BVP or EKG filtered graph, considering only peaks higher than peakDelta
    return: a pd DataFrame containing the inter-beat interval (in s) indexed with time
    signal: the filtered BVP or EKG signal
    SAMP_F: the sampling frequency of the data
    peakDelta: the minimum height of a peak to be recognised
    minFr: (default 40) the minimum frequence (in min^(-1), or bpm) to recognize (two nearer peaks are signed as false positive)
    maxFr: (default 200) the maximum frequence (in min^(-1), or bpm) to recognize (two further peaks makes the algorithm looks for peaks between those two)
    '''
    # estimating peaks and IBI
    t = np.arange(0, len(signal)/float(SAMP_F), 1.0/SAMP_F)
    maxp, minp = peakdet(signal, peakDelta, t)
    IBI, tIBI = max2interval(maxp[:,0], minFr, maxFr)
    
    #ibi contains the Inter-Beat interval between two beats, indexed with the time of the beats
    ibi = DataFrame(IBI, index = tIBI, columns=['IBI'])
    return ibi