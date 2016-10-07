'''
Created on 24/09/2015

@author: EJArizaR
'''
import hashlib, random
from django.core.urlresolvers import reverse
from apps.DaneUsers.forms import UserCreateForm, UserDataCitizenForm, UserModifyForm,\
    UserDataServantForm, UserDataModifyCitizenForm, UserDataModifyServantForm
from django.contrib.auth.models import Group
from apps.DaneUsers.models import UserProfile
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView
from django.contrib.auth import login
from apps.DaneUsers.views.UsersGetter import UsersGetter
from django.contrib.auth import get_user_model
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import get_template
from django.template.context import Context
from django.contrib.sites.shortcuts import get_current_site
User = get_user_model()

class MultipleFormsMixin(FormMixin):
    """
    A mixin that provides a way to show and handle several forms in a
    request.
    """
    form_classes = {} # set the form classes as a mapping

    def get_form_classes(self, user):
        return self.form_classes

    def get_forms(self, form_classes, request):
        return dict([(key, klass(**self.get_form_kwargs())) \
            for key, klass in form_classes.items()])

    def forms_valid(self, forms):
        return super(MultipleFormsMixin, self).form_valid(forms)

    def forms_invalid(self, forms):
        return self.render_to_response(self.get_context_data(forms=forms, next=self.request.GET.get('next',None)))

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        return kwargs    


class ProcessMultipleFormsView(ProcessFormView):
    """
    A mixin that processes multiple forms on POST. Every form must be
    valid.
    """
    def get(self, request, *args, **kwargs):
        form_classes = self.get_form_classes(request.user)
        forms = self.get_forms(form_classes, request)
        return self.render_to_response(self.get_context_data(forms=forms, next=request.GET.get('next')))

    def post(self, request, *args, **kwargs):
        form_classes = self.get_form_classes(request.user)
        forms = self.get_forms(form_classes, request)
        if self.are_forms_valid(forms):
            return self.forms_valid(forms, request)
        else:
            return self.forms_invalid(forms)

    def are_forms_valid(self, forms):
        return all([form.is_valid() for form in forms.values()])

class BaseMultipleFormsView(MultipleFormsMixin, ProcessMultipleFormsView):
    """
    A base view for displaying several forms.
    """

    def forms_valid(self, forms, request = None):
        self.save(forms, request)
        return MultipleFormsMixin.forms_valid(self, forms)
    
    def save(self, forms, request=None):
        raise NotImplementedError

    
class ProfileManagerMixinView(TemplateResponseMixin, BaseMultipleFormsView):
    """
    A view for displaing several forms, and rendering a template response.
    """
    template_name = "DaneUsers/modifyUserData.html"
    form_classes = {'user_form':UserCreateForm,
                    'user_profile_form':UserDataCitizenForm}
    users_getter = UsersGetter()
     
    def get_success_url(self):
        next_url = self.request.POST.get('next',None)
        if next_url:
            next_page = next_url
        else:
            next_page = reverse('DaneUsers:userModified')
        return next_page

    def save(self, forms, request=None):
        user_form = forms['user_form']
        user = user_form.save()
        self._add_confirmation_account_fields(user)
        if isinstance(user, get_user_model()):
            if not request.user.is_authenticated():
                user.set_password(user.password)
            self._add_user_to_groups(user)
        user.save()
        domain = get_current_site(request).domain
        protocol = 'https' if request.is_secure() else 'http'
        self._save_profile_user(forms, user)
        self._send_confirmation_mail(user, domain, protocol)
        
    def _save_profile_user(self, forms, user):
        user_profile = forms['user_profile_form'].save(commit=False)
        user_profile.user = user
        user_profile.save()
        
    def _add_confirmation_account_fields(self, user):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha1(salt + user.email).hexdigest()
        user.activation_key = activation_key

       
    def _send_confirmation_mail(self, user, domain, protocol):
        email_body = "Hello, %s, and thanks for signing up for a\
                    kiosco account!\n\nTo activate your account, click this link within 48\
                    hours:\n\n%s" % (
                                    user.email,
                                    protocol + "://" + domain + reverse("DaneUsers:confirm", kwargs={"activation_key":user.activation_key}))
        mail = EmailMultiAlternatives('Account Created', email_body, 'from@example.com', [user.email])
        email_template = get_template("DaneUsers/mail/confirm.html")
        email_html = email_template.render({"user":user,
                                            "activation_key": user.activation_key,
                                            "protocol": protocol,
                                            "domain": domain})
        mail.attach_alternative(email_html, "text/html")    
        mail.send()    
                
    def _add_user_to_groups(self, user):
        if self._is_servant(user):
            servant = Group.objects.get(name='servant')
            servant.user_set.add(user)
        else:
            citizen = Group.objects.get(name='citizen')
            citizen.user_set.add(user)
 
    def _is_servant(self, user):
        return user.email.split("@")[-1] == "dane.gov.co"   
     
    def get_form_classes(self, user):
        form_classes = {'user_form':UserCreateForm,
                'user_profile_form':UserDataCitizenForm}
        if isinstance(user, get_user_model()):
            form_classes['user_form'] = UserModifyForm
            if self._is_servant(user):
                form_classes['user_profile_form'] = UserDataServantForm
            else:          
                form_classes['user_profile_form'] = UserDataCitizenForm    
             
            if hasattr(user, "userprofile"):
                if self._is_servant(user):
                    form_classes['user_profile_form'] = UserDataModifyServantForm
                else:          
                    form_classes['user_profile_form'] = UserDataModifyCitizenForm
            
        return form_classes 
          
    def get_forms(self, form_classes, request):
        forms ={}
        for key, klass in form_classes.items():
                forms[key] = klass(**self.get_form_kwargs())       
        if isinstance(request.user, get_user_model()):
            forms["user_form"] = form_classes["user_form"](instance=request.user, **self.get_form_kwargs())
            if UserProfile.objects.filter(user=request.user).exists():
                forms["user_profile_form"] = form_classes["user_profile_form"](instance=UserProfile.objects.get(user=request.user), **self.get_form_kwargs())
        return forms 
    
    def forms_valid(self, forms, request=None):
        response = BaseMultipleFormsView.forms_valid(self, forms, request=request)
        if not isinstance(request.user, User):
            user = self.users_getter.get_autenticathed_user(request)
            login(request, user)
        return response
    
class ProfileManagerView(ProfileManagerMixinView):
    pass

