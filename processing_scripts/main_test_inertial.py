import inertial
import tools
import numpy as np
import pandas as pd

filename="./data/Accelerometer.csv"
lables=["timestamp", "accX", "accY", "accZ"]

data=tools.load_file_pd(filename)
data=inertial.convert_units(data, lables[1:], coeff=2*9.81/128)
print data
feats=inertial.extract_features_acc(data, fsamp=32, col_acc=lables[1:])
print len(feats.columns)
