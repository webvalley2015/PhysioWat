from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Upload
from .forms import UploadForm
from PhysioWat.models import Sensordevices
from PhysioWat.models import Experiment



# Create your views here.

def upload(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('imageupload'))
    else:
        form = UploadForm()
    images = Upload.objects.all()
    context = {'form': form, 'images': images, 'manufacturer': sensor_manufacturer()}
    return render(request, 'uploader/home.html', context)

def sensor_manufacturer():
    ids = Sensordevices.objects.values_list('device', flat=True).distinct()
    return ids
