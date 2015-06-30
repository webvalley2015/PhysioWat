import numpy as np
import matplotlib.pyplot as plt

def peakdet(v, delta, x = None, startMax = True):
    '''
    Functions for detecting peaks in EKG/GSR
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

def load_file(filename):
    '''
    Load data from file
    :param filename: name of the file where data is stored
    :return: data as np.array
    '''
    data = np.genfromtxt(filename, delimiter=";", skip_header=1)
    data[:,0]-=data[0,0]
    return data