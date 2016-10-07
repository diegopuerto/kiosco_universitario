# -*- coding: utf-8 -*- 
'''
Created on 23/09/2015

@author: ejarizar
'''
from django.contrib.auth import authenticate
from apps.DaneUsers.models import UserProfile
from libs.dane_auth_ldap.backend import DaneLDAPBackend
from django.contrib.auth import get_user_model
User = get_user_model()

class NonExistentUser():
    def __init__(self, email, in_local_database = False):
        self.email = email
        self.in_local_database = in_local_database

class UsersGetter(object):
    def get_current_authenticated_user(self, request):
        if len(UserProfile.objects.filter(user=request.user)) > 0:
            userProfile = UserProfile.objects.get(user=request.user)
        else:
            userProfile = None
        return userProfile

    def get_autenticathed_user(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = self.authenticate_dane_user(email=email, password=password)
        return user
    
    def authenticate_dane_user(self, email, password):
        if self._is_valid_email(email) and not self.is_dane_email(email):
            return authenticate(email=email, password=password)
        else:
            if len(User.objects.filter(email = email)) > 0:
                return NonExistentUser(email, True)
            else:
                return NonExistentUser(email)
            
    def _is_valid_email(self, email):
        return not email == None and len(email.split("@")) > 1   
    
    def is_dane_email(self, email):
        return email.split("@")[-1].lower() == "dane.gov.co" and DaneLDAPBackend().populate_user(email) == None     