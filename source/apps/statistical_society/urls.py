'''
Created on 13/10/2015

@author: EJArizaR
'''
from django.conf.urls import patterns, url
from views.views import home
from views.SearchUserView import SearchUserView
from views.RegisterUserView import RegisterSEUserView

urlpatterns = [
                       url(r'^search_user', SearchUserView.as_view(), name = "search_user"),
                       url(r'^register_user', RegisterSEUserView.as_view(), name = "register_user"),
                       url(r'^.*', home, name='home')]