from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from forms import filterAlg, downsampling, BVP, EKG, GSR, inertial, remove_spike, smoothGaussian
from PhysioWat.models import Experiment
from django.contrib import messages
from .jsongen import getavaliabledatavals
from scripts.processing_scripts import tools, inertial
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
            formSpec = inertial()
        if (True):
            formPick = remove_spike()
            formDown = downsampling(initial={'switch': False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(initial={'filterType': 'none'})
            formSpec = GSR()

        opt_temp = getavaliabledatavals(id_num)
        opt_list = opt_temp[1:]

        context = {'forms': {'Filter': formFilt, 'Downpass': formDown,
                     'Spike': formPick, 'Special': formSpec, 'Gaussian': formGau},
           'opt_list': opt_list, 'id_num':id_num}
        return render(request, template, context)


def getExperimentsNames():
    return Experiment.objects.values_list('name', flat=True).distinct()


def getExperimentsList():
    return Experiment.objects.values_list('name', 'token').distinct()


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
        context = {'name_list': name_list}
        return render(request, 'preproc/experiments.html', context)

def test(request):
    print "OK"
    data = tools.load_raw_db(8)
    sensAccCoeff=8*9.81/32768
    sensGyrCoeff=2000/32768
    sensMagCoeff=0.007629
    t=data[:,1]
    acc=data[:,3:6]
    gyr=data[:,6:9]
    mag=data[:,9:12]

    acc= inertial.convert_units(acc, coeff=sensAccCoeff)
    gyr= inertial.convert_units(gyr, coeff=sensGyrCoeff)
    mag= inertial.convert_units(mag, coeff=sensMagCoeff)
    output_columns=["timeStamp","AccX","AccY","AccZ","GyrX","GyrY","GyrZ","MagX","MagY","MagZ"]
    tools.putPreprocArrayintodb(8, np.column_stack([t, acc, gyr, mag]), np.array(output_columns))

    return render(request,'preproc/experiments.html', {'name_list':["exp1"]})