from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .forms import filterAlg, downsampling, BVP_Form, EKG_Form, GSR_Form, Inertial_Form, remove_spike, smoothGaussian
from PhysioWat.models import Experiment, Recording, SensorRawData, Preprocessed_Recording, Preprocessed_Data
from django.db.models import Max
from django.contrib import messages
from .jsongen import getavaliabledatavals
from scripts.processing_scripts import tools, filters, IBI, windowing
from scripts.processing_scripts.tools import selectCol as selcol
from scripts.processing_scripts.GSR import remove_spikes, preproc as GSR_preproc
from scripts.processing_scripts.inertial import extract_features_acc, extract_features_gyr, extract_features_mag, \
    preproc as inertial_preproc
import numpy as np
from StringIO import StringIO
import csv


def QueryDb(recordingID):
    table = Recording.objects.get(id=recordingID)
    data = SensorRawData.objects.filter(recording_id=recordingID).order_by('id')

    retarray = np.zeros((len(data), len(table.dict_keys)))
    mykeys = data[0].store.keys()
    # [j for i in bb for j,z in enumerate(cc) if z == i]

    for i in xrange(len(data)):
        retarray[i] = [float(j) for j in data[i].store.values()]
    retarray.astype(float)

    return retarray, mykeys


def putPreprocArrayintodb(rec_id, preProcArray, preProcLabel, applied_preproc_funcs_names,
                          preproc_funcs_parameters, signal_type_name, bid=None):
    # Andrew's method to convert array to CSV string???
    # csvasstring = ",".join(preProcLabel) + '\n'
    # for dataarr in preProcArray:
    #     for dataval in dataarr:
    #         csvasstring += str(dataval) + ','
    #     csvasstring = csvasstring[:-1]
    #     csvasstring += '\n'
    #
    # # Initiate the CSV Reader
    # csvreader = csv.reader(StringIO(csvasstring), delimiter=',')
    # dictky = csvreader.next()

    if not bid:
        try:
            new_batch_id = Preprocessed_Recording.objects.all().aggregate(Max('batch_id'))['batch_id__max'] + 1
        except TypeError:  # None + 1 ?
            new_batch_id = 1
    else:
        new_batch_id = bid

    dictky = [str(i) for i in preProcLabel]
    # Submit data to model and thus the database table
    print "creating preprocessed recording", rec_id
    pr = Preprocessed_Recording(recording_id=rec_id, applied_preproc_funcs_names=applied_preproc_funcs_names,
                                preproc_funcs_parameters=preproc_funcs_parameters, dict_keys=dictky,
                                batch_id=new_batch_id, signal_type_name=signal_type_name)

    pr.save()
    values = preProcArray.astype(str)
    # print "pr.id", pr.id
    id_gen = xrange(len(preProcArray))
    record_list = [None for i in id_gen]
    for i in id_gen:
        record_list[i] = Preprocessed_Data(pp_recording_id=pr.id, store=dict(zip(dictky, values[i])))

    Preprocessed_Data.objects.bulk_create(record_list, batch_size=32768)
    return new_batch_id


