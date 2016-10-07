'''
Created on 1/12/2015

@author: EJArizaR
'''
from django.conf.urls import patterns, url
from apps.services_requests.views.views import home
from apps.services_requests.views.SpecializedChamberRequestView import SpecializedChamberRequestView
from apps.services_requests.views.StatisticCultureRequestView import StatisticalCultureRequestView

urlpatterns = [
                       url(r'^specializedChamber', SpecializedChamberRequestView.as_view(), name='specializedChamber'),
                       url(r'^statisticalCulture', StatisticalCultureRequestView.as_view(), name='statisticalCulture'),
                       url(r'^.*', home, name='home')
                       ]