# -*- coding: utf-8 -*- 
'''
Created on 25/09/2015

@author: EJArizaR
'''
from django.test.testcases import TestCase
from django.core.management import call_command
from apps.DaneUsers.models import UserProfile
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
User = get_user_model()

@override_settings( PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',))
class test_base(TestCase):
    @classmethod
    def setUpTestData(cls):   
        call_command("fix_permissions", verbosity=0)
        call_command("initialdata", verbosity=0, is_unittest=True)

    def setUp(self):
        self.data = {'password':'password',
            'email':'email@email.com',
            'id_type':'1',
            'id_doc':'666',
            'first_name':'Un',
            'last_name':'De',
            'cellphone':'1234567890',
            'gender':'True',
            'age_range':'1',
            'place_of_birth':'CO',
            'land_line1': '666',
            'land_line2': '666',
            'education': '1',
            'activity':'1',
            'profession':'1',
            'departament':'01',
            'city':'01001'}
        
    def create_user(self, data = None):
        if data == None:
            data = self.data
        user = User.objects.create_user(data["email"],
                                        data["password"],
                                        first_name = data["first_name"],
                                        last_name = data["last_name"]
                                        )
        user.save()
        profile = UserProfile.objects.create(user=user, departament_id=data["departament"], city_id=data["city"])
        profile.save()
        return user