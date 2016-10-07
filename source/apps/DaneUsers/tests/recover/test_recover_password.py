'''
Created on 23/02/2016

@author: EJArizaR
'''
import unittest
from apps.DaneUsers.tests.test_base import test_base
from mock.mock import patch
from django.core.urlresolvers import reverse
from unittest.case import skip
from django.http.response import HttpResponse


class test_recover_password(test_base):
    
    @patch("apps.DaneUsers.views.PasswordReset.password_reset")
    def test_when_no_dane_mail_given_does_call_reset_password(self, password_reset_mock):
        password_reset_mock.return_value = HttpResponse("")
        response = self.client.post(reverse('DaneUsers:recoverPassword'), {"email": "someuser@notfromdane.gov.co"})
        self.assertTrue(password_reset_mock.called)


    @patch("apps.DaneUsers.views.PasswordReset.password_reset")
    def test_when_dane_mail_given_does_not_call_reset_password(self, password_reset_mock):
        password_reset_mock.return_value = HttpResponse("")
        response = self.client.post(reverse('DaneUsers:recoverPassword'), {"email": "someuser@dane.gov.co"})
        password_reset_mock.assert_not_called()
        
    def test_when_dane_mail_given_uses_right_informative_template(self):
        response = self.client.post(reverse('DaneUsers:recoverPassword'), {"email": "someuser@dane.gov.co"})
        self.assertTemplateUsed(response, 'DaneUsers/ServantCannotChangePassword.html')

