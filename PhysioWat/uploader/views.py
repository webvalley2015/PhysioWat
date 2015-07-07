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
            experiment_id = request.POST.get('experiment')
            actualPasscode = Experiment.objects.get(id=experiment_id).token
            enteredPasscode = form.cleaned_data
            enteredPasscode = enteredPasscode["password"]

            if enteredPasscode == actualPasscode:
                csvtodb.putintodbflex(request.FILES.getlist('file'), request.POST.get('device'), request.POST.get('description'), experiment_id)
                messages.success(request, 'Successfully Uploaded File')
            else:
                messages.error(request, 'Invalid Password')

        return HttpResponseRedirect(reverse('user_upload'))
    else:
        form = UploadForm()
        context = {'form': form, 'experiments': getExperiments()}
    return render(request, 'uploader/home.html', context)


#Gets a list of all available experiments
def getExperiments():
        return Experiment.objects.values_list('id', 'name')
