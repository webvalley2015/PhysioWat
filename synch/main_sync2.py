import numpy as np
import sync2 as s2

s2.correlate_features("feat_GSR_F01_F.txt","feat_GSR_F01_M.txt")     #print the value of linear correlation GSR
s2.correlate_features("feat_EKG_F01_F.txt"," feat_EKG_F01_M.txt")       #print the value of linear correlation EKG

s2.dtw("GSR_F01_F.txt","GSR_F01_M.txt")              #print the dynamic time warping between the GSR signals
