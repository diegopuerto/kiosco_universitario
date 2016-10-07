# -*- coding: utf-8 -*- 
'''
Created on 2/12/2015

@author: EJArizaR
'''
import unittest
from apps.DaneUsers.tests.test_base import test_base
from libs.user_info_extractor.UserInfoExtractor import UserInfoExtractor
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
User = get_user_model()



class Test(test_base):
    
    def setUp(self):
        test_base.setUp(self)      
        self.expectedUserInfo = u'first_name: Un\n\
last_name: De\n\
email: email@email.com\n\
id_type: None\n\
id_doc: None\n\
cellphone: None\n\
age_range: None\n\
country_of_residence: \n\
education: None\n\
activity: None\n\
profession: None\n'

    def login(self):
        self.client.login(email = "email@email.com", password='password')

    def test_get_user_info_formatted(self):
        self.client.post(reverse('DaneUsers:registerUser'), self.data)
        user = User.objects.get(email="email@email.com")
        userInfoExtractor = UserInfoExtractor()
        userInfo = userInfoExtractor.extract(user)
        self.assertEqual(userInfo, self.expectedUserInfo)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()