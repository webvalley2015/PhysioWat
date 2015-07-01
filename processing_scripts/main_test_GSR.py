'''
at the moment, just for gsr (ap)
'''

import tools
import GSR
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

filename="./data/GSR.csv"

T1=0.75
T2=2
MX=1
DELTA=0.02

#tools.plotter(filename)

gsr_data = tools.load_file(filename)

t_driver, driver, phasic_d, tonic_d = GSR.estimate_drivers(gsr_data[:,0], gsr_data[:,1], T1, T2, MX, DELTA)

plt.figure()
plt.plot(t_driver, np.c_[driver, tonic_d])
plt.legend(["Driver", "Tonic"])
plt.show()