from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .forms import filterAlg, downsampling, BVP_Form, EKG_Form, GSR_Form, Inertial_Form, remove_spike, smoothGaussian
from PhysioWat.models import Experiment, Recording, SensorRawData
from django.contrib import messages
from .jsongen import getavaliabledatavals
from scripts.processing_scripts import tools, filters, IBI, windowing
from scripts.processing_scripts.GSR import preproc as GSR_preproc
from scripts.processing_scripts.inertial import extract_features_acc, extract_features_gyr, extract_features_mag, \
    preproc as inertial_preproc
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
    return datacsv, table.dict_keys


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
    alg_type = str(alg_type)
    mytype = ['bvp', 'ekg', 'inertial', 'gsr']
    # load all the algorithms forms
    # TODO discuss a way to obtain all the form dinamically
    if request.method == "POST":

        data, cols = QueryDb(id_num)

        # DATA TYPES in ALG TYPES:
        # 1 : BVP
        # 2 : EKG
        # 3 : inertial
        # 4 : GSR

        print request.POST

        # iterate over the data types passed with url parameters
        for data_type in alg_type:
            count = int(data_type) - 1

            try:
                if request.POST['{}-apply_downsampling'.format(mytype[count])] == "on":
                    FS_NEW = request.POST['{}-FS_NEW'.format(mytype[count])]
                    data = tools.downsampling(data, FS_NEW)
            except:
                pass

            try:
                if request.POST['{}-apply_smooth'.format(mytype[count])] == "on":
                    sigma = request.POST['{}-sigma'.format(mytype[count])]
                    data = filters.smoothGaussian(data, sigma)
            except:
                pass

            try:
                if request.POST['{}-apply_alg_filter'.format(mytype[count])] == "on":
                    passFr = request.POST['{}-passFr'.format(mytype[count])]
                    stopFr = request.POST['{}-stopFr'.format(mytype[count])]
                    LOSS = request.POST['{}-LOSS'.format(mytype[count])]
                    ATTENUATION = request.POST['{}-ATTENUATION'.format(mytype[count])]
                    filterType = request.POST['{}-filterType'.format(mytype[count])]
                    data = filters.filterSignal(data, passFr, stopFr, LOSS, ATTENUATION, filterType)
            except:
                pass

            if data_type == "4":
                try:
                    if request.POST['{}-apply_spike'.format(mytype[count])] == "on":
                        TH = request.POST['{}-TH'.format(mytype[count])]
                        data = GSR.remove_spikes(data, TH)
                except:
                    pass

            if data_type == "4":
                T1 = request.POST['{}-T1'.format(mytype[count])]
                T2 = request.POST['{}-T2'.format(mytype[count])]
                MX = request.POST['{}-MX'.format(mytype[count])]
                DELTA_PEAK = request.POST['{}-DELTA_PEAK'.format(mytype[count])]
                k_near = request.POST['{}-k_near'.format(mytype[count])]
                grid_size = request.POST['{}-grid_size'.format(mytype[count])]
                s = request.POST['{}-s'.format(mytype[count])]
                pre_data, columns_out = GSR_preproc(data, cols, T1, T2, MX, DELTA_PEAK, k_near, grid_size, s)

            if data_type == "1" or data_type == "2":
                SAMP_F = int(round(1 / (data[1, 0] - data[0, 0])))
                delta = request.POST['{}-delta'.format(mytype[count])]
                peaks = IBI.getPeaksIBI(data, SAMP_F, delta)
                minFr = request.POST['{}-minFr'.format(mytype[count])]
                maxFr = request.POST['{}-maxFr'.format(mytype[count])]
                pre_data, columns_out = IBI.max2interval(peaks, minFr, maxFr)

            # if data_type == "3":
            #     coeff = request.POST['{}-coeff'.format(mytype[count])]
            #
            #     data_type = "ACC"  # Or GYR or MAG
            #     pre_data = inertial_preproc(data, cols, data_type, coeff)

            # putPreprocArrayintodb(id_num, pre_data, columns_out)

            context = {'id_num': id_num, 'elab': 'proc'}
        return render(request, template, context)

    else:
        bvp_tmp, ekg_tmp, inertial_tmp, gsr_tmp = None, None, None, None
        if alg_type == "":
            res = searchInLabels(id_num)
            if res:
                return HttpResponseRedirect(reverse('chart_show', kwargs={'id_num': id_num, 'alg_type': int(res)}))
            else:
                messages.add_message(request, messages.ERROR, 'Error no processable data found')
        else:
            if "1" in alg_type:
                count = 0
                formDown = downsampling(initial={'apply_filter': False}, prefix=mytype[count])
                formGau = smoothGaussian(initial={'sigma': 2, 'apply_filter': False}, prefix=mytype[count])
                formFilt = filterAlg(
                    initial={'passFr': 2, 'stopFr': 6, 'LOSS': 0.1, 'ATTENUATION': 40, 'filterType': 'cheby2',
                             'apply_filter': True}, prefix=mytype[count])
                formSpec = BVP_Form(initial={'delta': 1, 'minFr': 40, 'maxFr': 200}, prefix=mytype[count])
                bvp_tmp = {'formDown': formDown, 'formGau': formGau, 'formFilt': formFilt, 'formSpec': formSpec}
            if "2" in alg_type:
                count = 1
                formDown = downsampling(initial={'apply_filter': False}, prefix=mytype[count])
                formGau = smoothGaussian(initial={'sigma': 2, 'apply_filter': False}, prefix=mytype[count])
                formFilt = filterAlg(initial={'filterType': 'none', 'apply_filter': False},
                                     prefix=mytype[count])
                formSpec = EKG_Form(initial={'delta': 0.2, 'minFr': 40, 'maxFr': 200}, prefix=mytype[count])
                ekg_tmp = {'formDown': formDown, 'formGau': formGau, 'formFilt': formFilt, 'formSpec': formSpec}
            if "3" in alg_type:
                count = 2
                formDown = downsampling(initial={'apply_filter': False}, prefix=mytype[count])
                formGau = smoothGaussian(initial={'sigma': 2, 'apply_filter': False}, prefix=mytype[count])
                formFilt = filterAlg(initial={'filterType': 'none', 'apply_filter': False},
                                     prefix=mytype[count])
                formSpec = Inertial_Form()
                inertial_tmp = {'formDown': formDown, 'formGau': formGau, 'formFilt': formFilt, 'formSpec': formSpec}
            if "4" in alg_type:
                count = 3
                formPick = remove_spike(initial={'apply_filter': False}, prefix=mytype[count])
                formDown = downsampling(initial={'apply_filter': False}, prefix=mytype[count])
                formGau = smoothGaussian(initial={'sigma': 2, 'apply_filter': False}, prefix=mytype[count])
                formFilt = filterAlg(initial={'filterType': 'none', 'apply_filter': False},
                                     prefix=mytype[count])
                formSpec = GSR_Form(
                    initial={'T1': 0.75, 'T2': 2, 'MX': 1, 'DELTA_PEAK': 0.02, 'k_near': 5, 'grid_size': 5, 's': 0.2},
                    prefix=mytype[count])
                gsr_tmp = {'formPick': formPick, 'formDown': formDown, 'formGau': formGau, 'formFilt': formFilt,
                           'formSpec': formSpec}

        opt_temp = getavaliabledatavals(id_num)
        opt_list = opt_temp[1:]

        context = {'forms': {'bvp_tmp': bvp_tmp, 'ekg_tmp': ekg_tmp, 'inertial_tmp': inertial_tmp, 'gsr_tmp': gsr_tmp},
                   'opt_list': opt_list, 'id_num': id_num, 'elab': 'raw'}
        return render(request, template, context)


