from __future__ import division
import inertial
import numpy as np
import tools
import windowing as win

filename="./data/test.csv"

columns_in=["TIME", "ACCX","ACCY","ACCZ", "GYRX","GYRY","GYRZ", "MAGX","MAGY","MAGZ", "LAB"]
col_acc=["ACCX", "ACCY", "ACCZ"]
col_gyr=["GYRX", "GYRY", "GYRZ"]
col_mag=["MAGX", "MAGY", "MAGZ"]


empaticaAccCoeff=2*9.81/128
empaticafsamp=32

sensAccCoeff=8*9.81/32768
sensGyrCoeff=2000/32768
sensMagCoeff=0.007629
sensfsamp=100

data = tools.load_file(filename, sep=',', header=1)

data=tools.downsampling(data, 50)

t=tools.selectCol(data, columns_in, "TIME")
acc=tools.selectCol(data, columns_in, col_acc)
gyr=tools.selectCol(data, columns_in, col_gyr)
mag=tools.selectCol(data, columns_in, col_mag)
lab=tools.selectCol(data, columns_in, "LAB")

acc= inertial.convert_units(acc, coeff=sensAccCoeff)
gyr= inertial.convert_units(gyr, coeff=sensGyrCoeff)
mag= inertial.convert_units(mag, coeff=sensMagCoeff)

# tools.array_labels_to_csv(np.column_stack([t, acc]), np.array(columns_in), "./output/preproc_"+filename[7:-4]+".csv")

#-----EXTRACT FEATURES-----

windows, winlab=win.get_windows_no_mix(t,lab , 1, 0.5)
feats_acc, fcol_acc= inertial.extract_features_acc(acc, t, col_acc, windows)
feats_gyr, fcol_gyr= inertial.extract_features_gyr(gyr, t, col_gyr, windows)
feats_mag, fcol_mag= inertial.extract_features_mag(mag, t, col_mag, windows)
feats=np.column_stack([feats_acc, feats_gyr, feats_mag, winlab])
columns_out=np.r_[fcol_acc, fcol_gyr, fcol_mag, np.array(["LAB"])]
# print feats.shape
# print columns.shape, columns
tools.array_labels_to_csv(feats, columns_out, "./output2/feat_"+filename[7:-4]+".csv")
# # feats.to_csv("./output/feat_6.csv")

