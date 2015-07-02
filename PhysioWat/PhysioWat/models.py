from django.db import models


class Experiment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    experimenterid = models.IntegerField()
    experimentname = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'experiment'


class Experimenter(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'experimenter'


class Sensordevices(models.Model):
    device = models.CharField(max_length=50)
    sensortype = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True, null=True)
    device.primary_key = True;
    sensortype.primary_key = True;

    class Meta:
        managed = False
        db_table = 'sensordevices'
        unique_together = (('device', 'sensortype'),)


class Sensors(models.Model):
    sensornames = models.CharField(max_length=50)
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sensors'


class Subject(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subject'

class Sensorexample(models.Model):
    experimenterid = models.IntegerField(db_column='ExperimenterID')  # Field name made lowercase.
    experimentid = models.IntegerField(db_column='ExperimentID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='SubjectID')  # Field name made lowercase.
    timestamp = models.FloatField(db_column='TimeStamp')  # Field name made lowercase.
    paramatervalue = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'sensorexample'
        unique_together = (('ExperimenterID', 'ExperimentID', 'TimeStamp', 'SubjectID'),)




