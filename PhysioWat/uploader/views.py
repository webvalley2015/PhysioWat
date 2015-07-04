from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import UploadForm
import csvtodb
from PhysioWat.models import Experiment
from django.contrib import messages

#View to Upload a CSV File
def upload(request):

    if request.method == "POST":

        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():

            a = request.POST.get('devicename')
            b = Experiment.objects.get(name=a)
            b = b.token
            d = form.cleaned_data
            d = d["password"]

            print b
            print d

            if b == d:
                csvtodb.putintodb(request.FILES.getlist('file'), request.POST.get('devicename'))
                messages.success(request, 'Successfully Uploaded File')
            else:
                messages.error(request, 'Invalid Password')

            return HttpResponseRedirect(reverse('humanupload'))

    else:
        form = UploadForm()
        context = {'form': form, 'experiments': getExperiments()}

    return render(request, 'uploader/home.html', context)


#Gets a list of all available experiments
def getExperiments():
        return Experiment.objects.values_list('name', flat=True)
