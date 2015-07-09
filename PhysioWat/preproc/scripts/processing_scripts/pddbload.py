__author__ = 'andrew'

import pandas as pd
import os
from PhysioWat.models import FeatExtractedData


def load_file_pd_db(recordingID):
#<<<<<<< HEAD
    #fpath = FeatExtractedData.objects.filter(pp_recording=recordingID).latest('id').path_to_file
#=======
    fpath = FeatExtractedData.objects.filter(pp_recording=recordingID).values_list('path_to_file') #[0][0]
    #fpath = FeatExtractedData.objects.get(pp_recording=recordingID).path_to_file.distinct()
#>>>>>>> 07bf5f5b1497ab2bfac2badc70b025e3993943a3
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
