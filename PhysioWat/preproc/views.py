from django.shortcuts import render
from forms import filter, downsampling, BVP, EKG, GSR, inertial, remove_spike

def preproc_settings(request):
    if request.method == "POST":
        form = PreprocSettings(request.POST, request.FILES)
        if form.is_valid():

            return HttpResponseRedirect(reverse('humanupload'))
    else:
        if (True):
            formPick = remove_spike()
            formDown = downsampling(initial={'switch':False})
            formFilt = filter(initial={'filterType':'none'})
            formSpec = GSR()
        if (True):
            formDown = downsampling(initial={'switch':False})
            formFilt = filter(initial={'passFr': 2, 'stopFr': 6, 'LOSS': 0.1, 'ATTENUATION': 40, 'filterType':'cheby2'})
            formSpec = BVP()
        if (True):
            formDown = downsampling(initial={'switch':False})
            formFilt = filter(initial={'filterType':'none'})
            formSpec = EKG()
        if (True):
            formDown = downsampling(initial={'switch':False})
            formFilt = filter(initial={'filterType':'none'})
            formSpec = inertial()


    context = {'formFilt': formFilt, 'formDown': formDown, 'formPick':formPick, 'formSpec':formSpec}
    return render(request, 'preproc/settings.html', context)

def show_chart(request):
	#context
	template = "preproc/chart.html"
	return render(request, template)