def show_chart(request, id_num, alg_type=""):
    template = "preproc/chart.html"
    alg_type = str(alg_type)
    mytype = ['bvp', 'ekg', 'inertial', 'gsr']
    # load all the algorithms forms
    # TODO discuss a way to obtain all the form dinamically
    ret_bid = None
    if request.method == "POST":
        print request.POST
        print "GETTING DATA"
        raw_data, cols_in = QueryDb(id_num)
        print "RAW_DATA ACQUIRED: type", type(raw_data), raw_data.dtype

        # DATA TYPES in ALG TYPES:
        # 1 : BVP
        # 2 : EKG
        # 3 : inertial
        # 4 : GSR

        # iterate over the data types passed with url parameters
        for data_type in alg_type:
            count = int(data_type) - 1
            print "PROCESSING DATA", mytype[count]

            try:
                lab = selcol(raw_data, cols_in, "LAB")
            except IndexError as e:
                print e.message
                lab = np.zeros(raw_data.shape[0])

            if data_type == "1":  # BVP
                bvp = selcol(raw_data, cols_in, "BVP")
                time = selcol(raw_data, cols_in, "TIME")
                data = np.column_stack((time, bvp))
                cols = ["TIME", "BVP"]

            elif data_type == "2":  # EKG
                ekg = selcol(raw_data, cols_in, "EKG")
                time = selcol(raw_data, cols_in, "TIME")
                data = np.column_stack((time, ekg))
                cols = ["TIME", "EKG"]

            elif data_type == "3":  # Inertial
                col_acc = ["ACCX", "ACCY", "ACCZ"]
                col_gyr = ["GYRX", "GYRY", "GYRZ"]
                col_mag = ["MAGX", "MAGY", "MAGZ"]
                keep_col = []

                try:
                    acc = selcol(raw_data, cols_in, col_acc)
                    keep_col += col_acc
                    thereIsAcc = True
                except IndexError as e:
                    print "NO ACC:" + e.message
                    thereIsAcc = False

                try:
                    gyr = selcol(raw_data, cols_in, col_gyr)
                    keep_col += col_gyr
                    thereIsGyr = True
                except IndexError as e:
                    print "NO GYR:" + e.message
                    thereIsGyr = False

                try:
                    mag = selcol(raw_data, cols_in, col_mag)
                    keep_col += col_mag
                    thereIsMag = True
                except IndexError as e:
                    print "NO MAG:" + e.message
                    thereIsMag = False

                data = selcol(raw_data, cols_in, "TIME")
                if thereIsAcc:
                    data = np.column_stack((data, acc))
                if thereIsGyr:
                    data = np.column_stack((data, gyr))
                if thereIsMag:
                    data = np.column_stack((data, mag))

                cols = ["TIME"] + keep_col

            elif data_type == "4":  # GSR
                gsr = selcol(raw_data, cols_in, "GSR")
                time = selcol(raw_data, cols_in, "TIME")
                data = np.column_stack((time, gsr))
                cols = ["TIME", "GSR"]

            funcs_par = {}

            try:
                if request.POST.get('{}-apply_downsampling'.format(mytype[count]), '') == "on":
                    print "DOWNSAMPLING"
                    FS_NEW = float(request.POST['{}-FS_NEW'.format(mytype[count])])
                    data_labelled = np.column_stack((data, lab))
                    cols_labelled = cols + ["LAB"]
                    data_labelled = tools.downsampling(data_labelled, FS_NEW)
                    lab = selcol(data_labelled, cols_labelled, "LAB")
                    data = selcol(data_labelled, cols_labelled, cols)
                    funcs_par.update({"tools.downsampling": {"FS_NEW": str(FS_NEW)}})
            except ValueError as e:
                print "ERROR DOWNSAMPLING"
                print e.message
                messages.error(request, "Downsampling errorret_bid: " + e.message)
            except Exception as e:
                print "ERROR DOWNSAMPLING"
                print e.message
                messages.error(request, "Downsampling error in %s, proceeding without applying." % (mytype[count]))

            try:
                if request.POST.get('{}-apply_smooth'.format(mytype[count]), '') == "on":
                    print "SMOOTHING"
                    sigma = float(request.POST['{}-sigma'.format(mytype[count])])
                    t = selcol(data, cols, "TIME")
                    data_col = cols[:]
                    data_col.remove("TIME")
                    data_only = selcol(data, cols, data_col)
                    for i in range(data_only.shape[1]):
                        data_only[:, i] = filters.smoothGaussian(data_only[:, 1], sigma)
                    data = np.column_stack((t, data_only))
                    funcs_par.update({"filters.smoothGaussian": {"sigma": str(sigma)}})

            except Exception as e:
                print "ERROR SMOOTH GAUSSIAN"
                print e.message
                messages.error(request, "Gaussian smoothing error in %s, proceeding without applying." %(mytype[count]))

            try:
                if request.POST.get('{}-apply_alg_filter'.format(mytype[count]), '') == "on":
                    print "FILTERING"
                    passFr = float(request.POST['{}-passFr'.format(mytype[count])])
                    stopFr = float(request.POST['{}-stopFr'.format(mytype[count])])
                    LOSS = float(request.POST['{}-LOSS'.format(mytype[count])])
                    ATTENUATION = float(request.POST['{}-ATTENUATION'.format(mytype[count])])
                    filterType = str(request.POST['{}-filterType'.format(mytype[count])])
                    data = filters.filterSignal(data, passFr, stopFr, LOSS, ATTENUATION, filterType)
                    funcs_par.update({"filters.filterSignal": {"passFr": str(passFr), "stopFr": str(stopFr),
                                                               "LOSS": str(LOSS), "ATTENUATION": str(ATTENUATION),
                                                               "filterType": str(filterType)}})

            except Exception as e:
                print "ERROR FILTER"
                print e.message
                messages.error(request, "Filtering error in %s, proceeding without applying." % (mytype[count]))

            print "START SPECIFIC PROCESSING"

            if data_type == "4":
                try:
                    if request.POST.get('{}-apply_spike'.format(mytype[count]), '') == "on":
                        print "REMOVING SPIKES"
                        TH = float(request.POST['{}-TH'.format(mytype[count])])
                        data_col = cols[:]
                        data_col.remove("TIME")
                        data_only = selcol(data, cols, data_col)
                        t, data_only = remove_spikes(data_only, sigma)
                        data = np.column_stack((t, data_only))
                        funcs_par.update({"GSR.remove_spikes": {"TH": str(TH)}})

                except Exception as e:
                    print "ERROR SPIKES"
                    print e.message
                    messages.error(request, "Removing spikes error in %s, proceeding without applying." % (mytype[count]))

            try:
                if data_type == "4":
                    T1 = float(request.POST['{}-T1'.format(mytype[count])])
                    T2 = float(request.POST['{}-T2'.format(mytype[count])])
                    MX = float(request.POST['{}-MX'.format(mytype[count])])
                    DELTA_PEAK = float(request.POST['{}-DELTA_PEAK'.format(mytype[count])])
                    k_near = float(request.POST['{}-k_near'.format(mytype[count])])
                    grid_size = float(request.POST['{}-grid_size'.format(mytype[count])])
                    s = float(request.POST['{}-s'.format(mytype[count])])
                    data_labelled = np.column_stack((data, lab))
                    cols_labelled = cols + ["LAB"]
                    pre_data, columns_out = GSR_preproc(data_labelled, cols_labelled, T1, T2, MX, DELTA_PEAK, k_near,
                                                        grid_size, s)
                    funcs_par.update({"GSR.preproc": {"T1": str(T1), "T2": str(T2), "MX": str(MX),
                                                      "DELTA_PEAK": str(DELTA_PEAK), "k_near": str(k_near),
                                                      "grid_size": str(grid_size), "s": str(s)}})

                if data_type == "1" or data_type == "2":
                    t = selcol(data, cols, "TIME")
                    delta = float(request.POST['{}-delta'.format(mytype[count])])
                    data_labelled = np.column_stack((data, lab))
                    cols_labelled = cols + ["LAB"]
                    peaks, cols_temp = IBI.getPeaksIBI(data_labelled, cols_labelled, delta, mytype[count])
                    minFr = float(request.POST['{}-minFr'.format(mytype[count])])
                    maxFr = float(request.POST['{}-maxFr'.format(mytype[count])])
                    pre_data, columns_out = IBI.max2interval(peaks, cols_temp, minFr, maxFr)
                    funcs_par.update({"IBI.getPeaksIBI": {"delta": str(delta)}})
                    funcs_par.update({"IBI.max2intervals": {"minFr": str(minFr), "maxFr": str(maxFr)}})

                if data_type == "3":
                    coeffAcc = float(request.POST['{}-coeffAcc'.format(mytype[count])])
                    coeffGyr = float(request.POST['{}-coeffGyr'.format(mytype[count])])
                    coeffMag = float(request.POST['{}-coeffMag'.format(mytype[count])])
                    data_labelled = np.column_stack((data, lab))
                    cols_labelled = cols + ["LAB"]
                    pre_data, columns_out = inertial_preproc(data_labelled, cols_labelled, coeffAcc, coeffGyr, coeffMag)
                    funcs_par.update({"inertial.preproc": {"coeffAcc": str(coeffAcc), "coeffGyr": str(coeffGyr),
                                                           "coeffMag": str(coeffMag)}})

                print "FINISHED SPECIFIC PROCESSING"
                print "id_num", id_num
                ret_bid = putPreprocArrayintodb(id_num, pre_data, columns_out, funcs_par.keys(), funcs_par.values(),
                                                mytype[int(data_type) - 1], ret_bid)
                print "FINISHED PUTTING IN DB"

            except Exception as e:
                print "CANNOT PREPROCESS!!!", e.message
                messages.error(request, 'Cannot process ' + mytype[count] + '! Review your parameters.')

            # print "pr_id", pr_id
            context = {'id_num': id_num, 'elab': 'proc', 'batch_id': ret_bid}
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
                formDown = downsampling(initial={'apply_downsampling': False}, prefix=mytype[count])
                formGau = smoothGaussian(initial={'sigma': 2, 'apply_smooth': False}, prefix=mytype[count])
                formFilt = filterAlg(
                    initial={'passFr': 2, 'stopFr': 6, 'LOSS': 0.1, 'ATTENUATION': 40, 'filterType': 'cheby2',
                             'apply_alg_filter': True}, prefix=mytype[count])
                formSpec = BVP_Form(initial={'delta': 1, 'minFr': 40, 'maxFr': 200}, prefix=mytype[count])
                bvp_tmp = {'Downsampling': formDown, 'Gaussian': formGau, 'Filter': formFilt, 'Specfic': formSpec}
            if "2" in alg_type:
                count = 1
                formDown = downsampling(initial={'apply_downsampling': False}, prefix=mytype[count])
                formGau = smoothGaussian(initial={'sigma': 2, 'apply_smooth': False}, prefix=mytype[count])
                formFilt = filterAlg(initial={'filterType': 'none', 'apply_filter': False},
                                     prefix=mytype[count])
                formSpec = EKG_Form(initial={'delta': 0.2, 'minFr': 40, 'maxFr': 200}, prefix=mytype[count])
                ekg_tmp = {'Downsampling': formDown, 'Gaussian': formGau, 'Filter': formFilt, 'Specific': formSpec}
            if "3" in alg_type:
                count = 2
                formDown = downsampling(initial={'apply_downsampling': False}, prefix=mytype[count])
                formGau = smoothGaussian(initial={'sigma': 2, 'apply_smooth': False}, prefix=mytype[count])
                formFilt = filterAlg(initial={'filterType': 'none', 'apply_filter': False},
                                     prefix=mytype[count])
                formSpec = Inertial_Form(initial={'coeffAcc': 1, 'coeffGyr': 1, 'coeffMag': 1},
                                         prefix=mytype[count])  ##
                inertial_tmp = {'Downsampling': formDown, 'Gaussian': formGau, 'Filter': formFilt, 'Specific': formSpec}
            if "4" in alg_type:
                count = 3
                formPeak = remove_spike(initial={'apply_spike': False}, prefix=mytype[count])
                formDown = downsampling(initial={'apply_downsampling': False}, prefix=mytype[count])
                formGau = smoothGaussian(initial={'sigma': 2, 'apply_smooth': False}, prefix=mytype[count])
                formFilt = filterAlg(initial={'filterType': 'none', 'apply_filter': False},
                                     prefix=mytype[count])
                formSpec = GSR_Form(
                    initial={'T1': 0.75, 'T2': 2, 'MX': 1, 'DELTA_PEAK': 0.02, 'k_near': 5, 'grid_size': 5, 's': 0.2},
                    prefix=mytype[count])
                gsr_tmp = {'Peak': formPeak, 'Downsampling': formDown, 'Gaussian': formGau, 'Filter': formFilt,
                           'Specific': formSpec}

        opt_temp = getavaliabledatavals(id_num)
        opt_list = opt_temp[1:]

        context = {'forms': {'BVP': bvp_tmp, 'EKG': ekg_tmp, 'Inertial': inertial_tmp, 'GSR': gsr_tmp},
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
    return Recording.objects.filter(experiment=experimentId).values_list('id', 'device_name', 'description',
                                                                         'dict_keys', 'ts').order_by('id')


def select_record(request, id_num):
    if request.method == 'POST':
        record_id = request.POST.get('rec_name')
        return HttpResponseRedirect(reverse('chart_show', kwargs={'id_num': record_id, 'alg_type': ""}))
    else:
        name_list = getRecordsList(id_num)
        context = {'name_list': name_list}
        return render(request, 'preproc/records.html', context)
