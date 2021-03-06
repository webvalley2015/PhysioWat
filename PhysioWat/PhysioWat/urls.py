"""PhysioWat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import django.contrib.auth
from PhysioWat import views
from django.conf.urls.static import static, settings

urlpatterns = [
    # all the urls to manage users
    url('^', include('django.contrib.auth.urls')),
    # adminpage
    url(r'^admin/', include(admin.site.urls)),
    # homepage
    url(r'^$', views.index, name='index'),
    url(r'^contact_form/$', views.contact_view, name='contact'),
    # redirect to preproc
    url(r'^preproc/', include('preproc.urls'), name='preproc'),
    # redirect to uploader
    url(r'^uploader/', include('uploader.urls'), name='uploader'),
    # redirect to designer
    url(r'^designer/', include('designer.urls'), name='designer'),
    # redirect to login
    url(r'^/', views.login, name='login'),
    #redirect to feature extraction
    url(r'^extfeat/', include('extfeat.urls'), name='exfeat'),
    url(r'^design/', views.design_view, name='design'),

]
