from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from forms import filterAlg, downsampling, BVP, EKG, GSR, inertial, remove_spike, smoothGaussian
from PhysioWat.models import Experiment, Recording
from django.contrib import messages
from .jsongen import getavaliabledatavals
from scripts.processing_scripts import tools, inertial, filters, IBI
import numpy as np


def show_chart(request, id_num):
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
            #formSpec = inertial()
        if (True):
            formPick = remove_spike()
            formDown = downsampling(initial={'switch': False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(initial={'filterType': 'none'})
            formSpec = GSR()

        opt_temp = getavaliabledatavals(id_num)
        opt_list = opt_temp#[1:]

        context = {'forms': {'Filter': formFilt, 'Downpass': formDown,
                     'Spike': formPick, 'Special': formSpec, 'Gaussian': formGau},
           'opt_list': opt_list, 'id_num':id_num}
        return render(request, template, context)

def getExperimentsNames():
    return Experiment.objects.values_list('name', flat=True).distinct()


def getExperimentsList():
    return Experiment.objects.values_list('id', 'name', 'token').distinct()


def select_experiment(request):
    if request.method == 'POST':
        exp_name = request.POST.get('exp_name')
        password = request.POST.get('password')
        err_log = False
        for i in getExperimentsList():
            if exp_name == i[1] and password == i[2]:
                err_log = True
                num_exp = i[0]
        if err_log:
            return HttpResponseRedirect('/preproc/records/'+str(num_exp))
        else:
            messages.error(request, 'Error wrong password')
    else:
        name_list = getExperimentsNames()
        context = {'name_list': name_list}
        return render(request, 'preproc/experiments.html', context)

def getRecordsList(experimentId):
    return Recording.objects.filter(experiment=experimentId).values_list('id', flat=True)

def select_record(request, id_num):
    print(id_num)
    if request.method == 'POST':
        record_id = request.POST.get('rec_name')
        return HttpResponseRedirect('/preproc/chart/'+str(record_id))
    else:
        name_list = getRecordsList(id_num)
        context = {'name_list': name_list}
        return render(request, 'preproc/records.html', context)

def test(request):
    print "OK"
    ID=10
    SAMP_F = 64

    #load data from the file
    rawdata = tools.load_raw_db(ID)

    #filter the signal
    #the user selects the parameters, with default suggested
    filterType = 'butter'
    F_PASS = 2
    F_STOP = 6
    ILOSS = 0.1
    IATT = 40
    filtered_signal = filters.filterSignal(rawdata, SAMP_F, passFr = F_PASS, stopFr = F_STOP, LOSS = ILOSS, ATTENUATION = IATT, filterType = filterType)
    #filtered_signal = rawdata

    #extraction peaks from the signal
    #the user selects the parameters, with default suggested
    delta = 1
    peaks = IBI.getPeaksIBI(filtered_signal,SAMP_F, delta)

    #calculation of the IBI
    #the user selects the parameters, with default suggested
    minFr = 40
    maxFr = 200
    ibi = IBI.max2interval(peaks[:,0], minFr, maxFr)

    tools.putPreprocArrayintodb(ID, ibi, np.array(["timestamp", "IBI"]))

    return render(request,'preproc/experiments.html', {'name_list':["exp1"]})

