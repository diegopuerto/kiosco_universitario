# -*- coding: utf-8 -*-
__author__ = "Emmanuel Ariza, Orlando Saavedra"
__status__ = "Prototype"

from views.LoggedView import LoggedView
from django.conf.urls import url
import views
from django.contrib.auth.views import logout, password_reset_done, password_reset_confirm, password_reset_complete
from views.LoginView import LoginView
from views.DeactivateUserView import DeactivateUserView
from views.ProfileManagerView import ProfileManagerView
from views.RecoverAccountView import RecoverAccountView
from views.PasswordReset import DanePasswordReset
from views.views import isUsernameRegistered

urlpatterns = [
    url(r'^login', LoginView.as_view(), name='login'),
    url(r'^logged$', LoggedView.as_view(), name='logged'),
    url(r'^logout$', 
        logout, {"template_name": "DaneUsers/logout.html"}, 
        name = 'logout'),
               
    # Recover password section
    url(r'^user/password/reset/$', 
        DanePasswordReset.as_view(),
        {'template_name': 'DaneUsers/password_reset_form.html',
        'post_reset_redirect' : "DaneUsers:password_reset_done",
        'email_template_name': 'DaneUsers/password_reset_email.html'},
        name='recoverPassword'),
    url(r'^user/password/reset/done/$', 
        password_reset_done, 
        {'template_name': 'DaneUsers/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        password_reset_confirm, 
        {'post_reset_redirect' : 'DaneUsers:password_reset_complete',
         'template_name': 'DaneUsers/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^user/password/done/$',
        password_reset_complete, 
        {'template_name': 'DaneUsers/password_reset_complete.html'},
        name='password_reset_complete'),
               
    url(r'^register', ProfileManagerView.as_view(), name='registerUser'),
    url(r'^userRegistered$', views.user_registered, name='userRegistered'), 
    url(r'^deactivate$', DeactivateUserView.as_view(), name='deactivate'),
    url(r'^notActiveUser$', views.user_notActive, name='notActiveUser'),   
    url(r'^modifyUserData$', ProfileManagerView.as_view(), name='modifyUserData'),
    url(r'^modifyUserData/(?P<next>\.+)/$', ProfileManagerView.as_view()),    
    url(r'^userModified$', views.user_modified, name='userModified'),
    url(r'^recoverAccount/(?P<user>.+)/$', RecoverAccountView.as_view(), name='recoverAccount'),
    url(r'^isUsernameRegistered$', isUsernameRegistered, name='isUsernameRegistered'),
    url(r'^confirm/(?P<activation_key>.+)', views.views.confirm, name='confirm'),
    url(r'^emailTest$', views.views.tryEmail_delete, name='emailTest'),
    url(r'^.*', LoginView.as_view(), name='index'),
]