'''
Created on 1/12/2015

@author: EJArizaR
'''
from apps.DaneUsers.views.ProfileManagerView import ProfileManagerMixinView
from django.core.mail.message import EmailMultiAlternatives
from libs.user_info_extractor.UserInfoExtractor import UserInfoExtractor
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator  
import win_inet_pton #Necessary for make get_ip work in windows         
from ipware.ip import get_ip

class ServicesRequestBase(ProfileManagerMixinView):
    '''
    classdocs
    '''
    template_name = None
    request_form = None
    
    def get_form_classes(self, user):
        forms = ProfileManagerMixinView.get_form_classes(self, user)
        forms["services_request_form"] = self.request_form
        return forms

    def save(self, forms, request):
        if not request.user.is_authenticated():
            user_form = forms['user_form']
            user = user_form.save()
            ProfileManagerMixinView.save(self, forms, request)
        else:
            user = request.user
        request_instance = self.craft_request(forms, user)
        ip = get_ip(request) 
        request_instance.from_ip = ip
        request_instance.save()
        self._send_mail_request(user, request_instance)     
    
    def _send_mail_request(self, user, request_instance):
        userInfoExtractor = UserInfoExtractor()
        userInfo = userInfoExtractor.extract(user)
        body = userInfo + request_instance.detail
        mail = EmailMultiAlternatives(self.get_subject(request_instance.service), body, 'from@example.com', ["contacto@dane.gov.co"])   
        mail.send()
        
    def are_forms_valid(self, forms):
        return forms["services_request_form"].is_valid()
    
    def get_context_data(self, **kwargs):
        context = super(ServicesRequestBase, self).get_context_data(**kwargs)
        if context["forms"]["user_form"].instance.pk is not None:
            context["userProfile"] = context["forms"]["user_profile_form"].instance
        return context
    
    def craft_request(self, forms, user):
        raise NotImplementedError 
    
    def get_subject(self, subject):
        raise NotImplementedError 
    
    @method_decorator(login_required(login_url='/users/login/'))
    def dispatch(self, *args, **kwargs):
        return super(ServicesRequestBase, self).dispatch(*args, **kwargs)