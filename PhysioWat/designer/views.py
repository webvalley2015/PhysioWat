from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .forms import experiments
from PhysioWat.models import Experiment
# from PhysioWat.models import S
# from PhysioWat.models import Sensor
# Create your views here.

def create_experiement(request):
    if request.method == "POST":
        form = experiments(request.POST)
        if form.is_valid():
            errCount = True
            for i in getExperimentsNames():
                if form.cleaned_data["name"] == i:
                    errCount = False
            if errCount:
                if form.cleaned_data["token"] == form.cleaned_data["repeat_token"]:
                    form.save()
                    messages.success(request, 'Experiment created succesfully')
                else:
                    messages.error(request, 'Tokens dont match')
            else:
                messages.error(request, 'Experiment already exists')
        else:
            messages.error(request, 'Error while creating the experiment.')
        #return HttpResponse("/")
    else:
        form = experiments()
    context = {'form': form}
    return render(request, 'designer/experiments.html', context)

def getExperimentsNames():
    return Experiment.objects.values_list('name', flat=True).distinct()

# def getAvaliableSensors():
#     return Sensordevices.objects.values_list('sensortype', flat=True).distinct().order_by('sensortype')
