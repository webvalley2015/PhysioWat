# implementation for single txt file containing Exel sensor data

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
 
filenames = ['claire1.txt'] # first trial from Claire's wrist

# init arrays for data storage
data_all = []
data_mean = []          
data_var = []
data_combined = np.zeroes(9)
data_mean_combined = np.zeroes(9)
data_var_combined = np.zeroes(9)

WINDOW_SIZE = 50
STEP = 25

# N = len(filenames)

data_all.append(np.loadtxt(filenames(i))
data_combined = np.vstack((data_combined, data_all[i]))
[row, col] = data_all[i].shape
_mean = np.zeros(( len(range(0, row, STEP)) , col ))
_var = np.zeros(( len(range(0, row, STEP)) , col ))

for i_col in range(col):
	idx = 0
	for i_row in range(0, row, STEP):
	# compute mean of window elements
	_mean[idx,i_col] = np.mean(data_all[i][i_row:i_row+WINDOW_SIZE-1,i_col])
        _var[idx,i_col] = np.var(data_all[i][i_row:i_row+WINDOW_SIZE-1,i_col])
        idx += 1
data_mean.append(_mean)
data_mean_combined = np.vstack((data_mean_combined, data_mean[i]))

data_var.append(_var)
data_var_combined = np.vstack((data_var_combined, data_var[i]))

np.save('data_mean', data_mean)
np.save('data_var', data_var)

