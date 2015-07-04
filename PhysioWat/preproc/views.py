from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from forms import filterAlg, downsampling, BVP, EKG, GSR, inertial, remove_spike, smoothGaussian, choose_exp
from PhysioWat.models import Experiment
from django.contrib import messages


def preproc_settings(request):
    if request.method == "POST":
        form = PreprocSettings(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponseRedirect(reverse('humanupload'))
    else:

        formPick = None
        if (True):
            formDown = downsampling(initial={'switch': False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(
                initial={'passFr': 2, 'stopFr': 6, 'LOSS': 0.1, 'ATTENUATION': 40, 'filterType': 'cheby2'})
            formSpec = BVP()
        if (True):
            formDown = downsampling(initial={'switch': False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(initial={'filterType': 'none'})
            formSpec = EKG()
        if (True):
            formDown = downsampling(initial={'switch': False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(initial={'filterType': 'none'})
            formSpec = inertial()
        if (True):
            formPick = remove_spike()
            formDown = downsampling(initial={'switch': False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(initial={'filterType': 'none'})
            formSpec = GSR()

    context = {'formFilt': formFilt, 'formDown': formDown, 'formPick': formPick, 'formSpec': formSpec,
               'formGau': formGau}
    return render(request, 'preproc/settings.html', context)


def show_chart(request):
    template = "preproc/chart.html"

    # load all the algorithms forms
    # TODO discuss a way to obtain all the form dinamically

    if request.method == "POST":
        form = PreprocSettings(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponseRedirect(reverse('humanupload'))
    else:
        formPick = None
        if (True):
            formDown = downsampling(initial={'switch': False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(
                initial={'passFr': 2, 'stopFr': 6, 'LOSS': 0.1, 'ATTENUATION': 40, 'filterType': 'cheby2'})
            formSpec = BVP()
        if (True):
            formDown = downsampling(initial={'switch': False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(initial={'filterType': 'none'})
            formSpec = EKG()
        if (True):
            formDown = downsampling(initial={'switch': False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(initial={'filterType': 'none'})
            formSpec = inertial()
        if (True):
            formPick = remove_spike()
            formDown = downsampling(initial={'switch': False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(initial={'filterType': 'none'})
            formSpec = GSR()

    context = {'forms': {'formFilt': formFilt, 'formDown': formDown,
                         'formPick': formPick, 'formSpec': formSpec, 'formGau': formGau}}
    return render(request, template, context)


def select_experiment(request):
    if request.method == 'POST':
        exp_name = request.POST.get('exp_name')
        password = request.POST.get('password')
        err_log = False
        for i in getExperimentsList():
            if exp_name == i[0] and password == i[1]:
                err_log = True
        if err_log:
            return HttpResponseRedirect('/preproc/recording')
        else:
            messages.error(request, 'Error wrong password')
    else:
        name_list = getExperimentsNames()
        context = {'name_list':name_list}
        return render(request, 'preproc/experiments.html', context)

def getExperimentsNames():
    return Experiment.objects.values_list('name', flat=True).distinct()

def getExperimentsList():
    return Experiment.objects.values_list('name', 'token').distinct()

