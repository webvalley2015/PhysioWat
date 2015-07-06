from __future__ import division
import sys
import numpy as np
filenames=sys.argv
fs=100
filenames=filenames[1:]

head=0

columns_in=["timeStamp","packetCounter", "AccX","AccY","AccZ", "GyrX","GyrY","GyrZ", "MagX","MagY","MagZ"]
columns_out=["TIME", "ACCX","ACCY","ACCZ", "GYRX","GYRY","GYRZ", "MAGX","MAGY","MAGZ", "LAB"]

data_out=np.empty((1,11))
for i, fname in enumerate(filenames):
    data_in=np.genfromtxt(fname, skip_header=head, delimiter=",")
    label_col=np.ones((data_in.shape[0]))*i
    new_rows=np.column_stack([data_in[:,0], data_in[:,2:11], label_col])
    data_out=np.concatenate((data_out, new_rows), axis=0)

data_out=np.delete(data_out, 0, 0)

for i in range(data_out.shape[0]):
    data_out[i,0]=i/fs

np.savetxt(raw_input("Filename: ./output/"), data_out, delimiter=",", header=",".join(columns_out), comments="")