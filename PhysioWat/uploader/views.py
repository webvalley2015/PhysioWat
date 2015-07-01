from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Upload
from .forms import UploadForm
from PhysioWat.models import Sensordevices



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
    context = {'form': form, 'images': images, 'manufacturer': fun()}
    return render(request, 'uploader/home.html', context)

def fun():
    return Sensordevices.objects.distinct('device')
