from django.contrib import admin
from .models import Experiment, Recording, Sensor, SensorRawData, Preprocessed_Data, Preprocessed_Recording, FeatExtractedData

admin.site.register(Experiment)
admin.site.register(Sensor)
admin.site.register(Recording)
admin.site.register(SensorRawData)
admin.site.register(Preprocessed_Data)
admin.site.register(Preprocessed_Recording)
admin.site.register(FeatExtractedData)
