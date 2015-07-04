from django.shortcuts import render
from django.http import HttpResponse
from .forms import experiments
from django.contrib import messages
from PhysioWat.models import PhysiowatExperiment
# from PhysioWat.models import S
# from PhysioWat.models import Sensor
# Create your views here.

def create_experiement(request):
    if request.method == "POST":
        form = experiments(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experiment created succesfully')
        else:
            messages.error(request, 'Error while creating the experiment.')
        #return HttpResponse()
    else:
        form = experiments()
    context = {'form': form}
    return render(request, 'designer/experiments.html', context)

# def getSensordevices():
#     return Sensordevices.objects.values_list('device', flat=True).distinct()

# def getAvaliableSensors():
#     return Sensordevices.objects.values_list('sensortype', flat=True).distinct().order_by('sensortype')
