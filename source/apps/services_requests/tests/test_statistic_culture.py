'''
Created on 2/12/2015

@author: EJArizaR
'''
from apps.DaneUsers.tests.test_base import test_base
from apps.services_requests.forms import StatisticalCultureForm
from django.core.urlresolvers import reverse
from apps.services_requests.models import StatisticalCultureRequest,\
    SpecializedChamberRequest
from libs.user_info_extractor.UserInfoExtractor import UserInfoExtractor
from mock.mock import patch, call
from unittest.case import skip
from apps.DaneUsers.models import UserProfile
from django.contrib.auth import get_user_model
User = get_user_model()


class StatisticCultureTestBase(test_base):
    REQUEST_URI = reverse('services_requests:statisticalCulture')
    REQUEST_MODEL = SpecializedChamberRequest
    
    def setUp(self):
        test_base.setUp(self)
        self.data["detail"] = "because YOLO"
        
    def get_default_user(self):
        return User.objects.get(email="email@email.com")
    

class NotLoggedUserTest(StatisticCultureTestBase):

    def test_reditects_to_logged_view(self):
        response = self.client.get(self.REQUEST_URI)
        self.assertRedirects(response, reverse('DaneUsers:login') + "/?next=" + self.REQUEST_URI)   

class LoggedUserTest(StatisticCultureTestBase):
    REQUEST_MODEL = StatisticalCultureRequest
    
    def setUp(self):
        StatisticCultureTestBase.setUp(self)
        self.data["service"] = "1"
        self.client.post(reverse('DaneUsers:registerUser'), self.data)
        self.client.login(email='email@email.com', password='password')  
        
    def test_modify_data_page_contains_correct_template(self):
        response = self.client.get(self.REQUEST_URI)
        self.assertTemplateUsed(response, 'services_requests/statistical_culture.html')

    def test_is_passed_ServicesRequestForm(self):
        response = self.client.get(self.REQUEST_URI)
        self.assertIsInstance(response.context["forms"]["services_request_form"], StatisticalCultureForm)

    def test_saves_request_with_the_correct_subject(self):
        self.client.post(self.REQUEST_URI, self.data)        
        user = self.get_default_user()
        SpecializedChamberRequest = self.REQUEST_MODEL.objects.get(user=user)
        self.assertEqual(str(SpecializedChamberRequest.service), "Dane in Academics")   
        
    def test_does_not_modifies_data_from_logged_users(self):
        self.data["first_name"] = "Another Name"  
        self.client.post(self.REQUEST_URI, self.data)
        user = self.get_default_user()
        self.assertEqual(user.first_name, "Un")      
        
    def test_only_validates_service_request_form_when_logged(self):  
        self.data["first_name"] = ""  
        self.client.post(self.REQUEST_URI, self.data)
        user = self.get_default_user()
        services_requests_list = self.REQUEST_MODEL.objects.filter(user=user)
        self.assertGreater(len(services_requests_list),0, "did not created a new request as expected")   
         
    def test_user_profile_is_passed_in_context(self):
        response = self.client.get(self.REQUEST_URI)         
        expectedUser = self.get_default_user()
        self.assertEqual(response.context['userProfile'], UserProfile.objects.get(user = expectedUser))
    
    def test_saves_request_in_database(self):
        self.client.post(self.REQUEST_URI, self.data)
        user = self.get_default_user()
        services_requests_list = self.REQUEST_MODEL.objects.filter(user=user)
        self.assertGreater(len(services_requests_list),0)
        
    def test_an_user_can_do_multiple_requests_in_database(self):
        self.client.post(self.REQUEST_URI, self.data)    
        self.client.post(self.REQUEST_URI, self.data)
        user = self.get_default_user()
        services_requests_list = self.REQUEST_MODEL.objects.filter(user=user)
        self.assertEqual(len(services_requests_list),2)

    def test_user_cannot_close_request_from_form(self):
        self.data["is_closed"] = True
        self.client.post(self.REQUEST_URI, self.data)        
        user = self.get_default_user()
        SpecializedChamberRequest = self.REQUEST_MODEL.objects.get(user=user)
        self.assertFalse(SpecializedChamberRequest.is_closed)

@patch("apps.services_requests.views.ServicesRequesterBase.EmailMultiAlternatives")
class MailTest(StatisticCultureTestBase):
    def setUp(self):
        StatisticCultureTestBase.setUp(self)
        self.data["service"] = "1"
        self.client.post(reverse('DaneUsers:registerUser'), self.data)
        self.client.login(email='email@email.com', password='password')   
         
    def test_create_mail(self, mocked_send_mail):
        self.client.post(self.REQUEST_URI, self.data) 
        user = self.get_default_user()
        userInfoExtractor = UserInfoExtractor()
        userInfo = userInfoExtractor.extract(user)
        expected_body = userInfo + self.data["detail"]       
        mocked_send_mail.assert_called_with('Dane in Academics', 
                                            expected_body, 
                                            'from@example.com', 
                                            ["contacto@dane.gov.co"])
    
    def test_sends_mail(self, mocked_send_mail):
        self.client.post(self.REQUEST_URI, self.data) 
        self.assertTrue(mocked_send_mail().send.called)
   
    def test_send_mail_at_last(self, mocked_send_mail):
        self.client.post(self.REQUEST_URI, self.data)   
        last_call = mocked_send_mail().mock_calls[-1]
        expected_last_call =  call.send()
        self.assertEqual(last_call, expected_last_call)          

        