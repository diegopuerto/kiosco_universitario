'''
Created on 23/11/2015

@author: ejarizar
'''
from django.conf.urls import patterns, url
from apps.kiosco_app.views import Home


urlpatterns = [url(r'^.*', Home.as_view(), name='home')]