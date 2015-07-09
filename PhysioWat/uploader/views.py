from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .forms import UploadForm
import csvtodb
from PhysioWat.models import Experiment
from django.contrib import messages
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt


#View to Upload a CSV File
def upload(request):

    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            exp_id = request.POST.get('experiment')
            actualPasscode = Experiment.objects.get(id=exp_id).token
            enteredPasscode = form.cleaned_data
            enteredPasscode = enteredPasscode["password"]
            if enteredPasscode == actualPasscode:
                try:
                    csvtodb.putintodbflex(request.FILES.getlist('file'), request.POST.get('device'),
                                          request.POST.get('description'), exp_id)
                    messages.success(request, 'Successfully Uploaded File!')

                except Exception:
                    messages.error(request, 'Invalid request. Make sure that the file to import is in csv/txt format.')
            else:
                messages.error(request, 'Wrong password.')

        return HttpResponseRedirect(reverse('user_upload'))
    else:
        form = UploadForm()
        context = {'form': form, 'experiments': getExperiments()}
    return render(request, 'uploader/home.html', context)


#Gets a list of all available experiments
def getExperiments():
        return Experiment.objects.values_list('id', 'name')

@csrf_exempt
def get_data_from_mobile(request):
    if request.method == 'POST':
        data = request.POST['file']
    else:
        data = []
    return HttpResponse(data)


def list_experiment_id(request):
    myexp = Experiment.objects.all()
    myret = [[f.id, f.name] for f in myexp]
    return HttpResponse(myret)
