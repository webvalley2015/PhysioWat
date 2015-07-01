# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 17:56:22 2015

@author: flavio
"""
'''
function for BVP only
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import filters as ourFilters

if __name__ == '__main__':
    path = '/home/flavio/Work/PhysioWat/robaNoGit/data/SUB100/SUB100/Empatica_E4/'
    fileName = 'BVP.csv'
    SAMPLING_FREQ = 64

    data = pd.DataFrame.from_csv(path+fileName, sep=';')
    plt.plot(data.index, data.BVP)
    datanp= data.as_matrix().reshape(data.shape[0])

    filtered_signal = ourFilters.filterSignal(datanp, SAMPLING_FREQ)

    plt.plot(data.index, filtered_signal)
    plt.show()
