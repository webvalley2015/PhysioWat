__author__ = 'andrew'

import csv


def putintodb(fname, devicename):
    csvreader = csv.reader(fname[0], delimiter=',')
    for row in csvreader:
        if row[0].find("#") == -1:
            print row
    print devicename
    return 0
