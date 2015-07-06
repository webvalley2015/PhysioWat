from django.shortcuts import render
from django.core.urlresolvers import reverse
from .forms import windowing


def getAlgorithm(request):
    if(request.method=='POST'):
        print("I HAVE A POST!!!")

    else:
        form = windowing()
        template = "extfeat/choose_alg.html"
        print "ciaoooo"
        print form
        context = {'form':form}
        return render(request,template,context)