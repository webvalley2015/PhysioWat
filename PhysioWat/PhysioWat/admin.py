from django.contrib import admin
from .models import Experiment, Recording, Sensor, SensorRawData, PreprocessedData, FeatExtractedData

admin.site.register(Experiment)
admin.site.register(Sensor)
admin.site.register(Recording)
admin.site.register(SensorRawData)
admin.site.register(PreprocessedData)
admin.site.register(FeatExtractedData)
