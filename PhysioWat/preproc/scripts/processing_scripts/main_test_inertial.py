from __future__ import division

import pandas as pd

import inertial
import tools
import windowing as win
import pyparsing
import matplotlib.pyplot as plt

filename="./data/claire_ASD.txt"
lables=["usernum","timeStamp","packetCounter","AccX","AccY","AccZ","GyrX","GyrY","GyrZ","MagX","MagY","MagZ"]
lables_acc=["AccX", "AccY", "AccZ"]
lables_gyr=["GyrX", "GyrY", "GyrZ"]
lables_mag=["MagX", "MagY", "MagZ"]


empaticaAccCoeff=2*9.81/128
empaticafsamp=32

sensAccCoeff=8*9.81/32768
sensGyrCoeff=2000/32768
sensMagCoeff=0.007629
sensfsamp=100

#data= tools.load_file_pd(filename, sep=",", names=lables)
data = tools.load_file_pd_db(6)
data= inertial.convert_units(data, lables_acc, coeff=sensAccCoeff)
data= inertial.convert_units(data, lables_gyr, coeff=sensGyrCoeff)
data= inertial.convert_units(data, lables_mag, coeff=sensMagCoeff)

plt.figure(1)
plt.plot(data.timeStamp, data[lables_acc])
plt.legend(lables_acc)
plt.xlabel("Time (ms)")
plt.ylabel("Acceleration (m/s^2)")
plt.title("Accelerometer")
plt.figure(2)
plt.plot(data.timeStamp, data[lables_gyr])
plt.legend(lables_gyr)
plt.xlabel("Time (ms)")
plt.ylabel("Angular Speed (degree/s)")
plt.title("Gyroscope")
plt.figure(3)
plt.plot(data.timeStamp, data[lables_mag])
plt.legend(lables_mag)
plt.title("Magnetometer")
plt.ylabel("uT")
plt.xlabel("Time (ms)")
plt.show()

# data=inertial.convert_units(data, lables[1:], coeff=empaticaAccCoeff)
# print data
windows=win.generate_dummy_windows(len(data), 100, 50)
feats_acc= inertial.extract_features_acc(data, windows, fsamp=sensfsamp, col_acc=lables_acc)
feats_gyr= inertial.extract_features_gyr(data, windows, fsamp=sensfsamp, col_gyr=lables_gyr)
feats_mag= inertial.extract_features_mag(data, windows, fsamp=sensfsamp, col_mag=lables_mag)
feats=pd.concat([feats_acc, feats_gyr, feats_mag], axis=1)
print feats.shape
feats.to_csv("./output/feat_6.csv")

