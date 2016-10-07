'''
Created on 21/10/2015

@author: ejarizar
'''
import unittest
from apps.DaneUsers.tests.test_base import test_base
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.http.response import HttpResponseRedirect
from django.contrib.auth import get_user_model
from unittest.case import skip
from apps.statistical_society.forms import SearchUsersForm
from apps.DaneUsers.models import UserProfile
User = get_user_model()

class SearchUserGETTest(test_base):


    def setUp(self):
        test_base.setUp(self)
        self.client.post(reverse('DaneUsers:registerUser'), self.data)


    def tearDown(self):
        pass


    def test_if_user_does_not_belong_to_statistical_society_reader_is_redirected_to_login(self):
        self.client.login(email='email@email.com', password='password')
        response = self.client.get(reverse('statistical_society:search_user'))     
        self.assertRedirects(response, reverse('DaneUsers:login'), target_status_code= 302)
        
    def test_if_user_belongs_to_statistical_society_reader_is_not_redirected(self):
        user = self.client.login(email='email@email.com', password='password')
        statistical_society_reader = Group.objects.get(name='statistical_society_reader')
        statistical_society_reader.user_set.add(user)
        response = self.client.get(reverse('statistical_society:search_user'))     
        self.assertNotIsInstance(response, HttpResponseRedirect)
    
    def test_to_login_page_is_passed_user_profile_form(self):
        user = self.client.login(email='email@email.com', password='password')
        statistical_society_reader = Group.objects.get(name='statistical_society_reader')
        statistical_society_reader.user_set.add(user)
        response = self.client.get(reverse('statistical_society:search_user'))
        self.assertIsInstance(response.context["search_form"], SearchUsersForm) 
        
        
class SearchUserPOSTTest(test_base):



    def _add_id_doc_to_user(self, id_doc, email):
        user = User.objects.get(email=email)
        profile = UserProfile.objects.get(user=user)
        profile.id_doc = id_doc
        profile.save()

    def setUp(self):
        test_base.setUp(self)
        self.client.post(reverse('DaneUsers:registerUser'), self.data)
        id_doc = self.data["id_doc"]        
        email = "email@email.com"
        self._add_id_doc_to_user(id_doc, email)
    

    def tearDown(self):
        pass 

    def _create_statistical_society_user(self, id_doc, email, first_name, add_to_SE = True):
        newdata = self.data.copy()        
        newdata['id_doc'] = id_doc
        newdata['email'] = email
        newdata['first_name'] = first_name
        self.create_user(newdata)
        if add_to_SE:        
            statistical_society_user = Group.objects.get(name='statistical_society_user')
            user = User.objects.get(email=email)
            statistical_society_user.user_set.add(user)
        self._add_id_doc_to_user(id_doc, email)   
        

    def _create_and_login_statistical_society_reader(self):
        user = self.client.login(email='email@email.com', password='password')
        statistical_society_reader = Group.objects.get(name='statistical_society_reader')
        statistical_society_reader.user_set.add(user)

    def test_if_user_does_not_belong_to_statistical_society_reader_is_redirected_to_login(self):
        self.client.login(email='email@email.com', password='password')
        response = self.client.post(reverse('statistical_society:search_user'), data = {"cedulas": "008"})  
        self.assertRedirects(response, reverse('DaneUsers:login'), target_status_code= 302)
        
    def test_to_login_page_is_passed_user_profile_form(self):
        user = self.client.login(email='email@email.com', password='password')
        statistical_society_reader = Group.objects.get(name='statistical_society_reader')
        statistical_society_reader.user_set.add(user)
        response = self.client.post(reverse('statistical_society:search_user'), data = {"cedulas": "008"})
        self.assertIsInstance(response.context["search_form"], SearchUsersForm) 

    def test_get_user_if_in_statistical_society_correctly(self):
        self._create_statistical_society_user("013", "email013@email.com", "Number13")         
        self._create_and_login_statistical_society_reader()
        response = self.client.post(reverse('statistical_society:search_user'), data = {"cedulas": "013"})  
        self.assertEqual(response.context['users'], [
                                                     {"Cedula":u"013","name":"Number13 De", "belongs_to_SE":True}, 
                                                     ])  
    
    def test_get_user_if_not_in_statistical_society_correctly(self):  
        self._create_statistical_society_user("014", "email014@email.com", "Number14", False)    
        self._create_and_login_statistical_society_reader()
        response = self.client.post(reverse('statistical_society:search_user'), data = {"cedulas": "014"})  
        self.assertEqual(response.context['users'], [
                                                     {"Cedula":u"014","name":"Number14 De", "belongs_to_SE":False}, 
                                                     ])  
        
    def test_shows_user_if_does_not_exists(self):  
        self._create_and_login_statistical_society_reader()
        response = self.client.post(reverse('statistical_society:search_user'), data = {"cedulas": "015"})  
        self.assertEqual(response.context['users'], [
                                                     {"Cedula":u"015","name":None, "belongs_to_SE":False}, 
                                                     ])  
    def test_gets_more_than_one_user(self):
        self._create_statistical_society_user("017", "email017@email.com", "Number17")              
        self._create_statistical_society_user("018", "email018@email.com", "Number18")              
        self._create_and_login_statistical_society_reader()
        response = self.client.post(reverse('statistical_society:search_user'), data = {"cedulas": "017,018"})  
        self.assertEqual(response.context['users'], [
                                                     {"Cedula":u"017","name":"Number17 De", "belongs_to_SE":True}, 
                                                     {"Cedula":u"018","name":"Number18 De", "belongs_to_SE":True}, 
                                                     ])  
           
    def test_separate_cedulas_by_spaces(self):
        self._create_statistical_society_user("017", "email017@email.com", "Number17")              
        self._create_statistical_society_user("018", "email018@email.com", "Number18")              
        self._create_and_login_statistical_society_reader()
        response = self.client.post(reverse('statistical_society:search_user'), data = {"cedulas": "017 018"})  
        self.assertEqual(response.context['users'], [
                                                     {"Cedula":u"017","name":"Number17 De", "belongs_to_SE":True}, 
                                                     {"Cedula":u"018","name":"Number18 De", "belongs_to_SE":True}, 
                                                     ])  
           
    def test_separate_cedulas_by_multiple_separator_characters(self):
        self._create_statistical_society_user("017", "email017@email.com", "Number17")              
        self._create_statistical_society_user("018", "email018@email.com", "Number18")              
        self._create_and_login_statistical_society_reader()
        response = self.client.post(reverse('statistical_society:search_user'), data = {"cedulas": "017,,  ,,  ,018"})  
        self.assertEqual(response.context['users'], [
                                                     {"Cedula":u"017","name":"Number17 De", "belongs_to_SE":True}, 
                                                     {"Cedula":u"018","name":"Number18 De", "belongs_to_SE":True}, 
                                                     ])  
           

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()