from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField
from datetime import datetime


class Experiment(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True, null=True)
    token = models.CharField(max_length=50)


class Recording(models.Model):
    experiment = models.ForeignKey(Experiment)
    device_name = models.CharField(max_length=50)
    dict_keys = ArrayField(
        models.CharField(max_length=50, blank=True, null=True)
    )
    description = models.CharField(max_length=200, blank=True)
    ts = models.DateTimeField(default=datetime.now)


class Sensor(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)


class SensorRawData(models.Model):
    recording = models.ForeignKey(Recording)
    store = HStoreField()


class PreprocessedData(models.Model):
    raw_data = models.ForeignKey(SensorRawData)
    parameters = HStoreField()
    store = HStoreField()


class FeatExtractedData(models.Model):
    preprocessed = models.ForeignKey(PreprocessedData)
    parameters = HStoreField()
    path_to_file = models.CharField(max_length=500)
