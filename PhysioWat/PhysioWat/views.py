__author__ = 'federico'
from django.shortcuts import render

def index(request):
    template = 'PhysioWat/index.html'
    context = {}
    return render(request, template, context)
