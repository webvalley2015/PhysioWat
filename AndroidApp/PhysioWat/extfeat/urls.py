__author__ = 'federico'
from django.conf.urls import url, patterns
from .views import getAlgorithm

urlpatterns = patterns('extfeat.views',
    url( regex='^alg_selection/$', view=getAlgorithm, name="alg_choose" ),

                       )