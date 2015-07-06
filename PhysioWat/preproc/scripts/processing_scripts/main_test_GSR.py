
'''
at the moment, just for gsr (ap)
'''
from __future__ import division
import tools
import GSR
import numpy as np

# import matplotlib.pyplot as plt
import windowing as win

filename="./data/GSR_F01_F.txt"

T1=0.75
T2=2
MX=1
DELTA=0.02
nFS=16

gsr_data = tools.load_file(filename, header=8, sep=",") # 8 ","
#TODO GAUSSIANA

gsr_data= tools.downsampling(gsr_data, nFS)
# plt.figure(1)
# plt.plot(gsr_data[:,0], gsr_data[:,1])
# plt.xlabel("Time (s)")
# plt.ylabel("GSR (uS)")
# plt.title("Raw GSR")
# t_gsr, gsr = GSR.remove_spikes(gsr_data[:,1], nFS)
t_gsr = gsr_data[:,0]
gsr   = gsr_data[:,1]
print gsr.shape
# print t_gsr.shape, gsr.shape, gsr_data.shape
t_driver, driver, phasic_d, tonic_d= GSR.estimate_drivers(t_gsr, gsr, T1, T2, MX, DELTA)
outputlabels=["timestamp", "driver", "phasic", "tonic"]


tools.array_labels_to_csv(np.column_stack([t_driver, driver, phasic_d, tonic_d]), np.array(outputlabels), "./output/preproc_"+filename[7:-4]+".csv")

#-----FEATURES-----

windows=win.generate_dummy_windows(t_driver, 20, 10)
features = GSR.extract_features(phasic_d, t_driver, DELTA, windows)
tools.dict_to_csv(features, "./output/feat_"+filename[7:-4]+".csv")

# tools.prepare_json_to_plot_time(t_driver, [driver, phasic_d, tonic_d], ["Driver", "Phasic", "Tonic"])
# plt.figure(2)
# plt.plot(t_driver, np.c_[tonic_d, driver, phasic_d])
# plt.legend(["Tonic", "Driver", "Phasic"])
# plt.title("Processed GSR")
# plt.xlabel("Time (s)")
# plt.ylabel("GSR (uS)")
# plt.show()