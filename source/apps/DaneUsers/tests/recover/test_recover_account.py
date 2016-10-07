# -*- coding: utf-8 -*- 
'''
Created on 5/10/2015

@author: EJArizaR
'''
from apps.DaneUsers.tests.test_base import test_base
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from mock.mock import patch
from unittest.case import skip
from django.contrib.auth.forms import PasswordResetForm
from django.http.response import HttpResponseRedirect
User = get_user_model()


class test_recover_base(test_base):
    def setUp(self):
        test_base.setUp(self)
        self.NOT_IN_LDAP_USER_MAIL = "non_existent_in_LDAP@dane.gov.co"   
        self.DEFAULT_RECOVER_URI = reverse('DaneUsers:recoverAccount', kwargs={'user':self.NOT_IN_LDAP_USER_MAIL})

    def _create_user_in_local_database(self, email = None):
        local_email = self.NOT_IN_LDAP_USER_MAIL
        User.objects.create_user(local_email, "password")
        self.client.login(email=local_email, password="password")
        self.data["email"] = local_email
        self.data["alternative_mail"] = "alternativemail@anyserver.com"
        self.client.post(reverse('DaneUsers:registerUser'), self.data)
        self.client.logout()
        
    

@patch("apps.DaneUsers.views.UsersGetter.DaneLDAPBackend.populate_user")   
class test_recover_get(test_recover_base):

    def test_passes_to_template_context_user_email(self, populate_user_mock):
        self._create_user_in_local_database()
        populate_user_mock.return_value = None        
        response = self.client.get(reverse('DaneUsers:recoverAccount', kwargs={'user':self.NOT_IN_LDAP_USER_MAIL}))
        self.assertEqual(response.context["email"], self.NOT_IN_LDAP_USER_MAIL) 
        
    def test_passes_to_template_context_password_reset_form(self, populate_user_mock):
        self._create_user_in_local_database()
        populate_user_mock.return_value = None        
        response = self.client.get(reverse('DaneUsers:recoverAccount', kwargs={'user':self.NOT_IN_LDAP_USER_MAIL}))
        self.assertIsInstance(response.context["form"], PasswordResetForm) 
        
    def test_when_user_is_not_a_valid_email_redirects_to_login(self, populate_user_mock):
        response = self.client.get(reverse('DaneUsers:recoverAccount', kwargs={'user':'notavalidmail'}))
        self.assertRedirects(response, reverse("DaneUsers:login"))  

    def test_if_user_in_LDAP_redirects_to_login(self, populate_user_mock):
        self._create_user_in_local_database()
        populate_user_mock.return_value = User.objects.get(email = self.NOT_IN_LDAP_USER_MAIL)            
        response = self.client.get(reverse('DaneUsers:recoverAccount', kwargs={'user':self.NOT_IN_LDAP_USER_MAIL}))
        self.assertRedirects(response, reverse("DaneUsers:login"))       
        
    def test_when_mail_is_not_from_dane_redirects_to_login(self, populate_user_mock):
        self.NOT_IN_LDAP_USER_MAIL = "non_existent_in_LDAP@anyserver.gov.co"
        self._create_user_in_local_database()
        populate_user_mock.return_value = None   
        response = self.client.post(reverse('DaneUsers:recoverAccount', kwargs={'user':self.NOT_IN_LDAP_USER_MAIL}))    
        self.assertRedirects(response, reverse("DaneUsers:login"))     
        

@patch("apps.DaneUsers.views.UsersGetter.DaneLDAPBackend.populate_user")   
class test_recover_post(test_recover_base):
    
    def _default_recover_post(self):
        return self.client.post(self.DEFAULT_RECOVER_URI, {"email": "alternativemail@anyserver.com"})

    def test_changes_login_mail_for_alternative_mail(self, populate_user_mock):
        self._create_user_in_local_database()  
        populate_user_mock.return_value = None      
        response = self._default_recover_post()
        self.assertNotEqual(0, len(User.objects.filter(email = "alternativemail@anyserver.com")))

    def test_when_user_is_not_a_valid_email_does_not_change_username(self, populate_user_mock):
        response = self._default_recover_post()
        self.assertEqual(0, len(User.objects.filter(email = "alternativemail@anyserver.com")))
          
    def test_if_user_in_LDAP_does_not_change_username(self, populate_user_mock):
        self._create_user_in_local_database()
        populate_user_mock.return_value = User.objects.get(email = self.NOT_IN_LDAP_USER_MAIL)            
        response = self._default_recover_post()
        self.assertEqual(0, len(User.objects.filter(email = "alternativemail@anyserver.com")))

    def test_when_mail_is_not_from_dane_does_not_change_username(self, populate_user_mock):
        self.NOT_IN_LDAP_USER_MAIL = "non_existent_in_LDAP@anyserver.gov.co"
        self._create_user_in_local_database()
        populate_user_mock.return_value = None   
        response = self._default_recover_post()  
        self.assertEqual(0, len(User.objects.filter(email = "alternativemail@anyserver.com")))   
    
    def test_when_POSTed_mail_is_not_alternative_mail_does_not_change_username(self, populate_user_mock):
        self._create_user_in_local_database()  
        populate_user_mock.return_value = None      
        response = self.client.post(self.DEFAULT_RECOVER_URI, {"email": "wrong_alternative_mail@anyserver.com"})
        self.assertEqual(0, len(User.objects.filter(email = "alternativemail@anyserver.com")))
        
    def test_when_wrong_email_POSTed_remains_in_recover_page(self, populate_user_mock):
        self._create_user_in_local_database()  
        populate_user_mock.return_value = None      
        response = self.client.post(self.DEFAULT_RECOVER_URI, {"email": "wrong_alternative_mail@anyserver.com"})  
        self.assertNotIsInstance(response, HttpResponseRedirect)       

    def test_when_wrong_email_POSTed_send_form_with_errorlist(self, populate_user_mock):
        self._create_user_in_local_database()  
        populate_user_mock.return_value = None      
        response = self.client.post(self.DEFAULT_RECOVER_URI, {"email": ""})
        error = '<ul class="errorlist"><li>This field is required.</li></ul>'
        self.assertIn(error, response.content) 

@patch("apps.DaneUsers.views.UsersGetter.DaneLDAPBackend.populate_user")   
class test_recover_email(test_recover_base):       
    def _default_recover_post(self):
        return self.client.post(self.DEFAULT_RECOVER_URI, {"email": "alternativemail@anyserver.com"})
        
    @patch("apps.DaneUsers.views.RecoverAccountView.password_reset")    
    def test_calls_password_reset_view(self, password_reset_mock, populate_user_mock):
        self._create_user_in_local_database()  
        populate_user_mock.return_value = None      
        response = self._default_recover_post()
        password_reset_mock.assert_called_once_with(response.wsgi_request,
                                                    template_name = 'DaneUsers/password_reset_form.html',
                                                    post_reset_redirect = "DaneUsers:password_reset_done",
                                                    email_template_name = 'DaneUsers/password_reset_email.html')
