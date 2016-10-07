'''
Created on 23/03/2016

@author: ejarizar
'''
from registration.signals import user_registered
from forms import UserCreateForm, UserDataCitizenForm, UserModifyForm,\
    UserDataServantForm
from django.contrib.auth import get_user_model
User = get_user_model()

def get_form_classes(self, user):
    form_classes = {'user_form':UserCreateForm,
            'user_profile_form':UserDataCitizenForm}
    if isinstance(user, get_user_model()):
        form_classes['user_form'] = UserModifyForm
        if self._is_servant(user):
            form_classes['user_profile_form'] = UserDataServantForm
        else:          
            form_classes['user_profile_form'] = UserDataCitizenForm                
    return form_classes 
    
def create_profile(sender, instance, request, **kwargs):

        print request
        user= instance
        print "hey!"
        forms = get_form_classes(user)
        data_instance = forms['user_profile_form'].save(commit=False)
        data_instance.user = user
        data_instance.save()
        

user_registered.connect(create_profile)