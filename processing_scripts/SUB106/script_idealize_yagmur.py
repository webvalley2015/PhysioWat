from __future__ import division
import numpy as np

def interpolate(data, fs_old, fs_new, length):
    rate=fs_new/fs_old
    print "Rate = %d" % (rate)
    data_out=np.empty(data.shape[1])
    for i in range(data.shape[0]):
        item=data[i,:]
        if data_out.shape[0]-1+rate>length:
            act_rate=length-data_out.shape[0]+1
        else :
            act_rate=rate

        new_cols=np.ones((act_rate, item.shape[0])) * item
        data_out=np.vstack([data_out, new_cols])
    data_out=data_out[1:,:]
    return data_out

fs_gsr=4
fs_bvp=64
fs_st=4
fs_acc=32

head=1
folder=""
files_in=["BVP.csv","Accelerometer.csv", "GSR.csv","Temperature.csv"]
freq_samples=[fs_bvp, fs_acc, fs_gsr, fs_st]
columns_out=["TIME","BVP", "ACCX","ACCY","ACCZ", "GSR", "ST", "LAB"]

data_out=np.genfromtxt(folder+files_in[0], skip_header=head, delimiter=";")[:,1]
time_col=np.empty(data_out.shape[0])

for i in range(data_out.shape[0]):
    time_col[i]=i/fs_bvp

data_out=np.column_stack((time_col, data_out))

for i in range(1,len(files_in)):
    fname=files_in[i]
    print fname
    data_in=np.genfromtxt(folder+fname, skip_header=head, delimiter=";")
    new_cols=interpolate(data_in[:,1:], freq_samples[i], fs_bvp, data_out.shape[0])
    print i, new_cols.shape, data_out.shape
    if (new_cols.shape[0]<data_out.shape[0]):
        data_out=data_out[:new_cols.shape[0],:]
    data_out=np.column_stack((data_out, new_cols))

label_col = np.zeros((data_out.shape[0]))
data_out = np.column_stack((data_out, label_col))

np.savetxt(raw_input("Filename: "), data_out, delimiter=",", header=",".join(columns_out), comments="")