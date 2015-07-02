from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import UploadForm
import csvtodb


# Create your views here.

def upload(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            csvtodb.putintodb(request.FILES.getlist('file'), request.POST.get('devicename'))
            #form.save()
            return HttpResponseRedirect(reverse('humanupload'))
    else:
        form = UploadForm()
    context = {'form': form, 'manufacturer': fun(), 'sensortypes': getSensorTypes()}
    return render(request, 'uploader/home.html', context)

def fun():
        return ['a','b','c','d']
def getSensorTypes():
        return ['e','f','g','h']