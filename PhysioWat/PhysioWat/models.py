from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField
from datetime import datetime


class PhysiowatExperiment(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True, null=True)
    token = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'PhysioWat_experiment'


class PhysiowatRecording(models.Model):
    experiment_id = models.ForeignKey(PhysiowatExperiment)
    device_name = models.CharField(max_length=50)
    dict_keys = ArrayField(
        models.CharField(max_length=50, blank=True, null=True)
    )
    description = models.CharField(max_length=200)
    ts = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'PhysioWat_recording'


class PhysiowatSensor(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PhysioWat_sensor'


class PhysiowatSensordata(models.Model):
    recording_id = models.ForeignKey(PhysiowatRecording)
    store = HStoreField()

    class Meta:
        managed = False
        db_table = 'PhysioWat_sensordata'
