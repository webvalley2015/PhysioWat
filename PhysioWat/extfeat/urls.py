__author__ = 'federico'
from django.conf.urls import url, patterns
from .views import getAlgorithm, ml_input

urlpatterns = patterns('extfeat.views',
    url( regex='^alg_selection/(?P<id_num>\d+)$', view=getAlgorithm, name="alg_choose" ),
    url( regex='^machine_learning/$', view=ml_input, name="ml_param_setting" ),
                       )
