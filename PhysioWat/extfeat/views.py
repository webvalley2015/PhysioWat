import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from scipy.stats import itemfreq
from .forms import windowing, viewFeatures, FeatPar, TestParam, AlgChoose, AlgParam, SvmParam, KNearParam, DecTreeParam, \
    signal_choose, RndForParam, AdaBoostParam, LatDirAssParam, autoFitParam, id_choose
from preproc.scripts.processing_scripts import windowing as wd, feat_script as ft
from preproc.scripts.processing_scripts.GSR import extract_features as extfeat_GSR
from preproc.scripts.processing_scripts.IBI import extract_IBI_features as extfeat_IBI
from preproc.scripts.processing_scripts.inertial import extract_features_acc as extfeat_ACC, \
    extract_features_mag as extfeat_MAG, extract_features_gyr as extfeat_GYR
from preproc.scripts.processing_scripts.tools import selectCol as selcol, dict_to_arrays, array_labels_to_csv as toCsv
from django.contrib import messages
from PhysioWat.models import Experiment, Recording, Preprocessed_Recording, Preprocessed_Data
import numpy as np
from PhysioWat.settings import MEDIA_ROOT, BASE_DIR
from time import time as get_timestamp
from preproc.scripts.processing_scripts import pddbload
import datetime
import pandas as pd
from PhysioWat.models import Experiment, Preprocessed_Recording, Preprocessed_Data, FeatExtractedData
from preproc.graphs import linegraph2, heatmap, linegraph3
from django.core.servers.basehttp import FileWrapper
import mimetypes
import os


def get_signal_type(cols):
    if 'PHA' in cols:  # GSR
        type_sig = "GSR"
    elif 'ACCX' in cols or 'GYRX' in cols or 'MAGX' in cols:
        type_sig = "inertial"
    elif "IBI" in cols:
        type_sig = "IBI"
    return type_sig


def form_select_signal(id_record):
    signal_list = Preprocessed_Recording.objects.filter(recording_id=id_record).values_list('id', 'dict_keys').order_by(
        'id')
    checkbox_in = []
    for ID, cols in signal_list:
        count = Preprocessed_Data.objects.filter(pp_recording_id=ID).count()
        if (count > 0):
            type_sig = get_signal_type(cols)
            checkbox_in.append((ID, str(ID) + " - " + " " + str(type_sig)))
    form_sel_id = signal_choose(choices=checkbox_in)
    return form_sel_id


def QueryDb(recordingID):  # JUST COPY, PASTE AND CHANGED RECORDS
    table = Preprocessed_Recording.objects.get(id=recordingID)
    data = Preprocessed_Data.objects.filter(pp_recording_id=recordingID).order_by('id')

    retarray = np.zeros((len(data), len(table.dict_keys)))
    mykeys = data[0].store.keys()
    # [j for i in bb for j,z in enumerate(cc) if z == i]

    for i in xrange(len(data)):
        retarray[i] = [float(j) for j in data[i].store.values()]
    retarray.astype(float)

    return retarray, mykeys


def WritePathtoDB(fname, pp_rec_id, parameters=None):
    print "ID ", pp_rec_id
    print "FNAME ", fname
    print "PAR ", parameters
    record = FeatExtractedData(pp_recording_id=pp_rec_id, path_to_file=fname, parameters=parameters)
    record.save()
    return record.id


