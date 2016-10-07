'''
Created on 28/09/2015

@author: EJArizaR
'''
from models import UserProfile
from django.contrib.auth.models import AnonymousUser
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
        
class RestringedSitesMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user
        if self._is_user_authenticated(user):
            return self._redirect_authenticated_user(view_func, user)
        return None
        
    def _redirect_authenticated_user(self, view_func, user):
        if self._should_user_be_redirected_to_fill_register(view_func, user):
            response = HttpResponseRedirect(reverse('DaneUsers:modifyUserData'))
        elif view_func.func_name == "LoginView":
            response = HttpResponseRedirect(reverse('kiosco_app:home'))
        else:
            response = None
        return response       
     
    def _should_user_be_redirected_to_fill_register(self, view_func, user):
        return (len(UserProfile.objects.filter(user=user)) == 0 
                and not view_func.func_name == "ProfileManagerView"
                and not view_func.func_name == "logout"
                and not view_func.func_name == "filterchain"
                and not view_func.func_name == "filterchain_all"
                )

    def _is_user_authenticated(self, user):
        return not isinstance(user, AnonymousUser)

