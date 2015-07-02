from django.shortcuts import render

def preproc_settings(request):
    if request.method == "POST":
        form = PreprocSettings(request.POST, request.FILES)
        if form.is_valid():

            return HttpResponseRedirect(reverse('humanupload'))
    else:
        form = PreprocSettings()
    context = {'form': form}
    return render(request, 'preproc/settings.html', context)

def show_chart(request):
	#context
	template = "preproc/chart.html"
	return render(request, template)