def getAlgorithm(request, id_record):  # ADD THE TYPE ODF THE SIGNAL ALSO IN URLS!!!

    # read parameters from url
    # get data type list
    allow_ml = False
    id_file = -1

    if request.method == 'POST':
        mydict = dict(request.POST.iterlists())
        # if 'choose_signal' in mydict:
        # print request.POST
        print id_record
        type_sig = ''
        id_num = id_record
        try:
            print "RUNNING FOR ", id_num
            data, cols = QueryDb(id_num)
            # print cols
            time = selcol(data, cols, "TIME")
            labs = selcol(data, cols, "LAB")
            type_sig = get_signal_type(cols)
            # print type_sig
            params = dict()

            if (mydict['type'][0] == 'contigous'):
                windows, winlab = wd.get_windows_contiguos(time, labs, float(mydict['length'][0]),
                                                           float(mydict['step'][0]))

            if (mydict['type'][0] == 'no_mix'):  # for the values, make reference to .forms --> windowing.!!!!
                windows, winlab = wd.get_windows_no_mix(time, labs, float(mydict['length'][0]),
                                                        float(mydict['step'][0]))

            if (mydict['type'][0] == 'full_label'):
                windows, winlab = wd.get_windows_full_label(time, labs)
            params.update({"windowing.type": str(mydict["type"][0]), "windowing.length": str(mydict["length"][0]),
                           "windowing.step": str(mydict["step"][0])})
            # extract features from result
            # store feats. in the db
            params.update({"signal_type": type_sig})
            if type_sig == "GSR":  # GSR
                data_in = selcol(data, cols, "PHA")
                funcs, pars = list(
                    Preprocessed_Recording.objects.filter(pk=id_num).values_list('applied_preproc_funcs_names',
                                                                                 'preproc_funcs_parameters'))[0]
                DELTA = float(pars[funcs.index(u"GSR.preproc")][u"DELTA_PEAK"])
                feat_dict = extfeat_GSR(data_in, time, DELTA, windows)
                data_out, cols_out = dict_to_arrays(feat_dict)
                data_out = np.column_stack((data_out, winlab))
                columns_out = np.r_[cols_out, ["LAB"]]

            elif type_sig == "inertial":
                col_acc = ["ACCX", "ACCY", "ACCZ"]
                col_gyr = ["GYRX", "GYRY", "GYRZ"]
                col_mag = ["MAGX", "MAGY", "MAGZ"]
                try:
                    acc = selcol(data, cols, col_acc)
                    thereIsAcc = True
                except IndexError as e:
                    print e
                    thereIsAcc = False
                try:
                    gyr = selcol(data, cols, col_gyr)
                    thereIsGyr = True
                except IndexError as e:
                    print e
                    thereIsGyr = False
                try:
                    mag = selcol(data, cols, col_mag)
                    thereIsMag = True
                except IndexError as e:
                    print e
                    thereIsMag = False
                columns_out = np.array(["LAB"])
                data_out = winlab[:]
                if thereIsAcc:
                    feats_acc, fcol_acc = extfeat_ACC(acc, time, col_acc, windows)
                    data_out = np.column_stack([feats_acc, data_out])
                    columns_out = np.r_[fcol_acc, columns_out]
                if thereIsGyr:
                    feats_gyr, fcol_gyr = extfeat_GYR(gyr, time, col_gyr, windows)
                    data_out = np.column_stack([feats_gyr, data_out])
                    columns_out = np.r_[fcol_gyr, columns_out]
                if thereIsMag:
                    feats_mag, fcol_mag = extfeat_MAG(mag, time, col_mag, windows)
                    data_out = np.column_stack([feats_mag, data_out])
                    columns_out = np.r_[fcol_mag, columns_out]

            elif type_sig == "IBI":
                data_in = selcol(data, cols, ["TIME", "IBI"])
                cols_in = ["TIME", "IBI"]
                data_out, winlab = extfeat_IBI(data_in, cols_in, windows, winlab)
                columns_out = np.array(['RRmean', 'RRSTD', 'pNN50', 'pNN25', 'pNN10', 'RMSSD', 'SDSD'])
                # print data_out.shape, winlab.shape
                data_out = np.column_stack((data_out, winlab))
                columns_out = np.r_[columns_out, ["LAB"]]

            st = datetime.datetime.fromtimestamp(get_timestamp()).strftime('%Y%m%d_%H%M%S')
            fname = MEDIA_ROOT + type_sig + "_" + id_num + "_" + st + ".csv"
            # print(fname)
            toCsv(data_out, columns_out, fname)
            id_file = WritePathtoDB(fname, id_num, params)
            success = True

            # check distinct label
            print "COLUMNS", columns_out, type(columns_out), np.where(columns_out == "LAB")[0]
            allow_ml = False if len(np.unique(data_out[:, np.where(columns_out == "LAB")])) == 1 else True

        except Exception as e:
            print "COULD NOT PROCESS " + id_num + ": " + e.message
            if type_sig is not None:
                messages.error(request,
                               "Error processing " + id_num + " (" + type_sig + "). Review your parameters! It will not be saved.")
            else:
                messages.error(request, "Error processing. Review your parameters! It will not be saved.")
            success = False
            # else:
            #    success=False
            #    messages.error(request, "Choose at least one preprocessed signal")
    else:
        success = False

    form = windowing()
    # form_signal = form_select_signal(id_record)
    template = "extfeat/choose_alg.html"
    # print urlTmp['id_num']

    context = {'form': form, 'id_record': id_record, 'success': success, 'allow_ml': allow_ml, 'id_file': id_file}
    return render(request, template, context)


