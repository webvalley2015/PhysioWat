import numpy as np

def normalize(dfToNorm):
    df = dfToNorm
    #per ogni colonna in mezzo, devo normalizzare
    for i in xrange(len(df.columns)-1):
        temp_mean = np.mean(df[i])
        temp_std = np.std(df[i])
        df[i] -= temp_mean
        df[i] /= temp_std
    #l'ultima colonna contiene le labels
    return df