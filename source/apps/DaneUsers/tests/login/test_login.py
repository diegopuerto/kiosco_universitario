# -*- coding: utf-8 -*- 
'''
Created on 28/08/2015

@author: EJArizaR
'''

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from apps.DaneUsers.forms import UserLoginForm
from unittest.case import skip
from django.http.response import HttpResponseRedirect
from apps.DaneUsers.tests.test_base import test_base
User = get_user_model()

class Test_login(test_base):
    
    def setUp(self):
        cache.clear()        
        test_base.setUp(self)
        self.create_user()
        self.LOGIN_URI = reverse('DaneUsers:login')
        self.default_user_credentials = {'email':'email@email.com', 'password':'password'}
        self.wrongCredentials = {'email':'usuario@erroneo.com', 'password':'contrasenia'}

    def login_default_user(self):
        return self.client.login(email='email@email.com', password='password')
        
    def get_default_user(self):
        return User.objects.get(email='email@email.com')
        
    def test_login_page_contains_login_template(self):
        response = self.client.get(self.LOGIN_URI)
        self.assertIn('DaneUsers/login.html', [t.name for t in response.templates])
        
    def test_to_login_page_is_passed_user_profile_form(self):
        response = self.client.get(self.LOGIN_URI)
        self.assertIsInstance(response.context["user_login_form"], UserLoginForm)
    
    def test_logs_user_when_given_correcy_credentials(self):
        self.client.post(self.LOGIN_URI,  self.default_user_credentials)
        self.assertIn('_auth_user_id', self.client.session)
    
    def test_does_not_redirect_when_given_wrong_credentials(self):   
        response = self.client.post(self.LOGIN_URI, self.wrongCredentials)
        self.assertNotIsInstance(response, HttpResponseRedirect)  
        
    def test_redirects_correctly_when_given_right_credentials(self):
        response = self.client.post(self.LOGIN_URI, self.default_user_credentials)
        self.assertRedirects(response, reverse('kiosco_app:home')) 
        
    def test_redirects_correctly_when_user_already_logged(self):
        self.login_default_user()
        response = self.client.get(self.LOGIN_URI)
        self.assertRedirects(response, reverse('kiosco_app:home')) 
           
    def test_throttling_of_login_attempts_after_three(self):
        for attemps in range(3):  # @UnusedVariable
            response = self.client.post(self.LOGIN_URI, self.wrongCredentials)
        self.assertRedirects(response, reverse('DaneUsers:recoverPassword'))
        
    def test_does_not_throttle_login_before_three_attemps(self):
        for attemps in range(2):
            response = self.client.post(self.LOGIN_URI, self.wrongCredentials)
            self.assertNotIsInstance(response, HttpResponseRedirect, msg= "wrong redirected after the " + repr(attemps) + " attemps")  
        
    def test_does_not_throttle_when_third_attempt_is_correct(self):
        for attemps in range(2):  # @UnusedVariable
            self.client.post(self.LOGIN_URI, self.wrongCredentials)
        response = self.client.post(self.LOGIN_URI,  self.default_user_credentials)
        self.assertRedirects(response, reverse('kiosco_app:home')) 
    
    def test_when_account_deactivated_redirects_to_deactivated_user_page(self):
        user = self.get_default_user()
        user.is_active = False
        user.save()
        response = self.client.post(self.LOGIN_URI,  self.default_user_credentials)
        self.assertRedirects(response, reverse('DaneUsers:notActiveUser'))
        
    def test_when_account_deactivated_does_not_authenticate_user(self):
        user = self.get_default_user()
        user.is_active = False
        user.save()
        self.client.post(self.LOGIN_URI, self.wrongCredentials)       
        self.assertNotIn('_auth_user_id', self.client.session)
        
    def test_if_there_is_no_user_data_asks_user_for_creating_it(self):
        User.objects.create_user("nodata@user.com", "contrasenia")
        response = self.client.post(self.LOGIN_URI, {'email':'nodata@user.com', 'password':'contrasenia'}, follow = True)
        self.assertRedirects(response, reverse('DaneUsers:modifyUserData'))    
        
    def test_user_with_no_data_is_kept_in_modify_profile_until_completes_form(self):
        User.objects.create_user("nodata@user.com", "contrasenia")
        self.client.post(self.LOGIN_URI, {'email':'nodata@user.com', 'password':'contrasenia'})
        response = self.client.get(reverse('kiosco_app:home'))
        self.assertRedirects(response, reverse('DaneUsers:modifyUserData'))           
        
    def test_allows_user_logout_even_if_has_no_completed_user_profile_form(self):
        User.objects.create_user("nodata@user.com", "contrasenia")
        self.client.post(self.LOGIN_URI, {'email':'nodata@user.com', 'password':'contrasenia'})
        self.client.get(reverse('DaneUsers:logout'))
        self.assertNotIn('_auth_user_id', self.client.session)
        
    def test_when_validations_fail_send_form_with_errorlist(self):
        response =  self.client.post(self.LOGIN_URI,   {'email':'nodata@user.com', 'password':''} )
        error = '<ul class="errorlist"><li>This field is required.</li></ul>'
        self.assertIn(error, response.content)
        
    def test_when_user_exists_and_fail_send_form_with_errorlist(self):
        response = self.client.post(self.LOGIN_URI, {'email':'email@email.com', 'password':'wrongpassword'} )
        error = '<ul class="errorlist nonfield"><li>Please enter a correct email address and password. Note that both fields may be case-sensitive.</li></ul>'
        self.assertIn(error, response.content)        
        
class TestRedirectWithNextParameter(test_base):
    def setUp(self):
        cache.clear()        
        test_base.setUp(self)
        self.create_user()
        self.LOGIN_URI = reverse('DaneUsers:login')
        self.default_user_credentials = {'email':'email@email.com', 'password':'password'}
        self.wrongCredentials = {'email':'usuario@erroneo.com', 'password':'contrasenia'}

    def login_default_user(self):
        return self.client.login(email='email@email.com', password='password')
        
    def get_default_user(self):
        return User.objects.get(email='email@email.com')
    
    def test_redirects_correctly_when_given_next_parameter(self):
        data = self.default_user_credentials.copy()
        data["next"] = reverse('DaneUsers:modifyUserData')
        response = self.client.post(self.LOGIN_URI, data)
        self.assertRedirects(response, reverse('DaneUsers:modifyUserData'))  
    
    def test_passes_next_get_parameter_to_the_template(self):
        response = self.client.get(self.LOGIN_URI + "?next=/some_page/")
        self.assertEqual(response.context["next"], "/some_page/")
        