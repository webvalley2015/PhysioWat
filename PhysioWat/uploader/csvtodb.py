# __author__ = 'andrew'
#
# import csv
#
# #from PhysioWat.models import Sensordevices
# from PhysioWat.models_dynamic import *
#
#
# def putintodb(fname, devicename):
#     csvreader = csv.reader(fname[0], delimiter=',')
#     for row in csvreader:
#         if row[0].find("#") == -1:
#             print row
#             imuUPLOAD(0,0,int(row[0]),int(row[1]),row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11])
#     sensortypes = Sensordevices.objects.values_list('sensortype', flat=True).filter(device=devicename)
#     tablesfordata = []
#     for sensorparam in sensortypes:
#         tablesfordata += [sensorparam]
#     for x in tablesfordata:
#         print x
#     return 0
#
# def imuUPLOAD(tistID,entID,subID,TS,ax,ay,az,gx,gy,gz,mx,my,mz):
#     ACCX(experimenterid=tistID,
#          experimentid=entID,
#          subjectid=subID,
#          timestamp=TS,
#          paramatervalue=ax).save()
#
#     ACCY(experimenterid=tistID,
#          experimentid=entID,
#          subjectid=subID,
#          timestamp=TS,
#          paramatervalue=ay).save()
#
#     ACCZ(experimenterid=tistID,
#          experimentid=entID,
#          subjectid=subID,
#          timestamp=TS,
#          paramatervalue=az).save()
#
#     GYROX(experimenterid=tistID,
#           experimentid=entID,
#           subjectid=subID,
#           timestamp=TS,
#           paramatervalue=gx).save()
#
#     GYROY(experimenterid=tistID,
#           experimentid=entID,
#           subjectid=subID,
#           timestamp=TS,
#           paramatervalue=gy).save()
#
#     GYROZ(experimenterid=tistID,
#           experimentid=entID,
#           subjectid=subID,
#           timestamp=TS,
#           paramatervalue=gz).save()
#
#     MAGX(experimenterid=tistID,
#          experimentid=entID,
#          subjectid=subID,
#          timestamp=TS,
#          paramatervalue=mx).save()
#
#     MAGY(experimenterid=tistID,
#          experimentid=entID,
#          subjectid=subID,
#          timestamp=TS,
#          paramatervalue=my).save()
#
#     MAGZ(experimenterid=tistID,
#          experimentid=entID,
#          subjectid=subID,
#          timestamp=TS,
#          paramatervalue=mz).save()
#     return 0