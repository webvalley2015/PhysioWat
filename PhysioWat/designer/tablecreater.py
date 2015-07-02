__author__ = 'andrew'

from PhysioWat.models import Sensordevices
import psycopg2


def addrowstosensordevices(devicename, sensorname, descritpion):
    for index in range(len(sensorname)):
        temprow = Sensordevices(device=devicename,
                                sensortype=sensorname[index],
                                description=descritpion[index])
        temprow.save()


def makenewtables(devicename):
    sensortypes = Sensordevices.objects.values_list('sensortype', flat=True).filter(device=devicename)
    tablesfordata = []
    for sensorparam in sensortypes:
        tablesfordata += [sensorparam]
    for x in tablesfordata:
        print x
        newtablenamed(x)
        newmodelnamed(x)
    return 0


def newtablenamed(tablenm):
    command = "CREATE TABLE " + tablenm + " (\"ExperimenterID\" integer NOT NULL,\"ExperimentID\" integer NOT NULL, \"SubjectID\" integer NOT NULL, \"TS\" double precision NOT NULL,paramatervalue character varying(50) NOT NULL, CONSTRAINT " + tablenm + "_pkey PRIMARY KEY (\"ExperimenterID\", \"ExperimentID\", \"TS\", \"SubjectID\"))"
    conn = psycopg2.connect(database='physiowat', user='developer', password='webvalley', host='192.168.210.175',
                            port='5432')
    maincur = conn.cursor()
    maincur.execute(command)
    conn.commit()
    maincur.close()
    conn.close()


def newmodelnamed(tablenm):
    f = open("models_dynamic.py", "a")
    f.write('\n')
    f.write('class ' + tablenm.upper() + '(models.Model):\n')
    f.write('    experimenterid = models.IntegerField(db_column=\'ExperimenterID\', primary_key=True)  # Field name made lowercase.\n')
    f.write('    experimentid = models.IntegerField(db_column=\'ExperimentID\', primary_key=True)  # Field name made lowercase.\n')
    f.write('    subjectid = models.IntegerField(db_column=\'SubjectID\', primary_key=True)  # Field name made lowercase.\n')
    f.write('    timestamp = models.FloatField(db_column=\'TS\', primary_key=True)  # Field name made lowercase.\n')
    f.write('    paramatervalue = models.CharField(max_length=50)\n')
    f.write('    class Meta:\n')
    f.write('        managed = False\n')
    f.write('        db_table = \'' + tablenm.lower() + '\'\n')
    f.write('        unique_together = ((\'experimenterid\', \'experimentid\', \'timestamp\', \'subjectid\'),)\n')
