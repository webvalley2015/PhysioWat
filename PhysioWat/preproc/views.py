from django.shortcuts import render


def show_chart(request):
	#context
	template = "preproc/chart.html"
	return render(request, template)

