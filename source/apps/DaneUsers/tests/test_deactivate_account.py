'''
Created on 28/08/2015

@author: EJArizaR
'''
from django.core.urlresolvers import reverse
from mock import patch
from django.template.loader import get_template
from django.template.context import Context
from mock.mock import call
from django.contrib.auth import get_user_model
from apps.DaneUsers.tests.test_base import test_base
User = get_user_model()

class DeactivateAccountBase(test_base):

    def setUp(self):
        test_base.setUp(self)        
        self.create_user()
        self.DEFAULT_CREDENTIALS = {"email":"email@email.com", "password":"password"}
        self.WRONG_CREDENTIALS = {'email':'usuario@erroneo.com', 'password':'contrasenia'}
        
    def login(self):
        self.client.login(email = "email@email.com", password='password')
        
    def post_for_deactivate_defaul_user(self):
        return self.client.post(reverse('DaneUsers:deactivate'), self.DEFAULT_CREDENTIALS)


class DeactivateAccountTest(DeactivateAccountBase):
    def test_redirect_to_login_page_when_no_logged(self):
        response = self.client.get(reverse('DaneUsers:deactivate'))     
        self.assertRedirects(response, reverse('DaneUsers:login') + "/?next=" + reverse('DaneUsers:deactivate'))        

    def post_for_deactivate_unexistent_user(self):
        return self.client.post(reverse('DaneUsers:deactivate'), self.WRONG_CREDENTIALS)    

    def get_default_user(self):
        return User.objects.get(email="email@email.com")
        
    def test_when_given_correct_credentials_deactivate_account(self):
        self.login()        
        self.post_for_deactivate_defaul_user()
        userDeactivated = User.objects.get(email="email@email.com")
        self.assertFalse(userDeactivated.is_active)

    def test_when_given_wrong_credentials_does_not_deactivate_account(self):
        self.client.login(username='usuario', password='contrasenia')        
        self.client.post(reverse('DaneUsers:deactivate'), {"email":"wrong_user" , "password": "wrong_pass"})
        userDeactivated = self.get_default_user()
        self.assertTrue(userDeactivated.is_active)
        
    def test_when_given_no_email_does_not_deactivate_account(self):
        self.login() 
        self.client.post(reverse('DaneUsers:deactivate'), {"password": "wrong_pass"})
        userDeactivated = self.get_default_user()
        self.assertTrue(userDeactivated.is_active)        

    def test_when_given_invalid_email_does_not_deactivate_account(self):
        self.login() 
        self.client.post(reverse('DaneUsers:deactivate'), {"email": "invalidstuff","password": "wrong_pass"})
        userDeactivated = self.get_default_user()
        self.assertTrue(userDeactivated.is_active)  

    def test_when_logged_opens_the_deactivate_template(self):
        self.login()
        response = self.client.get(reverse('DaneUsers:deactivate')) 
        self.assertIn('DaneUsers/deactivate.html', [t.name for t in response.templates])
        
    def test_when_deactivate_redirect_to_deactivated_page(self):
        self.login()        
        response = self.post_for_deactivate_defaul_user()
        self.assertRedirects(response, reverse('DaneUsers:notActiveUser')) 
              
    def test_when_deactivate_logs_out(self):
        self.login()      
        self.post_for_deactivate_defaul_user()
        self.assertNotIn('_auth_user_id', self.client.session)  

    def test_redirects_correctly_when_given_wrong_credentials(self):
        self.login()    
        response = self.post_for_deactivate_unexistent_user()
        self.assertRedirects(response, reverse('DaneUsers:deactivate') +'?wrongCredentials=True')
        
    def test_does_not_deactivate_account_when_user_given_is_not_the_authenticated_user(self):
        User.objects.create_user( "corre2@forest.com", "contrasenia")
        self.login()   
        response = self.client.post(reverse('DaneUsers:deactivate'), {"email":"corre2@forest.com" , "password": "contrasenia"})
        self.assertRedirects(response, reverse('DaneUsers:deactivate') +'?wrongCredentials=True')        
        
        
@patch("apps.DaneUsers.views.DeactivateUserView.EmailMultiAlternatives")
class DeactivateUserMailTest(DeactivateAccountBase):
    def test_create_mail_when_account_deactivated(self, mocked_send_mail):
        self.login()   
        self.post_for_deactivate_defaul_user()
        mocked_send_mail.assert_called_with('Deactivated Account', 
                                            'Your account has been deactivated', 
                                            'from@example.com', 
                                            ["email@email.com"])

    def test_deactivated_mail_contains_deactivate_mail_template(self, mocked_send_mail):
        self.login()      
        self.post_for_deactivate_defaul_user()
        email_template =  get_template("DaneUsers/mail/deactivate.html")
        email_html = email_template.render({})
        mocked_send_mail().attach_alternative.assert_called_with(email_html, "text/html")
        
    def test_sends_mail_for_deactivated_accounts(self, mocked_send_mail):
        self.login()       
        self.post_for_deactivate_defaul_user()
        self.assertTrue(mocked_send_mail().send.called)

    def test_send_mail_at_last(self, mocked_send_mail):
        self.login()      
        self.client.post(reverse('DaneUsers:deactivate'), self.DEFAULT_CREDENTIALS)        
        last_call = mocked_send_mail().mock_calls[-1]
        expected_last_call =  call.send()
        self.assertEqual(last_call, expected_last_call)
        
        