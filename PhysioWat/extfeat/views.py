from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import windowing, viewFeatures, FeatPar, TestParam, AlgChoose, AlgParam, SvmParam, KNearParam, DecTreeParam, \
    RndForParam, AdaBoostParam, LatDirAssParam, autoFitParam
from preproc.scripts.processing_scripts import windowing as wd
from preproc.scripts.processing_scripts.GSR import extract_features as extfeat_GSR
from preproc.scripts.processing_scripts.IBI import extract_IBI_features as extfeat_IBI
from preproc.scripts.processing_scripts.inertial import extract_features_acc as extfeat_ACC, extract_features_mag as extfeat_MAG, extract_features_gyr as extfeat_GYR
from preproc.scripts.processing_scripts.tools import selectCol as selcol, dict_to_arrays
from PhysioWat.models import Experiment, Preprocessed_Recording, Preprocessed_Data
import numpy as np


def QueryDb(recordingID):   #TODO NOT TESTED YET, IT MAY SUCK
    table = Preprocessed_Recording.objects.get(id=recordingID)
    data = Preprocessed_Data.objects.filter(recording_id=recordingID).order_by('id')
    # alldata = (','.join(table.dict_keys) + '\n').replace(' ', '')
    retarray=np.array([])
    ll = []
    for key in table.dict_keys:
        ll.append(data[0].store[key])
    retarray=np.append(retarray,ll)
    for record in data[1:]:
        ll = []
        for key in table.dict_keys:
            ll.append(record.store[key])
        retarray=np.vstack((retarray,ll))
    # datacsv = np.genfromtxt(StringIO(alldata), delimiter=',')
    return retarray, table.dict_keys

def getAlgorithm(request, id_num):  # ADD THE TYPE ODF THE SIGNAL ALSO IN URLS!!!

    # read parameters from url
    print(id_num)
    # get data type list

    if (request.method == 'POST'):
        print("I HAVE A POST!!!")
        a = windowing(request.POST)
        if a.is_valid():
            # print a.cleaned_data
            # time = GET THE COLUMN TIME FROM DB (ASK RICCARDO)
            # label = GET THE COLUMN OF THE LABEL FROM THE DB (ASK RICCARDO)
            # those prevoious 2 variabliles were for windowing. as i wrote, ask riccardo for further inforation
            # after having done the db stuffs, please un-comment the 2 variabiles and feel free to delete this 2 comments
            ID=25 #TODO test value!, get from user
            data, cols = QueryDb(ID)

            # vals = vals[1:]
            # print vals

            # timestamplist = ['timestamp', 'timeStamp', 'times', 'time', 'TIME']
            #
            # data = jsongen.makejson("raw", id_num, cols)
            # for i in data['series']:
            #     if i['name'] in timestamplist:
            #         time = i['data']

            time=selcol(data, cols, "TIME")
            labs=data["LAB"]    #template

            a = a.cleaned_data
            if (a['type'] == 'contigous'):
                windows, winlab = wd.get_windows_contiguos(time, labs, a['length'], a['step]'])

            if (a['type'] == 'no_mix'):  # for the values, make reference to .forms --> windowing.!!!!
                windows, winlab = wd.get_windows_no_mix(time, labs, a['length'], a['step]'])

            if (a['type'] == 'full_label'):
                windows, winlab = wd.get_windows_full_label(time, labs, a['length'], a['step]'])

        # extract features from result
        # store feats. in the db
        if 'PHA' in cols:   #GSR
            data_in=selcol(data, cols, "PHA")
            DELTA=0 #TODO GET FROM DB params!
            feat_dict = extfeat_GSR(data_in, time, DELTA, windows)
            feats, cols_out=dict_to_arrays(feat_dict)
            feats=np.column_stack((feats, winlab))
            feat_col=np.r_[cols_out, "LAB"]
        elif 'ACCX' or 'GYRX' or 'MAGX' in cols:
            col_acc=["ACCX", "ACCY", "ACCZ"]
            col_gyr=["GYRX", "GYRY", "GYRZ"]
            col_mag=["MAGX", "MAGY", "MAGZ"]
            try:
                acc=selcol(data, cols, col_acc)
                thereIsAcc=True
            except ValueError as e:
                print e
                thereIsAcc=False
            try:
                gyr=selcol(data, cols, col_gyr)
                thereIsGyr=True
            except ValueError as e:
                print e
                thereIsGyr=False
            try:
                mag=selcol(data, cols, col_mag)
                thereIsMag=True
            except ValueError as e:
                print e
                thereIsMag=False
            feat_col=np.array(["LAB"])
            feats=winlab[:]
            if thereIsAcc:
                feats_acc, fcol_acc= extfeat_ACC(acc, time, col_acc, windows)
                feats=np.column_stack([feats_acc, feats])
                feat_col=np.r_[fcol_acc, feat_col]
            if thereIsGyr:
                feats_gyr, fcol_gyr= extfeat_GYR(gyr, time, col_gyr, windows)
                feats=np.column_stack([feats_gyr, feats])
                feat_col=np.r_[fcol_gyr, feat_col]
            if thereIsMag:
                feats_mag, fcol_mag= extfeat_MAG(mag, time, col_mag, windows)
                feats=np.column_stack([feats_mag, feats])
                feat_col=np.r_[fcol_mag, feat_col]

        elif 'IBI' in cols:
            data_in=selcol(data, cols, "IBI")
            feats, winlab = extfeat_IBI(np.column_stack((time, data_in)), windows, winlab)
            feat_col=np.array(['RRmean', 'RRSTD', 'pNN50', 'pNN25', 'pNN10', 'RMSSD', 'SDSD'])

        data_out=np.concatenate((feats, winlab))
        columns_out=np.r_[feat_col, "LAB"]

    else:
        form = windowing()
        template = "extfeat/choose_alg.html"
        print "ciaoooo"
        # print urlTmp['id_num']
        context = {'form': form, 'id_num': id_num}
        return render(request, template, context)


# ----------------end get_algorithm

def ml_input(request):  # obviously, it has to be added id record and everything concerning db
    if (request.method == 'POST'):

        print "culoculoculoculo"  # GET THE POST, ELABORATE AND GO TO THE DB OR THE PLOT
        print request.POST
        mydict = dict(request.POST.iterlists())
        for key in request.POST.iterkeys():  # "for key in request.GET" works too.
            # Add filtering logic here.

            print key, request.POST.getlist(key)

        print mydict



        return render(request,"machine_learning/form_error.html")

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

        print(form_viewf)
        print form_f_par

        context = {'viewf': form_viewf,
                   'FPar': FeatPar,
                   'TPar': form_test_par,
                   'AlgChoose': form_alg_choose,
                   'AlgParamChoose': form_alg_param,
                   'forms': {'form_svm': form_svm,
                             'form_knear': form_knear,
                             'form_dectree': form_dectree,
                             'form_rndfor': form_rndfor,
                             'form_adaboost': form_adaboost,
                             'form_lda': form_lda, },

                   'autoParam': form_autoParam
                   }
        print '-' * 60
        print context['forms']
        print '-' * 60
        return render(request, template, context)
