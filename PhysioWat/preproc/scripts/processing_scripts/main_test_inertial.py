from __future__ import division
import inertial
import numpy as np
from PhysioWat.PhysioWat.preproc.scripts.processing_scripts import tools
import windowing as win
# import matplotlib.pyplot as plt

filename="./data/Accelerometer.csv"

# columns=["timeStamp","packetCounter","AccX","AccY","AccZ","GyrX","GyrY","GyrZ","MagX","MagY","MagZ"]
output_columns=["timeStamp","AccX","AccY","AccZ"]#,"GyrX","GyrY","GyrZ","MagX","MagY","MagZ"]
col_acc=["AccX", "AccY", "AccZ"]
# col_gyr=["GyrX", "GyrY", "GyrZ"]
# col_mag=["MagX", "MagY", "MagZ"]


empaticaAccCoeff=2*9.81/128
empaticafsamp=32

sensAccCoeff=8*9.81/32768
sensGyrCoeff=2000/32768
sensMagCoeff=0.007629
sensfsamp=100

data = tools.load_file(filename, sep=';', header=1)
# t=data[:,0]
# acc=data[:,2:5]
# gyr=data[:,5:8]
# mag=data[:,8:11]
t=data[:,0]
acc=data[:,1:]

acc= inertial.convert_units(acc, coeff=sensAccCoeff)
# gyr= inertial.convert_units(gyr, coeff=sensGyrCoeff)
# mag= inertial.convert_units(mag, coeff=sensMagCoeff)

tools.array_labels_to_csv(np.column_stack([t, acc]), np.array(output_columns), "./output/preproc_"+filename[7:-4]+".csv")

#-----EXTRACT FEATURES-----

# windows=win.generate_dummy_windows(t, 1000, 500)
# feats_acc, fcol_acc= inertial.extract_features_acc(acc, t, col_acc, windows, fsamp=sensfsamp)
# feats_gyr, fcol_gyr= inertial.extract_features_gyr(gyr, t, col_gyr, windows, fsamp=sensfsamp)
# feats_mag, fcol_mag= inertial.extract_features_mag(mag, t, col_mag, windows, fsamp=sensfsamp)
# feats=np.column_stack([feats_acc, feats_gyr, feats_mag])
# columns=np.r_[fcol_acc, fcol_gyr, fcol_mag]
# print feats.shape
# print columns.shape, columns
# tools.array_labels_to_csv(feats, columns, "./output/feat_ASD.csv")
# # feats.to_csv("./output/feat_6.csv")

