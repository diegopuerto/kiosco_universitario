'''
Created on 8/03/2016

@author: EJArizaR
'''
import unittest
from apps.DaneUsers.tests.test_base import test_base
from django.core.urlresolvers import reverse


class IsUsernameRegisteredTest(test_base):


    def setUp(self):
        test_base.setUp(self)     

    def test_returns_False_if_user_doesnt_exist(self):
        response = self.client.get(reverse('DaneUsers:isUsernameRegistered'),{"username":"email@email.com"})
        self.assertEqual(response.content, "False")   
        
    def test_returns_True_if_exists(self):
        self.create_user()
        response = self.client.get(reverse('DaneUsers:isUsernameRegistered'),{"username":"email@email.com"})
        self.assertEqual(response.content, "True")   


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()