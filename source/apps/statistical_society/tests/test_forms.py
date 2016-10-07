from apps.statistical_society.forms import StatisticalSocietyUserForm
from django.contrib.auth import get_user_model
from apps.DaneUsers.tests.test_base import test_base
User = get_user_model()

# Create your tests here.

# DjangoTestSuiteRunner

class testStatisticalSocietyUserForm(test_base):
    def test_creates_user_with_usable_password(self):
        userForm = StatisticalSocietyUserForm({'email':"user@anyserver.com", 
                                "first_name":"Billy", 
                                "last_name": "Pendiado",
                                "password1":"password",
                                "password2":"password"
                                })
        userForm.save()
        user = User.objects.get(email = "user@anyserver.com")
        self.assertTrue(user.has_usable_password())
        
    def test_users_created_belongs_to_statistical_society_user(self):
        userForm = StatisticalSocietyUserForm({'email':"user@anyserver.com", 
                                "first_name":"Billy", 
                                "last_name": "Pendiado",
                                "password1":"password",
                                "password2":"password"})
        userForm.save()
        user = User.objects.get(email = "user@anyserver.com")
        self.assertTrue(user.groups.filter(name='statistical_society_user').exists(), "User does not belong to group")
        
    def test_shows_correct_error_message_when_email_already_exists(self):
        User.objects.create(email="already@exists.com")
        userForm = StatisticalSocietyUserForm({'email':"already@exists.com", "first_name":"Billy", "last_name": "Pendiado"})
        self.assertTrue(u'this email already exists: if you already have an account please login' in userForm.errors.as_data()["email"][0])
        
        
        
        