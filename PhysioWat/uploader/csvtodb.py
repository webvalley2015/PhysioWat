__author__ = 'andrew'

import csv
from PhysioWat.models import Sensordevices


def putintodb(fname, devicename):
    csvreader = csv.reader(fname[0], delimiter=',')
    for row in csvreader:
        if row[0].find("#") == -1:
            print row
    sensortypes = Sensordevices.objects.values_list('sensortype', flat=True).filter(device=devicename)
    tablesfordata = []
    for sensorparam in sensortypes:
        tablesfordata += [devicename + '_' + sensorparam]
    for x in tablesfordata:
        print x
    return 0
