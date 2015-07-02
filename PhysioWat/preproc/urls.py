from  django.conf.urls import patterns, url
from .graphs import linegraph
from .views import show_chart


urlpatterns = patterns('preproc.views', 
    url(regex='^linegraph_getdata/$', view=linegraph.as_view(), name="chart_getdata" ),
    url( regex='^linegraph_getdata/(?P<title>\w+)/$', view=linegraph.as_view(), name="chart_getdata" ),	
    url( regex='^chart/$', view=show_chart, name="chart_show" ), 

)
 


#the method as_view(), from the library, will  call get_data(), written, and mabye other things.

