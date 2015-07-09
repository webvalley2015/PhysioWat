

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .forms import UploadForm
import csvtodb
from PhysioWat.models import Experiment
from django.contrib import messages
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt
import json
from django.core.serializers.json import DjangoJSONEncoder

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
        # POST:
        # in 'data'   -> file to be read
        # in 'exp_id' -> experiment id

        if 'data' not in request.POST:
            print "Error: no data received or bad POST key for data ",
            print "(it must be 'data'). No data will be save to db."
        elif 'exp_id' not in request.POST:
            print "Error: no experiment selected. No data will be save to db."
        else:
            exp_id = request.POST['exp_id']
            descr = "mobile data for exp n. {0}".format(exp_id)
            try:
                csvtodb.putintodbflex(request.FILES.getlist(),
                                      'mobile',
                                      desc,
                                      exp_id)
            except Exception as e:
                print "Error while saving mobile data to db."
                print "Details: {0}".format(e)
    else:
        print "Warning: No POST request received. Doing nothing."
        
    return HttpResponse(data)


def list_experiment_id(request):
    myexp = Experiment.objects.all().values_list('id', 'name')
    myret_json = json.dumps({"tot":len(myexp), "experiments": [{'id':i[0], 'desc': i[1]} for i in myexp]})
    return HttpResponse(myret_json, content_type="application/json")