def ml_input(request, id_record):  # obviously, it has to be added id record and everything concerning db
    if (request.method == 'POST'):

        # print "culoculoculoculo"  # GET THE POST, ELABORATE AND GO TO THE DB OR THE PLOT
        # print request.POST
        mydict = dict(request.POST.iterlists())
        # for key in request.POST.iterkeys():  # "for key in request.GET" works too.
        #     # Add filtering logic here.
        #
        #     print key, request.POST.getlist(key)

        print mydict
        # print '-' * 60
        # localdir = '/home/emanuele/wv_physio/PhysioWat/PhysioWat/preproc/scripts/processing_scripts/output/'
        # input_data = pd.DataFrame.from_csv(path=localdir + 'feat_claire_labeled.csv')  # , index_col=None, sep=','
        exprecid = mydict['choose_id']
        print exprecid
        input_data = pddbload.load_file_pd_db(int(exprecid[0]))
        num_feat = -1  # set to -1 because of
        print 'Ciao'
        print input_data.shape
        print 'hola'
        percentage = mydict['test_percentage'][0]
        percentage = float(percentage) / 100.0

        num_iteration = mydict['number_of_iterations'][0]
        ft.iterations = int(num_iteration)
        algorithm = mydict['alg_choice'][0]
        flag = True

        flag_has_selected_auto_feat = False
        list_of_feat = None
        best_feat_n_mat = []
        num_feat = -1
        auto_alg_result_mat = None
        best_feat_json = None

        if 'viewf' in mydict:
            print "hellp"
            if 'norm' in mydict['viewf']:
                input_data = ft.normalize(input_data)
                print input_data.shape
            train_data, test_data = ft.split(input_data, percentage)
            print train_data.shape, test_data.shape
            flag = False

            if 'sel' in mydict['viewf']:
                # print "i have selected the first stuff!"
                if 'k_selected' in mydict['FeatChoose']:
                    num_feat = int(mydict['feat_num'][0])
                    if (num_feat <= 0):
                        return render(request, "machine_learning/form_error.html")
                    train_data, test_data, list_of_feat = ft.getfeatnumber(train_data, test_data,
                                                                           num_feat)  # RETURNS 2 SUBSET DF GIVEN IN INPUT THE TRAIN DATA, THE TEST DATA, AND THE NUMBER OF FEATS

                if ('k_auto' in mydict['FeatChoose']):
                    print "hi"
                    train_data, test_data, best_feat_n_mat, list_of_feat = ft.bestfeatn(train_data, test_data)
                    flag_has_selected_auto_feat = True
                    list_of_feat = list_of_feat[4]

        if (flag == True):
            train_data, test_data = ft.split(input_data, percentage)
            flag = False

        if (algorithm == 'ALL') and ('auto' not in mydict['parameter_choice']):
            return render(request, "machine_learning/form_error.html")

        if 'def' in mydict['parameter_choice']:
            clf, score, error = ft.quick_crossvalidate(train_data, alg=algorithm)

        if 'pers' in mydict['parameter_choice']:

            if (algorithm == 'KNN'):
                k_neighbour = mydict['k_neighbour'][0]
                print(k_neighbour)
                clf, score, error = ft.pers_crossvalidation1(train_data, algorithm, k_neighbour)
            if (algorithm == 'DCT'):
                max_features = mydict['max_features'][0]
                clf, score, error = ft.pers_crossvalidation1(train_data, algorithm, max_features)
            if (algorithm == 'SVM'):
                kernel = mydict['kernel']
                C = mydict['C']
                clf, score, error = ft.pers_crossvalidation2(train_data, algorithm, kernel, C)
            if (algorithm == 'RFC'):
                max_features = mydict['max_features']
                number_estimators = mydict['number_estimators']
                clf, score, error = ft.pers_crossvalidation2(train_data, algorithm, max_features, number_estimators)
            if (algorithm == 'ADA'):
                number_estimators = mydict['number_estimators']
                learning_rate = mydict['learning_rate']
                clf, score, error = ft.pers_crossvalidation2(train_data, algorithm, number_estimators, learning_rate)
            if (algorithm == 'LDA'):
                solver = mydict['solver']
                clf, score, error = ft.pers_crossvalidation1(train_data, algorithm, solver)

        if 'auto' in mydict['parameter_choice']:
            metrics = mydict['maximize'][0]
            # print  metrics
            if (algorithm == 'ALL'):
                clf, auto_alg_result_mat = ft.bestAlg(train_data, metrics)
            else:
                clf, loc_metric, loc_error, loc_mat = ft.bestfit(train_data, algorithm, metrics)

        dic_metric, conf_mat = ft.test_learning(clf, test_data)

        # print dic_metric, conf_mat
        # print  best_feat_n_mat

        # print "BEST FEAT NUMBER: PRECISION IN FUNFCION OF THE UMBER", type(best_feat_n_mat), best_feat_n_mat
        # print "CONFUSION MATRIX" ,conf_mat
        # print "DICTIONARY OF THE METRICS", dic_metric


        best_feat_json = best_feat_n_mat  # see if it's needed
        # categories = #PICK ALGORITHM CATEGORIES
        if best_feat_n_mat != []:
            s = linegraph3()
            best_feat_json = s.get_data(data_tmp=best_feat_n_mat.tolist())  # xcategories = categories)
            best_feat_json = json.dumps(best_feat_json)
            print "LA MATRICE DELLE FEATURES, CHE SUL TEMPLATE FUNZIONA  ", best_feat_json

        # PART OF THE BEST ALGORITHM
        if auto_alg_result_mat != None:
            s = linegraph3()
            auto_alg_result_mat = list(np.array(auto_alg_result_mat[:, 1:]))
            algorithm_categories = ['KNN', 'SVM', 'DCT', 'RND', 'ADA', 'QDA', 'LDA']  # TODO PEDOT FUNCTION!!!!
            auto_alg_result_mat = s.get_data(data_tmp=auto_alg_result_mat, xcategories=algorithm_categories,
                                             tipo="errorbar", title="precision of the various algorithms")
            auto_alg_result_mat = json.dumps(auto_alg_result_mat)

        # PART OF THE METRICS VALUE!!!

        dict_sigla_parola = {'ACC': 'accuracy %',
                             'F1M': 'F-Test macro',
                             'F1m': 'F-Test micro',
                             'F1W': 'F-Test weighted',
                             'WHM': 'Weighted Harmonic Mean of precision and recall',
                             'PRM': 'Precision Score Macro',
                             'PRm': 'Precision Score Micro',
                             'PRW': 'Precision Score Weighted',
                             'REM': 'Recall Score Macro',
                             'REm': 'Recall Score Micro',
                             'REW': 'Recall Score Weighted'}

        print "dizionario -------", dic_metric
        s = linegraph3()
        xcate = []
        for i in dic_metric.keys():
            xcate.append(dict_sigla_parola[i])
        metrics = s.get_data(data_tmp=dic_metric.values(), title="metrics accuracy", tipo="scatter", xcategories=xcate)
        metrics = json.dumps(metrics)
        print "metriche --->", metrics  # todo delete line
        # PART OF THE CONFUSION MATRIX
        h = heatmap()
        # conf_mat = conf_mat.tolist() #!!!important
        conf_data = h.get_data(conf_mat)
        conf_data = json.dumps(conf_data)

        context = {'auto_alg_result_mat': auto_alg_result_mat,  # boxplot with the algorithms cosres
                   'conf_mat': conf_data,
                   'metrics': metrics,
                   'list_of_feat': list_of_feat,
                   # second part, with the list of features and the function score vs nfeat
                   'best_feat_scores': best_feat_n_mat,
                   }

        if best_feat_n_mat != []:
            best_feat_n_mat[:, 1] *= 100.0
        # best_feat_n_mat = best_feat_n_mat.tolist() #LIST: CONTAINS THE PRECISION IN FUNCTIONM OF THE NUMBER OF FEATURES


        # TODO check the 'matrix for'
        # todo best n feat NAMES?
        if list_of_feat:
            list_of_feat = [i.replace('_', ' ') for i in list_of_feat]
        template = "machine_learning/results.html"
        # context = {'conf_mat': conf_data,
        #            'dic_result':dic_metric,  # essential part, the last one (conf.matrix)
        #            'list_of_feat': list_of_feat,     #second part, with the list of features and the function score vs nfeat
        #            'best_feat_scores': best_feat_n_mat,
        #            'dict_sigla_parola': dict_sigla_parola,
        #            'best_feat_scores_json': best_feat_json,
        #
        #            'auto_alg_result_mat':auto_alg_result_mat, #boxplot with the algorithms cosres
        #            }
        return render(request, template, context)


        # CALL OTHER FUNCTIONS / GET OTHER DATAS/
        # final_ml_page(request, result_dict=dic_metric, conf_mat=conf_mat)
    # ---------------------------------------------------------------------------------------
    # TODO HERE STARTS THE FINAL PART OF THE MACHINE LEARNING, WHICH IS NO MORE PROCESSING BUT JUST RENDERING THE FORM (and getting the json)
    # -------------------------------------------------------------------------------


    else:
        template = "machine_learning/ml_input.html"
        form_viewf = viewFeatures()
        form_f_par = FeatPar()
        form_test_par = TestParam()
        form_alg_choose = AlgChoose()
        form_alg_param = AlgParam()

        # form_knn = KnnParam()
        form_svm = SvmParam()
        form_knear = KNearParam()
        form_dectree = DecTreeParam()
        form_rndfor = RndForParam()
        form_adaboost = AdaBoostParam()
        form_lda = LatDirAssParam()
        form_autoParam = autoFitParam()
        form_list = [form_svm, form_knear, form_dectree, form_rndfor, form_adaboost, form_lda]

        id_list = getprocessedrecordid(id_record)
        # print  id_list
        # id_list=[(i, str(i)) for i in id_list ]
        # print id_list
        form_list_id = id_choose(choices=id_list)
        print '###############'
        print form_list_id
        print '###############'
        # print(form_viewf)
        # print form_f_par

        context = {'viewf': form_viewf,
                   'FPar': FeatPar,
                   'TPar': form_test_par,
                   'AlgChoose': form_alg_choose,
                   'AlgParamChoose': form_alg_param,
                   'forms': {'form_SVM': form_svm,
                             'form_KNN': form_knear,
                             'form_DCT': form_dectree,
                             'form_RFC': form_rndfor,
                             'form_ADA': form_adaboost,
                             'form_LDA': form_lda, },

                   'autoParam': form_autoParam,
                   'formListId': form_list_id
                   }
        print '-' * 60
        # print context['forms']
        # print '-' * 60
        return render(request, template, context)


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
            return HttpResponseRedirect(reverse('extf_record_selector', kwargs={'id_num': num_exp}))
        else:
            messages.add_message(request, messages.ERROR, 'Error wrong password')
            return render(request, 'extfeat/experiments.html', context)
    else:
        return render(request, 'extfeat/experiments.html', context)


