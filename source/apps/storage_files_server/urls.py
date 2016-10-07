'''
Created on 18/03/2016

@author: EJArizaR
'''
from django.conf.urls import patterns, url
from views import index

urlpatterns = [ url(r'^.*', index)]