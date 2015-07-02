'''
at the moment, just for gsr (ap)
'''

import tools
import GSR
import matplotlib.pyplot as plt
import numpy as np

filename="./data/GSR.csv"

T1=0.75
T2=2
MX=1
DELTA=0.02
FS=4
nFS=16

gsr_data = tools.load_file(filename, header=1, sep=";") # 8 ","
# gsr_data=tools.downsampling(gsr_data, FS, nFS)
plt.figure(1)
plt.plot(gsr_data[:,0], gsr_data[:,1])
plt.xlabel("Time (s)")
plt.ylabel("GSR (uS)")
plt.title("Raw GSR")
# t_gsr, gsr = GSR.remove_spikes(gsr_data[:,1], nFS)
t_gsr = gsr_data[:,0]
gsr   = gsr_data[:,1]
# print t_gsr.shape, gsr.shape, gsr_data.shape
t_driver, driver, phasic_d, tonic_d= GSR.estimate_drivers(t_gsr, gsr, T1, T2, MX, DELTA, FS=FS)


pha_processed = GSR.processPSR(phasic_d, t_driver, DELTA)
features = GSR.extract_features(pha_processed)
features.to_csv("./output/feat_"+filename[7:-4]+".csv")

plt.figure(2)
plt.plot(t_driver, np.c_[tonic_d, driver, phasic_d])
plt.legend(["Tonic", "Driver", "Phasic"])
plt.title("Processed GSR")
plt.xlabel("Time (s)")
plt.ylabel("GSR (uS)")
plt.show()