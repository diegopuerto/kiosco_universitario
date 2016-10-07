# -*- coding: utf-8 -*- 
'''
Created on 28/08/2015

@author: EJArizaR
'''
from django.views.generic.base import View
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.contrib.auth import get_user_model
from apps.DaneUsers.models import UserProfile
from django.shortcuts import render_to_response
from apps.statistical_society.forms import SearchUsersForm
import re
User = get_user_model()


def redirect_not_allowed_users(function):
    def function_wrapper(self, request):
        if bool(request.user.groups.filter(name = "statistical_society_reader")) | request.user.is_superuser:
            return function(self, request)
        return HttpResponseRedirect(reverse('DaneUsers:login'))
    return function_wrapper

class SearchUserView(View):
    @redirect_not_allowed_users
    def get(self, request):
        response = render_to_response("statistical_society/search_user.html", 
                                      {"search_form": SearchUsersForm()}, 
                                      context_instance=RequestContext(request))
        return response

    @redirect_not_allowed_users   
    def post(self, request):
#         cedulas = request.POST["cedulas"].split(",")
        cedulas = re.split("[,\s]+", request.POST["cedulas"])
        users = self._get_users_list(cedulas)
        response = render_to_response("statistical_society/search_user.html", 
                                      {'users':users, 
                                       "search_form": SearchUsersForm()}, 
                                      context_instance=RequestContext(request))
        return response
    
    def _get_users_list(self, cedulas):
        users= []
        for cedula in cedulas:
            user = self._get_user(cedula)
            users.append(user)
            
        return users

    def _get_user(self, cedula):
        user = {"Cedula": cedula}
        try:
            userProfile = UserProfile.objects.get(id_doc=cedula)
            user["name"] = userProfile.fullname 
            user["belongs_to_SE"] = bool(userProfile.user.groups.filter(name="statistical_society_user"))
        except:
            user["name"] = None 
            user["belongs_to_SE"] = False
        return user

    
    