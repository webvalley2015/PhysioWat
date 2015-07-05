from django.conf.urls import patterns, url
from .graphs import linegraph
from .views import show_chart, select_experiment

#the method as_view(), from the library, will  call get_data(), written, and mabye other things.

urlpatterns = patterns('preproc.views',
    url(r'^experiments/$', view=select_experiment, name='experiment_selector'),
    url( regex='^linegraph_getdata/$', view=linegraph.as_view(), name="chart_getdata" ),
    url( regex='^chart/(?P<id_num>\d+)/$', view=show_chart, name="chart_show" ),
    #url( regex='^select/$', view=select_experiment_no_use, name="exp_selection")
)
