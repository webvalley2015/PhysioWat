'''
at the moment, just for gsr (ap)
'''

import tools
import GSR
import matplotlib.pyplot as plt
import numpy as np

filename="./data/GSR_F01_M.txt"

T1=0.75
T2=2
MX=1
DELTA=0.02
FS=2048
nFS=16

gsr_data = tools.load_file(filename, header=8, sep=",")
gsr_data=tools.downsampling(gsr_data, FS, nFS)
plt.figure(1)
plt.plot(gsr_data[:,0], gsr_data[:,1])
plt.xlabel("Time (s)")
plt.ylabel("GSR (uS)")
plt.title("Raw GSR")
plt.show()

t_driver, driver, phasic_d, tonic_d = GSR.estimate_drivers(gsr_data[:,0], gsr_data[:,1], T1, T2, MX, DELTA)


pha_processed = GSR.processPSR(phasic_d, t_driver, DELTA)
features = GSR.extract_features(pha_processed)
features.to_csv("./output/feat_"+filename[7:-4]+".csv")

plt.figure(2)
plt.plot(t_driver, np.c_[driver, tonic_d, phasic_d])
plt.legend(["Driver", "Tonic", "Phasic"])
plt.title("Processed GSR")
plt.xlabel("Time (s)")
plt.ylabel("GSR (uS)")
plt.show()