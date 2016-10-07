# -*- coding: utf-8 -*- 
'''
Created on 25/09/2015

@author: EJArizaR
'''
from django.test.testcases import TestCase
from apps.DaneUsers.forms import UserCreateForm, UserDataServantForm
from apps.DaneUsers.tests.test_base import test_base

class test_userform(TestCase):
    def test_does_not_validates_dane_gov_co_mails(self):
        self.data =  {'password':'password',
                        'email':'email@dane.gov.co',
                        'first_name':'Yon',
                        'last_name':'do'}
        
        userform  = UserCreateForm(self.data)
        self.assertFalse(userform.is_valid())
        
class test_UserDataServantForm(test_base):
    def test_does_not_validates_dane_gov_co_alternative_mails(self):
        userdataform = UserDataServantForm(self.data)
        self.data["alternative_mail"] = 'email@dane.gov.co'
        self.assertFalse(userdataform.is_valid())
        
        