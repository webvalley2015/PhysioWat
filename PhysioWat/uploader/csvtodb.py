__author__ = 'andrew'

import csv

from PhysioWat.PhysioWat.models import Recording, SensorData
# from django.db import connection


def putintodb(fname, dvname):t
    csvreader = csv.reader(fname[0], delimiter=',')
    dictky = csvreader.next()
    r = Recording(experiment_id=1, devicename=dvname, dictkeys=dictky)
    r.save()

    for row in csvreader:
        import_dict = dict.fromkeys(dictky, row)
        SensorData(recording_id=r.id(), store=import_dict)
        # raw query for each csv line
        # cursor = connection.cursor()
        # cursor.execute('INSERT INTO sensor_data (recordingid, store) VALUES (1,hstore(%s,%s))', [dictky,row])
        # create a new record, referencing the newly added recording and a hstore by passing
        # the keys and the values with two different lists
        # results = cursor.fetchall()
    return 0
