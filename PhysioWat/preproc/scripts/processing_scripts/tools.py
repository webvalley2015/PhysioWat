from __future__ import division
import numpy as np
import json
from PhysioWat.models import Recording, SensorRawData
from StringIO import StringIO
from PhysioWat.models import Preprocessed_Recording, Preprocessed_Data
import csv


def peakdet(v, delta, x=None, startMax=True):
    '''
    Functions for detecting peaks
    return: two nparrays (N,2), containing the time (in s) in the first column and the height of the peak in the second column
    v: np.array (N,) containing the signal in which search the peaks
    delta: minimum peak height
    x: (default None) the timestamp
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
            if this < mx - delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn + delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return np.array(maxtab), np.array(mintab)


def gen_bateman(mx, T1, T2, fsamp=4, gsr=None):
    """
    BATEMAN, T_BATEMAN [, GSR_WITH_BAT] = BATEMAN, T_BATEMAN = gen_bateman(max, T1, T2, fsamp=4 [, gsr = None])
    Generates the bateman function:
    bateman = A * (exp(-t/T1) - exp(-t/T2))

    If gsr is given it return also the gsr tailored with the bateman function to be deconvolved.
    """
    # TODO: fix bateman (start) and duration

    t_bat = np.arange(1.000 / fsamp, 100, 1.000 / fsamp)
    g = -1
    bateman = g * (np.exp(-t_bat / T1) - np.exp(-t_bat / T2))
    #    d_bateman=g*(-1/(T1)*np.exp(-t_bat/T1)-(-1/T2)*np.exp(-t_bat/T2))
    bateman = mx * bateman / np.max(bateman)
    bateman = bateman[t_bat < 20]
    #    bateman[0]=np.nan
    bateman = bateman[1:]

    t_bat = t_bat[t_bat < 20]
    t_bat = t_bat[1:]

    if gsr is not None:
        bateman_first_half = bateman[0:np.argmax(bateman)] * gsr[0] / bateman[np.argmax(bateman)]
        bateman_second_half = bateman[np.argmax(bateman):] * gsr[-1] / bateman[np.argmax(bateman)]
        gsr_in = np.r_[bateman_first_half, gsr, bateman_second_half]
        return bateman, t_bat, gsr_in
    else:
        return bateman, t_bat


# Deprecated
def plotter(filename):
    '''
    :param filename: file to plot
    :return: nothing, just plot
    '''
    data = load_file(filename)
    plt.figure()
    plt.plot(data[:, 0], data[:, 1])
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
    return data


def load_raw_db(recordingID):
    # raw query for i csv line
    table = Recording.objects.get(id=recordingID)
    data = SensorRawData.objects.filter(recording_id=recordingID).order_by('id')
    alldata = (','.join(table.dict_keys) + '\n').replace(' ', '')
    for record in data:
        ll = []
        for key in table.dict_keys:
            ll.append(record.store[key])
        alldata += ','.join(ll) + '\n'
    datacsv = np.genfromtxt(StringIO(alldata), delimiter=',')
    return datacsv
    # results = cursor.fetchall()

def load_preproc_db(recordingID):
    # raw query for i csv line
    table = Preprocessed_Recording.objects.get(id=recordingID)
    data = Preprocessed_Data.objects.filter(recording_id=recordingID).order_by('id')
    alldata = (','.join(table.dict_keys) + '\n').replace(' ', '')
    for record in data:
        ll = []
        for key in table.dict_keys:
            ll.append(record.store[key])
        alldata += ','.join(ll) + '\n'
    datacsv = np.genfromtxt(StringIO(alldata), delimiter=',')
    return datacsv
    # results = cursor.fetchall()



def prepare_json_to_plot(series, labels):
    '''
    Saves a json file in order to pass it to the layout team
    :param series: list of series
    :param labels: list of labels
    :return: nothing
    '''
    if len(series) == len(labels):
        li = []
        for i in range(len(series)):
            li.append({"name": labels[i],
                       "data": series[i].tolist()
                       })
        json_string = json.dumps({"series": li})
        file = open("graph.json", "w")
        file.write(json_string)
        file.close()


# def load_file_pd(filename, sep=";", names=None):
#     '''
#     Load data from file
#     :param filename: name of the file where data is stored
#     :return: data as pandas.DataFrame
#     '''
#     data = pd.read_csv(filename, sep=sep, names=names)
#     return data
#
# def load_file_pd_db(recordingID):
#     # raw query for i csv line
#     table = Recording.objects.get(id=recordingID)
#     data = SensorRawData.objects.filter(recording_id_id=recordingID)
#     alldata = (','.join(table.dict_keys)+'\n').replace(' ','')
#     for record in data:
#         ll=[]
#         for key in table.dict_keys:
#             ll.append(record.store[key])
#         alldata+=','.join(ll)+'\n'
#     datacsv = pd.read_csv(StringIO(alldata), sep=',')
#     return datacsv
#     # results = cursor.fetchall()


