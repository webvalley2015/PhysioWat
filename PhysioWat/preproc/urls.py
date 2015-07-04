from django.conf.urls import patterns, url
from .graphs import linegraph
#from .views import show_chart, preproc_settings

#the method as_view(), from the library, will  call get_data(), written, and mabye other things.

urlpatterns = patterns('preproc.views',
    url(r'^experiments/$', 'select_experiment', name='experiment_selector'),
	#url(regex='^settings/$', view=preproc_settings, name="settings_preproc"),
    #url(regex='^linegraph_getdata/$', view=linegraph.as_view(), name="chart_getdata" ),
    #url( regex='^linegraph_getdata/(?P<title>\w+)/$', view=linegraph.as_view(), name="chart_getdata" ),
    #url( regex='^linegraph_getdata/(?P<title>\w+)/(?P<begin>\d+)/(?P<end>\d+)/$', view=linegraph.as_view(), name="chart_getdata" ),
    #url( regex='^chart/$', view=show_chart, name="chart_show" ),
)
