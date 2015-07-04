from django.shortcuts import render
from django.http import HttpResponse
from .forms import experiments
# from PhysioWat.models import S
# from PhysioWat.models import Sensor
# Create your views here.

def create_experiement(request):
    if request.method == "POST":
        form = experiments(request.POST)
        if form.is_valid():
            b1 = form.cleaned_data['name']
            b2 = form.cleaned_data['desc']
            b3 = form.cleaned_data['password']

        # b2.save()
        # return HttpResponse(form.cleaned_data['Name'] + str(form.cleaned_data['Sensors']))#request.POST.get('Name')     #form.cleaned_data['Name']
    else:
        form = experiments()
    context = {'form': form}
    return render(request, 'designer/experiments.html', context)

# def getSensordevices():
#     return Sensordevices.objects.values_list('device', flat=True).distinct()

# def getAvaliableSensors():
#     return Sensordevices.objects.values_list('sensortype', flat=True).distinct().order_by('sensortype')
