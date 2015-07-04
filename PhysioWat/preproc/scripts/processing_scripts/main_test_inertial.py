from __future__ import division
import inertial
import numpy as np
from PhysioWat.PhysioWat.preproc.scripts.processing_scripts import tools
import windowing as win
# import matplotlib.pyplot as plt

filename="./data/claire_ASD.txt"
columns=["timeStamp","packetCounter","AccX","AccY","AccZ","GyrX","GyrY","GyrZ","MagX","MagY","MagZ"]
col_acc=["AccX", "AccY", "AccZ"]
col_gyr=["GyrX", "GyrY", "GyrZ"]
col_mag=["MagX", "MagY", "MagZ"]


empaticaAccCoeff=2*9.81/128
empaticafsamp=32

sensAccCoeff=8*9.81/32768
sensGyrCoeff=2000/32768
sensMagCoeff=0.007629
sensfsamp=100

#data= tools.load_file_pd(filename, sep=",", names=lables)
data = tools.load_file("./data/claire_ASD.txt", sep=',')
t=data[:,0]
acc=data[:,2:5]
gyr=data[:,5:8]
mag=data[:,8:11]

acc= inertial.convert_units(acc, coeff=sensAccCoeff)
gyr= inertial.convert_units(gyr, coeff=sensGyrCoeff)
mag= inertial.convert_units(mag, coeff=sensMagCoeff)

# plt.figure(1)
# plt.plot(data.timeStamp, data[lables_acc])
# plt.legend(lables_acc)
# plt.xlabel("Time (ms)")
# plt.ylabel("Acceleration (m/s^2)")
# plt.title("Accelerometer")
# plt.figure(2)
# plt.plot(data.timeStamp, data[lables_gyr])
# plt.legend(lables_gyr)
# plt.xlabel("Time (ms)")
# plt.ylabel("Angular Speed (degree/s)")
# plt.title("Gyroscope")
# plt.figure(3)
# plt.plot(data.timeStamp, data[lables_mag])
# plt.legend(lables_mag)
# plt.title("Magnetometer")
# plt.ylabel("uT")
# plt.xlabel("Time (ms)")
# plt.show()

# data=inertial.convert_units(data, lables[1:], coeff=empaticaAccCoeff)
# print data
windows=win.generate_dummy_windows(t, 1000, 500)
feats_acc, fcol_acc= inertial.extract_features_acc(acc, t, col_acc, windows, fsamp=sensfsamp)
feats_gyr, fcol_gyr= inertial.extract_features_gyr(gyr, t, col_gyr, windows, fsamp=sensfsamp)
feats_mag, fcol_mag= inertial.extract_features_mag(mag, t, col_mag, windows, fsamp=sensfsamp)
feats=np.column_stack([feats_acc, feats_gyr, feats_mag])
columns=np.r_[fcol_acc, fcol_gyr, fcol_mag]
print feats.shape
print columns.shape, columns
tools.array_labels_to_csv(feats, columns, "./output/feat_ASD.csv")
# feats.to_csv("./output/feat_6.csv")

