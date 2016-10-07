'''
Created on 2/10/2015

@author: EJArizaR
'''

from apps.DaneUsers.tests.test_base import test_base
from mock.mock import patch
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from unittest.case import skip
User = get_user_model()


@patch("apps.DaneUsers.views.UsersGetter.DaneLDAPBackend.populate_user")    
class test_login_servant(test_base):
    
    def setUp(self):      
        test_base.setUp(self)
        self.LOGIN_URI = reverse('DaneUsers:login')
        self.NOT_IN_LDAP_USER_MAIL = "nonexistentInLDAP@dane.gov.co"
       
    def test_user_not_found_in_LDSP_but_exists_locally_redirects_to_recover_account(self, populate_user_mock):
        populate_user_mock.return_value = None        
        user = User.objects.create_user(self.NOT_IN_LDAP_USER_MAIL, "password")
        user.set_unusable_password()
        user.save()
        self.client.login(email = self.NOT_IN_LDAP_USER_MAIL, password = "password")
        self.data["email"] = self.NOT_IN_LDAP_USER_MAIL
        self.data["alternative_mail"] = "alternativemail@anyserver.com"
        self.client.post(reverse('DaneUsers:registerUser'), self.data) 
        self.client.logout()
        response = self.client.post(self.LOGIN_URI,  {"email":self.NOT_IN_LDAP_USER_MAIL,"password":"password"})
        expected_redirect_to = reverse('DaneUsers:recoverAccount', kwargs={'user':self.NOT_IN_LDAP_USER_MAIL})
        self.assertRedirects(response, expected_redirect_to)

           

    