def searchInLabels(id_num):
    desc = Recording.objects.filter(id=id_num).values_list('dict_keys', flat=True)[0]
    found = ""
    for i in desc:
        var = str(i).lower()
        if "bvp" in var:
            if not "1" in found:
                found += "1"
        if "ekg" in var:
            if not "2" in found:
                found += "2"
        if "acc" in var or "gyr" in var or "mag" in var:
            if not "3" in found:
                found += "3"
        if "gsr" in var:
            if not "4" in found:
                found += "4"
    if found != "":
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
def getRecordsListDesc(experimentId):
    return Recording.objects.filter(experiment=experimentId).values_list('description', flat=True)


def select_record(request, id_num):
    if request.method == 'POST':
        record_id = request.POST.get('rec_name')
        return HttpResponseRedirect(reverse('chart_show', kwargs={'id_num': record_id, 'alg_type': ""}))
    else:
        name_list = getRecordsList(id_num)
        desc_list = getRecordsListDesc(id_num)
        d = dict(zip(name_list, desc_list))
        context = {'dict': d}
        return render(request, 'preproc/records.html', context)


def test(request):
    ID = 1
    funcs_par=dict()
    sensAccCoeff=8*9.81/32768
    sensGyrCoeff=2000/32768
    sensMagCoeff=0.007629

    data, columns_in = tools.load_raw_db(ID)

    # t=tools.selectCol(data, columns_in, "TIME")
    #
    # try:
    #     lab=tools.selectCol(data, columns_in, "LAB")
    # except IndexError as e:
    #     print e
    #     lab=np.zeros(t.shape[0])
    #     pass

    data_out, columns_out=inertial_preproc(data, columns_in, sensAccCoeff, sensGyrCoeff, sensMagCoeff)
    funcs_par.update({"inertial.preproc": {"coeffAcc":str(sensAccCoeff), "coeffGyr":str(sensGyrCoeff), "coeffMag":str(sensMagCoeff)}})

    tools.putPreprocArrayintodb(ID, data_out, np.array(columns_out), funcs_par.keys(), funcs_par.values() )

    return render(request, 'preproc/experiments.html', {'name_list': ["exp1"]})

def test2(request):
    ID = 1
    preproc_data=tools.load_preproc_db(ID)

    return render(request, 'preproc/experiments.html', {'name_list': ["exp1"]})
