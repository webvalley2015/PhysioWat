__author__ = 'Stephen'
from django.conf.urls import url, patterns

urlpatterns = patterns('designer.views',
                       # sensor creation page
                       url(r'^experiments/$', 'create_experiement', name='experiment_creator'),
                       )
