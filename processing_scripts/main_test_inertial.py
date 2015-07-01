from __future__ import division
import inertial
import tools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filename="./data/claire_ASD.txt"
lables=["timestamp", "packetCounter","accX", "accY", "accZ", "gyrX", "gyrY", "gyrZ", "magX", "magY", "magZ"]
lables_acc=["accX", "accY", "accZ"]
lables_gyr=["gyrX", "gyrY", "gyrZ"]
lables_mag=["magX", "magY", "magZ"]


empaticaAccCoeff=2*9.81/128
empaticafsamp=32
sensAccCoeff=8*9.81/32768
sensGyrCoeff=2000/32768
sensMagCoeff=0.007629
sensfsamp=100

data=tools.load_file_pd(filename, sep=",", names=lables)

data=inertial.convert_units(data, lables_acc, coeff=sensAccCoeff)
data=inertial.convert_units(data, lables_gyr, coeff=sensGyrCoeff)
data=inertial.convert_units(data, lables_mag, coeff=sensMagCoeff)

plt.figure(1)
plt.plot(data.timestamp, data[lables_acc])
plt.legend(lables_acc)
plt.xlabel("Time (ms)")
plt.ylabel("Acceleration (m/s^2)")
plt.title("Accelerometer")
plt.figure(2)
plt.plot(data.timestamp, data[lables_gyr])
plt.legend(lables_gyr)
plt.xlabel("Time (ms)")
plt.ylabel("Angular Speed (degree/s)")
plt.title("Gyroscope")
plt.figure(3)
plt.plot(data.timestamp, data[lables_mag])
plt.legend(lables_mag)
plt.title("Magnetometer")
plt.ylabel("uT")
plt.xlabel("Time (ms)")
plt.show()

# data=inertial.convert_units(data, lables[1:], coeff=empaticaAccCoeff)
# print data

feats_acc=inertial.extract_features_acc(data, fsamp=sensfsamp, col_acc=lables_acc, WINLEN=1000, WINSTEP=500)
feats_gyr=inertial.extract_features_gyr(data, fsamp=sensfsamp, col_gyr=lables_gyr, WINLEN=1000, WINSTEP=500)
feats_mag=inertial.extract_features_mag(data, fsamp=sensfsamp, col_mag=lables_mag, WINLEN=1000, WINSTEP=500)
feats=pd.concat([feats_acc, feats_gyr, feats_mag], axis=1)

# feats.to_csv("./output/feat_"+filename[7:-4]+".csv")

