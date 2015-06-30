__author__ = 'federico'
from django.shortcuts import render

def index(request):
    template = 'PhysioWat/index.html'
    context = {'a': 1234, 'name':"ema"}
    return render(request, template, context)
