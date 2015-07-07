from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .forms import filterAlg, downsampling, BVP_Form, EKG_Form, GSR_Form, Inertial_Form, remove_spike, smoothGaussian
from PhysioWat.models import Experiment, Recording, SensorRawData
from django.contrib import messages
from .jsongen import getavaliabledatavals
from scripts.processing_scripts import tools, inertial, filters, IBI, GSR
import numpy as np
from StringIO import StringIO


def QueryDb(recordingID):
    table = Recording.objects.get(id=recordingID)
    data = SensorRawData.objects.filter(recording_id=recordingID)
    alldata = (','.join(table.dict_keys) + '\n').replace(' ', '')
    for record in data:
        ll = []
        for key in table.dict_keys:
            ll.append(record.store[key])
        alldata += ','.join(ll) + '\n'
    datacsv = np.genfromtxt(StringIO(alldata), delimiter=',')
    return datacsv


def putPreprocArrayintodb(rec_id, preProcArray, preProcLabel):
    # Andrew's crazy method to convert array to CSV-ish string??? IDK what it means, but IT WORKS!!!
    csvasstring = ",".join(preProcLabel.tolist()) + '\n'
    for dataarr in preProcArray:
        for dataval in dataarr:
            csvasstring += str(dataval) + ','
        csvasstring = csvasstring[:-1]
        csvasstring += '\n'

    # Initiate the CSV Reader
    csvreader = csv.reader(StringIO(csvasstring), delimiter=',')
    dictky = csvreader.next()

    # Submit data to model and thus the database table
    pr = Preprocessed_Recording(recording_id=rec_id, dict_keys=dictky)
    pr.save()

    for row in csvreader:
        Preprocessed_Data(pp_recording=pr.id, store=dict(zip(dictky, row))).save()

    return 0


def show_chart(request, id_num, alg_type=""):
    template = "preproc/chart.html"
    # load all the algorithms forms
    # TODO discuss a way to obtain all the form dinamically
    if request.method == "POST":
        # PreprocSettings does not exists here will have an error!!!!

        data = QueryDb(id_num)

        if request.POST['apply_downsampling'] == "on":
            data = tools.downsampling(data, request.POST['FS_NEW'])

        if request.POST['apply_smooth'] == "on":
            data = filters.smoothGaussian(data, request.POST['sigma'])

        if request.POST['apply_alg_filter'] == "on":
            data = filters.filterSignal(data, request.POST['passFr'], request.POST['stopFr'], request.POST['LOSS'],
                                        request.POST['ATTENUATION'], request.POST['filterType'])

        if request.POST['apply_spike'] == "on":
            data = GSR.remove_spikes(data, request.POST['TH'])

        if alg_type == "GSR":
            pre_data = GSR.estimate_drivers(data, request.POST['T1'], request.POST['T2'], request.POST['MX'],
                                            request.POST['DELTA_PEAK'], request.POST['k_near'],
                                            request.POST['grid_size'],
                                            request.POST['s'])
        elif alg_type == "EKG":
            peaks = IBI.getPeaksIBI(data, request.POST['delta'])
            pre_data = IBI.max2interval(peaks, request.POST['minFr'], request.POST['maxFr'])

        elif alg_type == "BVP":
            peaks = IBI.getPeaksIBI(data, request.POST['delta'])
            pre_data = IBI.max2interval(peaks, request.POST['minFr'], request.POST['maxFr'])

        elif alg_type == "inertial":
            pre_data = inertial.convert_units(data, request.POST['coeff'])

        print pre_data

        return HttpResponseRedirect(reverse('user_upload'))
    else:
        formFilt, formDown, formPick, formSpec, formGau, alg_select = None, None, None, None, None, None
        if alg_type == "":
            res = searchInDesc(id_num)
            if res:
                return HttpResponseRedirect(reverse('chart_show', kwargs={'id_num': id_num, 'alg_type': res}))
            else:
                alg_select = ["BVP", "EKG", "inertial", "GSR"]
                existVar = False
        elif alg_type == "BVP":
            formDown = downsampling(initial={'apply_filter': False})
            formGau = smoothGaussian(initial={'sigma': 2, 'apply_filter': False})
            formFilt = filterAlg(
                initial={'passFr': 2, 'stopFr': 6, 'LOSS': 0.1, 'ATTENUATION': 40, 'filterType': 'cheby2',
                         'apply_filter': True})
            formSpec = BVP_Form(initial={'delta': 1, 'minFr': 40, 'maxFr': 200})
            existVar = True
        elif alg_type == "EKG":
            formDown = downsampling(initial={'apply_filter': False})
            formGau = smoothGaussian(initial={'sigma': 2, 'apply_filter': False})
            formFilt = filterAlg(initial={'filterType': 'none', 'apply_filter': False})
            formSpec = EKG_Form(initial={'delta': 0.2, 'minFr': 40, 'maxFr': 200})
            existVar = True
        elif alg_type == "inertial":
            formDown = downsampling(initial={'apply_filter': False})
            formGau = smoothGaussian(initial={'sigma': 2, 'apply_filter': False})
            formFilt = filterAlg(initial={'filterType': 'none', 'apply_filter': False})
            formSpec = Inertial_Form()
            existVar = True
        elif alg_type == "GSR":
            formPick = remove_spike(initial={'apply_filter': False})
            formDown = downsampling(initial={'apply_filter': False})
            formGau = smoothGaussian(initial={'sigma': 2, 'apply_filter': False})
            formFilt = filterAlg(initial={'filterType': 'none', 'apply_filter': False})
            formSpec = GSR_Form(initial={'T1': 0.75, 'T2': 2, 'MX': 1, 'DELTA_PEAK': 0.02, 'k_near': 5, 'grid_size': 5, 's': 0.2})
            existVar = True

        opt_temp = getavaliabledatavals(id_num)
        opt_list = opt_temp[1:]

        context = {'forms': {'Filter': formFilt, 'Downpass': formDown,
                             'Spike': formPick, str(alg_type) + '*': formSpec, 'Gaussian': formGau},
                   'opt_list': opt_list, 'id_num': id_num, 'alg_select': alg_select, 'show_menu':existVar}
        return render(request, template, context)


