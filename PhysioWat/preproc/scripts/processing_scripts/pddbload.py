__author__ = 'andrew'

import pandas as pd
import os
from PhysioWat.models import FeatExtractedData


def load_file_pd_db(recordingID):
    fpath = FeatExtractedData.objects.get(pp_recording=recordingID).path_to_file
    uncleanedfile = open(fpath, 'r')
    if os.path.isfile(fpath + 'p'):
        uncleanedfile.close()
    else:
        file = open(fpath + 'p', 'w')
        for line in uncleanedfile:
            file.write(line.replace(' ', ''))
        uncleanedfile.close()
        file.close()
    filecleaned = open(fpath + 'p', 'r')
    datacsv = pd.read_csv(filecleaned, sep=',')
    return datacsv
