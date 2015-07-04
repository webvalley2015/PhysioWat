
__author__ = 'andrew'

import csv

from PhysioWat.models import Recording, SensorRawData
# from django.db import connection


def putintodb(fname, dvname):
    ## NB check for parameter size and specify number of columns!!
    csvreader = csv.reader(fname[0], delimiter=',')
    dictky = csvreader.next()
    r = Recording(experiment_id=1, device_name='test', dict_keys=dictky, description='fuffa')
    r.save()
    newrecording_id = r.id
    for row in csvreader:
        # import_dict = dict.fromkeys(dictky, row)
        SensorRawData(recording_id=newrecording_id, store=dict(zip(dictky, row))).save()
        # raw query for each csv line
        # cursor = connection.cursor()
        # cursor.execute('INSERT INTO sensor_data (recordingid, store) VALUES (1,hstore(%s,%s))', [dictky,row])
        # create a new record, referencing the newly added recording and a hstore by passing
        # the keys and the values with two different lists
        # results = cursor.fetchall()
    return 0