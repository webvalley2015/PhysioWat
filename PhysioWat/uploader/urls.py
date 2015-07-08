__author__ = 'federico'
from django.conf.urls import url, patterns

urlpatterns = patterns('uploader.views',
                       # human upload page
                       url(r'^web/$', 'upload', name='user_upload'),
                       url(r'^mobile/upload/$', 'get_data_from_mobile', name='mobile_upload'),
                       url(r'^mobile/list/$', 'list_experiment_id', name='mobile_list'),
                       )
