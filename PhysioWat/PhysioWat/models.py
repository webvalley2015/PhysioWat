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
    batch_id = models.PositiveIntegerField()
    signal_type_name = models.CharField(max_length=20)
    applied_preproc_funcs_names = ArrayField(
        models.CharField(max_length=50)
    )
    preproc_funcs_parameters = ArrayField(
        HStoreField(blank=True, null=True)
    )
    dict_keys = ArrayField(
        models.CharField(max_length=50, blank=True, null=True)
    )


class Preprocessed_Data(models.Model):
    pp_recording = models.ForeignKey(Preprocessed_Recording, on_delete=models.CASCADE)
    store = HStoreField()

class FeatExtractedData(models.Model):
    pp_recording = models.ForeignKey(Preprocessed_Recording, on_delete=models.CASCADE)
    parameters = HStoreField(null=True, default=None)
    path_to_file = models.CharField(max_length=250)#FileField()  # To become FileField...

class MLData(models.Model):
    fe = models.ForeignKey(FeatExtractedData, on_delete=models.CASCADE)
    parameters = HStoreField(null=True, default=None)
    path_to_file = models.CharField(max_length=250)#FileField()
