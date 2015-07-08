from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import windowing, viewFeatures, FeatPar, TestParam, AlgChoose, AlgParam, SvmParam, KNearParam, DecTreeParam, \
    RndForParam, AdaBoostParam, LatDirAssParam, autoFitParam
from preproc import jsongen
from preproc.scripts.processing_scripts import windowing as wd, import feat_script as ft
from preproc.scripts.processing_scripts.GSR import extract_features as extfeat_GSR
from preproc.scripts.processing_scripts.IBI import extract_IBI_features as extfeat_IBI
from preproc.scripts.processing_scripts.inertial import extract_features_acc as extfeat_ACC, extract_features_mag as extfeat_MAG, extract_features_gyr as extfeat_GYR
from preproc.scripts.processing_scripts.tools import selectCol as selcol
import pandas as pd

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

            cols = jsongen.getavaliabledatavals(id_num)

            data="asdas" #TODO GET FROM DB!

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
            print "aaa"
            a = a.cleaned_data
            if (a['type'] == 'contigous'):
                window, labs = wd.get_windows_contiguos(time, labs, a['length'], a['step'])

            if (a['type'] == 'no_mix'):  # for the values, make reference to .forms --> windowing.!!!!
                window, labs = wd.get_windows_no_mix(time, labs, a['length'], a['step'])

            if (a['type'] == 'full_label'):
                window, labs = wd.get_windows_full_label(time, labs, a['length'], a['step'])

        # extract features from result
        # store feats. in the db
        if (type == 'GSR'):
            data_in=selcol(data, cols, "PHA")
            DELTA=0 #TODO GET FROM DB params!
            feat = extfeat_GSR(data_in, time, DELTA, window)
        if (type == 'inertial'):
            col_acc=["ACCX", "ACCY", "ACCZ"]
            col_gyr=["GYRX", "GYRY", "GYRZ"]
            col_mag=["MAGX", "MAGY", "MAGZ"]

            data_acc=selcol(data, cols, col_acc)
            data_gyr=selcol(data, cols, col_gyr)
            data_mag=selcol(data, cols, col_mag)



        if (type == "IBI"):
            escape = "escape3ibi"

            # after having extracted the fieatures --> save on db
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
        
        localdir = '/home/andrea/Work/data/Physio/PhysioWat/PhysioWat/preproc/scripts/processing_scripts/output/'
        input_data = pd.DataFrame.from_csv(path=localdir + 'feat_claire_labeled.csv')#, index_col=None, sep=',')


        if 'norm' in mydict['viewf']:
            input_data =             
            
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
