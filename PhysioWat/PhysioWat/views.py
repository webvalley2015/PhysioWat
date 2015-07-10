__author__ = 'federico'
from django.shortcuts import render
from .models import Sensor, Recording
from PhysioWat.settings import MEDIA_ROOT


def index(request):
    template = 'PhysioWat/index.html'
    sensors = Recording.objects.all()
    context = {'sensors': sensors, 'name': "txt"}
    return render(request, template, context)


def trialpage(request):
    """this function was added just to see how the django - html works.
    Begging the pardon of the db team, i may put on more functions like this. just don't worry (for now :) )
    i know who you are -.-"
    """
    template = 'PhysioWat/index.html'
    context = {'l':['a','b','c']}
    return render(request, template, context)

def login(request):
    template = 'registration/login.html'
    context = {}
    return render(request, template, context)


def contact_view(request):
    template = 'contact_form/contact_form.html'
    context = {}
    return render(request, template, context)


def design_view(request):
    return render(request, template_name="PhysioWat/design.html")


