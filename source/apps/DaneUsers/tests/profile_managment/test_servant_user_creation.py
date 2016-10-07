'''
Created on 2/10/2015

@author: EJArizaR
'''
from apps.DaneUsers.tests.test_base import test_base
from mock.mock import patch
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from apps.DaneUsers.forms import UserDataServantForm, UserDataModifyServantForm
from apps.DaneUsers.models import UserProfile
from unittest.case import skip
User = get_user_model()

class test_servant_profile_manage_base(test_base):
    REQUEST_URI = reverse('DaneUsers:registerUser')
    
    def setUp(self):
        test_base.setUp(self)
        servant_user_with_no_data = User.objects.create_user(email="nodata@dane.gov.co", password="password")  # @UnusedVariable

    def _create_user_profile(self):
        newData = self.data.copy()
        newData["id_doc"] = '9999'
        newData["email"] = 'nodata@dane.gov.co'
        newData["alternative_mail"] = 'alternative@anyserver.com'
        return self.client.post(self.REQUEST_URI, newData)
        

class test_servant_user_creation(test_servant_profile_manage_base): 
    
    @patch("libs.dane_auth_ldap.backend.DaneLDAPBackend")     
    def test_uses_profile_modification_form_for_users_when_user_is_logged(self, backendMock):
        self.client.login(email='nodata@dane.gov.co', password='password')         
        self._create_user_profile()
        response = self.client.get(reverse("DaneUsers:modifyUserData"))
        self.assertIsInstance(response.context["forms"]["user_profile_form"], UserDataModifyServantForm)
        
    @patch("libs.dane_auth_ldap.backend.DaneLDAPBackend")         
    def test_when_email_is_from_dane_is_not_added_to_citizen_group(self, backendMock):
        self.client.login(email='nodata@dane.gov.co', password='password') 
        self._create_user_profile()
        user = User.objects.get(email='nodata@dane.gov.co')
        self.assertFalse(user.groups.filter(name='citizen').exists(), "servant user belongs to citizen group")
        
    @patch("libs.dane_auth_ldap.backend.DaneLDAPBackend")         
    def test_when_creates_servant_UserDataServantForm_is_used(self, backendMock):
        self.client.login(email='nodata@dane.gov.co', password='password')         
        response = self.client.get(self.REQUEST_URI)
        self.assertIsInstance(response.context["forms"]["user_profile_form"], UserDataServantForm)

    @patch("libs.dane_auth_ldap.backend.DaneLDAPBackend")         
    def test_two_users_with_same_alternative_mail_are_not_allowed(self, backendMock):
        self.client.login(email='nodata@dane.gov.co', password='password')         
        self._create_user_profile()
        User.objects.create_user(email="nodata2@dane.gov.co", password="password")
        self.client.login(email='nodata2@dane.gov.co', password='password')         
        newData = self.data.copy()
        newData["id_doc"] = '99999'
        newData["email"] = 'nodata2@dane.gov.co'
        newData["alternative_mail"] = 'alternative@anyserver.com'
        self.client.post(reverse("DaneUsers:modifyUserData"), newData)  
        self.assertEqual(1, len(UserProfile.objects.filter(alternative_mail = "alternative@anyserver.com")))    
        
    def test_cannot_use_alternative_mail_if_its_used_by_another_user_s_login(self):
        User.objects.create(email =  "alternative@anyserver.com", password = "password")    
        self.client.login(email='nodata@dane.gov.co', password='password')         
        self._create_user_profile()
        self.assertEqual(0, len(UserProfile.objects.filter(alternative_mail = "alternative@anyserver.com"))) 
