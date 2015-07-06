from __future__ import division
import numpy as np
import os

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

def get_first_col(data):
    result=np.empty(len(data))
    for i, tup in enumerate(data):
        result[i]=tup[0]
    return result

subj=raw_input("Subject: ")
snd="./SUB"+subj+"/"
meta="./SUB"+subj+"/SUB"+subj+"/Meta.csv"
folder_data="./SUB"+subj+"/SUB"+subj+"/Empatica E4/"
for root, dirs, files in os.walk('./SUB'+subj):
    for dir in dirs:
        if dir[-len(subj)-4:-4]==subj :
            snd+=dir+"/snd.csv"
data_snd=np.genfromtxt(snd, skip_header=1, delimiter="\t", dtype=None)

try:
    data_meta=np.genfromtxt(meta, skip_header=1, delimiter=";", dtype=None)
    offset=data_meta[data_meta[:,0]=="time_offset_average",1]
    offset=float(offset[0])
except ValueError as e:
    offset=float(raw_input("Error encountered, manually insert time_offset_average (from Meta.csv): "))

data_snd=get_first_col(data_snd)
data_snd=data_snd-offset
fs_gsr=4
fs_bvp=64
fs_st=4
fs_acc=32

head=1
files_in=["BVP.csv","Accelerometer.csv", "GSR.csv","Temperature.csv"]
freq_samples=[fs_bvp, fs_acc, fs_gsr, fs_st]
columns_out=["TIME","BVP", "ACCX","ACCY","ACCZ", "GSR", "ST", "LAB"]

try:
    data_out=np.genfromtxt(folder_data+files_in[0], skip_header=head, delimiter=";")
except IOError as e:
    folder_data=raw_input("Error encountered, manually insert the folder of the data: ")
    if folder_data[-1]!="/":
        folder_data+="/"
    data_out=np.genfromtxt(folder_data+files_in[0], skip_header=head, delimiter=";")

t_orig=data_out[:,0]
data_out=data_out[:,1:]
time_col=np.empty(data_out.shape[0])

for i in range(data_out.shape[0]):
    time_col[i]=i/fs_bvp

data_out=np.column_stack((time_col, data_out))

for i in range(1,len(files_in)):
    fname=files_in[i]
    print fname
    data_in=np.genfromtxt(folder_data+fname, skip_header=head, delimiter=";")
    new_cols=interpolate(data_in[:,1:], freq_samples[i], fs_bvp, data_out.shape[0])
    print i, new_cols.shape, data_out.shape
    if (new_cols.shape[0]<data_out.shape[0]):
        data_out=data_out[:new_cols.shape[0],:]
        t_orig=t_orig[:new_cols.shape[0]]
    data_out=np.column_stack((data_out, new_cols))

label_col = np.zeros((data_out.shape[0]))
for start in data_snd:
    end=start+6
    mask=(t_orig>=start)&(t_orig<end)
    label_col[mask]+=1

data_out = np.column_stack((data_out, label_col))

np.savetxt("SUB"+subj+".csv", data_out, delimiter=",", header=",".join(columns_out), comments="")