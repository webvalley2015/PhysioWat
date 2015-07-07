from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField
from datetime import datetime

# Not actually used as of now...
class Sensor(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)



class Experiment(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True, null=True)
    token = models.CharField(max_length=50)


class Recording(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=50)
    dict_keys = ArrayField(
        models.CharField(max_length=50, blank=True, null=True)
    )
    description = models.CharField(max_length=200, blank=True)
    ts = models.DateTimeField(default=datetime.now)

class SensorRawData(models.Model):
    recording = models.ForeignKey(Recording, on_delete=models.CASCADE)
    store = HStoreField()

class Preprocessed_Recording(models.Model):
    recording = models.ForeignKey(Recording, on_delete=models.CASCADE)
    parameters = HStoreField(null=True, default=None)
    dict_keys = ArrayField(
        models.CharField(max_length=50, blank=True, null=True)
    )

class Preprocessed_Data(models.Model):
    pp_recording = models.ForeignKey(Preprocessed_Recording, on_delete=models.CASCADE)
    store = HStoreField()

class FeatExtractedData(models.Model):
    pp_recording = models.ForeignKey(Preprocessed_Recording, on_delete=models.CASCADE)
    parameters = HStoreField(null=True, default=None)
    path_to_file = models.TextField()
