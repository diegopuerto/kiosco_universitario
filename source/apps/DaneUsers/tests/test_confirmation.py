'''
Created on 29/03/2016

@author: EJArizaR
'''
import unittest
from apps.DaneUsers.tests.test_base import test_base
import hashlib
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from unittest.case import skip
User = get_user_model()

class TestConfirmation(test_base):

    def test_if_user_not_found_return_404(self):
        activation_key =  hashlib.sha1("This is not a valid hash").hexdigest()
        response = self.client.get(reverse("DaneUsers:confirm", kwargs={"activation_key":activation_key}))
        self.assertEqual(response.status_code, 404)
    
    def test_if_activation_key_corresponds_to_an_user_is_confirmed_field_flips_to_true(self):
        self.client.post(reverse('DaneUsers:registerUser'), self.data)
        user = User.objects.get(email=self.data["email"])        
        self.client.get(reverse("DaneUsers:confirm", kwargs={"activation_key":user.activation_key}))
        user_after_confirmation = User.objects.get(email=self.data["email"])  
        self.assertTrue(user_after_confirmation.is_confirmed)      

    def test_uses_apropiated_template(self):
        self.client.post(reverse('DaneUsers:registerUser'), self.data)
        user = User.objects.get(email=self.data["email"])        
        response = self.client.get(reverse("DaneUsers:confirm", kwargs={"activation_key":user.activation_key}))        
        self.assertIn('DaneUsers/validatedAccount.html', [t.name for t in response.templates])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()