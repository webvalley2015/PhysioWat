from django.db import models
from django.contrib.postgres.fields import ArrayField


class Experiment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True, null=True)
    token = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'experiment'


class Recording(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    experimentid = models.ForeignKey(Experiment)
    devicename = models.CharField(max_length=50)
    dictkeys = ArrayField(
        models.CharField(max_length=50, blank=True, null=True)  # This field type is a guess.
    )
    ts = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'recording'


class Sensor(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor'


class SensorData(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    recordingid = models.ForeignKey(Recording)
    store = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'sensor_data'
