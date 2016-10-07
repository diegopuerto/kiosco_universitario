'''
Created on 1/12/2015

@author: EJArizaR
'''
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from apps.DaneUsers.tests.test_base import test_base
from unittest.case import skip
from apps.services_requests.models import SpecializedChamberRequest
from mock.mock import patch
from mock.mock import call
from libs.user_info_extractor.UserInfoExtractor import UserInfoExtractor
from apps.DaneUsers.models import UserProfile
User = get_user_model()


class SpecializedChamberTestBase(test_base):
    REQUEST_URI = reverse('services_requests:specializedChamber')
    REQUEST_MODEL = SpecializedChamberRequest
    
    def setUp(self):
        test_base.setUp(self)
        self.data["detail"] = "because YOLO"
        
    def get_default_user(self):
        return User.objects.get(email="email@email.com")
    
class NotLoggedUserTest(SpecializedChamberTestBase):
    def test_reditects_to_logged_view(self):
        response = self.client.get(self.REQUEST_URI)
        self.assertRedirects(response, reverse('DaneUsers:login') + "/?next=" + self.REQUEST_URI)   


class LoggedUserTest(SpecializedChamberTestBase):   
    def setUp(self):
        SpecializedChamberTestBase.setUp(self)
        self.client.post(reverse('DaneUsers:registerUser'), self.data)
        self.client.login(email='email@email.com', password='password')           
            
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

    def test_saves_request_with_the_correct_subject(self):
        self.client.post(self.REQUEST_URI, self.data)        
        user = self.get_default_user()
        SpecializedChamberRequest = self.REQUEST_MODEL.objects.get(user=user)
        self.assertEqual(SpecializedChamberRequest.service, "Solicitud Sala Especializada")   

    def test_user_cannot_close_request_from_form(self):
        self.data["is_closed"] = True
        self.client.post(self.REQUEST_URI, self.data)        
        user = self.get_default_user()
        SpecializedChamberRequest = self.REQUEST_MODEL.objects.get(user=user)
        self.assertFalse(SpecializedChamberRequest.is_closed)           

    @patch("apps.services_requests.views.ServicesRequesterBase.get_ip")    
    def test_ip_is_saved_in_request(self, mocked_get_ip):
        mocked_get_ip.return_value = "255.255.255.255"
        self.client.post(self.REQUEST_URI, self.data)      
        user = self.get_default_user()
        SpecializedChamberRequest = self.REQUEST_MODEL.objects.get(user=user)       
        self.assertEquals(SpecializedChamberRequest.from_ip, "255.255.255.255")         

       
@patch("apps.services_requests.views.ServicesRequesterBase.EmailMultiAlternatives")
class MailTest(SpecializedChamberTestBase):
    def setUp(self):
        SpecializedChamberTestBase.setUp(self)
        self.client.post(reverse('DaneUsers:registerUser'), self.data)
        self.client.login(email='email@email.com', password='password')   
    
    def test_create_mail(self, mocked_send_mail):
        self.client.post(self.REQUEST_URI, self.data) 
        user = self.get_default_user()
        userInfoExtractor = UserInfoExtractor()
        userInfo = userInfoExtractor.extract(user)
        expected_body = userInfo + self.data["detail"]       
        mocked_send_mail.assert_called_with('Solicitud Sala Especializada', 
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


        


