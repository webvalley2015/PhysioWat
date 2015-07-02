from __future__ import division
import pandas as pd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import spectrum as spct

#####################################
## NOTE
# PSD estimation: AR method
# INTERPOLATION: cubic spline
# ! ! !
# RR in milliseconds!
#####################################

def calculateHRVindexes(RR, Finterp=4):
    '''
    funzione per calcolare le features di una finestra di IBI
    RR: frammento di IBI (in ms) come array (N,)
    return: array numpy di numeri (le features) ed eventualmente un array di labels
    '''
    TDindexes, TDlabels=calculateTDindexes(RR) # TD indexes
    FDindexes, FDlabels=calculateFDindexes(RR, Finterp) # FD indexes
    
    Indexes=np.hstack((TDindexes, FDindexes))#, NLindexes, POINindexes, Hindex, PFDindex,  DFAindex)) # remove not calculated indexes
    return Indexes

def calculateTDindexes(RR):
    #calculates Time domain indexes
    RRmean=np.mean(RR)
    RRSTD= np.std(RR)            
    
    RRDiffs=np.diff(RR) 
        
    RRDiffs50 = [x for x in np.abs(RRDiffs) if x>50]
    pNN50=100.0*len(RRDiffs50)/len(RRDiffs)
    RRDiffs25 = [x for x in np.abs(RRDiffs) if x>25]
    pNN25=100.0*len(RRDiffs25)/len(RRDiffs)
    RRDiffs10 = [x for x in np.abs(RRDiffs) if x>10]
    pNN10=100.0*len(RRDiffs10)/len(RRDiffs)
    
    RMSSD = np.sqrt(sum(RRDiffs**2)/(len(RRDiffs)-1))
    SDSD = np.std(RRDiffs)

    labels= np.array(['RRmean', 'RRSTD', 'pNN50', 'pNN25', 'pNN10', 'RMSSD', 'SDSD'], dtype='S10')
    
    return [RRmean, RRSTD, pNN50, pNN25, pNN10, RMSSD,  SDSD], labels

def calculateFDindexes(RR,  Finterp):
    
    def power(spec,freq,fmin,fmax):
        #returns power in band
        band = np.array([spec[i] for i in range(len(spec)) if freq[i] >= fmin and freq[i]<fmax])
        powerinband = np.sum(band)/len(spec)
        return powerinband
   
    def InterpolateRR(RR, Finterp):
        # returns cubic spline interpolated array with sample rate = Finterp
        step=1/Finterp 
        BT=np.cumsum(RR) 
        xmin=BT[0]
        xmax=BT[-1]
        BT = np.insert(BT,0,0)
        BT=np.append(BT, BT[-1]+1)
        RR = np.insert(RR,0,0)
        RR=np.append(RR, RR[-1])
        
        tck = interpolate.splrep(BT,RR)
        BT_interp = np.arange(xmin,xmax,step)
        RR_interp = interpolate.splev(BT_interp,  tck)
        return RR_interp,  BT_interp
    
    RR=RR/1000 #RR in seconds
    RR_interp, BT_interp=InterpolateRR(RR, Finterp)
    RR_interp=RR_interp-np.mean(RR_interp)

    freqs=np.arange(0, 2, 0.0001)
    
    # calculates AR coefficients
    AR, P, k = spct.arburg(RR_interp*1000, 16) #burg
    
    # estimates PSD from AR coefficients
    spec = spct.arma2psd(AR,  T=0.25, NFFT=2*len(freqs)) # pectrum estimation
    spec = spec[0:len(spec)/2]   
    
    # WELCH psd estimation
    
    # calculates power in different bands
    VLF=power(spec,freqs,0,0.04)
    LF=power(spec,freqs,0.04,0.15)
    HF=power(spec,freqs,0.15,0.4)
    Total=power(spec,freqs,0,2)
    LFHF = LF/HF
    nVLF=VLF/Total # Normalized
    nLF=LF/Total
    nHF=HF/Total
    
    #NormalizedHF HFNormal

    LFn=LF/(HF+LF)
    HFn=HF/(HF+LF)
    Power = [VLF, HF, LF]
    
    Power_Ratio= Power/sum(Power)
#    Power_Ratio=spec/sum(spec) # uncomment to calculate Spectral Entropy using all frequencies
    Spectral_Entropy = 0
    lenPower=0 # tengo conto delle bande che ho utilizzato
    for i in xrange(0, len(Power_Ratio)):
        if Power_Ratio[i]>0: # potrei avere VLF=0
            Spectral_Entropy += Power_Ratio[i] * np.log(Power_Ratio[i])
            lenPower +=1
    Spectral_Entropy /= np.log(lenPower) #al posto di len(Power_Ratio) perche' magari non ho usato VLF
    
    labels= np.array(['VLF', 'LF', 'HF', 'Total', 'nVLF', 'nLF', 'nHF', 'LFn', 'HFn', 'LFHF', 'SpecEn'],  dtype='S10')
    
    return [VLF, LF, HF, Total, nVLF, nLF, nHF, LFn, HFn, LFHF, Spectral_Entropy], labels
