'''
Created on 14/10/2015

@author: EJArizaR
'''
import unittest
from apps.DaneUsers.models import BasicDaneUser, UserProfile
from django.contrib.auth.models import Group
from django.test.testcases import TestCase
from apps.DaneUsers.tests.test_base import test_base
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
import datetime
from django.utils import timezone
from unittest.case import skip



class BasicDaneUser_Test(test_base):

    def tearDown(self):
        pass


    def test_do_not_allow_non_servants_become_staff(self):
        user = BasicDaneUser.objects.create_user("user@anyserver.com", "password")
        user.is_staff = True
        user.save()
        self.assertFalse(user.is_staff)
        
    
        
    def test_allow_servants_become_staff(self):
        user = BasicDaneUser.objects.create_user("user@anyserver.com", "password")
        servant = Group.objects.get(name='servant')
        servant.user_set.add(user)
        user.is_staff = True
        user.save()
        self.assertTrue(user.is_staff)       
        
    def test_if_not_confirmed_and_activation_date_expired_is_not_active(self):
        user = self.create_user(self.data)
        user.key_expires = timezone.now() - datetime.timedelta(days=7)
        user.is_confirmed = False
        user.save()
        self.assertFalse(user.is_active)
        
    def test_if_confirmed_and_activation_date_expired_is_active(self):
        user = self.create_user(self.data)
        user.key_expires = timezone.now() - datetime.timedelta(days=7)
        user.is_confirmed = True
        user.save()
        self.assertTrue(user.is_active)
        

class DaneUserTest(test_base):
    
    def test_gets_full_name_from_user(self): 
        self.create_user()
        user = BasicDaneUser.objects.get(email = "email@email.com")
        userProfile = UserProfile.objects.get(user = user)
        self.assertEqual(userProfile.fullname, "Un De")   
    
    
    def test_does_not_allow_save_cities_that_are_not_from_department(self):
        self.data['departament'] = "01"
        self.data['city'] = "02001"
        self.client.post(reverse('DaneUsers:registerUser'), self.data)
        self.assertFalse(BasicDaneUser.objects.filter(email = "email@email.com").exists())
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()