
__author__ = 'andrew'

import csv

from PhysioWat.models import Recording, SensorRawData, Experiment
# from django.db import connection

def putintodbflex(fnames, dvname, desc, exp_id):
    if hasattr(fnames, '__iter__'):
        for filename in fnames:
            csvreader = csv.reader(filename, delimiter=',')
            dictky = csvreader.next()
            for index in range(len(dictky)):
                dictky[index] = dictky[index].replace('#','').replace(' ','')

            r = Recording(experiment_id=exp_id, device_name=dvname, dict_keys=dictky, description=desc)

            r.save()
            ll=[]
            for row in csvreader:
                ll.append(SensorRawData(recording_id=r.id, store=dict(zip(dictky, row))))

            SensorRawData.objects.bulk_create(ll, batch_size=1000)
    return 0

'''
def putintodb(fname, dvname, desc, exp_id):
    csvreader = csv.reader(fname[0], delimiter=',')
    dictky = csvreader.next()
    for index in range(len(dictky)):
        dictky[index] = dictky[index].replace('#','').replace(' ','')

    print exp_id
    r = Recording(experiment_id=exp_id, device_name=dvname, dict_keys=dictky, description=desc)
    r.save()

    for row in csvreader:
        # import_dict = dict.fromkeys(dictky, row)
        SensorRawData(recording_id=r.id, store=dict(zip(dictky, row))).save()
        # raw query for each csv line
        # cursor = connection.cursor()
        # cursor.execute('INSERT INTO sensor_data (recordingid, store) VALUES (1,hstore(%s,%s))', [dictky,row])
        # create a new record, referencing the newly added recording and a hstore by passing
        # the keys and the values with two different lists
        # results = cursor.fetchall()
    return 0
'''