'''
Created on 23/10/2015

@author: ejarizar
'''
import unittest
from apps.DaneUsers.tests.test_base import test_base
from django.core.urlresolvers import reverse
from apps.statistical_society.forms import SEPreferencesForm
from apps.statistical_society.models import StatisticalSocietyUserPreference
from django.contrib.auth import get_user_model
from apps.DaneUsers.models import UserProfile
User = get_user_model()

class RegisteUserTestBase(test_base):
    REQUEST_URI = reverse('statistical_society:register_user')
        
    def get_default_user(self):
        return User.objects.get(email="email@email.com")
    
    def setUp(self):
        test_base.setUp(self)
        self.data["use_of_info"] = "because YOLO"
        self.data["suscription_media"] = "because YOLO"
        self.data["password1"] = "password"
        self.data["password2"] = "password"

class CreateUsersTest(RegisteUserTestBase):
        
    def test_to_creation_page_is_passed_user_preferences_form(self):
        response = self.client.get(self.REQUEST_URI)
        self.assertIsInstance(response.context["forms"]["user_preferences_form"], SEPreferencesForm)
     
    def test_creates_user_when_data_is_sent(self):        
        self.client.post(self.REQUEST_URI, self.data)
        self.assertTrue(User.objects.filter(email="email@email.com").exists(), "User hasn't been created")
    
    def test_user_created_belongs_to_statistical_society_user_group_by_default(self):
        self.client.post(self.REQUEST_URI, self.data)
        user = self.get_default_user()
        self.assertTrue(user.groups.filter(name='statistical_society_user').exists(), "User does not belong to group")
         
    def test_modify_data_page_contains_register_template(self):
        response = self.client.get(self.REQUEST_URI)
        self.assertTemplateUsed(response, 'statistical_society/register.html')

    def test_statistical_society_user_preferences_are_vreated_with_the_user(self):
        self.client.post(self.REQUEST_URI, self.data)
        user = self.get_default_user()
        statistical_society_members_preferences_asociated = StatisticalSocietyUserPreference.objects.filter(user=user)
        self.assertGreater(len(statistical_society_members_preferences_asociated),0)

    def test_modifies_members_preferences_model_data_when_logged_and_post(self): 
        self.data['want_cell_messages'] = "on"
        self.client.post(self.REQUEST_URI, self.data)     
        self.client.login(email='email@email.com', password='password') 
        response = self.client.get(self.REQUEST_URI)   
        self.assertTrue(response.context["forms"]["user_preferences_form"].initial['want_cell_messages'])

    def test_user_profile_is_not_passed_in_context(self):
        response = self.client.get(self.REQUEST_URI)   
        self.assertNotIn("userProfile", response.context)
        
class LoggedUsersTest(RegisteUserTestBase):
           
    def setUp(self):
        RegisteUserTestBase.setUp(self)
        self.client.post(reverse('DaneUsers:registerUser'), self.data)
        self.client.login(email='email@email.com', password='password')    
        
    def test_already_existent_user_belongs_to_statistical_aociety_user_group_when_modified(self):                 
        self.client.post(self.REQUEST_URI, self.data)
        user = self.get_default_user()
        self.assertTrue(user.groups.filter(name='statistical_society_user').exists(), "User does not belong to group")
        
           
    def test_already_existent_user_got_preferences_model_associated(self):
        self.client.post(self.REQUEST_URI, self.data)
        user = self.get_default_user()
        statistical_society_members_preferences_asociated = StatisticalSocietyUserPreference.objects.filter(user=user)
        self.assertGreater(len(statistical_society_members_preferences_asociated),0)

    def test_does_not_modifies_data_from_logged_users(self):   
        self.data["first_name"] = "Another Name"  
        self.client.post(self.REQUEST_URI, self.data)
        user = self.get_default_user()
        self.assertEqual(user.first_name, "Un")                
        
    def test_only_validates_service_request_form_when_logged(self):    
        self.data["first_name"] = ""  
        self.client.post(self.REQUEST_URI, self.data)
        user = self.get_default_user()
        services_requests_list = StatisticalSocietyUserPreference.objects.filter(user=user)
        self.assertGreater(len(services_requests_list),0, "did not created a new request as expected")   

    def test_user_profile_is_passed_in_context(self):
        response = self.client.get(self.REQUEST_URI)         
        expectedUser = self.get_default_user()
        self.assertEqual(response.context['userProfile'], UserProfile.objects.get(user = expectedUser))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()