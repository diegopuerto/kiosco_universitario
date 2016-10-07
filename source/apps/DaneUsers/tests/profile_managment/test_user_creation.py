# -*- coding: utf-8 -*- 
'''
Created on 28/08/2015

@author: EJArizaR
'''
from apps.DaneUsers.models import UserProfile
from apps.DaneUsers.forms import UserCreateForm, UserDataCitizenForm
from django.http.response import HttpResponseRedirect
from django.contrib.auth import get_user_model
from apps.DaneUsers.tests.test_base import test_base
from django.db.utils import IntegrityError
from mock.mock import patch, call
import datetime
from django.utils import timezone
from django.template.loader import get_template
from django.template.context import Context
from django.core.urlresolvers import reverse
import hashlib
User = get_user_model()

class TestRegisterBase(test_base):
    
    REQUEST_URI = reverse('DaneUsers:registerUser')

    def login_default_user(self):
        return self.client.login(email='email@email.com', password='password')
        
    def get_default_user(self):
        return User.objects.get(email="email@email.com")

    def _add_id_doc_to_user(self, email, id_doc):
        user = User.objects.get(email=email)
        profile = UserProfile.objects.get(user=user)
        profile.id_doc = id_doc
        profile.save()

class TestGetMethod(TestRegisterBase):  

    def test_to_creation_page_is_passed_user_form(self):
        response = self.client.get(self.REQUEST_URI)
        self.assertIsInstance(response.context["forms"]["user_form"], UserCreateForm)
        
    def test_to_creation_page_is_passed_user_profile_form(self):
        response = self.client.get(self.REQUEST_URI)
        self.assertIsInstance(response.context["forms"]["user_profile_form"], UserDataCitizenForm)
        
class TestPostMethod(TestRegisterBase):

    def test_creates_user_when_data_is_sent(self):        
        self.client.post(self.REQUEST_URI, self.data)
        self.assertTrue(User.objects.filter(email="email@email.com").exists(), "User hasn't been created")
    
    def test_there_is_a_profile_asociated_at_the_user_just_created(self):
        self.client.post(self.REQUEST_URI, self.data)
        user = self.get_default_user()
        profileAsociated = UserProfile.objects.filter(user=user)
        self.assertGreater(len(profileAsociated),0)         

    def test_does_not_allow_create_two_users_with_same_id_doc(self):
        self.data2 = self.data.copy()
        self.data2["email"] = "email2@email.com"
        self.client.post(self.REQUEST_URI, self.data)
        self._add_id_doc_to_user(self.data["email"], self.data["id_doc"])
        self.create_user(self.data2)
        with self.assertRaises(IntegrityError):
            self._add_id_doc_to_user(self.data2["email"], self.data2["id_doc"])

    def test_user_created_belongs_to_citizens_group_by_default(self):
        self.client.post(self.REQUEST_URI, self.data)
        user = self.get_default_user()
        self.assertTrue(user.groups.filter(name='citizen').exists(), "User does not belong to citizen group")

    def test_user_created_does_not_belongs_to_servants_group_by_default(self):
        self.client.post(self.REQUEST_URI, self.data)
        user = self.get_default_user()
        self.assertFalse(user.groups.filter(name='servant').exists(), "User does belong to servant group")

    def test_cannot_use_login_mail_if_its_used_by_another_user_as_alternative(self):
        User.objects.create_user(email="nodata@dane.gov.co", password="password") 
        self.client.login(email='nodata@dane.gov.co', password='password')         
        newData = self.data.copy()
        newData["id_doc"] = '9999'
        newData["email"] = 'nodata@dane.gov.co'
        newData["alternative_mail"] = 'email@email.com'
        self.client.post(reverse("DaneUsers:modifyUserData"), newData)
        self.client.logout()
        self.client.post(self.REQUEST_URI, self.data)
        self.assertEqual(0, len(User.objects.filter(email = "email@email.com")))  
        
    def test_user_is_logged_when_registers_correctly(self):
        self.client.post(self.REQUEST_URI, self.data)
        self.assertIn('_auth_user_id', self.client.session)    

      
    @patch("apps.DaneUsers.views.ProfileManagerView.random")        
    def test_activation_key_is_correctly_set(self, random_mock):
        random_mock.random.return_value = 0
        expected_salt = hashlib.sha1(str(random_mock.random())).hexdigest()[:5]
        expected_activation_key = str(hashlib.sha1(expected_salt + self.data["email"]).hexdigest())
        self.client.post(self.REQUEST_URI, self.data)
        user = User.objects.get(email = "email@email.com")
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(expected_activation_key, user.activation_key)
        

    #    If you find a way for doing this without depending on current time, please implement it
    #    Sorry for being so CHAMBÓN
    def test_expiration_date_is_correctly_set(self):
        account_activation_days = 7
        self.client.post(self.REQUEST_URI, self.data)
        
        user = User.objects.get(email = "email@email.com")
        profile = UserProfile.objects.get(user=user)
        activation_delta_time = abs(user.key_expires - timezone.now())
        self.assertAlmostEqual(abs(activation_delta_time - datetime.timedelta(account_activation_days)).total_seconds(),0,delta=1000)


