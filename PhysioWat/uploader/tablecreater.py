__author__ = 'andrew'

import csv
from PhysioWat.models import Sensordevices


def addrowstosensordevices(devicename, sensorname, descritpion):
    for index in len(sensorname):
        temprow = Sensordevices(device=form.cleaned_data[devicename],
                                sensortype=form.cleaned_data[sensorname[index]],
                                description=form.cleaned_data[descritpion[index]])
        temprow.save()


def makenewtables(devicename):
    sensortypes = Sensordevices.objects.values_list('sensortype', flat=True).filter(device=devicename)
    tablesfordata = []
    for sensorparam in sensortypes:
        tablesfordata += [devicename + '_' + sensorparam]
    for x in tablesfordata:
        print x
    return 0
