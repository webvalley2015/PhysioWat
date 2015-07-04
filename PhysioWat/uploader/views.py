from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import UploadForm
import csvtodb
from PhysioWat.models import Experiment
from django.db import connection


# Create your views here.

def upload(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():

            a = request.POST.get('devicename')
            b = Experiment.objects.filter(name=a)
            print b[0].name


            #csvtodb.putintodb(request.FILES.getlist('file'), request.POST.get('devicename'))
            #form.save()
            return HttpResponseRedirect(reverse('humanupload'))
    else:
        form = UploadForm()
        context = {'form': form, 'experiments': getExperiments()}

    return render(request, 'uploader/home.html', context)

def getExperiments():
        return Experiment.objects.values_list('name', flat=True)
