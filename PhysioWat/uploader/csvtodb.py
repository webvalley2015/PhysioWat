__author__ = 'andrew'

import csv

from PhysioWat.models import PhysiowatRecording
from datetime import datetime
from django.db import connection


def putintodb(fname, devicename):
    csvreader = csv.reader(fname[0], delimiter=',')
    dictky = csvreader.next()

    #This won't work because experimentid is a foreign key and we must ensure data integrity.
        #Recording(experimentid=1, devicename='IMU', dictkeys=dictky, ts=datetime.now()).save()

    for row in csvreader:
        # raw query for each csv line
        cursor = connection.cursor()
        cursor.execute('INSERT INTO sensor_data (recordingid,store) VALUES (1,hstore(%s,%s))', [dictky,row])
        # results = cursor.fetchall()
    return 0
