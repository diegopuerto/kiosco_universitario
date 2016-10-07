'''
Created on 13/08/2015

@author: EJArizaR
'''
from django import forms
from django.contrib.auth import get_user_model, authenticate
from models import UserProfile
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import models
from django.contrib.auth.forms import AuthenticationForm
User = get_user_model()

def validate_email_is_not_from_dane(email):
    if email.split("@")[-1].lower() == "dane.gov.co":
        raise ValidationError(_('If you have an accoun from dane.gov.co server,\
                             please try login with your credentials instead creating an account'))
        
def validate_alternative_mail_is_not_used_for_someones_login(alternative_mail):
    if len(User.objects.filter(email = alternative_mail)) > 0:
        raise ValidationError(_('This email is already in use'))
     
def validate_login_mail_is_not_used_for_someones_alternative(email):
    if len(UserProfile.objects.filter(alternative_mail = email)) > 0:
        raise ValidationError(_('This email is already in use'))  
    
def validate_user_with_email_exists(email): 
    if not User.objects.filter(email = email).exists():
        raise ValidationError(_('This email does not exists')) 
        


#WARNING: NOT TESTED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class ModelCssClassForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs["placeholder"] = field.label
            
class UserLoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=64,
                                help_text="The person's email address.",
                                label=_('E-mail'),
                                validators=[validate_user_with_email_exists])

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(email=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
    
    def __init__(self,*args, **kwargs):
        new_kwargs = kwargs
        if "data" in kwargs.keys():
            data = kwargs["data"].dict()
            data["username"] = data["email"]
            new_kwargs["data"] = data
        super(UserLoginForm, self).__init__(*args, **new_kwargs)        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs["placeholder"] = field.label   
               
class UserCreateForm(ModelCssClassForm):    
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput())
    email = forms.EmailField(label=_('E-mail'), required=True, validators=[validate_email_is_not_from_dane,
                                                        validate_login_mail_is_not_used_for_someones_alternative])
    first_name = forms.CharField(label=_('Names'), required = True)
    last_name = forms.CharField(label=_('Surnames'), required = True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name')
        
class UserModifyForm(ModelCssClassForm):
    first_name = forms.CharField(label=_('Names'), required = True)
    last_name = forms.CharField(label=_('Surnames'), required = True)
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name')
        
class UserDataBaseForm(ModelCssClassForm):        
    disability        = forms.ModelChoiceField(models.DisabilityType.objects.all(), empty_label=  _("(Choose one if applies)"), required=False)       
    pass
    
        
class UserDataCitizenForm(UserDataBaseForm):
    class Meta:
        model = UserProfile
        fields = ['city', 'departament']
        exclude = ('user','alternative_mail')
        
class UserDataServantForm(UserDataBaseForm):
    alternative_mail = forms.EmailField(required=True, validators=[validate_email_is_not_from_dane,
                                                                   validate_alternative_mail_is_not_used_for_someones_login],
                                                                   label=  _("alternative mail") )
    class Meta:
        model = UserProfile
        fields = ['city', 'departament', 'alternative_mail']
        exclude = ('user',)


class UserDataModifyCitizenForm(UserDataBaseForm):
    class Meta:
        model = UserProfile
        exclude = ('user','alternative_mail')

class UserDataModifyServantForm(UserDataBaseForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

