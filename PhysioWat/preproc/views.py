from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from forms import filterAlg, downsampling, BVP, EKG, GSR, inertial, remove_spike, smoothGaussian, choose_exp


def preproc_settings(request):
    if request.method == "POST":
        form = PreprocSettings(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponseRedirect(reverse('humanupload'))
    else:

        formPick = None
        if (True):
            formDown = downsampling(initial={'switch':False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(initial={'passFr': 2, 'stopFr': 6, 'LOSS': 0.1, 'ATTENUATION': 40, 'filterType':'cheby2'})
            formSpec = BVP()
        if (True):
            formDown = downsampling(initial={'switch':False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(initial={'filterType':'none'})
            formSpec = EKG()
        if (True):
            formDown = downsampling(initial={'switch':False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(initial={'filterType':'none'})
            formSpec = inertial()    
        if (True):
            formPick = remove_spike()
            formDown = downsampling(initial={'switch':False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(initial={'filterType':'none'})
            formSpec = GSR()

    context = {'formFilt': formFilt, 'formDown': formDown, 'formPick':formPick, 'formSpec':formSpec, 'formGau':formGau}
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
            formDown = downsampling(initial={'switch':False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(initial={'passFr': 2, 'stopFr': 6, 'LOSS': 0.1, 'ATTENUATION': 40, 'filterType':'cheby2'})
            formSpec = BVP()
        if (True):
            formDown = downsampling(initial={'switch':False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(initial={'filterType':'none'})
            formSpec = EKG()
        if (True):
            formDown = downsampling(initial={'switch':False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(initial={'filterType':'none'})
            formSpec = inertial()    
        if (True):
            formPick = remove_spike()
            formDown = downsampling(initial={'switch':False})
            formGau = smoothGaussian(initial={'sigma': 2})
            formFilt = filterAlg(initial={'filterType':'none'})
            formSpec = GSR()

    context = {'forms': { 'formFilt':formFilt, 'formDown':formDown, 
    'formPick':formPick, 'formSpec':formSpec, 'formGau':formGau }}

    return render(request, template, context)

def select_experiment(request):

    if (request.method == 'POST'):
        form = choose_exp(request.POST)
        if (form.is_valid()):
            print form.selected()		
            #GET DATA FORM DB ::(GET THE LIST OF SUBJECTS , NAME, WHATEVER, given in inpyt THE ID OF THE EXPERIMENT)
            subj_list = (('1','SOGG1'),('2','GIANLUCA ADELANTE'),('3','UN BARBONE A CASO'))
            return HttpResponse('Ok')
    else:
        #GET DATA FROM DATABASE ::(GET THE LIST OF EXPERIMENTS: NAME, TIME, given in input THE ID OF RESEARCHER (you server have it!) )
        form = choose_exp()
        context = {'form':form}
        template = ('preproc/select.html')
        return render(request, template, context)
	
