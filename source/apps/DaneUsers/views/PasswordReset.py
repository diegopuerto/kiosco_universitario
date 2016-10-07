'''
Created on 23/02/2016

@author: EJArizaR
'''
from django.contrib.auth.views import password_reset
from django.shortcuts import render
from django.views.generic.base import View


class DanePasswordReset(View):
    def post(self, request, *args, **kwargs):
        if self._is_mail_from_dane(request.POST["email"]):
                return render(request, "DaneUsers/ServantCannotChangePassword.html")
        return password_reset(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return password_reset(request, *args, **kwargs)
    
    def _is_mail_from_dane(self, email):
        return email.split("@")[-1].lower() == "dane.gov.co"