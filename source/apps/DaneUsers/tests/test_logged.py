# -*- coding: utf-8 -*- 
'''
Created on 28/08/2015

@author: EJArizaR
'''
from django.core.urlresolvers import reverse
from apps.DaneUsers.models import UserProfile
from apps.DaneUsers.tests.test_base import test_base
from unittest.case import skip
from django.contrib.auth import get_user_model
User = get_user_model()

class LoggedTest(test_base):

    def setUp(self):
        test_base.setUp(self)        
        self.create_user()
        
    def login_default_user(self):
        return self.client.login(email='email@email.com', password='password')
            
    def get_default_user(self):
        return User.objects.get(email="email@email.com")
    
    def test_redirect_to_login_if_user_is_not_logged(self):
        response = self.client.get(reverse('DaneUsers:logged'))     
        self.assertRedirects(response, reverse('DaneUsers:login') + "/?next=" + reverse('DaneUsers:logged'))