def getprocessedrecordid(idf):
    return FeatExtractedData.objects.filter(pp_recording_id=idf).values_list('id', 'path_to_file')


def getRecordsList(experimentId):
    exp = Preprocessed_Recording.objects.filter(recording__experiment=experimentId). \
        values_list('recording__id', 'recording__device_name', 'recording__description',
                    'recording__dict_keys', 'recording__ts', 'batch_id', 'signal_type_name',
                    'applied_preproc_funcs_names', 'id').order_by('recording__id')
    # rec = Recording.objects.filter(experiment=experimentId).values_list('id', 'device_name', 'description', 'dict_keys', 'ts').order_by('id')

    return exp


def select_record(request, id_num):
    if request.method == 'POST':
        record_id = request.POST.get('rec_name')
        name = Recording.objects.filter(pk=record_id).values_list('device_name')
        print name
        if Preprocessed_Data.objects.filter(pp_recording_id=record_id).count() == 0:
            messages.error(request, "No preprocessed data found for " + name)
            name_list = getRecordsList(id_num)
            context = {'name_list': name_list}
            return render(request, 'extfeat/records.html', context)
        else:
            return HttpResponseRedirect(
                reverse('alg_choose', args=(record_id,)))  # , kwargs={'id_num': record_id}), 'alg_type': 1234
    else:
        name_list = getRecordsList(id_num)
        context = {'name_list': name_list}
        return render(request, 'extfeat/records.html', context)


def final_ml_page(request, result_dict, conf_mat):
    print conf_mat
    print type(result_dict)

    # PROCESS CONFUSION MAT AND WHATHEVER ELSE WITH ANDREW'S FUNCTION!!!!


def send_file(request, id_file):
    filename = FeatExtractedData.objects.filter(pk=id_file).values_list('path_to_file')[0][0]
    print filename, type(filename)
    name = filename.split("/")[-1]
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = "attachment; filename=%s" % name
    return response
