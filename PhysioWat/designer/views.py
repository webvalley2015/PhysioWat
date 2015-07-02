from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from .forms import SensorDesignerForm
from PhysioWat.models import Sensordevices
from PhysioWat.models import Sensors
import tablecreater

# Create your views here.

def createsensor(request):
    if request.method == "POST":
        form = SensorDesignerForm(request.POST, request.FILES)
        if form.is_valid():
            b2 = Sensors(sensornames=form.cleaned_data['Name'])
            b2.save()
            return HttpResponse(form.cleaned_data['Name'] + str(form.cleaned_data['Sensors']))#request.POST.get('Name')     #form.cleaned_data['Name']
    else:
        form = SensorDesignerForm()

    context = {'form': form, 'manufacturer': getSensordevices(), 'sensornumber': request.POST.get('Sensors')}
    return render(request, 'designer/home.html', context)

def getSensordevices():
    return Sensordevices.objects.values_list('device', flat=True).distinct()

def getAvaliableSensors():
    return Sensordevices.objects.values_list('sensortype', flat=True).distinct()


