# -*- coding: utf-8 -*-
'''
Created on 15/10/2015

@author: EJArizaR
'''
from custom_user.forms import EmailUserCreationForm
from django.contrib.auth.models import Group
from django import forms
from apps.statistical_society.models import StatisticalSocietyUserPreference
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from apps.DaneUsers.forms import ModelCssClassForm

class StatisticalSocietyUserForm(EmailUserCreationForm):
    first_name = forms.CharField(max_length=250)
    last_name = forms.CharField(max_length=250)
    error_messages = EmailUserCreationForm.error_messages
    error_messages['duplicate_email'] = _(u'this email already exists: if you already have an account please login')
    
    def save(self, commit = True):
        user = EmailUserCreationForm.save(self, True)
        statistical_society_user_group = Group.objects.get(name='statistical_society_user')
        statistical_society_user_group.user_set.add(user)
        user.save()
        return user
    
class SearchUsersForm(forms.Form):
    cedulas = forms.CharField(max_length=20)
    
class SEPreferencesForm(ModelCssClassForm):
    class Meta:
        model = StatisticalSocietyUserPreference
        exclude = ('user',)
        
class SEUserRegisterForm(StatisticalSocietyUserForm):
    pass

class SEUserModifyForm(StatisticalSocietyUserForm):
    def __init__(self, *args, **kwargs):
        super(StatisticalSocietyUserForm, self).__init__(*args, **kwargs)   
        self.fields.pop("password1")   
        self.fields.pop("password2")   
        
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name')
    
    def save(self, commit=True):
        user = super(forms.ModelForm, self).save(commit=False)
        if commit:
            user.save()
        return user