def downsampling(data, FS_NEW, switch=True, t_col=0):
    '''
    Downsamples the signals (too much data is long to extract!)
    :param data: The data to downsample
    :param FSAMP: The strating frequency
    :param FS_NEW: The new frequency
    :param off: Do not downsample
    :return: The downsampled data
    '''
    FSAMP=int(round(1/(data[1,t_col]-data[0,t_col])))

    if not switch:
        return data

    if FSAMP <= FS_NEW or FSAMP % FS_NEW != 0:
        raise ValueError("FS_NEW should be lower than FSAMP and one of its divisors #illy")
    N_SAMP = FSAMP / FS_NEW

    indexes = np.arange(len(data))
    keep = (indexes % N_SAMP == 0)

    result = np.array(data[keep, :])
    return result


def normalize(data):
    '''
    normalize (mean = 0, std = 1) an array (N,) passed
    return: the array normalized
    data: he array to normalize
    '''
    new_data = (data - np.mean(data)) / np.std(data)
    return new_data


def dict_to_csv(d, filename):
    feats = []
    for key, value in d.items():
        feats.append(value)
        print key
    print d.keys()
    np.savetxt(filename, np.column_stack(feats), delimiter=",", header=",".join(d.keys()))


def array_labels_to_csv(array, labels, filename):
    np.savetxt(filename, array, delimiter=",", header=",".join(labels.tolist()), comments="")

#Puts data int the preprocessed array into the database
def putPreprocArrayintodb(rec_id, preProcArray, preProcLabel):

    #Andrew's crazy method to convert array to CSV-ish string??? IDK what it means, but IT WORKS!!!
    csvasstring = ",".join(preProcLabel.tolist()) + '\n'
    for dataarr in preProcArray:
        for dataval in dataarr:
            csvasstring += str(dataval)+','
        csvasstring = csvasstring[:-1]
        csvasstring += '\n'

    #Initiate the CSV Reader
    csvreader = csv.reader(StringIO(csvasstring), delimiter=',')
    dictky = csvreader.next()

    #Submit data to model and thus the database table
    pr = Preprocessed_Recording(recording_id=rec_id, dict_keys=dictky)
    pr.save()

    for row in csvreader:
        Preprocessed_Data(pp_recording=pr.id, store=dict(zip(dictky, row))).save()

    print csvreader

    return 0

def get_row_for_col(mat, indexes):
    '''
    extract the rows of mat that has an element of indexes in their first position
    return: np.array that contains the rows of mat required
    mat: np.array (N,M)
    indexes: np.array (A,)
    '''
    result = []
    for row in mat:
        if row[0] in indexes:
            result.append(row)
    return np.array(result)

def selectCol(vect, head, cols):
    '''
    Select the cols columns from vector, given its header
    :param vect: the array to slice
    :param head: the header of the array (either as np.ndarray or list)
    :param cols: the columns to select (either as np.ndarray, list or str)
    :return: the slice of the array
    '''
    if type(head) is list:
        head=np.array(head)
    elif type(head) is not np.ndarray:
        raise ValueError("head is neither a np.ndarray or a list")

    if type(cols) is str:
        cols=[cols]
    elif type(cols) is not list and type(cols) is not np.ndarray:
        raise ValueError("\"Che cazzo ti sei fumato?\" cols must be a str, list or np.ndarray #droga #ilfumouccide #illy")
    mask=np.zeros(len(head), dtype=bool)

    for col in cols:
        mask = (mask) | (head==col)
    result=vect[:, mask]
    if result.shape[1]==1 :
        result=result.flatten()
    return result
