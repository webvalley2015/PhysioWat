from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from forms import filterAlg, downsampling, BVP, EKG, GSR, inertial, remove_spike, smoothGaussian
from scripts.processing_scripts import tools


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

def test(request):
    gsr_data = tools.load_file_db(6)
    print gsr_data
    return HttpResponse("OK")