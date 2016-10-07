# -*- coding: utf-8 -*- 
'''
Created on 28/08/2015

@author: EJArizaR
'''
from django.core.urlresolvers import reverse
from unittest.case import skip
from apps.DaneUsers.models import UserProfile
from apps.DaneUsers.forms import UserDataCitizenForm, UserModifyForm, UserDataModifyCitizenForm
from django_countries.fields import Country
from django.http.response import HttpResponseRedirect
from django.contrib.auth import get_user_model
from apps.DaneUsers.tests.test_base import test_base
User = get_user_model()


class test_modify_user_data(test_base): 

    def setUp(self):
        test_base.setUp(self)
        self.create_user()
        
    def login_default_user(self):
        return self.client.login(email='email@email.com', password='password')
    
    def test_uses_profile_modification_form_for_users_when_user_is_logged(self):
        self.login_default_user()
        response = self.client.get(reverse("DaneUsers:modifyUserData"))
        self.assertIsInstance(response.context["forms"]["user_profile_form"], UserDataModifyCitizenForm)
        
    def test_modifies_user_profile_when_logged_and_post_userdataform(self):          
        self.login_default_user()
        modifiedData = self.data.copy()
        modifiedData['city'] = "01002"
        self.client.post(reverse("DaneUsers:modifyUserData"), modifiedData)
        user = User.objects.get(email='email@email.com')
        userProfile = UserProfile.objects.get(user = user)
        self.assertEqual(userProfile.city.name, "City002")
       
    def test_modifies_user_model_data_when_logged_and_post_userform(self):          
        self.login_default_user()
        modifiedData = self.data.copy()
        modifiedData['first_name'] = "One"
        self.client.post(reverse("DaneUsers:modifyUserData"), modifiedData)
        user = User.objects.get(email="email@email.com")
        self.assertEqual(user.first_name, "One")
        
    def test_redirects_user_when_modified(self):
        self.login_default_user()
        modifiedData = self.data.copy()
        modifiedData['middle_name'] = "Sutano"
        response = self.client.post(reverse('DaneUsers:modifyUserData'),  modifiedData)
        self.assertRedirects(response, reverse('DaneUsers:userModified'))
        
    def test_if_user_profile_form_does_not_validate_does_not_redirect(self):
        self.login_default_user()
        modifiedData = self.data.copy()
        modifiedData["city"] =  "";
        response = self.client.post(reverse("DaneUsers:modifyUserData"), modifiedData)
        self.assertNotIsInstance(response, HttpResponseRedirect)        

    def test_if_user_form_does_not_validate_does_not_redirect(self):
        self.login_default_user()
        modifiedData = self.data.copy()
        modifiedData["first_name"] =  "";
        response = self.client.post(reverse("DaneUsers:modifyUserData"), modifiedData)
        self.assertNotIsInstance(response, HttpResponseRedirect)        
        
    def test_modify_data_page_contains_register_template(self):
        self.login_default_user()
        response = self.client.get(reverse('DaneUsers:modifyUserData'))
        self.assertTemplateUsed(response, 'DaneUsers/modifyUserData.html')

    def test_to_register_page_is_passed_user_form(self):
        self.login_default_user()
        response = self.client.get(reverse('DaneUsers:modifyUserData'))
        self.assertIsInstance(response.context["forms"]["user_form"], UserModifyForm)

    
    def test_user_form_is_loaded_with_initial_values(self):
        self.login_default_user()
        response = self.client.get(reverse('DaneUsers:modifyUserData'))
        expectedData = {'first_name':'Un', 'last_name':'De'}
        self.assertDictEqual(expectedData, response.context["forms"]["user_form"].initial)
        
    def test_user_dane_form_is_loaded_with_initial_values(self):
        self.login_default_user()
        response = self.client.get(reverse('DaneUsers:modifyUserData'))
        expectedData = {'id_type':1,
                        'id_doc':u'666',
                        'cellphone': u'1234567890',
                        'gender':True,
                        'age_range':1,
                        'place_of_birth':Country(code=u"CO"),
                        'education': 1,
                        'activity':1,
                        u'id':1,}


   
    def test_when_user_with_no_data_given_set_fields_blank(self):
        user_with_no_data = User.objects.create_user("nodata@user.com", "password")
        self.client.login(email='nodata@user.com', password='password')
        response = self.client.get(reverse('DaneUsers:modifyUserData'))
        self.assertDictEqual({}, response.context["forms"]["user_profile_form"].initial)
        
    def test_after_create_user_data_keeps_logged(self):
        user_with_no_data = User.objects.create_user("nodata@user.com", "password")  
        self.client.login(email='nodata@user.com', password='password')      
        newData = self.data.copy()
        newData["id_doc"] = '999'
        newData["email"] = 'nodata@user.com'
        response = self.client.post(reverse("DaneUsers:modifyUserData"), newData)
        self.assertIn('_auth_user_id', self.client.session)
             
    def test_when_user_data_does_not_exists_to_register_page_is_passed_user_modify_form(self):
        User.objects.create_user(email="nodata@anyserver.com", password="password")  
        response = self.client.post(reverse("DaneUsers:login"),
                                    {'email':'nodata@anyserver.com', 'password':'password'} , 
                                    follow = True)
        self.assertIsInstance(response.context["forms"]["user_form"], UserModifyForm)

    def test_when_validations_fail_on_user_profile_form_send_form_with_errorlist(self):
        self.login_default_user()
        modifiedData = self.data.copy()
        modifiedData["city"] =  "";
        response = self.client.post(reverse("DaneUsers:modifyUserData"), modifiedData)
        error = '<ul class="errorlist"><li>This field is required.</li></ul>'
        self.assertIn(error, response.content) 

    def test_does_not_modifies_password(self):
        self.login_default_user()
        modifiedData = self.data.copy()
        modifiedData["password"] =  "";       
        self.client.post(reverse("DaneUsers:modifyUserData"), modifiedData)
        self.client.logout()
        self.assertTrue(self.login_default_user())
           
        