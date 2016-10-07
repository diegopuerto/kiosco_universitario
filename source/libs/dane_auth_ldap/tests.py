# -*- coding: utf-8 -*- 
'''
Created on 17/09/2015

@author: EJArizaR
'''
from django.test.testcases import TestCase
from mock.mock import patch, Mock, MagicMock
from unittest.case import skip
from mock import ANY
from libs.dane_auth_ldap.backend import DaneLDAPBackend
from django.contrib.auth import get_user_model
from libs.dane_auth_ldap.config import DaneLDAPSearch
import ldap
User = get_user_model()

 
class MockLdapUser(object):
    attrs = {"displayname": ["Faustino Hernán Asprilla Hinestroza"]}

class MockUser(object):
    ldap_user = MockLdapUser()
    save = MagicMock()


class BackendTest(TestCase):
    @patch("libs.django_auth_ldap.backend._LDAPUser")  
    def test_does_not_call_LDAPUser_when_email_is_not_from_dane(self, _LDAPUserMock):
        backend = DaneLDAPBackend()
        email = "useremail@anyserver.gov.co"
        password = "password"
        backend.authenticate(email = email, password = password)
        _LDAPUserMock.assert_not_called()
    
    @patch("libs.django_auth_ldap.backend._LDAPUser")    
    def test_cn_is_extracted_from_email_and_passed_when_authenticate(self, _LDAPUserMock):
        backend = DaneLDAPBackend()        
        email = "useremail@dane.gov.co"
        password = "password"
        backend.authenticate(email = email, password = password)
        _LDAPUserMock.assert_called_with(ANY, username = "useremail")
        
    @patch("libs.django_auth_ldap.backend.LDAPBackend")    
    def test_email_user_is_setted_correctly(self, backend_parent_mock):
        backend = DaneLDAPBackend()      
        email = "useremail@dane.gov.co"
        backend.get_or_create_user("useremail", ANY)
        user_exists = User.objects.filter(email=email).count() > 0
        self.assertTrue(user_exists)
        
    @patch("libs.dane_auth_ldap.backend.Group")     
    @patch("libs.django_auth_ldap.backend.LDAPBackend.populate_user")      
    def test_populate_user_is_called_in_super_with_correct_dn_given_email(self, populate_user_mock, mockGroup):
        backend = DaneLDAPBackend()      
        email = "useremail@dane.gov.co"
        user =  backend.populate_user(email)
        populate_user_mock.assert_called_with("useremail")

    @patch("libs.dane_auth_ldap.backend.Group")  
    @patch("libs.django_auth_ldap.backend.LDAPBackend.populate_user")  
    def test_when_email_is_from_dane_is_added_to_servant_group(self, backendMock, mockGroup):
        servantMock = MagicMock()
        userMock = MagicMock()
        backendMock.return_value = userMock
        mockGroup.objects.get.return_value = servantMock
        backend = DaneLDAPBackend()      
        email = "useremail@dane.gov.co"
        backend.populate_user(email)
        servantMock.user_set.add.assert_called_with(userMock)

    @patch("libs.dane_auth_ldap.backend.Group") 
    @patch("libs.django_auth_ldap.backend.LDAPBackend.populate_user")         
    def test_when_user_exist_populates_the_first_name(self, populate_user_mock, mockGroup): 
        populate_user_mock.return_value = MockUser()
        backend = DaneLDAPBackend()      
        email = "useremail@dane.gov.co"
        user = backend.populate_user(email)
        self.assertEqual(user.first_name, "Faustino") 
    
    @patch("libs.dane_auth_ldap.backend.Group") 
    @patch("libs.django_auth_ldap.backend.LDAPBackend.populate_user")         
    def test_when_user_exist_populates_the_last_name(self, populate_user_mock, mockGroup): 
        populate_user_mock.return_value = MockUser()
        backend = DaneLDAPBackend()      
        email = "useremail@dane.gov.co"
        user = backend.populate_user(email)
        self.assertEqual(user.last_name, "Asprilla") 
        
    @patch("libs.dane_auth_ldap.backend.Group")         
    @patch("libs.django_auth_ldap.backend.LDAPBackend.populate_user")         
    def test_when_calls_populate_user_saves_user(self, populate_user_mock, mockGroup): 
        mockUser = MockUser()
        populate_user_mock.return_value = mockUser
        backend = DaneLDAPBackend()      
        email = "useremail@dane.gov.co"
        user = backend.populate_user(email)
        mockUser.save.assert_any_call()
        
    @patch("libs.django_auth_ldap.backend.LDAPBackend.populate_user")         
    def test_when_user_is_none_no_values_are_settled(self, populate_user_mock): 
        populate_user_mock.return_value = None
        try:
            backend = DaneLDAPBackend()      
            email = "useremail@dane.gov.co"
            user = backend.populate_user(email)
        except AttributeError:
            self.fail("tried to set values in a nonetype (unexistent) user")
        
        
class DaneLDAPSearchTest(TestCase):
            
    @patch("libs.django_auth_ldap.config.LDAPSearch.execute")       
    def test_when_user_exist_returns_response_from_parent(self, ParentExecute):
        expected_response =  [Mock()]
        ParentExecute.return_value = expected_response
        username = "user"
        search = DaneLDAPSearch("OU=DANE,DC=DANE,DC=GOV,DC=CO",
                                ldap.SCOPE_SUBTREE, "(&(mail=*)(cn=%(user)s))")
        connection = Mock()
        actual_response = search.execute(connection, {'user': username}, True)
        ParentExecute.assert_called_with(connection, filterargs={'user': username}, escape=True)
        self.assertEqual(expected_response, actual_response)
        
