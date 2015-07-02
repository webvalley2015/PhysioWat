from django.contrib import admin
from .models import Experiment, Recording, Sensor, SensorData

admin.site.register(Experiment)
admin.site.register(Sensor)
admin.site.register(Recording)
admin.site.register(SensorData)

