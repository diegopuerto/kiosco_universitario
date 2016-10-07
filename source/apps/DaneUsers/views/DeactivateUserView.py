'''
Created on 24/09/2015

@author: EJArizaR
'''
from django.views.generic.base import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.DaneUsers.views.UsersGetter import UsersGetter
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import get_template
from django.template.context import Context


class DeactivateUserView(View):
    users_getter = UsersGetter()
    
    @method_decorator(login_required(login_url='/users/login/'))
    def post(self, request):
        user = self.users_getter.get_autenticathed_user(request)
        if user == request.user:
            self._deactivate_user(request, user)
            response = HttpResponseRedirect(reverse('DaneUsers:notActiveUser'))
        else:
            response = HttpResponseRedirect(reverse('DaneUsers:deactivate') + '?wrongCredentials=True')
        return response

    @method_decorator(login_required(login_url='/users/login/'))   
    def get(self, request):
        return render(request, "DaneUsers/deactivate.html") 

    def _deactivate_user(self, request, user):
        request.user.is_active = False
        request.user.save()
        logout(request)
        self._send_deactivated_mail(user)
        
    def _send_deactivated_mail(self, user):
        mail = EmailMultiAlternatives('Deactivated Account', 'Your account has been deactivated', 'from@example.com', [user.email])
        email_template = get_template("DaneUsers/mail/deactivate.html")
        email_html = email_template.render({})
        mail.attach_alternative(email_html, "text/html")
        mail.send()

        
        
