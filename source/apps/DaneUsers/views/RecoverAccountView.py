'''
Created on 5/10/2015

@author: EJArizaR
'''
from django.views.generic.base import View

from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from libs.dane_auth_ldap.backend import DaneLDAPBackend
from libs.django_auth_ldap.backend import get_user_model
from apps.DaneUsers.models import UserProfile
from django.shortcuts import render
from django.contrib.auth.views import password_reset
from django.contrib.auth.forms import PasswordResetForm

User = get_user_model()
class RecoverAccountView(View):
    def get(self, request, **kwargs):
        user = kwargs['user']
        if self._is_mail_valid(user):
            return render(request, "DaneUsers/recover.html",  {'email':user, "form": PasswordResetForm()})    
        else:
            return HttpResponseRedirect(reverse("DaneUsers:login"))  

    def post(self, request, **kwargs):
        user = kwargs['user']   
        if self._is_mail_valid(user):
            try:
                return self._change_username(request, user)                   
            except ObjectDoesNotExist:
                pass
        return HttpResponseRedirect(reverse("DaneUsers:login"))
   

    def _change_username(self, request, user):
        userInstance = User.objects.get(email=user)
        userProfile = UserProfile.objects.get(user=userInstance)
        if request.POST["email"] == userProfile.alternative_mail:
            userInstance.email = userProfile.alternative_mail
            userInstance.save()
            password_reset(request, 
                           template_name='DaneUsers/password_reset_form.html',
                            post_reset_redirect="DaneUsers:password_reset_done", 
                            email_template_name='DaneUsers/password_reset_email.html')
            return HttpResponse("Recover Account")  
        return render(request, "DaneUsers/recover.html",  {'email':user, "form": PasswordResetForm(data = request.POST)})    
            
            
    def _is_mail_valid(self, email):
        try:
            validate_email(email)
            return not self._user_is_in_LDAP(email) and self._email_is_from_dane(email)
        except ValidationError:
            return False       
         
    def _user_is_in_LDAP(self, email):
        return not DaneLDAPBackend().populate_user(email) == None    

    def _email_is_from_dane(self, email):
        return email.split("@")[-1].lower() == "dane.gov.co"
    