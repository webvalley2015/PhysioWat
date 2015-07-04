from django.contrib import admin
from .models import PhysiowatExperiment, PhysiowatRecording, PhysiowatSensor, PhysiowatSensordata

admin.site.register(PhysiowatExperiment)
admin.site.register(PhysiowatSensor)
admin.site.register(PhysiowatRecording)
admin.site.register(PhysiowatSensordata)