@patch("apps.DaneUsers.views.ProfileManagerView.EmailMultiAlternatives")
class DeactivateUserMailTest(TestRegisterBase):
    
    def test_create_mail_when_account_created(self, mocked_send_mail):
        self.client.post(self.REQUEST_URI, self.data)
        user = User.objects.get(email = "email@email.com")
        profile = UserProfile.objects.get(user=user)
        email_body = "Hello, %s, and thanks for signing up for a\
                    kiosco account!\n\nTo activate your account, click this link within 48\
                    hours:\n\n%s" % (
                user.email,
                "http://testserver" + reverse("DaneUsers:confirm", kwargs={"activation_key":user.activation_key}))
        mocked_send_mail.assert_called_with('Account Created', 
                                            email_body, 
                                            'from@example.com', 
                                            ["email@email.com"])

    def test_confirm_mail_contains_deactivate_mail_template(self, mocked_send_mail):
        self.client.post(self.REQUEST_URI, self.data)
        user = User.objects.get(email = "email@email.com")
        profile = UserProfile.objects.get(user=user)
        email_template =  get_template("DaneUsers/mail/confirm.html")
        email_html = email_template.render({"user":user,
                                            "activation_key": user.activation_key,
                                            "protocol": "http",
                                            "domain": "testserver"})
        mocked_send_mail().attach_alternative.assert_called_with(email_html, "text/html")
         
    def test_sends_mail_for_confirm_account(self, mocked_send_mail):
        self.client.post(self.REQUEST_URI, self.data)
        self.assertTrue(mocked_send_mail().send.called)
 
    def test_send_mail_at_last(self, mocked_send_mail):
        self.client.post(self.REQUEST_URI, self.data)     
        last_call = mocked_send_mail().mock_calls[-1]
        expected_last_call =  call.send()
        self.assertEqual(last_call, expected_last_call)      

class TestValidationFails(TestRegisterBase):
    
    def test_if_user_profile_form_does_not_validate_remains_on_creation_page(self):
        self.data["city"] =  "";
        response = self.client.post(self.REQUEST_URI, self.data)
        self.assertNotIsInstance(response, HttpResponseRedirect)  

    def test_if_user_form_does_not_validate_remains_on_creation_page(self):
        self.data["email"] =  "";
        response = self.client.post(self.REQUEST_URI, self.data)
        self.assertNotIsInstance(response, HttpResponseRedirect)  

    def test_when_validations_fail_on_user_profile_form_send_form_with_errorlist(self):
        self.data['city'] =  "";
        response = self.client.post(self.REQUEST_URI, self.data)
        error = '<ul class="errorlist"><li>This field is required.</li></ul>'
        self.assertIn(error, response.content) 
        
    def test_when_validations_fail_on_user_form_send_form_with_errorlist(self):
        self.data["email"] =  "";
        response = self.client.post(self.REQUEST_URI, self.data)
        error = '<ul class="errorlist"><li>This field is required.</li></ul>'
        self.assertIn(error, response.content) 

class TestRedirectWithNextParameter(TestRegisterBase):
    def test_redirects_correctly_when_given_next_parameter(self):
        self.data["next"] = reverse('DaneUsers:logged')
        response = self.client.post(self.REQUEST_URI, self.data)
        self.assertRedirects(response, reverse('DaneUsers:logged'))  

    def test_passes_next_get_parameter_to_the_template(self):
        response = self.client.get(self.REQUEST_URI + "?next=/some_page/")
        self.assertEqual(response.context["next"], "/some_page/")