'''
Created on 23/09/2015

@author: ejarizar
'''
from django.views.generic.base import View
from apps.DaneUsers.forms import UserLoginForm
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from ratelimit.decorators import ratelimit
from django.contrib.auth import login
from apps.DaneUsers.views.UsersGetter import UsersGetter
from django.contrib.auth import get_user_model
from libs.dane_auth_ldap.backend import DaneLDAPBackend
User = get_user_model()

class LoginView(View):
    users_getter = UsersGetter()
    def get(self, request):
        response = render(request, "DaneUsers/login.html",  {'user_login_form':UserLoginForm(), 
                                                             'next' : self.request.GET.get('next',None)})   
        return response

    @ratelimit(key='post:username', rate='2/m', method=['POST'])
    def post(self, request):
        was_limited = getattr(request, 'limited', False)
        user_form = UserLoginForm(data=request.POST)
        if user_form.is_valid():
            return self._get_success_auth_response(user_form)    
        else:          
            return self._get_failed_auth_response(request, was_limited, user_form)   

    def _get_failed_auth_response(self, request, was_limited, user_form):
        response = render(request, "DaneUsers/login.html", {'user_login_form':user_form, "next":self.request.POST.get('next', None)})
        if was_limited:
            response = HttpResponseRedirect(reverse('DaneUsers:recoverPassword'))
        elif User.objects.filter(email=self.request.POST["email"]).exists():
            user = User.objects.get(email=self.request.POST["email"])
            if not user.is_active:
                response = HttpResponseRedirect(reverse('DaneUsers:notActiveUser'))
            elif user.email.split("@")[-1].lower() == "dane.gov.co" and DaneLDAPBackend().populate_user(user.email) == None:
                response = HttpResponseRedirect(reverse('DaneUsers:recoverAccount', kwargs={'user':user.email}))
        return response
             
     
    def _get_success_auth_response(self, user_form):
        user = user_form.get_user()
        login(self.request, user)
        if "next" in self.request.POST:
            return HttpResponseRedirect(self.request.POST["next"])
        return HttpResponseRedirect(reverse('kiosco_app:home'))


    