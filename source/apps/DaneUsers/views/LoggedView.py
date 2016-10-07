'''
Created on 23/09/2015

@author: ejarizar
'''
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from apps.DaneUsers.views.UsersGetter import UsersGetter

class LoggedView(View):
    users_getter = UsersGetter()

    @method_decorator(login_required(login_url='/users/login/'))
    def get(self, request):    
        return render(request, "DaneUsers/logged.html")