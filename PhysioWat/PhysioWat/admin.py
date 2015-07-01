from django.contrib import admin
from .models import Experimenter, Experiment, Sensors, Subject, Sensordevices

admin.site.register(Experimenter)
admin.site.register(Experiment)
admin.site.register(Sensors)
admin.site.register(Subject)
admin.site.register(Sensordevices)

