__author__ = 'federico'
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    template = 'PhysioWat/index.html'
    context = {'a': 1234}
    return render(request, html_file, context)
