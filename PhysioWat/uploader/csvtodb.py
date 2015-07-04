__author__ = 'andrew'

import csv

<<<<<<< HEAD
from PhysioWat.models import Recording, SensorRawData
# from django.db import connection
=======
from PhysioWat.models import Recording
from datetime import datetime
from django.db import connection
>>>>>>> dc28e6c8f4009a4746f6506c69cafc2d2d782f5e


def putintodb(fname, devicename):
    csvreader = csv.reader(fname[0], delimiter=',')
    dictky = csvreader.next()
<<<<<<< HEAD
    r = Recording(experiment_id=1, device_name='test', dict_keys=dictky, description='fuffa')
    r.save()
    newrecording_id = r.id
=======

    #This won't work because experimentid is a foreign key and we must ensure data integrity.
        #Recording(experimentid=1, devicename='IMU', dictkeys=dictky, ts=datetime.now()).save()

>>>>>>> dc28e6c8f4009a4746f6506c69cafc2d2d782f5e
    for row in csvreader:
        # raw query for each csv line
        cursor = connection.cursor()
        cursor.execute("INSERT INTO \"PhysioWat_sensordata\" (store) VALUES (hstore(%s,%s))", [dictky,row])
        # results = cursor.fetchall()
    return 0
