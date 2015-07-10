__author__ = 'andrew'

import pandas as pd
import os
from PhysioWat.models import FeatExtractedData
from django.conf import  settings

def load_file_pd_db(recordingID):
    fpath = FeatExtractedData.objects.filter(id=recordingID).values_list('path_to_file') #[0][0]
    #fpath = FeatExtractedData.objects.get(pp_recording=recordingID).path_to_file.distinct()
    file_name = '{0}/{1}'.format(settings.BASE_DIR, fpath[0][0])
    uncleanedfile = open(file_name, 'r')

    file = open(file_name + 'proc_ml', 'w')
    for line in uncleanedfile:
        file.write(line.replace(' ', ''))
    uncleanedfile.close()
    file.close()
    filecleaned = open(file_name + 'proc_ml', 'r')
    datacsv = pd.read_csv(filecleaned, sep=',')
    print datacsv
    return datacsv