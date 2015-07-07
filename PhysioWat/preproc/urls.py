from django.conf.urls import patterns, url
from .graphs import linegraph
from .views import show_chart, select_experiment, select_record

#the method as_view(), from the library, will  call get_data(), written, and mabye other things.

urlpatterns = patterns('preproc.views',
    url(r'^experiments/$', view=select_experiment, name='experiment_selector'),
    url(r'^records/(?P<id_num>\d+)/$', view=select_record, name='record_selector'),
    url( regex='^linegraph_getdata/(?P<id_num>\d+)/$', view=linegraph.as_view(), name="chart_getdata" ),
    url( regex='^chart/(?P<id_num>\d+)/(?P<alg_type>[A-Za-z]*)/{0,1}$', view=show_chart, name="chart_show" )
    #url( regex='^select/$', view=select_experiment_no_use, name="exp_selection")
)