def searchInDesc(id_num):
    desc = str(Recording.objects.filter(id=id_num).values_list('description', flat=True)[0]).lower()
    found = ""
    if "bvp" in desc:
        if found == "":
            found = "BVP"
        else:
            found = False
    if "ekg" in desc:
        if found == "":
            found = "EKG"
        else:
            found = False
    if "inertial" in desc:
        if found == "":
            found = "inertial"
        else:
            found = False
    if "gsr" in desc:
        if found == "":
            found = "GSR"
        else:
            found = False
    if not found and found != "":
        return found
    else:
        return False


def getExperimentsNames():
    return Experiment.objects.values_list('name', flat=True).distinct()


def getExperimentsList():
    return Experiment.objects.values_list('id', 'name', 'token').distinct()


def select_experiment(request):
    name_list = getExperimentsNames()
    context = {'name_list': name_list}
    if request.method == 'POST':
        exp_name = request.POST.get('exp_name')
        password = request.POST.get('token')
        err_log = False
        for i in getExperimentsList():
            if exp_name == i[1] and password == i[2]:
                err_log = True
                num_exp = i[0]
        if err_log:
            return HttpResponseRedirect(reverse('record_selector', kwargs={'id_num': num_exp}))
        else:
            messages.add_message(request, messages.ERROR, 'Error wrong password')
            return render(request, 'preproc/experiments.html', context)
    else:
        return render(request, 'preproc/experiments.html', context)


def getRecordsList(experimentId):
    return Recording.objects.filter(experiment=experimentId).values_list('id', flat=True).order_by('id')


def select_record(request, id_num):
    if request.method == 'POST':
        record_id = request.POST.get('rec_name')
        return HttpResponseRedirect(reverse('chart_show', kwargs={'id_num': id_num, 'alg_type': ""}))
    else:
        name_list = getRecordsList(id_num)
        context = {'name_list': name_list}
        return render(request, 'preproc/records.html', context)


def test(request):
    ID = 10
    SAMP_F = 64

    # load data from the file
    rawdata = tools.load_raw_db(ID)

    # filter the signal
    # the user selects the parameters, with default suggested
    filterType = 'butter'
    F_PASS = 2
    F_STOP = 6
    ILOSS = 0.1
    IATT = 40
    filtered_signal = filters.filterSignal(rawdata, SAMP_F, passFr=F_PASS, stopFr=F_STOP, LOSS=ILOSS, ATTENUATION=IATT,
                                           filterType=filterType)
    # filtered_signal = rawdata

    # extraction peaks from the signal
    # the user selects the parameters, with default suggested
    delta = 1
    peaks = IBI.getPeaksIBI(filtered_signal, SAMP_F, delta)

    # calculation of the IBI
    # the user selects the parameters, with default suggested
    minFr = 40
    maxFr = 200
    ibi = IBI.max2interval(peaks[:, 0], minFr, maxFr)

    tools.putPreprocArrayintodb(ID, ibi, np.array(["timestamp", "IBI"]))

    return render(request, 'preproc/experiments.html', {'name_list': ["exp1"]})
