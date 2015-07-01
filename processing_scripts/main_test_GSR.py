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

gsr_data = tools.load_file(filename)

t_driver, driver, phasic_d, tonic_d = GSR.estimate_drivers(gsr_data[:,0], gsr_data[:,1], T1, T2, MX, DELTA)

#plt.figure()
#plt.plot(gsr_data[:,0], gsr_data[:,1])
#plt.show()

plt.figure()
plt.plot(t_driver, np.c_[driver, tonic_d, phasic_d])
plt.legend(["Driver", "Tonic", "Phasic"])
plt.show()

pha_processed = GSR.processPSR(phasic_d, t_driver, DELTA)
features = GSR.PSRindexes(pha_processed)
