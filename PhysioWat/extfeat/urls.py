__author__ = 'federico'
from django.conf.urls import url, patterns
from .views import getAlgorithm, ml_input, select_experiment, select_record

urlpatterns = patterns('extfeat.views',
    url( regex='^alg_selection/(?P<id_record>\d+)/$', view=getAlgorithm, name="alg_choose" ),
    url( regex='^machine_learning/(?P<id_record>\d+)/$', view=ml_input, name="ml_param_setting" ),
    url(regex='^experiments/$', view=select_experiment, name='extf_experiment_selector'),
    url(regex='^records/(?P<id_num>\d+)/$', view=select_record, name='extf_record_selector'),
)
