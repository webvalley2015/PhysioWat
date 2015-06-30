__author__ = 'federico'
from django.shortcuts import render

def index(request):
    template = 'PhysioWat/index.html'
    context = {'a': 1234, 'name':"txt"}
    return render(request, template, context)

def trialpage(request):
	#this function was added just to see how the django - html works. Begging the pardon of the db team, i may put on more functions like this. just don't worry (for now :) )
	template = 'PhysioWat/index.html'
	context = {'l':['a','b','c']}
	return render(request, template, context)


